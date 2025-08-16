# 🚀 Complete Guide: How to Test Your CI/CD Pipeline

## 📋 **What We're Going to Do:**
1. Check if you have Git setup
2. Create a GitHub repository (if needed)
3. Push your code to GitHub
4. Watch CI/CD run automatically
5. See the results
6. Test failure scenarios

---

## **STEP 1: Check Git Setup** ⚙️

First, let's make sure Git is ready:

```bash
# Check if git is installed
git --version

# Check if you're in a git repository
git status
```

**If you see "not a git repository":**
```bash
# Initialize git in your project
cd /Users/sachinshukla/Documents/pytest-selenium
git init
git add .
git commit -m "Initial selenium framework setup"
```

---

## **STEP 2: Create GitHub Repository** 🌐

### Option A: If you DON'T have a GitHub repo yet

1. **Go to GitHub.com**
2. **Click "New" button** (green button)
3. **Repository name:** `pytest-selenium-framework`
4. **Make it Public** (so GitHub Actions work for free)
5. **DON'T check** "Add README" (you already have files)
6. **Click "Create repository"**

### Option B: If you ALREADY have a GitHub repo
- Just use your existing repository
- Make sure it's public for free GitHub Actions

---

## **STEP 3: Connect Your Local Code to GitHub** 🔗

Copy these commands from your new GitHub repository page:

```bash
# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/pytest-selenium-framework.git

# Check if it worked
git remote -v

# Push your code to GitHub
git branch -M main
git push -u origin main
```

**Replace `YOUR_USERNAME` with your actual GitHub username!**

---

## **STEP 4: Watch CI/CD Magic Happen** ✨

### 4.1 Go to Your Repository on GitHub
- Open your browser
- Go to: `https://github.com/YOUR_USERNAME/pytest-selenium-framework`

### 4.2 Click the "Actions" Tab
- You should see a tab called "Actions" 
- Click it!

### 4.3 Watch Your Pipeline Run
You should see something like:
```
🧪 Automated Selenium Tests
⚪ In Progress... (yellow circle)
```

### 4.4 Click on the Running Job
- Click on the job name
- You'll see live logs of your tests running!

---

## **STEP 5: What You Should See** 👀

### If Everything Works (Success ✅):
```
✅ Automated Selenium Tests
   All checks passed
   
Jobs:
✅ test (ubuntu-latest)
   - 📥 Get Code from GitHub
   - 🐍 Setup Python 3.12  
   - 🌐 Install Chrome Browser
   - 📦 Install Python Packages
   - 🧪 Run Selenium Tests
   - 📊 Install Allure
   - 📈 Generate Allure Report
   - 💾 Upload Test Results
   - 📸 Upload Screenshots
```

### If Something Fails (Failure ❌):
```
❌ Automated Selenium Tests
   Some checks failed
   
Jobs:
❌ test (ubuntu-latest)
   - ✅ Setup steps...
   - ❌ Run Selenium Tests (FAILED)
```

---

## **STEP 6: Download Your Reports** 📥

### 6.1 Go to the Completed Job
- Click on your completed CI/CD run
- Scroll to the bottom

### 6.2 Download Artifacts
You should see:
- 📊 **allure-report-123** (download this for HTML reports)
- 📸 **screenshots-123** (download this for screenshots)

### 6.3 View Reports Locally
```bash
# After downloading, unzip and open
cd ~/Downloads
unzip allure-report-123.zip
open allure-report-123/index.html
```

---

## **STEP 7: Test Failure Scenario** 🧪

Let's intentionally break a test to see CI/CD catch it:

### 7.1 Create a Failing Test
```bash
# Create a new test file that will fail
cd /Users/sachinshukla/Documents/pytest-selenium
```

Create `tests/test_failure_demo.py`:
```python
import pytest
from pages.saucelab_login_page import SauceLabLoginPage

class TestFailureDemo:
    def test_intentional_failure(self, driver, test_environment):
        """This test will fail on purpose to test CI/CD"""
        login_page = SauceLabLoginPage(driver)
        
        # This will fail because we're using wrong credentials
        login_page.enter_username("wrong_user")
        login_page.enter_password("wrong_password")
        login_page.click_login()
        
        # This assertion will fail
        assert False, "This test is supposed to fail!"
```

### 7.2 Push the Failing Test
```bash
git add .
git commit -m "Add failing test to test CI/CD"
git push origin main
```

### 7.3 Watch CI/CD Catch the Failure
- Go back to GitHub Actions
- Watch your new run fail
- See the failure screenshot automatically captured!

---

## **STEP 8: Fix and Test Again** 🔧

### 8.1 Delete the Failing Test
```bash
rm tests/test_failure_demo.py
git add .
git commit -m "Remove failing test"
git push origin main
```

### 8.2 Watch CI/CD Pass Again
- CI/CD should run and pass
- All green checkmarks!

---

## **TROUBLESHOOTING** 🔧

### Problem: "GitHub Actions not running"
**Solution:** 
- Make sure repository is public
- Check if `.github/workflows/selenium-tests.yml` exists
- Try pushing a new commit

### Problem: "Tests failing in CI but work locally"
**Solution:**
- CI runs in headless mode
- Check the logs in GitHub Actions
- Download screenshots to see what went wrong

### Problem: "Can't find requirements.txt"
**Solution:**
```bash
# Make sure requirements.txt exists
ls requirements.txt

# If missing, create it:
echo "selenium>=4.15.0
pytest>=7.4.0  
allure-pytest>=2.13.2" > requirements.txt

git add requirements.txt
git commit -m "Add requirements.txt"
git push origin main
```

---

## **SUCCESS CHECKLIST** ✅

After following this guide, you should have:

- [ ] Code pushed to GitHub repository
- [ ] CI/CD pipeline running automatically
- [ ] Green checkmarks for passing tests
- [ ] Downloaded Allure reports
- [ ] Downloaded failure screenshots
- [ ] Tested both pass and fail scenarios

---

## **Next Steps** 🎯

Once this works:
1. **Add more tests** → CI/CD runs them automatically
2. **Work in branches** → CI/CD tests before merging
3. **Team collaboration** → Everyone's code gets tested
4. **Deploy automatically** → After tests pass

**You now have professional-grade automated testing!** 🚀

