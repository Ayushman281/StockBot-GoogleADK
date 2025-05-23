import React, { useState } from 'react';
import { LineChart, ArrowUpRight, Bot } from 'lucide-react';
import AnalysisModal from './AnalysisModal';

const StockAnalysisCard = ({ analysis, ticker }) => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  
  // Safely destructure with defaults
  const { summary = "No analysis available", detailed_analysis = "", details = {} } = analysis || {};
  const isLlmEnhanced = details.llm_enhanced;
  
  const openModal = () => {
    console.log("Opening modal with analysis:", detailed_analysis); // Debug log
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
  };

  // Check if we have a non-empty detailed analysis to show
  // Make sure detailed_analysis is a string before calling trim()
  const hasDetailedAnalysis = typeof detailed_analysis === 'string' && detailed_analysis.trim().length > 0;

  return (
    <>
      <div className="bg-gray-50 p-4 rounded-lg border border-gray-200">
        <div className="flex items-start">
          <div className="bg-blue-100 p-2 rounded-lg mr-3">
            {isLlmEnhanced ? 
              <Bot className="w-4 h-4 text-[#1E40AF]" /> : 
              <LineChart className="w-4 h-4 text-[#1E40AF]" />
            }
          </div>
          <div>
            <h3 className="font-medium text-gray-900 mb-1 flex items-center">
              Analysis Summary
              {isLlmEnhanced && (
                <span className="ml-2 text-xs bg-blue-100 text-blue-800 px-2 py-0.5 rounded-full">AI Enhanced</span>
              )}
            </h3>
            
            <p className="text-sm text-gray-600">
              {summary || "No analysis available for this stock."}
            </p>
            
            {hasDetailedAnalysis && (
              <button 
                onClick={openModal}
                className="mt-3 flex items-center text-[#1E40AF] text-sm font-medium hover:text-blue-700 transition-colors"
              >
                <span>View detailed analysis</span>
                <ArrowUpRight className="w-3 h-3 ml-1" />
              </button>
            )}
          </div>
        </div>
      </div>
      
      <AnalysisModal 
        isOpen={isModalOpen}
        onClose={closeModal}
        analysis={typeof detailed_analysis === 'string' ? detailed_analysis : ""}
        ticker={ticker}
      />
    </>
  );
};

export default StockAnalysisCard;