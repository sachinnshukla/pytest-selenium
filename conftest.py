#!/usr/bin/env python3
"""
Simple conftest.py for Selenium Testing Framework
Just the essentials - driver, screenshots, allure helpers, and base URL
"""

import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
# Simplified - no WebDriver Manager for now
import allure
from allure_commons.types import AttachmentType
from datetime import datetime
from pathlib import Path
from config import config, get_base_url


def pytest_addoption(parser):
    """Add command line options"""
    parser.addoption(
        "--browser", action="store", default=None,
        help="Browser to use (chrome/firefox/edge). Overrides config file"
    )
    parser.addoption(
        "--headless", action="store_true", default=None,
        help="Run tests in headless mode"
    )


@pytest.fixture(scope="session")
def driver(request):
    """Create WebDriver instance"""
    
    # Get browser from command line or config
    browser_name = request.config.getoption("--browser") or config.BROWSER
    headless = request.config.getoption("--headless") or config.HEADLESS
    
    # Force headless mode in CI environments
    if os.getenv('CI', 'false').lower() == 'true':
        headless = True
    
    print(f"\n🚀 Starting {browser_name} browser (headless: {headless})")
    
    # Create WebDriver (simplified - Chrome only for now)
    if browser_name.lower() == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument(f"--window-size={config.WINDOW_WIDTH},{config.WINDOW_HEIGHT}")
        
        try:
            # Try to use Chrome without WebDriver Manager first
            driver_instance = webdriver.Chrome(options=options)
        except Exception as e:
            print(f"❌ Failed to start Chrome: {e}")
            print("💡 Please install ChromeDriver manually or use a different browser")
            raise
        
    else:
        # For demo purposes, let's create a simple mock or skip
        print(f"⚠️  Browser '{browser_name}' not yet configured in simplified mode")
        print("💡 Using Chrome as fallback...")
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        
        try:
            driver_instance = webdriver.Chrome(options=options)
        except Exception as e:
            print(f"❌ Failed to start Chrome: {e}")
            print("💡 Please install ChromeDriver or configure WebDriver Manager")
            raise
    
    # Configure timeouts
    driver_instance.implicitly_wait(config.IMPLICIT_WAIT)
    driver_instance.set_page_load_timeout(config.PAGE_LOAD_TIMEOUT)
    
    # Set window size (if not headless)
    if not headless:
        driver_instance.set_window_size(config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
    
    yield driver_instance
    
    print(f"\n🔚 Closing {browser_name} browser")
    driver_instance.quit()


@pytest.fixture(autouse=True)
def navigate_to_app(driver):
    """Navigate to application URL before each test"""
    base_url = get_base_url()
    print(f"\n🌐 Navigating to: {base_url}")
    driver.get(base_url)


@pytest.fixture
def take_screenshot(request, driver):
    """Screenshot capture helper"""
    def capture_screenshot(name="screenshot"):
        """Capture screenshot and attach to Allure report"""
        try:
            # Create screenshots directory
            screenshots_dir = Path(config.SCREENSHOTS_DIR)
            screenshots_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_name = request.node.name.replace("::", "_").replace(" ", "_")
            filename = f"{test_name}_{name}_{timestamp}.png"
            screenshot_path = screenshots_dir / filename
            
            # Capture screenshot
            screenshot_bytes = driver.get_screenshot_as_png()
            
            # Save to file
            with open(screenshot_path, 'wb') as f:
                f.write(screenshot_bytes)
            
            # Attach to Allure report
            allure.attach(
                screenshot_bytes,
                name=f"Screenshot - {name}",
                attachment_type=AttachmentType.PNG
            )
            
            print(f"📸 Screenshot saved: {screenshot_path}")
            return str(screenshot_path)
            
        except Exception as e:
            print(f"❌ Failed to capture screenshot: {e}")
            return None
    
    return capture_screenshot


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture screenshot on test failure"""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call" and report.failed:
        # Get the driver from the test's fixtures
        if hasattr(item, 'funcargs') and 'driver' in item.funcargs:
            driver = item.funcargs['driver']
            
            try:
                # Create screenshots directory
                screenshots_dir = Path(config.SCREENSHOTS_DIR)
                screenshots_dir.mkdir(parents=True, exist_ok=True)
                
                # Generate filename for failure screenshot
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                test_name = item.name.replace("::", "_").replace(" ", "_")
                filename = f"FAILED_{test_name}_{timestamp}.png"
                screenshot_path = screenshots_dir / filename
                
                # Capture and save screenshot
                screenshot_bytes = driver.get_screenshot_as_png()
                with open(screenshot_path, 'wb') as f:
                    f.write(screenshot_bytes)
                
                # Attach to Allure report
                allure.attach(
                    screenshot_bytes,
                    name="❌ Test Failure Screenshot",
                    attachment_type=AttachmentType.PNG
                )
                
                print(f"\n📸 Failure screenshot saved: {screenshot_path}")
                
            except Exception as e:
                print(f"\n❌ Failed to capture failure screenshot: {e}")


# Allure reporting helpers
@allure.step("Opening application")
def allure_open_app(driver, url):
    """Allure step for opening application"""
    driver.get(url)


@allure.step("Taking screenshots: {name}")
def allure_screenshot(driver, name="screenshot"):
    """Allure step for taking screenshots"""
    screenshot_bytes = driver.get_screenshot_as_png()
    allure.attach(
        screenshot_bytes,
        name=name,
        attachment_type=AttachmentType.PNG
    )
    return screenshot_bytes