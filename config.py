#!/usr/bin/env python3
import os

class Config:
    """Simple test configuration - edit these values for your application"""
    
    # Application Settings
    BASE_URL = "https://www.saucedemo.com/"
    USERNAME = "standard_user"
    PASSWORD = "secret_sauce"
    
    # Browser Settings
    BROWSER = "chrome"          # Options: chrome, firefox, edge
    HEADLESS = False           # Set to True for headless mode
    WINDOW_WIDTH = 1920
    WINDOW_HEIGHT = 1080
    
    # Timeout Settings (in seconds)
    IMPLICIT_WAIT = 10         # How long to wait for elements
    PAGE_LOAD_TIMEOUT = 30     # How long to wait for pages to load
    
    # Test Settings
    SCREENSHOT_ON_FAILURE = True    # Take screenshot when test fails
    
    # Allure Reporting
    SCREENSHOTS_DIR = "results/screenshots"


def get_base_url():
    """Get the base URL for the application"""
    return os.getenv('TEST_BASE_URL', Config.BASE_URL)


# Global config instance
config = Config()


if __name__ == "__main__":
    """Print configuration when run directly"""
    print("=" * 50)
    print("🔧 Test Configuration")
    print("=" * 50)
    print(f"📱 Base URL: {config.BASE_URL}")
    print(f"👤 Username: {config.USERNAME}")
    print(f"🔐 Password: {'*' * len(config.PASSWORD)}")
    print(f"🌐 Browser: {config.BROWSER}")
    print(f"👁️  Headless: {config.HEADLESS}")
    print(f"📐 Window: {config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")
    print(f"⏱️  Timeouts: {config.IMPLICIT_WAIT}s / {config.PAGE_LOAD_TIMEOUT}s")
    print("=" * 50)