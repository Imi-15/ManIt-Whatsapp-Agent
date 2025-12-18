"""
agents/planner.py - Planner Agent
Decides which tools to use based on user request.
This is the original planner from the user's code.
"""

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from config import DEFAULT_MODEL


class PlannerAgent:
    """
    Agent that analyzes user requests and creates an execution plan.
    Decides which tools (writer, calculator, email_sender, reviewer) to use.
    """
    
    def __init__(self):
        self.llm = ChatGroq(
            model_name=DEFAULT_MODEL,
            temperature=0.3,
        )
        
        self.prompt = ChatPromptTemplate.from_template(
            """
You are a planning assistant for a WhatsApp AI agent.
The agent has these tools:
- writer: writes or rewrites email text or short messages.
- calculator: does math or numeric calculations.
- email_sender: sends or schedules emails using a ready email body.
- reviewer: reviews draft content and decides APPROVE / REVISE_WRITER / REVISE_SEARCHER.
- search: searches the web for current information.
- create_document: creates a Word document with content.

Create a short ordered plan (1–3 steps) for how the agent should solve the user request.

Return ONLY JSON with this shape:
{{
  "overall_goal": "string",
  "steps": [
    {{
      "tool": "writer" | "calculator" | "email_sender" | "reviewer" | "search" | "create_document",
      "description": "string",
      "input": "string"
    }}
  ]
}}

User request:
{user_request}
"""
        )
        
        self.chain = self.prompt | self.llm | StrOutputParser()
    
    def create_plan(self, user_request: str) -> str:
        """
        Create an execution plan for the user request.
        
        Args:
            user_request: What the user wants to accomplish
            
        Returns:
            JSON string with the plan
        """
        return self.chain.invoke({"user_request": user_request})
