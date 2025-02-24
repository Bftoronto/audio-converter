import React, { useState } from 'react';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  const [isLogin, setIsLogin] = useState(true); // true - логин, false - регистрация
  const [username, setUsername] = useState('');
  const [userId, setUserId] = useState('');
  const [token, setToken] = useState('');
  const [file, setFile] = useState(null);
  const [downloadUrl, setDownloadUrl] = useState('');
  const [error, setError] = useState('');

  const handleAuth = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('username', username);

    try {
      const endpoint = isLogin ? '/login/' : '/users/';
      const response = await fetch(`${API_URL}${endpoint}`, {
        method: 'POST',
        body: formData
      });
      
      if (!response.ok) {
        throw new Error(isLogin ? 'Failed to login' : 'Failed to register');
      }
      
      const data = await response.json();
      setUserId(data.user_id);
      setToken(data.token);
      setError('');
    } catch (err) {
      setError(`Error: ${err.message}`);
    }
  };

  const uploadFile = async (e) => {
    e.preventDefault();
    if (!file || !userId || !token) return;

    const formData = new FormData();
    formData.append('file', file);
    formData.append('user_id', userId);
    formData.append('token', token);

    try {
      const response = await fetch(`${API_URL}/upload-audio/`, {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        throw new Error('Failed to upload file');
      }

      const data = await response.json();
      setDownloadUrl(data.url);
      setError('');
    } catch (err) {
      setError('Error uploading file: ' + err.message);
    }
  };

  const logout = () => {
    setUserId('');
    setToken('');
    setUsername('');
    setFile(null);
    setDownloadUrl('');
    setError('');
  };

  if (!userId || !token) {
    return (
      <div style={{ padding: '20px', maxWidth: '600px', margin: '0 auto' }}>
        <h1>Audio Service</h1>
        
        {/* Auth Form */}
        <div style={{ marginBottom: '20px', padding: '20px', border: '1px solid #ccc' }}>
          <h2>{isLogin ? 'Login' : 'Register'}</h2>
          <form onSubmit={handleAuth}>
            <div style={{ marginBottom: '10px' }}>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="Enter username"
                style={{ padding: '5px', width: '200px' }}
              />
            </div>
            <div style={{ display: 'flex', gap: '10px' }}>
              <button 
                type="submit" 
                disabled={!username}
                style={{ padding: '5px 10px' }}
              >
                {isLogin ? 'Login' : 'Register'}
              </button>
              <button 
                type="button"
                onClick={() => setIsLogin(!isLogin)}
                style={{ padding: '5px 10px' }}
              >
                Switch to {isLogin ? 'Register' : 'Login'}
              </button>
            </div>
          </form>
        </div>

        {/* Error Display */}
        {error && (
          <div style={{ color: 'red', marginTop: '10px' }}>
            {error}
          </div>
        )}
      </div>
    );
  }

  return (
    <div style={{ padding: '20px', maxWidth: '600px', margin: '0 auto' }}>
      <h1>Audio Service</h1>

      {/* User Info */}
      <div style={{ marginBottom: '20px', padding: '20px', border: '1px solid #ccc' }}>
        <h2>Welcome, {username}!</h2>
        <p>User ID: {userId}</p>
        <button 
          onClick={logout}
          style={{ padding: '5px 10px', marginTop: '10px' }}
        >
          Logout
        </button>
      </div>

      {/* File Upload Form */}
      <div style={{ marginBottom: '20px', padding: '20px', border: '1px solid #ccc' }}>
        <h2>Upload Audio</h2>
        <form onSubmit={uploadFile}>
          <div style={{ marginBottom: '10px' }}>
            <input
              type="file"
              accept=".wav"
              onChange={(e) => setFile(e.target.files[0])}
              style={{ marginBottom: '10px' }}
            />
          </div>
          <button 
            type="submit" 
            disabled={!file}
            style={{ padding: '5px 10px' }}
          >
            Upload
          </button>
        </form>

        {downloadUrl && (
          <div style={{ marginTop: '10px' }}>
            <p>Download URL: <a href={downloadUrl}>{downloadUrl}</a></p>
          </div>
        )}
      </div>

      {/* Error Display */}
      {error && (
        <div style={{ color: 'red', marginTop: '10px' }}>
          {error}
        </div>
      )}
    </div>
  );
}

export default App;
