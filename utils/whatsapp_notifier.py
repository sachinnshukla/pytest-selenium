#!/usr/bin/env python3
"""
WhatsApp Notification System for Selenium Test Results
Sends Allure dashboard URL to WhatsApp using Twilio API
"""

import os
import sys
from datetime import datetime
from twilio.rest import Client

# Import our custom config
from utils.whatsapp_config import whatsapp_config


def send_whatsapp_notification(dashboard_url, status="success", additional_info=None):
    """
    Send WhatsApp notification with test results and dashboard URL
    
    Args:
        dashboard_url (str): URL to the Allure dashboard
        status (str): Test status - "success" or "failure"
        additional_info (dict): Additional information like commit, branch, etc.
    
    Returns:
        bool: True if message sent successfully, False otherwise
    """
    
    # Get Twilio credentials from config
    credentials = whatsapp_config.get_credentials()
    account_sid = credentials['account_sid']
    auth_token = credentials['auth_token']
    from_whatsapp = credentials['from_number']
    to_whatsapp = credentials['to_number']
    
    # Validate configuration
    if not whatsapp_config.is_configured():
        print("❌ WhatsApp configuration is incomplete")
        whatsapp_config.print_config_status()
        return False
    
    # Validate credential format
    is_valid, error = whatsapp_config.validate_credentials()
    if not is_valid:
        print(f"❌ Configuration error: {error}")
        return False
    
    try:
        # Initialize Twilio client
        client = Client(account_sid, auth_token)
        
        # Create message content based on status
        if status == "success":
            emoji = "✅"
            status_text = "PASSED"
            message_body = f"""🎉 *Selenium Tests Completed Successfully!*

{emoji} *Status:* {status_text}
📊 *Live Dashboard:* {dashboard_url}
📅 *Completed:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
        else:
            emoji = "❌"
            status_text = "FAILED"
            message_body = f"""🚨 *Selenium Tests Failed!*

{emoji} *Status:* {status_text}
🔍 *Check logs for details*
📅 *Failed at:* {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"""
        
        # Add additional info if provided
        if additional_info:
            if additional_info.get('repository'):
                message_body += f"\n📁 *Repository:* {additional_info['repository']}"
            if additional_info.get('branch'):
                message_body += f"\n🌿 *Branch:* {additional_info['branch']}"
            if additional_info.get('commit'):
                message_body += f"\n💾 *Commit:* {additional_info['commit'][:8]}"
            if additional_info.get('workflow_url'):
                message_body += f"\n🔗 *Full Results:* {additional_info['workflow_url']}"
        
        # Send WhatsApp message
        message = client.messages.create(
            body=message_body,
            from_=from_whatsapp,
            to=to_whatsapp
        )
        
        print(f"✅ WhatsApp message sent successfully!")
        print(f"📱 Message SID: {message.sid}")
        print(f"📞 To: {to_whatsapp}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send WhatsApp message: {str(e)}")
        return False


def send_test_completion_notification(dashboard_url, workflow_info=None):
    """
    Convenience function for test completion notifications
    
    Args:
        dashboard_url (str): URL to the Allure dashboard
        workflow_info (dict): GitHub workflow information
    """
    additional_info = workflow_info or {}
    return send_whatsapp_notification(
        dashboard_url=dashboard_url,
        status="success",
        additional_info=additional_info
    )


def send_test_failure_notification(workflow_info=None):
    """
    Convenience function for test failure notifications
    
    Args:
        workflow_info (dict): GitHub workflow information
    """
    additional_info = workflow_info or {}
    return send_whatsapp_notification(
        dashboard_url=None,
        status="failure", 
        additional_info=additional_info
    )


if __name__ == "__main__":
    """
    Command line usage for GitHub Actions
    """
    if len(sys.argv) < 2:
        print("Usage: python whatsapp_notifier.py <status> [dashboard_url] [additional_args...]")
        print("Examples:")
        print("  python whatsapp_notifier.py success https://user.github.io/repo/")
        print("  python whatsapp_notifier.py failure")
        sys.exit(1)
    
    status = sys.argv[1].lower()
    dashboard_url = sys.argv[2] if len(sys.argv) > 2 and status == "success" else None
    
    # Parse additional arguments from GitHub Actions environment
    additional_info = {
        'repository': os.getenv('GITHUB_REPOSITORY'),
        'branch': os.getenv('GITHUB_REF_NAME'),
        'commit': os.getenv('GITHUB_SHA'),
        'workflow_url': f"{os.getenv('GITHUB_SERVER_URL')}/{os.getenv('GITHUB_REPOSITORY')}/actions/runs/{os.getenv('GITHUB_RUN_ID')}" if os.getenv('GITHUB_RUN_ID') else None
    }
    
    # Send appropriate notification
    if status == "success" and dashboard_url:
        success = send_test_completion_notification(dashboard_url, additional_info)
    elif status == "failure":
        success = send_test_failure_notification(additional_info)
    else:
        print("❌ Invalid arguments")
        sys.exit(1)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)
