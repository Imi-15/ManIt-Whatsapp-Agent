"""
main.py - Entry Point
FastAPI server with WhatsApp/Twilio integration.
Uses the original planner → executor workflow pattern.
"""

from fastapi import FastAPI, Form
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel

from twilio.twiml.messaging_response import MessagingResponse

# Import configuration (this loads .env automatically)
from config import validate_config, PUBLIC_BASE_URL

# Import the workflow
from workflows.research_flow import run_workflow


# =============================================================================
# VALIDATE CONFIGURATION ON STARTUP
# =============================================================================

print("🚀 Starting ManIt...")
validate_config()


# =============================================================================
# FASTAPI APPLICATION
# =============================================================================

app = FastAPI(
    title="WhatsApp AI Agent",
    description="AI Agent accessible via WhatsApp using Twilio",
    version="1.0.0"
)


class AgentRequest(BaseModel):
    """Request body for the JSON API endpoint."""
    message: str


@app.get("/")
def root():
    """Health check endpoint."""
    return {
        "status": "online",
        "message": "WhatsApp AI Agent is running!",
        "endpoints": {
            "test": "POST /agent-json",
            "whatsapp": "POST /twilio-whatsapp"
        }
    }


@app.post("/agent-json")
def agent_json(req: AgentRequest):
    """
    JSON API endpoint for testing the agent.
    Use this with Postman, curl, or any HTTP client.
    
    Example:
        curl -X POST http://localhost:8000/agent-json \
             -H "Content-Type: application/json" \
             -d '{"message": "What is 25 * 4?"}'
    """
    print(f"📨 Received JSON request: {req.message}")
    
    try:
        response = run_workflow(req.message)
        return {"reply": response}
    except Exception as e:
        return {"reply": f"Error: {str(e)}"}

@app.post("/twilio-whatsapp")
async def twilio_whatsapp(
    From: str = Form(...),
    Body: str = Form(...),
):
    """
    Webhook endpoint for Twilio WhatsApp messages.
    Configure this URL in Twilio Sandbox: "WHEN A MESSAGE COMES IN"
    
    Twilio sends:
        - From: The sender's WhatsApp number (e.g., whatsapp:+1234567890)
        - Body: The message text
    """
    print(f"📱 WhatsApp message from {From}: {Body}")
    
    try:
        # Run the agent workflow
        response = run_workflow(Body)
    except Exception as e:
        response = f"Sorry, I encountered an error: {str(e)}"
    
    # Build TwiML response
    twiml = MessagingResponse()
    twiml.message(response)
    
    # Return as XML
    return PlainTextResponse(str(twiml), media_type="application/xml")


# =============================================================================
# STARTUP MESSAGE
# =============================================================================

print("✅ WhatsApp AI Agent ready!")
print(f"   Configure Twilio webhook: {PUBLIC_BASE_URL}/twilio-whatsapp")
