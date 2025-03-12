from unittest.mock import MagicMock, patch

import pytest

from kagimcp.server import format_fastgpt_response, search, summarize


def test_search_disabled() -> None:
    """Test that search returns disabled message when ENABLE_SEARCH is False."""
    with patch("kagimcp.server.ENABLE_SEARCH", False):
        result = search(["test query"])
        assert "Search functionality is disabled" in result


def test_search_missing_queries() -> None:
    """Test that search raises ValueError when queries list is empty."""
    with patch("kagimcp.server.ENABLE_SEARCH", True), pytest.raises(
        ValueError, match="Search called with no queries"
    ):
        search([])


def test_search_success() -> None:
    """Test successful search with mocked results."""
    mock_results = [
        {
            "data": [
                {
                    "t": 0,
                    "title": "Test Result",
                    "url": "https://example.com",
                    "published": "2023-05-01",
                    "snippet": "This is a test result snippet."
                }
            ]
        }
    ]
    
    with patch("kagimcp.server.ENABLE_SEARCH", True), \
         patch("kagimcp.server.ThreadPoolExecutor") as mock_executor:
        
        mock_map = mock_executor.return_value.__enter__.return_value.map
        mock_map.return_value = mock_results
        
        result = search(["test query"])
        
        assert "Test Result" in result
        assert "https://example.com" in result
        assert "This is a test result snippet" in result


def test_fastgpt_disabled() -> None:
    """Test that summarize returns disabled message when ENABLE_FASTGPT is False."""
    with patch("kagimcp.server.ENABLE_FASTGPT", False):
        result = summarize("test query")
        assert "FastGPT functionality is disabled" in result


def test_fastgpt_success() -> None:
    """Test successful FastGPT summarize with mocked response."""
    mock_response = MagicMock()
    mock_response.output = "This is a test summary."
    mock_response.references = [
        MagicMock(title="Reference 1", url="https://example.com/ref1"),
        MagicMock(title="Reference 2", url="https://example.com/ref2"),
    ]
    
    with patch("kagimcp.server.ENABLE_FASTGPT", True), \
         patch("kagimcp.server.kagi_client.fastgpt", return_value=mock_response):
        
        result = summarize("test query")
        
        assert "This is a test summary." in result
        assert "Reference 1" in result
        assert "Reference 2" in result
        assert "https://example.com/ref1" in result
        assert "https://example.com/ref2" in result


def test_format_fastgpt_response() -> None:
    """Test FastGPT response formatting with and without references."""
    # Create a mock FastGPTResponse
    mock_response = MagicMock()
    mock_response.output = "This is a test summary."
    
    # Test with no references
    mock_response.references = []
    result = format_fastgpt_response(mock_response)
    assert result == "This is a test summary."
    
    # Test with references
    reference1 = MagicMock()
    reference1.title = "Reference 1"
    reference1.url = "https://example.com/ref1"
    
    reference2 = MagicMock()
    reference2.title = "Reference 2"
    reference2.url = "https://example.com/ref2"
    
    mock_response.references = [reference1, reference2]
    result = format_fastgpt_response(mock_response)
    
    assert "This is a test summary." in result
    assert "## References" in result
    assert "1. [Reference 1](https://example.com/ref1)" in result
    assert "2. [Reference 2](https://example.com/ref2)" in result