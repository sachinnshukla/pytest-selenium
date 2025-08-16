#!/usr/bin/env python3
"""
Environment Information Utility
Shows available environments and their configurations
"""

import sys
import json
from pathlib import Path
from config.environment_manager import environment_manager


def show_available_environments():
    """Display all available environments"""
    environments = environment_manager.get_available_environments()
    
    if not environments:
        print("❌ No environment configurations found!")
        print("   Create JSON files in the 'environments/' directory")
        return
    
    print("🌍 Available Environments:")
    print("=" * 50)
    
    for env_name in sorted(environments):
        try:
            config = environment_manager.load_environment(env_name)
            print(f"\n📋 Environment: {env_name.upper()}")
            print(f"   URL: {config.base_url}")
            print(f"   Browser: {config.browser}")
            print(f"   Headless: {config.headless}")
            print(f"   Timeout: {config.timeout}s")
            print(f"   Window: {config.window_size.width}x{config.window_size.height}")
        except Exception as e:
            print(f"\n❌ Environment: {env_name.upper()} - Error: {e}")


def show_current_environment(env_name: str = None):
    """Display current environment configuration"""
    try:
        if env_name:
            config = environment_manager.load_environment(env_name)
        else:
            config = environment_manager.config
        
        environment_manager.print_config()
        
    except Exception as e:
        print(f"❌ Error loading environment '{env_name}': {e}")


def show_usage_examples():
    """Show usage examples"""
    print("\n🚀 Usage Examples:")
    print("=" * 50)
    print("\n1. Run tests with default environment (prod):")
    print("   pytest tests/")
    
    print("\n2. Run tests with specific environment:")
    print("   pytest tests/ --env=dev")
    print("   pytest tests/ --env=staging")
    
    print("\n3. Override browser:")
    print("   pytest tests/ --env=dev --browser=firefox")
    print("   pytest tests/ --env=staging --browser=edge")
    
    print("\n4. Run in headless mode:")
    print("   pytest tests/ --env=prod --headless")
    
    print("\n5. Combine with Allure reporting:")
    print("   pytest tests/ --env=dev --alluredir=results/allure-results")
    
    print("\n6. Set environment via environment variable:")
    print("   export TEST_ENV=staging")
    print("   pytest tests/")


def main():
    """Main function"""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "list":
            show_available_environments()
        elif command == "current":
            env_name = sys.argv[2] if len(sys.argv) > 2 else None
            show_current_environment(env_name)
        elif command == "examples":
            show_usage_examples()
        else:
            print(f"Unknown command: {command}")
            print("Available commands: list, current, examples")
    else:
        print("🔧 Environment Manager")
        print("=" * 30)
        show_available_environments()
        show_usage_examples()


if __name__ == "__main__":
    main()
