import React from 'react';
import './PodcastSummary.css';

function PodcastSummary({ summary }) {
  const renderSummaryContent = (content) => {
    if (typeof content === 'string' && content.trim().startsWith('<')) {
      return <div dangerouslySetInnerHTML={{ __html: content }} />;
    } else if (typeof content === 'string') {
      return content.split('\n').map((paragraph, index) => (
        <p key={index}>{paragraph}</p>
      ));
    } else if (Array.isArray(content)) {
      return content.map((paragraph, index) => (
        <p key={index}>{paragraph}</p>
      ));
    } else {
      return <p>{JSON.stringify(content)}</p>;
    }
  };

  return (
    <div className="podcast-summary">
      <div className="summary-content">
        {renderSummaryContent(summary.content)}
      </div>
    </div>
  );
}

export default PodcastSummary;