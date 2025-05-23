import React from 'react';

const ExampleQueries = ({ onExampleClick }) => {
  const examples = [
    "Why did Tesla stock drop today?",
    "How has Apple performed this week?",
    "What's happening with Microsoft stock?",
    "How is Amazon doing this month?",
  ];

  return (
    <div className="flex flex-wrap gap-2">
      <span className="text-sm text-gray-500 self-center">Try:</span>
      {examples.map((example, index) => (
        <button
          key={index}
          onClick={() => onExampleClick(example)}
          className="text-sm bg-white border border-gray-300 hover:bg-gray-50 text-gray-700 px-3 py-1 rounded-full transition-colors"
        >
          {example}
        </button>
      ))}
    </div>
  );
};

export default ExampleQueries;