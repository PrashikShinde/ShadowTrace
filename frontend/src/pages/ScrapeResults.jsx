// src/pages/ScrapeResults.jsx

import React, { useEffect, useState } from 'react';
import axios from 'axios';

const ScrapeResults = () => {
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchScrapeResults = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/scrape-results');
        if (response.data.status === 'success') {
          setResults(response.data.data.results);
        } else {
          console.error('Failed to fetch results');
        }
      } catch (error) {
        console.error('Error fetching scrape results:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchScrapeResults();
  }, []);

  if (loading) {
    return <div className="text-center mt-10">Loading results...</div>;
  }

  if (results.length === 0) {
    return <div className="text-center mt-10">No results found.</div>;
  }

  return (
    <div className="p-8 grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
      {results.map((item, index) => (
        <div key={index} className="border rounded-xl p-4 shadow-md">
          {item.type === 'base64_image' ? (
            <>
              <img src={item.src} alt={`Result ${index}`} className="w-full h-48 object-cover rounded-md" />
              <a
                href={item.src}
                download={`result-${index}.jpg`}
                className="mt-2 inline-block text-blue-500 underline text-sm"
              >
                Download Image
              </a>
            </>
          ) : item.type === 'link' ? (
            <>
              <div className="text-gray-700 text-md font-semibold mb-2">Source Website</div>
              <a
                href={item.url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-600 underline break-words"
              >
                {item.url}
              </a>
            </>
          ) : null}
        </div>
      ))}
    </div>
  );
};

export default ScrapeResults;
