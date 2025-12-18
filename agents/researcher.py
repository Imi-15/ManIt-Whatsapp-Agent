"""
agents/researcher.py - Researcher Agent
Responsible for gathering and synthesizing information on a topic.
"""

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from config import DEFAULT_MODEL, DEFAULT_TEMPERATURE


class ResearcherAgent:
    """
    Agent that researches topics using available search tools.
    Takes a topic and returns structured research findings.
    """
    
    def __init__(self):
        self.llm = ChatGroq(
            model_name=DEFAULT_MODEL,
            temperature=DEFAULT_TEMPERATURE,
        )
        
        self.prompt = ChatPromptTemplate.from_template(
            """You are a thorough research assistant. Your job is to analyze 
            information and provide comprehensive, well-organized research findings.

            Given the following topic and any search results, synthesize the information
            into a clear research summary.

            Topic: {topic}
            
            Search Results (if any): {search_results}
            
            Provide a well-structured research summary covering:
            1. Key facts and findings
            2. Important details and context
            3. Any notable considerations
            
            Research Summary:
            """
        )
        
        self.chain = self.prompt | self.llm | StrOutputParser()
    
    def research(self, topic: str, search_results: str = "") -> str:
        """
        Perform research on a topic.
        
        Args:
            topic: The topic to research
            search_results: Optional pre-fetched search results
            
        Returns:
            A research summary string
        """
        return self.chain.invoke({
            "topic": topic,
            "search_results": search_results
        })
