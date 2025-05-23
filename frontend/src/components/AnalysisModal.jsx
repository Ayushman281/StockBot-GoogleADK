import React, { useRef, useEffect } from 'react';
import { X } from 'lucide-react';

const AnalysisModal = ({ isOpen, onClose, analysis, ticker }) => {
  const modalRef = useRef(null);
  
  // Handle click outside to close
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (modalRef.current && !modalRef.current.contains(event.target)) {
        onClose();
      }
    };
    
    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
      // Prevent body scrolling when modal is open
      document.body.style.overflow = 'hidden';
    }
    
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
      document.body.style.overflow = 'unset';
    };
  }, [isOpen, onClose]);

  // Handle escape key to close
  useEffect(() => {
    const handleEscapeKey = (e) => {
      if (e.key === 'Escape') {
        onClose();
      }
    };
    
    if (isOpen) {
      document.addEventListener('keydown', handleEscapeKey);
    }
    
    return () => {
      document.removeEventListener('keydown', handleEscapeKey);
    };
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  // Function to safely format text with enhanced heading styling
  const formatText = (text) => {
    // Make sure text is a string
    if (!text || typeof text !== 'string' || text.trim() === '') {
      return <p className="text-gray-500">No detailed analysis available.</p>;
    }
    
    try {
      // Split by new lines and create paragraphs
      const sections = [];
      const lines = text.split('\n');
      let currentSection = [];
      
      lines.forEach((line, index) => {
        if (line.startsWith('##')) {
          if (currentSection.length > 0) {
            sections.push(currentSection.join('\n'));
            currentSection = [];
          }
          
          // Add heading
          currentSection.push(line);
        } else {
          // Add to current section
          currentSection.push(line);
        }
      });
      
      // Add final section
      if (currentSection.length > 0) {
        sections.push(currentSection.join('\n'));
      }
      
      return sections.map((section, i) => {
        const sectionLines = section.split('\n');
        const firstLine = sectionLines[0];
        
        if (firstLine.startsWith('## ')) {
          return (
            <div key={i} className="mb-4">
              <h2 className="text-xl font-bold border-b border-gray-300 pb-1 mb-3">
                {firstLine.replace(/^## /, '')}
              </h2>
              <div className="font-normal">
                {sectionLines.slice(1).filter(l => l.trim() !== '').map((line, j) => (
                  <p key={j} className="mb-2">
                    {line}
                  </p>
                ))}
              </div>
            </div>
          );
        } 
        else if (firstLine.startsWith('### ')) {
          return (
            <div key={i} className="mb-4">
              <h3 className="text-lg font-bold border-b border-gray-200 pb-1 mb-2">
                {firstLine.replace(/^### /, '')}
              </h3>
              <div className="font-normal">
                {sectionLines.slice(1).filter(l => l.trim() !== '').map((line, j) => (
                  <p key={j} className="mb-2">
                    {line}
                  </p>
                ))}
              </div>
            </div>
          );
        }

        else {
          return (
            <div key={i} className="mb-4 font-normal">
              {sectionLines.map((line, j) => (
                <p key={j} className={line.startsWith('- ') ? "mb-1 ml-4 flex" : "mb-2"}>
                  {line.startsWith('- ') && <span className="mr-2">•</span>}
                  <span>{line.startsWith('- ') ? line.replace(/^- /, '') : line}</span>
                </p>
              ))}
            </div>
          );
        }
      });
    } catch (error) {
      console.error("Error formatting analysis text:", error);
      
      // Fallback to simple formatting if error occurs
      return (
        <div className="text-gray-800">
          {typeof text === 'string' ? text.split('\n').map((line, i) => (
            <p key={i} className="mb-2">{line}</p>
          )) : <p>Unable to display analysis.</p>}
        </div>
      );
    }
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div 
        ref={modalRef} 
        className="bg-white rounded-lg shadow-xl w-full max-w-3xl max-h-[90vh] overflow-hidden flex flex-col"
      >
        <div className="flex justify-between items-center p-4 border-b">
          <h2 className="text-xl font-semibold text-gray-800">
            Detailed Analysis - {ticker}
          </h2>
          <button 
            onClick={onClose}
            className="p-1 rounded-full hover:bg-gray-100"
            aria-label="Close"
          >
            <X className="h-5 w-5 text-gray-500" />
          </button>
        </div>
        
        <div className="p-6 overflow-y-auto">
          {formatText(analysis)}
        </div>
        
        <div className="border-t p-4 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 bg-gray-100 hover:bg-gray-200 text-gray-800 rounded-md transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

export default AnalysisModal;
