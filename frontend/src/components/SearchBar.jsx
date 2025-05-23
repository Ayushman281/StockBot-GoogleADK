import React, { useState, useEffect } from 'react';
import { Search } from 'lucide-react';

const SearchBar = ({ onSearch, initialQuery = '', isLoading }) => {
  const [query, setQuery] = useState(initialQuery);

  useEffect(() => {
    setQuery(initialQuery);
  }, [initialQuery]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim() && !isLoading) {
      onSearch(query.trim());
    }
  };

  return (
    <div className="w-full">
      <form onSubmit={handleSubmit} className="relative">
        <div className="relative">
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask about any stock... (e.g., 'Why did Tesla stock drop today?')"
            className="w-full p-4 pl-12 pr-20 rounded-lg border border-gray-300 shadow-sm focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all"
            disabled={isLoading}
          />
          <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
            <Search className="h-5 w-5 text-gray-400" />
          </div>
        </div>
        
        <button
          type="submit"
          disabled={!query.trim() || isLoading}
          className={`absolute right-2 top-1/2 transform -translate-y-1/2 px-4 py-2 rounded-md text-white font-medium 
                    ${!query.trim() || isLoading 
                      ? 'bg-blue-300 cursor-not-allowed'
                      : 'bg-[#1E40AF] hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 transition-colors'
                    }`}
        >
          {isLoading ? (
            <span className="flex items-center">
              <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Analyzing
            </span>
          ) : (
            'Search'
          )}
        </button>
      </form>
    </div>
  );
};

export default SearchBar;