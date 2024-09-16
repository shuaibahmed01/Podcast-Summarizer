import React, { useState } from 'react';
import './App.css';
import PodcastSummary from './PodcastSummary';
import { MermaidChart } from './MermaidChart';

function App() {
  const [audioFile, setAudioFile] = useState(null);
  const [email, setEmail] = useState('');
  const [summary, setSummary] = useState(null);
  // eslint-disable-next-line
  const [visualizations, setVisualizations] = useState([]);

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
      setVisualizations(data.visualizations || []);
    } catch (error) {
      console.error('Error:', error);
      
    }
  };

  return (
    <div className="App">
      <div className="dynamic-background"></div>
      <div className="content">
        <h1>Podcast Summary Generator</h1>
        <p className="slogan">Get Important Info, Save Time</p>
        <form onSubmit={handleSubmit}>
          <div className="input-group">
            <label htmlFor="audio-file">Upload Podcast Audio</label>
            <input
              type="file"
              id="audio-file"
              accept="audio/*"
              onChange={handleFileChange}
              required
            />
          </div>
          <div className="input-group">
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
          <PodcastSummary 
            summary={summary} 
            visualizations={visualizations}
          />
        )}
      </div>
    </div>
  );
}

export default App;