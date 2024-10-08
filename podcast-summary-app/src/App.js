import React, { useState } from 'react';
import './App.css';
import PodcastSummary from './components/PodcastSummary';

function App() {
  const [audioFile, setAudioFile] = useState(null);
  const [email, setEmail] = useState('');
  const [summary, setSummary] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [visualizations, setVisualizations] = useState([]);
  const [currentPage, setCurrentPage] = useState('home');

  const handleFileChange = (event) => {
    setAudioFile(event.target.files[0]);
  };

  const handleEmailChange = (event) => {
    setEmail(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setIsLoading(true);
    setProgress(0);
    setSummary(null);
    
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

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const decodedChunk = decoder.decode(value);
        const lines = decodedChunk.split('\n\n');
        
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = JSON.parse(line.slice(6));
            if (data.progress) {
              setProgress(data.progress);
            }
            if (data.summary) {
              setSummary({ content: data.summary });
            }
          }
        }
      }
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const renderContent = () => {
    switch(currentPage) {
      case 'home':
        return (
          <>
            <h1>Lecture Report Generator</h1>
            <p className="slogan">Get Important Info, Save Time</p>
            <form onSubmit={handleSubmit}>
              <div className="input-group">
                <label htmlFor="audio-file">Upload Lecture Audio</label>
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
              <button type="submit" disabled={isLoading}>
                {isLoading ? 'Generating Summary...' : 'Generate Summary'}
              </button>
            </form>
            {isLoading && (
              <div className="progress-bar-container">
                <div className="progress-bar" style={{ width: `${progress}%` }}></div>
                <p className="progress-text">{Math.round(progress)}% Complete</p>
              </div>
            )}
            {summary && (
              <PodcastSummary 
                summary={summary.content} 
                visualizations={visualizations}
              />
            )}
          </>
        );
      case 'past-reports':
        return (
          <>
            <h1 className="past-reports-header">Past Reports</h1>
            {/* Add your past reports content here */}
          </>
        );
      default:
        return <h1>Page Not Found</h1>;
    }
  };

  return (
    <div className="App">
      <div className="dynamic-background"></div>
      <nav className="navbar">
        <ul>
          <li>
            <button onClick={() => setCurrentPage('home')}>Generate Report</button>
          </li>
          <li>
            <button onClick={() => setCurrentPage('past-reports')}>Past Reports</button>
          </li>
        </ul>
      </nav>
      <div className="content">
        {renderContent()}
      </div>
    </div>
  );
}

export default App;