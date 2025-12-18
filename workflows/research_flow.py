"""
workflows/research_flow.py - Main Workflow
LangGraph workflow that uses planner → executor pattern from original code.
"""

import json
from typing import TypedDict

from langgraph.graph import StateGraph, END

from agents.planner import PlannerAgent
from agents.writer import WriterAgent
from agents.reviewer import ReviewerAgent
from tools.calculator import calculator
from tools.search import web_search
from tools.email_sender import email_sender
from tools.file_ops import create_docx


# =============================================================================
# STATE DEFINITION
# =============================================================================

class AgentState(TypedDict):
    """State that flows through the workflow (matches original code)."""
    user_message: str       # What the person typed on WhatsApp
    plan_json: str          # Planner's JSON text
    last_tool_result: str   # Result from the last tool execution
    final_reply: str        # Final response to send back


# =============================================================================
# PLANNER NODE
# =============================================================================

def planner_node(state: AgentState) -> dict:
    """
    Node 1: Look at the user_message and create a JSON plan.
    Uses the PlannerAgent to decide which tools to use.
    """
    print("--- 🧠 PLANNING ---")
    
    planner = PlannerAgent()
    plan_text = planner.create_plan(state["user_message"])
    
    return {"plan_json": plan_text}


# =============================================================================
# EXECUTOR NODE
# =============================================================================

def executor_node(state: AgentState) -> dict:
    """
    Node 2: Read plan_json and execute the steps.
    This matches the original executor logic from the user's code.
    """
    print("--- 🛠️ EXECUTING PLAN ---")
    
    plan_text = state.get("plan_json", "{}")
    
    # Parse the plan
    try:
        plan = json.loads(plan_text)
    except json.JSONDecodeError:
        reply = "Sorry, I could not understand the plan."
        return {"last_tool_result": reply, "final_reply": reply}
    
    steps = plan.get("steps", [])
    if not steps:
        reply = "I could not find any actions to take for your request."
        return {"last_tool_result": reply, "final_reply": reply}
    
    # Initialize agents
    writer = WriterAgent()
    reviewer = ReviewerAgent()
    
    # Execute each step
    result_text = ""
    
    for step in steps:
        tool_name = step.get("tool")
        tool_input = step.get("input", "")
        
        if tool_name == "calculator":
            try:
                result = calculator.invoke({"expression": tool_input})
                result_text = f"The result of your calculation is: {result}"
            except Exception as e:
                result_text = f"Calculator error: {e}"
        
        elif tool_name == "writer":
            # Use the WriterAgent
            result_text = writer.write(
                task=step.get("description", "write"),
                content=tool_input,
                instructions=""
            )
        
        elif tool_name == "reviewer":
            # Use the ReviewerAgent
            review = reviewer.review(topic="User request", draft=tool_input)
            result_text = f"Review decision: {review['decision']}.\nReason: {review['reason']}"
        
        elif tool_name == "email_sender":
            # Use email sender tool
            result_text = email_sender.invoke({"email_body": tool_input})
        
        elif tool_name == "search":
            try:
                result_text = web_search.invoke({"query": tool_input})
            except Exception as e:
                result_text = f"Search error: {e}"
        
        elif tool_name == "create_document":
            try:
                doc_result = create_docx.invoke({
                    "title": plan.get("overall_goal", "Document"),
                    "content": tool_input if tool_input else result_text
                })
                result_text = doc_result
            except Exception as e:
                result_text = f"Document creation error: {e}"
        
        else:
            result_text = f"I am not sure which tool to use for: {tool_name}"
    
    return {"last_tool_result": result_text, "final_reply": result_text}


# =============================================================================
# BUILD WORKFLOW
# =============================================================================

def create_workflow():
    """Create and compile the workflow graph."""
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("planner", planner_node)
    workflow.add_node("executor", executor_node)
    
    # Define flow: planner → executor → END
    workflow.set_entry_point("planner")
    workflow.add_edge("planner", "executor")
    workflow.add_edge("executor", END)
    
    return workflow.compile()


def run_workflow(user_message: str) -> str:
    """
    Run the workflow with a user message.
    
    Args:
        user_message: The user's request
        
    Returns:
        The final reply string
    """
    graph = create_workflow()
    
    # Stream through the graph
    last_state = None
    for s in graph.stream({"user_message": user_message}):
        last_state = s
    
    if last_state:
        last_node_name = list(last_state.keys())[0]
        return last_state[last_node_name].get(
            "final_reply", "Sorry, I could not create a reply."
        )
    
    return "No response generated."


# Create a compiled graph instance for import
app_graph = create_workflow()
print("✅ WhatsApp AI assistant LangGraph compiled!")
