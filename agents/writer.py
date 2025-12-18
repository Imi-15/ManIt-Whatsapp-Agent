"""
agents/writer.py - Writer Agent
Responsible for creating polished written content.
"""

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from config import DEFAULT_MODEL, DEFAULT_TEMPERATURE


class WriterAgent:
    """
    Agent that writes and refines text content.
    Can write emails, articles, messages, and other text.
    """
    
    def __init__(self):
        self.llm = ChatGroq(
            model_name=DEFAULT_MODEL,
            temperature=0.3,  # Slightly more creative for writing
        )
        
        self.prompt = ChatPromptTemplate.from_template(
            """You are a skilled writer. Your job is to create clear, engaging,
            and well-structured written content.

            Task: {task}
            
            Content/Topic: {content}
            
            Additional Instructions: {instructions}
            
            Write the requested content below:
            """
        )
        
        self.chain = self.prompt | self.llm | StrOutputParser()
    
    def write(self, task: str, content: str, instructions: str = "") -> str:
        """
        Write content based on the given task.
        
        Args:
            task: What to write (e.g., "email", "article", "summary")
            content: The topic or source content
            instructions: Additional instructions or style guidance
            
        Returns:
            The written content
        """
        return self.chain.invoke({
            "task": task,
            "content": content,
            "instructions": instructions
        })
    
    def rewrite(self, original: str, feedback: str) -> str:
        """
        Rewrite content based on feedback.
        
        Args:
            original: The original text to revise
            feedback: What to improve
            
        Returns:
            The revised content
        """
        rewrite_prompt = ChatPromptTemplate.from_template(
            """You are a skilled editor. Revise the following text based on the feedback.

            Original Text:
            {original}
            
            Feedback to Address:
            {feedback}
            
            Revised Text:
            """
        )
        chain = rewrite_prompt | self.llm | StrOutputParser()
        return chain.invoke({"original": original, "feedback": feedback})
