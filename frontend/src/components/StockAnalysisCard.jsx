import React from 'react';
import { LineChart, ArrowUpRight } from 'lucide-react';

const StockAnalysisCard = ({ analysis }) => {
  const { summary, details } = analysis;
  
  return (
    <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
      <div className="flex items-start">
        <div className="bg-blue-100 p-2 rounded-lg mr-3">
          <LineChart className="w-4 h-4 text-[#1E40AF]" />
        </div>
        <div>
          <h3 className="font-medium text-gray-900 mb-1">Analysis Summary</h3>
          <p className="text-sm text-gray-600">{summary}</p>
          
          {details && Object.keys(details).length > 0 && (
            <button className="mt-3 flex items-center text-[#1E40AF] text-sm font-medium hover:text-blue-700 transition-colors">
              <span>View detailed analysis</span>
              <ArrowUpRight className="w-3 h-3 ml-1" />
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default StockAnalysisCard;