import React from 'react';
import './PodcastSummary.css';

function PodcastSummary({ summary }) {
  const formatContent = (content) => {
    if (!content) return null;

    const sections = content.split('\n\n');
    return sections.map((section, index) => {
      const lines = section.split('\n');
      const title = lines[0].replace(/^#+\s*/, ''); // Remove leading hashtags
      const details = lines.slice(1);

      return (
        <div key={index} className="summary-section">
          <h3>{title}</h3>
          {details.map((detail, detailIndex) => (
            <p key={detailIndex}>{detail.replace(/^#+\s*/, '')}</p> // Remove leading hashtags from details too
          ))}
        </div>
      );
    });
  };

  return (
    <div className="podcast-summary">
      <h2>Podcast Summary</h2>
      <div className="summary-content">
        {summary && summary.content ? formatContent(summary.content) : <p>No summary available.</p>}
      </div>
    </div>
  );
}

export default PodcastSummary;