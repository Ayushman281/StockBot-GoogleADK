import React from 'react';
import { ChevronRight, TrendingUp, TrendingDown, Minus } from 'lucide-react';

// Mock function to determine sentiment
const getSentiment = (newsTitle) => {
  const lowerTitle = newsTitle.toLowerCase();
  
  if (lowerTitle.includes('up') || lowerTitle.includes('rise') || lowerTitle.includes('gain') || lowerTitle.includes('surge')) {
    return 'positive';
  } else if (lowerTitle.includes('down') || lowerTitle.includes('drop') || lowerTitle.includes('fall') || lowerTitle.includes('loss')) {
    return 'negative';
  }
  return 'neutral';
};

const NewsItem = ({ title }) => {
  const sentiment = getSentiment(title);
  
  let Icon, bgColor, textColor, borderColor;
  
  switch(sentiment) {
    case 'positive':
      Icon = TrendingUp;
      bgColor = 'bg-green-50';
      textColor = 'text-green-800';
      borderColor = 'border-green-100';
      break;
    case 'negative':
      Icon = TrendingDown;
      bgColor = 'bg-red-50';
      textColor = 'text-red-800';
      borderColor = 'border-red-100';
      break;
    default:
      Icon = Minus;
      bgColor = 'bg-gray-50';
      textColor = 'text-gray-800';
      borderColor = 'border-gray-100';
  }
  
  return (
    <div className={`p-3 rounded-lg ${bgColor} border ${borderColor} mb-3 flex items-center`}>
      <div className="mr-3">
        <Icon className={`h-5 w-5 ${textColor}`} />
      </div>
      <div className="flex-grow">
        <p className={`${textColor} font-medium`}>{title}</p>
        <p className="text-xs text-gray-500 mt-1">Today • Source: Financial News</p>
      </div>
      <ChevronRight className="h-5 w-5 text-gray-400" />
    </div>
  );
};

const NewsSection = ({ news }) => {
  return (
    <div>
      <h3 className="font-medium text-gray-900 mb-4">Related News</h3>
      
      {news && news.length > 0 ? (
        <div>
          {news.map((item, index) => (
            <NewsItem key={index} title={item} />
          ))}
        </div>
      ) : (
        <div className="text-center py-6 text-gray-500">
          No related news available
        </div>
      )}
    </div>
  );
};

export default NewsSection;