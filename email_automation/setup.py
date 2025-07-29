#!/usr/bin/env python3
"""
Setup script for Email Automation System
"""

import os
import shutil
from pathlib import Path

def setup_automation():
    """
    Set up the email automation system with proper directory structure
    and file permissions.
    """
    print("Setting up Email Automation System...")
    
    # Create necessary directories
    directories = ['logs', 'config']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")
        else:
            print(f"Directory already exists: {directory}")
    
    # Create .env file if it doesn't exist
    env_file = '.env'
    env_example = '.env.example'
    
    if not os.path.exists(env_file) and os.path.exists(env_example):
        shutil.copy(env_example, env_file)
        print(f"Created {env_file} from {env_example}")
        print("Please edit .env with your configuration!")
    elif os.path.exists(env_file):
        print(f"{env_file} already exists")
    else:
        print(f"Warning: {env_example} not found")
    
    # Make the main script executable
    main_script = 'email_automation.py'
    if os.path.exists(main_script):
        current_permissions = os.stat(main_script).st_mode
        os.chmod(main_script, current_permissions | 0o755)
        print(f"Made {main_script} executable")
    
    # Check for required files
    required_files = [
        'requirements.txt',
        'config/email_patterns.yaml',
        'gmail_client.py',
        'response_matcher.py',
        'email_automation.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
        else:
            print(f"✓ Found {file}")
    
    if missing_files:
        print("\nMissing required files:")
        for file in missing_files:
            print(f"✗ {file}")
        print("\nPlease ensure all files are present before running the automation.")
        return False
    
    print("\n" + "="*50)
    print("Setup completed successfully!")
    print("="*50)
    
    print("\nNext steps:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Set up Gmail API credentials (see README.md)")
    print("3. Edit .env with your configuration")
    print("4. Test the setup: python email_automation.py --test")
    print("5. Run the automation: python email_automation.py --run-once")
    
    print("\nFor detailed instructions, see README.md")
    
    return True

if __name__ == '__main__':
    setup_automation()