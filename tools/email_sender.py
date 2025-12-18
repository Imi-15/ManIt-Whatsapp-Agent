"""
tools/email_sender.py - Email Sender Tool
Placeholder for sending/scheduling emails.
"""

from langchain_core.tools import tool


@tool
def email_sender(email_body: str, recipient: str = "", subject: str = "") -> str:
    """
    Send or schedule an email (placeholder - integrate with Gmail/SendGrid/etc.)
    
    Args:
        email_body: The body text of the email
        recipient: Email recipient address
        subject: Email subject line
        
    Returns:
        Status message about the email
    """
    # This is a placeholder - you can integrate with:
    # - Gmail API
    # - SendGrid
    # - AWS SES
    # - Any SMTP server
    
    result = f"""📧 Email Draft Ready:
    
To: {recipient if recipient else '[recipient not specified]'}
Subject: {subject if subject else '[no subject]'}

{email_body}

---
⚠️ Note: This is a placeholder. Integrate with an email service to actually send."""
    
    return result
