import React from 'react';
import './PodcastSummary.css';

function PodcastSummary({ summary, visualizations }) {
  return (
    <div className="podcast-summary">
      {summary && summary.content && (
        <div dangerouslySetInnerHTML={{ __html: summary.content }} />
      )}
      {visualizations && visualizations.length > 0 && (
        <div className="visualizations">
          <h2>Visualizations</h2>
          {visualizations.map((viz, index) => (
            <div key={index} className="visualization">
              <h3>{viz.title}</h3>
              <img src={viz.imageUrl} alt={viz.title} />
              <p>{viz.description}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default PodcastSummary;