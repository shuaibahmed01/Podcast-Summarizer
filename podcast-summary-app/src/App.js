import React, { useState } from 'react';
import './App.css';

function App() {
  const [audioFile, setAudioFile] = useState(null);
  const [email, setEmail] = useState('');
  const [summary, setSummary] = useState(null);

  const handleFileChange = (event) => {
    setAudioFile(event.target.files[0]);
  };

  const handleEmailChange = (event) => {
    setEmail(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    
    const formData = new FormData();
    formData.append('audio', audioFile);
    formData.append('email', email);

    try {
      const response = await fetch('http://localhost:5001/process-audio', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to process audio');
      }

      const data = await response.json();
      setSummary(data.summary);
    } catch (error) {
      console.error('Error:', error);
      // Handle error (e.g., show error message to user)
    }
  };

  return (
    <div className="App">
      <h1>Podcast Summary Generator</h1>
      <h2 className='slogan'>Get Important Info, Save Time</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label htmlFor="audio-file">Upload Podcast Audio</label>
          <input
            type="file"
            id="audio-file"
            accept="audio/*"
            onChange={handleFileChange}
            required
          />
        </div>
        <div>
          <label htmlFor="email">Email</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={handleEmailChange}
            required
            placeholder="Enter your email"
          />
        </div>
        <button type="submit">Generate Summary</button>
      </form>
      {summary && (
        <div className="summary">
          <h2>Podcast Summary</h2>
          <pre>{summary.content}</pre>
        </div>
      )}
    </div>
  );
}

export default App;