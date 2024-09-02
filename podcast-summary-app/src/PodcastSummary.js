import React from 'react';
import './PodcastSummary.css';

function PodcastSummary({ summary }) {
  const formatContent = (content) => {
    return content.split('\n').map((line, index) => {
      if (line.trim().endsWith(':')) {
        return <h3 key={index}>{line}</h3>;
      }
      return <p key={index}>{line}</p>;
    });
  };

  return (
    <div className="podcast-summary">
      <h2>Podcast Summary</h2>
      <div className="summary-content">
        {formatContent(summary.content)}
      </div>
    </div>
  );
}

export default PodcastSummary;