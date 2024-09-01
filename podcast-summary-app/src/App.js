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
    // TODO: Implement API call to backend for processing
    console.log('Submitting:', { audioFile, email });
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
          <h2>{summary.title}</h2>
          <h3>Main Points</h3>
          <ul>
            {summary.mainPoints.map((point, index) => (
              <li key={index}>{point}</li>
            ))}
          </ul>
          <h3>Cool Points</h3>
          <ul>
            {summary.coolPoints.map((point, index) => (
              <li key={index}>{point}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;