import React from 'react';
import StockHeader from './StockHeader';
import PriceChangeSection from './PriceChangeSection';
import StockAnalysisCard from './StockAnalysisCard';
import NewsSection from './NewsSection';

const ResultsDashboard = ({ results, query }) => {
  // Ensure we always have valid data structure, even if parts are missing
  const answer = results?.answer || "No answer available";
  const metadata = results?.metadata || {};
  
  const ticker = metadata.ticker || "UNKNOWN";
  const companyName = metadata.company_name || "Unknown Company";
  const currentPrice = typeof metadata.current_price === 'number' ? metadata.current_price : 0;
  const priceChange = metadata.price_change || { change: 0, change_percent: 0, timeframe: 'today' };
  const news = Array.isArray(metadata.news) ? metadata.news : [];
  const analysis = metadata.analysis || { summary: "No analysis available", detailed_analysis: "", details: {} };
  
  return (
    <div className="mt-6 space-y-6 animate-fadeIn">
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold text-gray-800 mb-4">Your Query</h2>
        <p className="text-gray-700 italic">"{query}"</p>
        
        <div className="mt-4 p-4 bg-blue-50 rounded-lg border border-blue-100">
          <p className="text-gray-800">{answer}</p>
        </div>
      </div>
      
      <div className="bg-white rounded-lg shadow-md overflow-hidden">
        <StockHeader 
          ticker={ticker}
          companyName={companyName} 
          currentPrice={currentPrice} 
        />
        
        <div className="p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <PriceChangeSection priceChange={priceChange} />
            <StockAnalysisCard analysis={analysis} ticker={ticker} />
          </div>
          
          <div className="mt-8">
            <NewsSection news={news} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResultsDashboard;