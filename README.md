# Pytest-Selenium with Allure Reporting

This project is a Selenium test automation framework using pytest with integrated Allure reporting capabilities.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install Allure command-line tool (optional, for generating HTML reports):
```bash
# macOS
brew install allure

# Or download from: https://docs.qameta.io/allure/#_installing_a_commandline
```

## Running Tests

### Basic test execution:
```bash
pytest tests/
```

### Running tests with Allure reporting:
```bash
# Run tests and generate Allure results
pytest tests/ --allure

# Run tests with custom Allure results directory
pytest tests/ --allure --allure-dir=./custom/allure-results
```

### Generate Allure HTML report:
```bash
# After running tests with --allure flag
allure generate ./results/allure-results -o ./results/allure-reports --clean

# Serve the report in browser
allure serve ./results/allure-results
```

### Complete workflow example:
```bash
# Run tests with Allure
pytest tests/ --allure

# Generate and serve HTML report
allure serve ./results/allure-results
```

## Command Line Arguments

- `--allure`: Enable Allure reporting (default: False)
- `--allure-dir`: Specify Allure results directory (default: ./results/allure-results)

## Allure Features Included

- **Test Steps**: Detailed step-by-step execution
- **Screenshots**: Automatic screenshot capture on test failures
- **Test Metadata**: Feature, story, severity, and test case information
- **Rich Descriptions**: Detailed test descriptions and titles
- **Test Categories**: Organized by features and stories

## Project Structure

```
pytest-selenium/
├── config.py              # Test configuration
├── conftest.py            # Pytest fixtures and Allure configuration
├── pytest.ini            # Pytest configuration
├── requirements.txt       # Python dependencies
├── pages/                 # Page Object Model classes
│   ├── base_page.py
│   ├── saucelab_login_page.py
│   └── saucelabs_home_page.py
├── tests/                 # Test files
│   └── test_login.py
└── results/               # Test results and reports
    ├── allure-results/    # Allure test results (generated)
    └── allure-reports/    # Allure HTML reports (generated)
```

## Example Test Execution Output

When running with Allure enabled, you'll see:
- Detailed test steps in the console
- Screenshots automatically attached to failed tests
- Rich HTML reports with timeline, graphs, and detailed test information
