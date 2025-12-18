"""
agents/reviewer.py - Reviewer Agent
Reviews draft content and decides if it should be approved or revised.
This is the original reviewer from the user's code.
"""

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from config import DEFAULT_MODEL, DEFAULT_TEMPERATURE


class ReviewerAgent:
    """
    Agent that reviews draft content and makes editorial decisions.
    Returns one of: APPROVE, REVISE_WRITER, REVISE_SEARCHER
    """
    
    def __init__(self):
        self.llm = ChatGroq(
            model_name=DEFAULT_MODEL,
            temperature=DEFAULT_TEMPERATURE,
        )
        
        self.prompt = ChatPromptTemplate.from_template(
            """You are a pragmatic editor. Your goal is to ensure an article is factually correct,
coherent, and reasonably comprehensive. Do not aim for perfection.

Review the draft based on the topic. Your decision MUST be one of three choices:
'DECISION: APPROVE'
'DECISION: REVISE_WRITER'
'DECISION: REVISE_SEARCHER'

Follow these rules:
1. If the article is well-written and covers the main points of the topic, APPROVE it.
2. If the article has good information but is poorly structured or unclear,
   choose REVISE_WRITER.
3. If the article lacks key information or seems factually thin,
   choose REVISE_SEARCHER.

Provide a concise reason for your decision, then end with the required DECISION line.

Topic: {topic}
Draft Article:
{draft}

Your Critique:
"""
        )
        
        self.chain = self.prompt | self.llm | StrOutputParser()
    
    def review(self, topic: str, draft: str) -> dict:
        """
        Review a draft and return a decision.
        
        Args:
            topic: The topic being reviewed
            draft: The draft content to review
            
        Returns:
            Dict with 'decision' and 'reason' keys
        """
        response_text = self.chain.invoke({"topic": topic, "draft": draft})
        
        # Parse the decision from the response
        decision = "UNKNOWN"
        for line in response_text.splitlines():
            line = line.strip()
            if line.startswith("DECISION:"):
                decision = line.replace("DECISION:", "").strip()
                break
        
        reason = response_text.replace(f"DECISION: {decision}", "").strip()
        
        return {
            "decision": decision,
            "reason": reason
        }
