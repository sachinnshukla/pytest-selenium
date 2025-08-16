#!/usr/bin/env python3
"""
WhatsApp Configuration for Selenium Test Notifications
Manages Twilio credentials and settings for WhatsApp notifications
"""

import os
from typing import Dict, Optional


class WhatsAppConfig:
    """Configuration class for WhatsApp notifications via Twilio"""
    
    def __init__(self):
        """Initialize WhatsApp configuration with fallback priority:
        1. Environment variables (for GitHub Actions)
        2. Local config values (for development)
        3. Default values
        """
        
        # Twilio Account Settings - Use environment variables for security
        self.account_sid = self._get_config_value(
            env_key='TWILIO_ACCOUNT_SID',
            default_value=None  # No default - must be set via environment variable
        )
        
        self.auth_token = self._get_config_value(
            env_key='TWILIO_AUTH_TOKEN', 
            default_value=None  # No default - must be set via environment variable
        )
        
        # WhatsApp Phone Numbers
        self.from_number = self._get_config_value(
            env_key='TWILIO_WHATSAPP_FROM',
            default_value='whatsapp:+14155238886'  # Twilio sandbox default
        )
        
        self.to_number = self._get_config_value(
            env_key='TWILIO_WHATSAPP_TO',
            default_value=None  # No default - must be set via environment variable
        )
        
        # Message Settings
        self.enable_notifications = True
        self.max_retries = 3
        self.timeout_seconds = 30
        
    def _get_config_value(self, env_key: str, default_value: str) -> str:
        """Get configuration value with environment variable priority"""
        return os.getenv(env_key, default_value)
    
    def get_credentials(self) -> Dict[str, str]:
        """Get Twilio credentials as dictionary"""
        return {
            'account_sid': self.account_sid,
            'auth_token': self.auth_token,
            'from_number': self.from_number,
            'to_number': self.to_number
        }
    
    def is_configured(self) -> bool:
        """Check if all required credentials are available"""
        required_fields = [
            self.account_sid,
            self.auth_token, 
            self.from_number,
            self.to_number
        ]
        return all(field and field.strip() for field in required_fields)
    
    def validate_credentials(self) -> tuple[bool, Optional[str]]:
        """Validate credential format and completeness"""
        
        if not self.account_sid or not self.account_sid.startswith('AC'):
            return False, "Invalid Account SID format (should start with 'AC')"
            
        if not self.auth_token or len(self.auth_token) < 30:
            return False, "Invalid Auth Token format (should be 32+ characters)"
            
        if not self.from_number or not self.from_number.startswith('whatsapp:+'):
            return False, "Invalid from_number format (should be 'whatsapp:+1234567890')"
            
        if not self.to_number or not self.to_number.startswith('whatsapp:+'):
            return False, "Invalid to_number format (should be 'whatsapp:+1234567890')"
            
        return True, None
    
    def print_config_status(self):
        """Print configuration status for debugging"""
        print("🔧 WhatsApp Configuration Status:")
        print(f"  📱 From Number: {self.from_number}")
        print(f"  📞 To Number: {self.to_number}")
        print(f"  🔑 Account SID: {self.account_sid[:10]}...") 
        print(f"  🔐 Auth Token: {'*' * 20}...")
        print(f"  ✅ Configured: {self.is_configured()}")
        
        is_valid, error = self.validate_credentials()
        if is_valid:
            print(f"  ✅ Valid: Yes")
        else:
            print(f"  ❌ Valid: No - {error}")


# Global configuration instance
whatsapp_config = WhatsAppConfig()


# Convenience functions for backward compatibility
def get_whatsapp_credentials():
    """Get WhatsApp credentials dictionary"""
    return whatsapp_config.get_credentials()


def is_whatsapp_enabled():
    """Check if WhatsApp notifications are enabled and configured"""
    return whatsapp_config.enable_notifications and whatsapp_config.is_configured()


if __name__ == "__main__":
    """Test configuration when run directly"""
    config = WhatsAppConfig()
    config.print_config_status()
    
    is_valid, error = config.validate_credentials()
    if is_valid:
        print("\n✅ Configuration is valid and ready to use!")
    else:
        print(f"\n❌ Configuration error: {error}")
