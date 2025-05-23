import React, { useState } from 'react';
import { LineChart, ArrowUpRight, Bot } from 'lucide-react';
import AnalysisModal from './AnalysisModal';

const StockAnalysisCard = ({ analysis, ticker }) => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  
  // Safely destructure with defaults
  const { summary = "No analysis available", detailed_analysis = "", details = {} } = analysis || {};
  const isLlmEnhanced = details.llm_enhanced;
  
  // Initialize with either the actual detailed_analysis or generate a fallback
  const getDetailedAnalysis = () => {
    // If we have valid detailed analysis from the LLM, use it
    if (typeof detailed_analysis === 'string' && detailed_analysis.trim().length > 0) {
      return detailed_analysis;
    }
    
    // Otherwise generate a more detailed version from other available data
    let fallbackAnalysis = `## ${ticker} - Detailed Analysis\n\n`;
    
    // Add summary as first paragraph
    fallbackAnalysis += `${summary}\n\n`;
    
    // Add technical section
    fallbackAnalysis += `### Technical Analysis\n`;
    if (details.price_analysis) {
      const direction = details.price_analysis.direction || "unknown";
      fallbackAnalysis += `The stock is currently showing a ${direction} trend. `;
      if (direction === "up") {
        fallbackAnalysis += "Technical indicators suggest continued momentum may be possible if volume remains supportive.\n\n";
      } else if (direction === "down") {
        fallbackAnalysis += "Technical indicators suggest caution is warranted until a support level is established.\n\n";
      } else {
        fallbackAnalysis += "Technical indicators are currently mixed, suggesting a sideways trading pattern may develop.\n\n";
      }
    }
    
    // Add news section if available
    if (details.news_analysis && details.news_analysis.headlines) {
      fallbackAnalysis += `### News Analysis\n`;
      fallbackAnalysis += `Recent headlines that may be affecting ${ticker}:\n\n`;
      
      // Add headlines as bullet points
      details.news_analysis.headlines.forEach((headline, i) => {
        const sentiment = details.news_analysis.sentiments && details.news_analysis.sentiments[i] 
          ? details.news_analysis.sentiments[i] 
          : "neutral";
        fallbackAnalysis += `- ${headline} (${sentiment})\n`;
      });
      
      fallbackAnalysis += `\nTotal news items found: ${details.news_analysis.news_count || 0}\n\n`;
    }
    
    // Add outlook section
    fallbackAnalysis += `### Outlook\n`;
    fallbackAnalysis += `Investors should monitor upcoming news and earnings reports for ${ticker} to better understand the company's trajectory. `;
    fallbackAnalysis += `Market conditions and sector trends will also play a significant role in future price movements.`;
    
    return fallbackAnalysis;
  };
  
  const openModal = () => {
    setIsModalOpen(true);
  };

  const closeModal = () => {
    setIsModalOpen(false);
  };

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
            
            <button 
              onClick={openModal}
              className="mt-3 flex items-center text-[#1E40AF] text-sm font-medium hover:text-blue-700 transition-colors"
            >
              <span>View detailed analysis</span>
              <ArrowUpRight className="w-3 h-3 ml-1" />
            </button>
          </div>
        </div>
      </div>
      
      <AnalysisModal 
        isOpen={isModalOpen}
        onClose={closeModal}
        analysis={getDetailedAnalysis()}
        ticker={ticker}
      />
    </>
  );
};

export default StockAnalysisCard;