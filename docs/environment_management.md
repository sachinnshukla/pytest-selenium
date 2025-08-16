# Environment Management System

## 🎯 Overview

The environment management system allows you to run tests against different environments (dev, staging, prod) with different configurations, browsers, and settings.

## 📁 Structure

```
pytest-selenium/
├── environments/           # Environment configuration files
│   ├── dev.json           # Development environment settings
│   ├── staging.json       # Staging environment settings  
│   └── prod.json          # Production environment settings
├── config/
│   └── environment_manager.py  # Environment management logic
└── utils/
    └── env_info.py        # Environment information utility
```

## 🔧 Configuration Files

Each environment has its own JSON configuration file with settings:

### Example: `environments/prod.json`
```json
{
  "environment": "prod",
  "base_url": "https://www.saucedemo.com/",
  "username": "standard_user", 
  "password": "secret_sauce",
  "timeout": 10,
  "browser": "chrome",
  "headless": false,
  "window_size": {
    "width": 1920,
    "height": 1080
  },
  "implicit_wait": 3,
  "page_load_timeout": 20
}
```

## 🚀 Usage Examples

### 1. Basic Environment Selection
```bash
# Run with default environment (prod)
pytest tests/

# Run with specific environment
pytest tests/ --env=dev
pytest tests/ --env=staging
pytest tests/ --env=prod
```

### 2. Browser Override
```bash
# Use Firefox instead of environment default
pytest tests/ --env=dev --browser=firefox

# Use Edge browser
pytest tests/ --env=staging --browser=edge
```

### 3. Headless Mode
```bash
# Run in headless mode (no browser UI)
pytest tests/ --env=prod --headless

# Combine with other options
pytest tests/ --env=dev --browser=firefox --headless
```

### 4. With Allure Reporting
```bash
# Generate Allure reports with environment-specific tests
pytest tests/ --env=staging --alluredir=results/allure-results
```

### 5. Environment Variable
```bash
# Set environment via environment variable
export TEST_ENV=staging
pytest tests/
```

## 📊 Environment Configuration Details

| Environment | URL | Timeout | Browser | Use Case |
|------------|-----|---------|---------|----------|
| **dev** | dev.saucedemo.com | 15s | Chrome | Development testing |
| **staging** | staging.saucedemo.com | 20s | Chrome | Pre-production testing |
| **prod** | www.saucedemo.com | 10s | Chrome | Production testing |

## 🛠️ Available Command Line Options

| Option | Description | Default | Example |
|--------|-------------|---------|---------|
| `--env` | Environment to test against | prod | `--env=staging` |
| `--browser` | Browser to use (overrides env config) | (from env) | `--browser=firefox` |
| `--headless` | Run in headless mode | (from env) | `--headless` |

## 📝 Test Implementation

Tests now receive environment configuration via the `test_environment` fixture:

```python
class TestLogin:
    def test_login_valid_user(self, driver, test_environment):
        login_page = SauceLabLoginPage(driver)
        login_page.enter_username(test_environment.username)
        login_page.enter_password(test_environment.password)
        login_page.click_login()
        home_page = SauceLabHomePage(driver)
        assert home_page.is_home_page_displayed()
```

## 🔍 Debugging & Information

The system automatically displays configuration information when tests start:

```
=== Environment Configuration ===
Environment: staging
Base URL: https://staging.saucedemo.com/
Browser: firefox
Headless: False
Timeout: 20s
Window Size: 1920x1080
==================================
```

## ✅ Benefits

1. **Multi-Environment Support**: Test against dev, staging, prod with different URLs
2. **Browser Flexibility**: Override browser per test run
3. **Configuration Management**: Centralized settings per environment
4. **Override Capability**: Command line options override file settings
5. **Debugging Support**: Clear configuration display
6. **Maintainability**: Easy to add new environments

## 📋 Next Steps

1. Add more environments by creating new JSON files
2. Customize browser options per environment
3. Add environment-specific test data
4. Integrate with CI/CD pipelines using environment variables

## 🎉 Success!

Your framework now supports enterprise-level environment management! You can easily:
- Switch between environments with one command
- Override settings as needed
- Add new environments by creating JSON files
- Run tests consistently across different environments
