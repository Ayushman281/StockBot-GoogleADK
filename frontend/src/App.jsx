import React, { useState } from 'react';
import SearchBar from './components/SearchBar';
import ResultsDashboard from './components/ResultsDashboard';
import ExampleQueries from './components/ExampleQueries';
import { queryStockBot } from './services/api';

function App() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [results, setResults] = useState(null);
  const [query, setQuery] = useState('');

  const handleSearch = async (searchQuery) => {
    setQuery(searchQuery);
    setIsLoading(true);
    setError(null);
    
    try {
      const data = await queryStockBot(searchQuery);
      console.log('Received data from API:', data); // For debugging
      
      // Basic validation of response data structure
      if (!data || typeof data !== 'object') {
        throw new Error("Invalid response format from server");
      }
      
      // Ensure minimum required structure exists to prevent rendering errors
      const safeData = {
        answer: data.answer || "No answer provided",
        metadata: {
          ticker: data.metadata?.ticker || "UNKNOWN",
          company_name: data.metadata?.company_name || "Unknown Company",
          current_price: data.metadata?.current_price || 0,
          price_change: data.metadata?.price_change || { change: 0, change_percent: 0, timeframe: 'today' },
          news: Array.isArray(data.metadata?.news) ? data.metadata.news : [],
          analysis: data.metadata?.analysis || { summary: "No analysis available", details: {} }
        }
      };
      
      setResults(safeData);
    } catch (err) {
      console.error('Search error:', err);
      setError(err.message || 'Sorry, we encountered an error processing your request. Please try again.');
      setResults(null);
    } finally {
      setIsLoading(false);
    }
  };

  const handleExampleClick = (exampleQuery) => {
    setQuery(exampleQuery);
    handleSearch(exampleQuery);
  };
  
  const handleReset = () => {
    setResults(null);
    setQuery('');
    setError(null);
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <header className="bg-[#1E40AF] text-white p-4 shadow-md">
        <div className="container mx-auto flex items-center">
          <button 
            onClick={handleReset} 
            className="flex items-center focus:outline-none hover:opacity-80 transition-opacity"
            aria-label="Reset StockBot"
          >
            <h1 className="text-2xl font-bold">StockBot</h1>
            <span className="ml-2 text-sm bg-blue-700 px-2 py-1 rounded-full">Beta</span>
          </button>
        </div>
      </header>
      
      <main className="container mx-auto px-4 py-6 flex-1 flex flex-col">
        <SearchBar onSearch={handleSearch} initialQuery={query} isLoading={isLoading} />
        
        <div className="mt-4">
          <ExampleQueries onExampleClick={handleExampleClick} />
        </div>
        
        {error && (
          <div className="mt-8 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
            {error}
          </div>
        )}
        
        {isLoading ? (
          <div className="mt-8 flex-1 flex flex-col items-center justify-center">
            <div className="animate-pulse flex flex-col items-center">
              <div className="h-12 w-12 bg-blue-200 rounded-full mb-4"></div>
              <div className="h-4 w-48 bg-blue-200 rounded mb-2"></div>
              <div className="h-4 w-36 bg-blue-200 rounded"></div>
            </div>
          </div>
        ) : results ? (
          <ResultsDashboard results={results} query={query} />
        ) : (
          <div className="mt-8 flex-1 flex flex-col items-center justify-center text-gray-500">
            <p className="text-lg">Ask StockBot about any stock to get started</p>
          </div>
        )}
      </main>
      
      <footer className="bg-gray-100 border-t border-gray-200 py-4">
        <div className="container mx-auto px-4 text-center text-sm text-gray-600">
          <p>StockBot &copy; 2025 | Data provided for informational purposes only</p>
        </div>
      </footer>
    </div>
  );
}

export default App;