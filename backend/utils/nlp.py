import re

def extract_timeframe(text):
    """
    Extract timeframe information from query text.
    
    Args:
        text (str): The query text
        
    Returns:
        str: Identified timeframe ('today', 'week', 'month', etc.)
    """
    text = text.lower()
    
    # Define patterns for different timeframes
    timeframe_patterns = [
        (r'\btoday\b', 'today'),
        (r'\byesterday\b', 'yesterday'),
        (r'\blast\s+day\b', 'today'),
        (r'\blast\s+week\b|\bpast\s+week\b|\b7\s+days\b|\bseven\s+days\b', 'week'),
        (r'\blast\s+month\b|\bpast\s+month\b|\b30\s+days\b|\bthirty\s+days\b', 'month'),
        (r'\blast\s+3\s+months\b|\bpast\s+3\s+months\b|\bthree\s+months\b|\b90\s+days\b', '3months'),
        (r'\blast\s+6\s+months\b|\bpast\s+6\s+months\b|\bsix\s+months\b|\b180\s+days\b', '6months'),
        (r'\blast\s+year\b|\bpast\s+year\b|\btwelve\s+months\b|\b365\s+days\b', 'year'),
        (r'\brecently\b', 'week'),  # Default "recently" to one week
    ]
    
    # Check for each pattern
    for pattern, timeframe in timeframe_patterns:
        if re.search(pattern, text):
            return timeframe
    
    # Default to "today" if no timeframe is found
    return "today"
