import React from 'react';
import { TrendingUp } from 'lucide-react';

const StockHeader = ({ ticker, companyName, currentPrice }) => {
  const formatPrice = (price) => {
    // Ensure price is a number
    const validPrice = typeof price === 'number' && !isNaN(price) ? price : 0;
    
    return new Intl.NumberFormat('en-US', { 
      style: 'currency', 
      currency: 'USD',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(validPrice);
  };

  return (
    <div className="bg-[#1E40AF] text-white p-6">
      <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center">
        <div className="flex items-center">
          <div className="w-10 h-10 bg-white bg-opacity-20 rounded-lg flex items-center justify-center mr-4">
            <TrendingUp className="w-6 h-6" />
          </div>
          <div>
            <h2 className="text-xl font-bold">{ticker}</h2>
            <p className="text-blue-100">{companyName}</p>
          </div>
        </div>
        
        <div className="mt-4 sm:mt-0">
          <div className="text-sm text-blue-100">Current Price</div>
          <div className="text-2xl font-bold">{formatPrice(currentPrice)}</div>
        </div>
      </div>
    </div>
  );
};

export default StockHeader;