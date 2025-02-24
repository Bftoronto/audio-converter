from fastapi import FastAPI, File, UploadFile, Depends, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.orm import Session
from typing import Optional
from . import models, database
import uuid
import os
from pydub import AudioSegment

app = FastAPI()

@app.on_event("startup")
async def startup():
    # Создаем таблицы при запуске
    models.Base.metadata.create_all(bind=database.engine)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Создание директории для аудио файлов
os.makedirs("audio", exist_ok=True)

@app.post("/users/")
async def create_user(username: str = Form(...), db: Session = Depends(database.get_db)):
    try:
        user_id = str(uuid.uuid4())
        token = str(uuid.uuid4())
        
        user = models.User(
            id=user_id,
            username=username,
            token=token
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return JSONResponse(
            status_code=200,
            content={
                "user_id": user_id,
                "token": token,
                "username": username
            }
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Error creating user: {str(e)}"
        )

@app.post("/upload-audio/")
async def upload_audio(
    user_id: str = Form(...),
    token: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db)
):
    # Проверка пользователя и токена
    user = db.query(models.User).filter(
        models.User.id == user_id,
        models.User.token == token
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid user_id or token"
        )

    if not file.filename.endswith('.wav'):
        raise HTTPException(
            status_code=400,
            detail="File format not supported. Please upload a WAV file."
        )

    try:
        # Сохраняем WAV файл
        wav_path = f"audio/{uuid.uuid4()}.wav"
        with open(wav_path, "wb+") as audio_file:
            audio_file.write(await file.read())

        # Конвертируем в MP3
        audio = AudioSegment.from_wav(wav_path)
        mp3_path = f"audio/{uuid.uuid4()}.mp3"
        audio.export(mp3_path, format="mp3")

        # Удаляем временный WAV файл
        os.remove(wav_path)

        # Сохраняем запись в БД
        audio_id = str(uuid.uuid4())
        audio_record = models.AudioRecord(
            id=audio_id,
            user_id=user_id,
            file_path=mp3_path,
            format="mp3"
        )
        
        db.add(audio_record)
        db.commit()
        db.refresh(audio_record)

        return JSONResponse(
            status_code=200,
            content={
                "url": f"http://localhost:8000/record?id={audio_id}&user={user_id}"
            }
        )

    except Exception as e:
        if os.path.exists(wav_path):
            os.remove(wav_path)
        if 'mp3_path' in locals() and os.path.exists(mp3_path):
            os.remove(mp3_path)
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing the audio: {str(e)}"
        )

@app.get("/record/")
async def get_audio(
    id: str,
    user: str,
    db: Session = Depends(database.get_db)
):
    audio_record = db.query(models.AudioRecord).filter(
        models.AudioRecord.id == id,
        models.AudioRecord.user_id == user
    ).first()

    if not audio_record:
        raise HTTPException(
            status_code=404,
            detail="Audio record not found"
        )

    if not os.path.exists(audio_record.file_path):
        raise HTTPException(
            status_code=404,
            detail="Audio file not found"
        )

    return FileResponse(audio_record.file_path)

@app.post("/login/")
async def login(username: str = Form(...), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )
    
    return {
        "user_id": user.id,
        "token": user.token,
        "username": user.username
    }
