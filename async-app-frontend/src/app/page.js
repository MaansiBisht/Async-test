"use client";

import axios from "axios";
import { useState } from "react";
import ExpandableCard from "./ExpandableCard";

export default function Home() {
  const [url, setUrl] = useState(""); // URL input
  const [query, setQuery] = useState(""); // Search query input
  const [results, setResults] = useState([]); // Results array
  const [loading, setLoading] = useState(false); // Loading state

  const handleSearch = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResults([]);

    try {
      // Make POST request to FastAPI backend
      const response = await axios.post('http://localhost:8000/search/', {
        url: url,
        query: query
      });
      console.log('Response:', response.data);
      // Set results from the response
      setResults(response.data.results);
    } catch (error) {
      console.error('Error searching:', error);
    } finally {
      setLoading(false); // Stop loading state
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <div className="flex flex-col items-center w-full max-w-4xl mx-auto">
        <div className="text-center mb-6">
          <h1 className="text-4xl font-bold text-gray-800">Website Content Search</h1>
          <p className="text-lg text-gray-600">
            Search through website content with precision
          </p>
        </div>
        <form
          onSubmit={handleSearch}
          className="w-full flex flex-col gap-4 bg-white shadow-lg p-6 rounded-md"
        >
          <input
            type="url"
            placeholder="https://example.com"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            className="w-full border border-gray-300 rounded-md p-3 text-gray-700 focus:outline-none focus:ring focus:ring-blue-300"
            required
          />
          <div className="flex items-center gap-4">
            <input
              type="text"
              placeholder="Search query"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="flex-grow border border-gray-300 rounded-md p-3 text-gray-700 focus:outline-none focus:ring focus:ring-blue-300"
              required
            />
            <button
              type="submit"
              className="bg-blue-500 text-white px-6 py-3 rounded-md hover:bg-blue-600 transition-all"
              disabled={loading}
            >
              {loading ? "Searching..." : "Search"}
            </button>
          </div>
        </form>

        <div className="w-full mt-8 text-center">
          {loading && (
            <p className="text-gray-500 text-lg">Searching...</p>
          )}
          {!loading && results.length === 0 && (
            <p className="text-gray-500 text-lg">
              No results found for your search query.
            </p>
          )}
          {!loading && results.length > 0 && (
            <div className="flex flex-col gap-4">
              {results.slice(0, 10).map((result, index) => (
                <ExpandableCard
                  key={result.chunk_id}
                  content={result.content}
                  index={index}
                  matchPercentage={result.score} // assuming score is the match percentage
                  path={result.path} // Ensure path is available in the result if needed
                  html={result.html} // Pass the full HTML content
                />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );


}
