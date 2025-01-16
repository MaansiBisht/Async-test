import React, { useState } from "react";

const ExpandableCard = ({ chunkId, content, index, matchPercentage, path , html }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div className="border border-gray-300 rounded-lg shadow-md p-4 bg-white text-black">
      <div className="flex justify-end items-center">
        <span className="text-green-600 text-sm font-medium">{`${matchPercentage}% match`}</span>
      </div>
      <pre className="mt-3 p-3 bg-gray-100 rounded text-xs overflow-x-auto text-left" style={{ whiteSpace: 'pre-wrap', wordWrap: 'break-word' }}>
          {content}
      </pre>
      <p className="text-gray-500 text-sm mt-1 text-left">{`Path: ${path}`}</p>
      {/* Toggle HTML Content */}  
      <button
        onClick={() => setIsExpanded(!isExpanded)}
        className="mt-3 text-blue-600 underline text-sm flex justify-start"
      >
        {isExpanded ? "Hide HTML" : "View HTML"}
      </button>
      {isExpanded && (
        <textarea
            className="mt-3 p-3 bg-gray-100 rounded text-sm w-full h-64"
            value={html}
            readOnly 
          />
      )}
    </div>
  );
};

export default ExpandableCard;
