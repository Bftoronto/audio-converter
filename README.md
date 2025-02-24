# Аудио Сервис

Веб-приложение для конвертации аудиофайлов из WAV в MP3 формат с системой авторизации пользователей. Проект построен на FastAPI и React с использованием Docker для контейнеризации.

## Функциональность

- Создание пользователей с уникальными идентификаторами и токенами
- Загрузка аудиофайлов в формате WAV
- Автоматическая конвертация WAV в MP3
- Хранение файлов и метаданных в PostgreSQL
- Предоставление ссылок для скачивания конвертированных файлов

## Структура проекта

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   └── database.py
├── Dockerfile
└── requirements.txt
frontend/
├── public/
├── src/
│   ├── App.js
│   └── index.js
├── package.json
└── Dockerfile
docker-compose.yml
README.md
```

## Стек

### Backend
- FastAPI
- SQLAlchemy
- PostgreSQL
- pydub (для конвертации аудио)
- Docker

### Frontend
- React
- Material-UI
- Axios
- Docker

## Требования

- Docker
- Docker Compose

## Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd <repository-directory>
```

2. Создайте файл `.env` в корневой директории (опционально):
```bash
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=audio_service
```

3. Запустите сервисы:
```bash
docker-compose up --build
```

После запуска сервисы будут доступны по следующим адресам:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Swagger документация API: http://localhost:8000/docs
- PostgreSQL: localhost:5432


## Работа с данными

### Volumes
Проект использует два Docker volumes для сохранения данных:
- `postgres_data`: для хранения данных PostgreSQL
- `audio_files`: для хранения аудиофайлов

Эти volumes обеспечивают сохранность данных между перезапусками контейнеров.

## Разработка

### Backend разработка

1. Установите зависимости:
```bash
pip install -r backend/requirements.txt
```

2. Запустите сервер разработки:
```bash
cd backend
uvicorn app.main:app --reload
```

### Frontend разработка

1. Установите зависимости:
```bash
cd frontend
npm install
```

2. Запустите сервер разработки:
```bash
npm start
```

## Обработка ошибок

Сервис обрабатывает следующие типы ошибок:
- 400: Неверный формат файла
- 401: Неверный токен или ID пользователя
- 404: Файл или пользователь не найден
- 500: Внутренняя ошибка сервера

## Безопасность

- Все запросы на загрузку файлов требуют валидный токен пользователя
- Пользователи могут получить доступ только к своим файлам
- Используется UUID для идентификаторов пользователей и файлов

## Ограничения

- Поддерживается только загрузка WAV файлов
- Максимальный размер файла: 100MB
- Поддерживается только конвертация в формат MP3

## Лицензия

MIT

## Поддержка

При возникновении проблем создавайте issue в репозитории проекта.