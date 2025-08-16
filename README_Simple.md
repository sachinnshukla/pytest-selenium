# 🧪 Simple Selenium Testing Framework

A clean, simple Selenium test automation framework using pytest with Allure reporting and WhatsApp notifications.

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Your Tests
Edit `config.py` with your application details:

```python
class TestConfig:
    # Your application settings
    BASE_URL = "https://www.saucedemo.com/"
    USERNAME = "standard_user"
    PASSWORD = "secret_sauce"
    
    # Browser settings
    BROWSER = "chrome"          # Options: chrome, firefox, edge
    HEADLESS = False           # Set to True for headless mode
```

### 3. Run Tests
```bash
# Basic test run
pytest tests/

# With Allure reporting
pytest tests/ --alluredir=results/allure-results

# Headless mode
pytest tests/ --headless

# Different browser
pytest tests/ --browser=firefox
```

### 4. View Reports
```bash
# Generate and serve Allure report
allure serve results/allure-results
```

---

## 📁 Project Structure

```
pytest-selenium/
├── config.py                 # 🔧 Simple configuration file
├── conftest.py               # 🔌 Pytest fixtures and setup
├── requirements.txt          # 📦 Python dependencies
├── pages/                    # 📄 Page Object Model classes
│   ├── base_page.py
│   ├── saucelab_login_page.py
│   └── saucelabs_home_page.py
├── tests/                    # 🧪 Test files
│   └── test_login.py
├── utils/                    # 🛠️ Utilities
│   └── whatsapp_notifier.py  # 📱 WhatsApp notifications
├── config/                   # ⚙️ Configuration
│   └── whatsapp_config.py    # 📱 WhatsApp settings
└── results/                  # 📊 Test results and reports
    ├── allure-results/       # Allure test results
    ├── allure-reports/       # Allure HTML reports
    └── screenshots/          # Test screenshots
```

---

## ⚙️ Configuration

### Basic Configuration
Edit `config.py` to customize your tests:

```python
class TestConfig:
    # Application Settings
    BASE_URL = "https://your-app.com/"
    USERNAME = "your_username"
    PASSWORD = "your_password"
    
    # Browser Settings
    BROWSER = "chrome"          # chrome, firefox, edge
    HEADLESS = False           # True for headless mode
    WINDOW_WIDTH = 1920
    WINDOW_HEIGHT = 1080
    
    # Timeout Settings (in seconds)
    IMPLICIT_WAIT = 10         # Element wait timeout
    PAGE_LOAD_TIMEOUT = 30     # Page load timeout
    ELEMENT_TIMEOUT = 15       # Specific element timeout
```

### Environment Variable Overrides
Override configuration with environment variables (useful for CI/CD):

```bash
export TEST_BASE_URL="https://staging.your-app.com/"
export TEST_USERNAME="staging_user"
export TEST_PASSWORD="staging_pass"
export TEST_BROWSER="firefox"
export TEST_HEADLESS="true"

pytest tests/
```

---

## 🧪 Writing Tests

### Simple Test Example
```python
import pytest
from pages.saucelab_login_page import SauceLabLoginPage
from pages.saucelabs_home_page import SauceLabHomePage

class TestLogin:
    def test_login_valid_user(self, driver, app_credentials):
        # Initialize page objects
        login_page = SauceLabLoginPage(driver)
        home_page = SauceLabHomePage(driver)
        
        # Perform login
        login_page.enter_username(app_credentials['username'])
        login_page.enter_password(app_credentials['password'])
        login_page.click_login()
        
        # Verify successful login
        assert home_page.is_home_page_displayed()
```

### Available Fixtures
- `driver` - WebDriver instance (automatically configured)
- `app_url` - Application base URL
- `app_credentials` - Username and password dictionary
- `take_screenshot(name)` - Screenshot capture function

---

## 📊 Allure Reporting

### Rich Test Reports
The framework automatically generates beautiful Allure reports with:

- ✅ **Test Results**: Pass/fail status with details
- 📸 **Screenshots**: Automatic capture on failures
- ⏱️ **Timeline**: Test execution timeline
- 📈 **Trends**: Historical test trends
- 🏷️ **Categories**: Organized test categories

### Allure Features
```python
import allure

@allure.feature("User Authentication")
@allure.story("Login Functionality")
@allure.title("Test successful login")
@allure.severity(allure.severity_level.CRITICAL)
def test_login(self, driver, app_credentials):
    with allure.step("Enter username"):
        # test step code
    
    with allure.step("Verify login"):
        # verification code
```

---

## 📱 WhatsApp Notifications

Get instant notifications when your tests complete!

### Setup WhatsApp Notifications
1. **Sign up for Twilio**: https://www.twilio.com/try-twilio
2. **Configure WhatsApp sandbox** in Twilio console
3. **Add GitHub Secrets**:
   ```
   TWILIO_ACCOUNT_SID: your_account_sid
   TWILIO_AUTH_TOKEN: your_auth_token
   TWILIO_WHATSAPP_TO: whatsapp:+your_phone_number
   ```

### What You'll Get
```
🎉 Selenium Tests Completed Successfully!

✅ Status: PASSED
📊 Live Dashboard: https://your-username.github.io/your-repo/
📅 Completed: 2024-01-15 14:30:25
🔗 Full Results: [GitHub Actions link]
```

---

## 🚀 CI/CD with GitHub Actions

### Automatic Testing
The framework includes GitHub Actions workflow that:

1. 🔄 **Triggers on code push**
2. 🐍 **Sets up Python environment**
3. 🌐 **Installs Chrome browser**
4. 📦 **Installs dependencies**
5. 🧪 **Runs tests with Chrome headless**
6. 📊 **Generates Allure reports**
7. 🌐 **Deploys live dashboard to GitHub Pages**
8. 📱 **Sends WhatsApp notification**

### Live Dashboard
Your test results are automatically published to:
```
https://your-username.github.io/your-repo/
```

---

## 🎮 Command Line Options

```bash
# Browser selection
pytest tests/ --browser=chrome
pytest tests/ --browser=firefox
pytest tests/ --browser=edge

# Headless mode
pytest tests/ --headless

# Custom URL
pytest tests/ --base-url=https://staging.example.com

# Allure reporting
pytest tests/ --alluredir=results/allure-results

# Verbose output
pytest tests/ -v

# Run specific test
pytest tests/test_login.py::TestLogin::test_login_valid_user
```

---

## 🛠️ Available Browsers

| Browser | Command | Notes |
|---------|---------|-------|
| **Chrome** | `--browser=chrome` | Default browser, best for CI/CD |
| **Firefox** | `--browser=firefox` | Good for cross-browser testing |
| **Edge** | `--browser=edge` | Windows and macOS support |

---

## 📸 Screenshots

### Automatic Screenshots
- ✅ **On test failure** - Automatically captured and attached to reports
- 📱 **Manual capture** - Use `take_screenshot("description")` fixture
- 🔗 **Allure integration** - Screenshots appear in Allure reports

### Screenshot Locations
- **File system**: `results/screenshots/`
- **Allure reports**: Embedded in HTML reports
- **CI/CD artifacts**: Available for download

---

## 🔍 Debugging

### View Configuration
```bash
python config.py
```

Output:
```
==================================================
🔧 Test Configuration
==================================================
📱 Base URL: https://www.saucedemo.com/
👤 Username: standard_user
🔐 Password: ************
🌐 Browser: chrome
👁️  Headless: False
📐 Window: 1920x1080
⏱️  Timeouts: 10s / 30s
==================================================
```

### Common Issues

**Browser not found:**
```bash
# Install WebDriver Manager dependencies
pip install webdriver-manager
```

**Tests fail in CI:**
```bash
# Ensure headless mode in CI
export TEST_HEADLESS=true
```

**Screenshots not captured:**
```bash
# Check results directory exists
mkdir -p results/screenshots
```

---

## 🎯 Features

### ✅ What's Included
- 🔧 **Simple Configuration** - Single config file
- 🌐 **Multi-Browser Support** - Chrome, Firefox, Edge
- 📊 **Allure Reporting** - Beautiful HTML reports
- 📱 **WhatsApp Notifications** - Real-time alerts
- 🚀 **CI/CD Ready** - GitHub Actions workflow
- 📸 **Screenshot Capture** - Automatic failure screenshots
- 🎮 **Command Line Options** - Flexible test execution
- 📖 **Page Object Model** - Maintainable test structure

### 🎉 Benefits
- **Easy Setup** - Get started in minutes
- **No Complex Configuration** - Just edit one file
- **Rich Reporting** - Professional test reports
- **Live Dashboard** - Results published automatically
- **Real-time Notifications** - Know immediately when tests complete
- **Cross-Platform** - Works on Windows, macOS, Linux

---

## 📋 Example Workflow

1. **Clone repository**
2. **Edit `config.py`** with your app details
3. **Write tests** in `tests/` directory
4. **Run locally**: `pytest tests/`
5. **Push to GitHub** - CI/CD runs automatically
6. **View live dashboard** at GitHub Pages
7. **Get WhatsApp notification** with results

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your improvements
4. Run tests: `pytest tests/`
5. Submit a pull request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 🆘 Support

- 📖 **Documentation**: Check this README
- 🐛 **Issues**: Create GitHub issue
- 💬 **Discussions**: Use GitHub Discussions
- 📧 **Contact**: Open an issue for support

---

**Happy Testing!** 🧪✨
