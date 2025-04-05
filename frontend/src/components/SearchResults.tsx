import React from "react";

type Match = {
  source: string;
  url: string;
  match_confidence: number;
};

type Props = {
  matches: Match[];
};

const SearchResults: React.FC<Props> = ({ matches }) => {
  if (matches.length === 0) {
    return <p className="text-center text-gray-400">No matches found.</p>;
  }

  return (
    <div className="mt-6 space-y-4">
      <h2 className="text-xl font-bold text-center text-white">Search Results</h2>
      <ul className="space-y-4">
        {matches.map((match, index) => (
          <li
            key={index}
            className="bg-gray-800 p-4 rounded-xl shadow-md hover:shadow-xl transition-all"
          >
            <p><strong>Source:</strong> {match.source}</p>
            <p><strong>Confidence:</strong> {match.match_confidence}%</p>
            <p>
              <strong>URL:</strong>{" "}
              <a href={match.url} target="_blank" className="text-blue-400 underline">
                {match.url}
              </a>
            </p>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default SearchResults;
