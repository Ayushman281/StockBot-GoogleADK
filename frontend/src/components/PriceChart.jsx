import React, { useState, useEffect } from 'react';
import { Maximize2, Minimize2 } from 'lucide-react';

const generateChartData = (ticker, timeframe) => {
  const dataPoints = timeframe === 'today' ? 24 : 
                     timeframe === 'week' ? 7 : 
                     timeframe === 'month' ? 30 : 14;
  
  const data = [];
  let currentValue = 100 + Math.random() * 50;
  
  for (let i = 0; i < dataPoints; i++) {
    const change = (Math.random() - 0.48) * 5;
    currentValue += change;
    currentValue = Math.max(currentValue, 50);
    
    data.push({
      time: i,
      value: currentValue.toFixed(2)
    });
  }
  
  return data;
};

const PriceChart = ({ ticker, timeframe }) => {
  const [chartData, setChartData] = useState([]);
  const [selectedTimeframe, setSelectedTimeframe] = useState(timeframe || 'today');
  const [isLoading, setIsLoading] = useState(true);
  const [hoverPoint, setHoverPoint] = useState(null);
  const [isExpanded, setIsExpanded] = useState(false);
  
  const timeframes = [
    { id: 'today', label: '1D' },
    { id: 'week', label: '1W' },
    { id: 'month', label: '1M' },
    { id: 'quarter', label: '3M' }
  ];
  
  useEffect(() => {
    setIsLoading(true);
    
    const timer = setTimeout(() => {
      const data = generateChartData(ticker, selectedTimeframe);
      setChartData(data);
      setIsLoading(false);
    }, 600);
    
    return () => clearTimeout(timer);
  }, [ticker, selectedTimeframe]);
  
  const isPositive = chartData.length > 1 && 
    parseFloat(chartData[chartData.length - 1].value) > parseFloat(chartData[0].value);
  
  const chartColor = isPositive ? '#22C55E' : '#EF4444';
  const fillColor = isPositive ? 'rgba(34, 197, 94, 0.1)' : 'rgba(239, 68, 68, 0.1)';
  
  const chartWidth = 100;
  const chartHeight = 50;
  const maxValue = chartData.length > 0 ? Math.max(...chartData.map(d => parseFloat(d.value))) : 0;
  const minValue = chartData.length > 0 ? Math.min(...chartData.map(d => parseFloat(d.value))) : 0;
  const valueRange = maxValue - minValue;
  
  const generatePath = () => {
    if (chartData.length === 0) return '';
    
    const points = chartData.map((point, index) => {
      const x = (index / (chartData.length - 1)) * chartWidth;
      const y = chartHeight - ((parseFloat(point.value) - minValue) / valueRange) * chartHeight;
      return `${index === 0 ? 'M' : 'L'} ${x} ${y}`;
    }).join(' ');

    return `${points} L ${chartWidth} ${chartHeight} L 0 ${chartHeight} Z`;
  };

  const handleMouseMove = (event) => {
    const svgBounds = event.currentTarget.getBoundingClientRect();
    const x = event.clientX - svgBounds.left;
    const xPercent = x / svgBounds.width;
    const dataIndex = Math.min(
      Math.floor(xPercent * chartData.length),
      chartData.length - 1
    );
    
    if (dataIndex >= 0 && dataIndex < chartData.length) {
      const value = chartData[dataIndex].value;
      const xPos = (dataIndex / (chartData.length - 1)) * chartWidth;
      const yPos = chartHeight - ((parseFloat(value) - minValue) / valueRange) * chartHeight;
      
      setHoverPoint({
        x: xPos,
        y: yPos,
        value: value,
        time: selectedTimeframe === 'today' 
          ? `${Math.floor(dataIndex / (24/timeframes.length))}:00`
          : `Day ${dataIndex + 1}`
      });
    }
  };

  const handleMouseLeave = () => {
    setHoverPoint(null);
  };

  const formatTimeLabel = (index, total) => {
    if (selectedTimeframe === 'today') {
      const hour = Math.floor((24 / total) * index);
      return `${hour}:00`;
    }
    return `Day ${index + 1}`;
  };

  const formatPrice = (value) => {
    if (value >= 1000) {
      return `${(value / 1000).toFixed(1)}k`;
    }
    return value.toFixed(2);
  };
  
  const toggleExpand = () => {
    setIsExpanded(!isExpanded);
  };

  return (
    <div className="relative">
      <div className="flex justify-between items-center mb-4">
        <h3 className="font-medium text-gray-900">Price Chart</h3>
        
        <div className="flex space-x-1 items-center">
          <div className="flex space-x-1">
            {timeframes.map(tf => (
              <button
                key={tf.id}
                className={`px-3 py-1 text-xs font-medium rounded-md transition-colors
                  ${selectedTimeframe === tf.id 
                    ? 'bg-[#1E40AF] text-white' 
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'}`}
                onClick={() => setSelectedTimeframe(tf.id)}
              >
                {tf.label}
              </button>
            ))}
          </div>
          
          <button 
            onClick={toggleExpand}
            className="ml-2 p-1 rounded-full hover:bg-gray-100"
            aria-label={isExpanded ? "Minimize chart" : "Expand chart"}
            title={isExpanded ? "Minimize chart" : "Expand chart"}
          >
            {isExpanded ? 
              <Minimize2 className="w-4 h-4 text-gray-600" /> : 
              <Maximize2 className="w-4 h-4 text-gray-600" />
            }
          </button>
        </div>
      </div>
      
      {isExpanded && (
        <div className="fixed inset-0 z-50 bg-white p-6 flex flex-col">
          <div className="flex justify-between items-center mb-4">
            <h3 className="font-medium text-gray-900">Price Chart (Expanded)</h3>
            <button
              onClick={toggleExpand}
              className="p-2 rounded-md hover:bg-gray-100"
              aria-label="Close expanded view"
            >
              <Minimize2 className="w-5 h-5 text-gray-600" />
            </button>
          </div>
          <div className="flex-grow bg-white border border-gray-200 rounded-lg p-4">
            {isLoading ? (
              <div className="animate-pulse flex flex-col items-center">
                <div className="h-4 w-32 bg-gray-200 rounded mb-3"></div>
                <div className="h-[400px] w-full bg-gray-100 rounded"></div>
              </div>
            ) : (
              <div className="w-full h-full">
                <svg 
                  width="100%" 
                  height="100%" 
                  viewBox={`-25 -10 ${chartWidth + 45} ${chartHeight + 30}`} 
                  preserveAspectRatio="none"
                  onMouseMove={handleMouseMove}
                  onMouseLeave={handleMouseLeave}
                  className="cursor-crosshair"
                >
                  {[...Array(5)].map((_, i) => (
                    <line
                      key={`grid-${i}`}
                      x1="0"
                      y1={i * (chartHeight / 4)}
                      x2={chartWidth}
                      y2={i * (chartHeight / 4)}
                      stroke="#f0f0f0"
                      strokeWidth="0.5"
                    />
                  ))}
                  
                  <path
                    d={generatePath()}
                    fill={fillColor}
                    strokeWidth="0"
                  />
                  
                  <path
                    d={generatePath()}
                    fill="none"
                    stroke={chartColor}
                    strokeWidth="1.5"
                  />

                  {hoverPoint && (
                    <>
                      <line
                        x1={hoverPoint.x}
                        y1="0"
                        x2={hoverPoint.x}
                        y2={chartHeight}
                        stroke="#94A3B8"
                        strokeWidth="0.5"
                        strokeDasharray="2,2"
                      />
                      <circle
                        cx={hoverPoint.x}
                        cy={hoverPoint.y}
                        r="3"
                        fill={chartColor}
                        stroke="white"
                        strokeWidth="1.5"
                      />
                      <rect
                        x={hoverPoint.x - 40}
                        y={hoverPoint.y - 25}
                        width="80"
                        height="20"
                        rx="4"
                        fill="rgba(0, 0, 0, 0.75)"
                      />
                      <text
                        x={hoverPoint.x}
                        y={hoverPoint.y - 12}
                        textAnchor="middle"
                        fill="white"
                        fontSize="8"
                      >
                        ${hoverPoint.value} • {hoverPoint.time}
                      </text>
                    </>
                  )}
                </svg>
              </div>
            )}
          </div>
        </div>
      )}
      
      <div className="bg-white rounded-lg border border-gray-200 p-4" style={{ height: '220px' }}>
        {isLoading ? (
          <div className="animate-pulse flex flex-col items-center">
            <div className="h-4 w-32 bg-gray-200 rounded mb-3"></div>
            <div className="h-[180px] w-full bg-gray-100 rounded"></div>
          </div>
        ) : (
          <div className="w-full h-full">
            <svg 
              width="100%" 
              height="100%" 
              viewBox={`-25 -10 ${chartWidth + 45} ${chartHeight + 30}`} 
              preserveAspectRatio="none"
              onMouseMove={handleMouseMove}
              onMouseLeave={handleMouseLeave}
              className="cursor-crosshair"
            >
              {[...Array(5)].map((_, i) => (
                <line
                  key={`grid-${i}`}
                  x1="0"
                  y1={i * (chartHeight / 4)}
                  x2={chartWidth}
                  y2={i * (chartHeight / 4)}
                  stroke="#f0f0f0"
                  strokeWidth="0.5"
                />
              ))}
              
              <path
                d={generatePath()}
                fill={fillColor}
                strokeWidth="0"
              />
              
              <path
                d={generatePath()}
                fill="none"
                stroke={chartColor}
                strokeWidth="1.5"
              />

              {hoverPoint && (
                <>
                  <line
                    x1={hoverPoint.x}
                    y1="0"
                    x2={hoverPoint.x}
                    y2={chartHeight}
                    stroke="#94A3B8"
                    strokeWidth="0.5"
                    strokeDasharray="2,2"
                  />
                  <circle
                    cx={hoverPoint.x}
                    cy={hoverPoint.y}
                    r="3"
                    fill={chartColor}
                    stroke="white"
                    strokeWidth="1.5"
                  />
                  <rect
                    x={hoverPoint.x - 40}
                    y={hoverPoint.y - 25}
                    width="80"
                    height="20"
                    rx="4"
                    fill="rgba(0, 0, 0, 0.75)"
                  />
                  <text
                    x={hoverPoint.x}
                    y={hoverPoint.y - 12}
                    textAnchor="middle"
                    fill="white"
                    fontSize="8"
                  >
                    ${hoverPoint.value} • {hoverPoint.time}
                  </text>
                </>
              )}
            </svg>
          </div>
        )}
      </div>
    </div>
  );
};

export default PriceChart;