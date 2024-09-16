import React, { useEffect, useRef, useState } from 'react';
import mermaid from 'mermaid';
import './PodcastSummary.css';

mermaid.initialize({ startOnLoad: false, securityLevel: 'loose' });

const fixMermaidSyntax = (code) => {
  // Remove semicolons after graph statements
  code = code.replace(/^(graph\s+[A-Z]+);/gm, '$1');
  
  // Fix node labels with spaces
  code = code.replace(/\[([^\]]+)\]/g, (match, p1) => `["${p1.replace(/\s+/g, ' ')}"]`);
  
  // Fix gantt syntax
  code = code.replace(/^gantt_title/m, 'gantt\n    title');
  
  // Replace spaces in task names with underscores
  code = code.replace(/^(\s+)([^:]+):/gm, (match, indent, task) => `${indent}${task.replace(/\s+/g, '_')}:`);
  
  // Add more syntax fixes if needed
  code = code.replace(/^(\s*\w+)>>/gm, '$1-->');
  
  return code;
};

function PodcastSummary({ summary, visualizations }) {
  const [renderedDiagrams, setRenderedDiagrams] = useState([]);
  const containerRef = useRef(null);

  useEffect(() => {
    if (containerRef.current && visualizations.length > 0) {
      const renderDiagrams = async () => {
        const newRenderedDiagrams = await Promise.all(
          visualizations.map(async (viz, index) => {
            try {
              console.log(`Attempting to render diagram ${index}:`, viz.mermaidCode);
              const fixedCode = fixMermaidSyntax(viz.mermaidCode);
              console.log(`Fixed Mermaid code:`, fixedCode);
              
              const uniqueId = `mermaid-${Date.now()}-${index}`;
              const tempElement = document.createElement('div');
              tempElement.style.display = 'none';
              document.body.appendChild(tempElement);
              
              const { svg } = await mermaid.render(uniqueId, fixedCode, tempElement);
              
              document.body.removeChild(tempElement);
              
              console.log(`Successfully rendered diagram ${index}`);
              return { id: index, svg, error: null };
            } catch (error) {
              console.error(`Error rendering diagram ${index}:`, error);
              return { id: index, svg: null, error: error.message };
            }
          })
        );
        setRenderedDiagrams(newRenderedDiagrams);
      };

      renderDiagrams();
    }
  }, [visualizations]);

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
    <div className="podcast-summary" ref={containerRef}>
      <div className="summary-content">
        {renderSummaryContent(summary.content)}
      </div>
      <div className="visualizations">
        {visualizations.filter((_, index) => renderedDiagrams[index] && !renderedDiagrams[index].error).map((viz, index) => (
          <div key={index} className="visualization">
            <h3>{viz.title}</h3>
            <p>{viz.description}</p>
            <div
              className="mermaid-diagram"
              dangerouslySetInnerHTML={{ __html: renderedDiagrams[index]?.svg || '' }}
            />
          </div>
        ))}
      </div>
    </div>
  );
}

export default PodcastSummary;