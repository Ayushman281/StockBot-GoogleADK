import React from 'react';
import { TrendingUp, TrendingDown } from 'lucide-react';

const PriceChangeSection = ({ priceChange }) => {
  // Safeguard against undefined priceChange props with default values
  const { change = 0, change_percent = 0, timeframe = 'today' } = priceChange || {};
  
  const isPositive = change >= 0;
  const changeColor = isPositive ? 'text-[#22C55E]' : 'text-[#EF4444]';
  const bgColor = isPositive ? 'bg-green-50' : 'bg-red-50';
  const borderColor = isPositive ? 'border-green-100' : 'border-red-100';
  const Icon = isPositive ? TrendingUp : TrendingDown;

  const formatChange = (value) => {
    return new Intl.NumberFormat('en-US', { 
      style: 'currency', 
      currency: 'USD',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
      signDisplay: 'always'
    }).format(value);
  };

  const formatTimeframe = (tf) => {
    // Add null check to prevent errors on undefined timeframe
    if (!tf) return 'Today';
    
    switch(tf) {
      case 'today':
        return 'Today';
      case 'week':
        return 'This Week';
      case 'month':
        return 'This Month';
      default:
        return tf.charAt(0).toUpperCase() + tf.slice(1);
    }
  };

  return (
    <div className={`p-4 rounded-lg ${bgColor} border ${borderColor}`}>
      <h3 className="text-gray-700 text-sm font-medium mb-2">Price Change ({formatTimeframe(timeframe)})</h3>
      
      <div className="flex items-center">
        <Icon className={`w-5 h-5 ${changeColor} mr-2`} />
        <span className={`text-lg font-bold ${changeColor}`}>
          {formatChange(change)} ({change_percent > 0 ? '+' : ''}{change_percent}%)
        </span>
      </div>
    </div>
  );
};

export default PriceChangeSection;