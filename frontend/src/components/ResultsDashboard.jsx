import React from 'react';
import StockHeader from './StockHeader';
import PriceChangeSection from './PriceChangeSection';
import StockAnalysisCard from './StockAnalysisCard';
import PriceChart from './PriceChart';
import NewsSection from './NewsSection';

const ResultsDashboard = ({ results, query }) => {
  const { answer, metadata } = results;
  
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
          ticker={metadata.ticker} 
          companyName={metadata.company_name} 
          currentPrice={metadata.current_price} 
        />
        
        <div className="p-6">
          <div className="flex flex-col md:flex-row gap-6">
            <div className="w-full md:w-1/3">
              <PriceChangeSection priceChange={metadata.price_change} />
              <div className="mt-6">
                <StockAnalysisCard analysis={metadata.analysis} />
              </div>
            </div>
            
            <div className="w-full md:w-2/3">
              <PriceChart ticker={metadata.ticker} timeframe={metadata.price_change.timeframe} />
            </div>
          </div>
          
          <div className="mt-8">
            <NewsSection news={metadata.news} />
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResultsDashboard;