import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
import config
from config.environment_manager import environment_manager
import os
from datetime import datetime
from pathlib import Path
import allure
from allure_commons.types import AttachmentType

def pytest_addoption(parser):
    """Add command line options for environment and browser selection"""
    parser.addoption(
        "--env", action="store", default="prod",
        help="Environment to run tests against (dev/staging/prod). Default: prod"
    )
    parser.addoption(
        "--browser", action="store", default=None,
        help="Browser to use (chrome/firefox/edge). Overrides environment config"
    )
    parser.addoption(
        "--headless", action="store_true", default=None,
        help="Run tests in headless mode. Overrides environment config"
    )
    parser.addoption(
        "--screenshot-on-failure", action="store_true", default=True,
        help="Capture screenshot on test failure (default: True)"
    )
    parser.addoption(
        "--allure-attach-screenshot", action="store_true", default=True,
        help="Attach screenshots to Allure reports on failure (default: True)"
    )


@pytest.fixture(scope="session")
def test_environment(request):
    """Load and configure the test environment"""
    env_name = request.config.getoption("--env")
    
    # Load environment configuration
    env_config = environment_manager.load_environment(env_name)
    
    # Override with command line options if provided
    browser_override = request.config.getoption("--browser")
    headless_override = request.config.getoption("--headless")
    
    if browser_override:
        env_config.browser = browser_override
    if headless_override is not None:
        env_config.headless = headless_override
    
    # Print configuration for debugging
    environment_manager.print_config()
    
    return env_config


@pytest.fixture(scope="session")
def driver(test_environment):
    """Create WebDriver instance based on environment configuration"""
    browser_name = test_environment.browser.lower()
    # Force headless mode in CI environments
    headless = test_environment.headless or os.getenv('CI', 'false').lower() == 'true'
    
    # Create browser-specific options
    if browser_name == "chrome":
        options = ChromeOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=options)
    elif browser_name == "firefox":
        options = FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        driver = webdriver.Firefox(options=options)
    elif browser_name == "edge":
        options = EdgeOptions()
        if headless:
            options.add_argument("--headless")
        driver = webdriver.Edge(options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")
    
    # Configure driver timeouts
    driver.implicitly_wait(test_environment.implicit_wait)
    driver.set_page_load_timeout(test_environment.page_load_timeout)
    
    # Set window size
    if not headless:
        driver.set_window_size(
            test_environment.window_size.width,
            test_environment.window_size.height
        )
    
    yield driver
    driver.quit()


@pytest.fixture(autouse=True)
def open_base_url(driver, test_environment):
    """Navigate to base URL before each test"""
    driver.get(test_environment.base_url)


@pytest.fixture
def screenshot_helper(request, driver, test_environment):
    """Screenshot capture helper fixture with Allure integration"""
    def capture_screenshot(name_suffix="", attach_to_allure=True):
        """Capture a screenshot with optional name suffix and Allure attachment"""
        try:
            # Create screenshots directory if it doesn't exist
            screenshots_dir = Path("results/screenshots")
            screenshots_dir.mkdir(parents=True, exist_ok=True)
            
            # Generate filename with timestamp and test info
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_name = request.node.name.replace("::", "_").replace(" ", "_")
            env_name = test_environment.environment
            browser_name = test_environment.browser
            
            if name_suffix:
                filename = f"{test_name}_{env_name}_{browser_name}_{name_suffix}_{timestamp}.png"
                allure_name = f"{name_suffix.replace('_', ' ').title()} - {env_name} {browser_name}"
            else:
                filename = f"{test_name}_{env_name}_{browser_name}_{timestamp}.png"
                allure_name = f"Screenshot - {env_name} {browser_name}"
            
            screenshot_path = screenshots_dir / filename
            
            # Capture screenshot
            screenshot_bytes = driver.get_screenshot_as_png()
            
            # Save to file
            with open(screenshot_path, 'wb') as f:
                f.write(screenshot_bytes)
            
            # Attach to Allure report if enabled
            if attach_to_allure and request.config.getoption("--allure-attach-screenshot", default=True):
                allure.attach(
                    screenshot_bytes,
                    name=allure_name,
                    attachment_type=AttachmentType.PNG
                )
                print(f"\n📸 Screenshot saved and attached to Allure: {screenshot_path}")
            else:
                print(f"\n📸 Screenshot saved: {screenshot_path}")
            
            return str(screenshot_path)
            
        except Exception as e:
            print(f"\n❌ Failed to capture screenshot: {e}")
            return None
    
    return capture_screenshot


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Capture screenshot on test failure and attach to Allure"""
    outcome = yield
    rep = outcome.get_result()
    
    # Only capture screenshot on test failure during the "call" phase
    if rep.when == "call" and rep.failed:
        # Check if screenshot capture is enabled
        screenshot_enabled = item.config.getoption("--screenshot-on-failure", default=True)
        allure_attach_enabled = item.config.getoption("--allure-attach-screenshot", default=True)
        
        if screenshot_enabled and hasattr(item, 'funcargs'):
            # Get driver from test fixtures
            driver = item.funcargs.get('driver')
            test_environment = item.funcargs.get('test_environment')
            
            if driver and test_environment:
                try:
                    # Create screenshots directory
                    screenshots_dir = Path("results/screenshots")
                    screenshots_dir.mkdir(parents=True, exist_ok=True)
                    
                    # Generate failure screenshot filename
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    test_name = item.name.replace("::", "_").replace(" ", "_")
                    env_name = test_environment.environment
                    browser_name = test_environment.browser
                    
                    filename = f"FAILED_{test_name}_{env_name}_{browser_name}_{timestamp}.png"
                    screenshot_path = screenshots_dir / filename
                    
                    # Capture screenshot as bytes for both file and Allure
                    screenshot_bytes = driver.get_screenshot_as_png()
                    
                    # Save screenshot to file
                    with open(screenshot_path, 'wb') as f:
                        f.write(screenshot_bytes)
                    
                    # Attach to Allure report if enabled
                    if allure_attach_enabled:
                        allure.attach(
                            screenshot_bytes,
                            name=f"🚨 Failure Screenshot - {env_name.upper()} {browser_name.upper()}",
                            attachment_type=AttachmentType.PNG
                        )
                        print(f"\n📸 Failure screenshot saved and attached to Allure: {screenshot_path}")
                    else:
                        print(f"\n📸 Failure screenshot saved: {screenshot_path}")
                    
                    # Attach to test report for later use
                    setattr(rep, 'screenshot_path', str(screenshot_path))
                    
                except Exception as e:
                    print(f"\n❌ Failed to capture failure screenshot: {e}")