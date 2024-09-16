import React, { useEffect, useRef } from 'react';
import mermaid from 'mermaid';

export function MermaidChart({ chart }) {
  const ref = useRef(null);

  useEffect(() => {
    mermaid.initialize({ startOnLoad: false, securityLevel: 'loose' });

    const renderChart = async () => {
      if (ref.current) {
        ref.current.innerHTML = '';
        try {
          const { svg } = await mermaid.render('mermaid-chart', chart);
          ref.current.innerHTML = svg;
        } catch (error) {
          console.error('Mermaid rendering failed:', error);
          ref.current.innerHTML = 'Failed to render chart';
        }
      }
    };

    renderChart();
  }, [chart]);

  return <div ref={ref} />;
}