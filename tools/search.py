"""
tools/search.py - Web Search Tool
Uses Tavily API for web search capabilities.
"""

import os
from langchain_core.tools import tool

# Check if Tavily is available
try:
    from tavily import TavilyClient
    TAVILY_AVAILABLE = True
except ImportError:
    TAVILY_AVAILABLE = False


@tool
def web_search(query: str, max_results: int = 5) -> str:
    """
    Search the web for information on a topic.
    
    Args:
        query: The search query
        max_results: Maximum number of results to return (default 5)
        
    Returns:
        A formatted string with search results
    """
    if not TAVILY_AVAILABLE:
        return "Web search is not available. Please install tavily-python: pip install tavily-python"
    
    api_key = os.getenv("TAVILY_API_KEY", "")
    if not api_key:
        return "Web search requires a TAVILY_API_KEY. Get one free at https://tavily.com"
    
    try:
        client = TavilyClient(api_key=api_key)
        response = client.search(query, max_results=max_results)
        
        results = []
        for i, result in enumerate(response.get("results", []), 1):
            title = result.get("title", "No title")
            content = result.get("content", "No content")
            url = result.get("url", "")
            results.append(f"{i}. **{title}**\n   {content}\n   Source: {url}")
        
        if results:
            return "\n\n".join(results)
        else:
            return "No results found for your query."
            
    except Exception as e:
        return f"Search error: {str(e)}"
