import pytest
from agents.orchestrator import StockOrchestratorAgent

def test_orchestrator_initialization():
    """Test that the orchestrator can be initialized"""
    orchestrator = StockOrchestratorAgent()
    assert orchestrator is not None

def test_basic_query():
    """Test basic query about Apple stock"""
    orchestrator = StockOrchestratorAgent()
    result = orchestrator.process_query("What's happening with Apple stock recently?")
    
    # Basic validation - in a real test we'd mock the API calls
    assert isinstance(result, dict)
    assert "answer" in result
    assert "metadata" in result
    assert result["metadata"]["ticker"] == "AAPL"

@pytest.mark.skip(reason="Requires API keys to be set")
def test_price_change_query():
    """Test query about price changes"""
    orchestrator = StockOrchestratorAgent()
    result = orchestrator.process_query("How has Tesla stock changed in the last 7 days?")
    
    assert isinstance(result, dict)
    assert "answer" in result
    assert "metadata" in result
    assert result["metadata"]["ticker"] == "TSLA"
    assert "price_change" in result["metadata"]

@pytest.mark.skip(reason="Requires API keys to be set")
def test_analysis_query():
    """Test query about why stock price changed"""
    orchestrator = StockOrchestratorAgent()
    result = orchestrator.process_query("Why did Microsoft stock drop today?")
    
    assert isinstance(result, dict)
    assert "answer" in result
    assert "metadata" in result
    assert result["metadata"]["ticker"] == "MSFT"
    assert "analysis" in result["metadata"]
