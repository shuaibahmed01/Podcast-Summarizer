import React from 'react';
import './PodcastSummary.css';
import DOMPurify from 'dompurify';

function PodcastSummary({ summary }) {
  const createMarkup = (html) => {
    return {__html: DOMPurify.sanitize(html)};
  }

  return (
    <div className="podcast-summary">
      <div className="summary-content" dangerouslySetInnerHTML={createMarkup(summary)} />
    </div>
  );
}

export default PodcastSummary;