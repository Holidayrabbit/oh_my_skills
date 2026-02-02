#!/usr/bin/env python3
"""
Setup Twitter credentials
Helps configure Twitter API credentials
"""

import os
import json
import sys


def setup_credentials():
    """Interactive setup for Twitter credentials"""
    
    print("=" * 60)
    print("Twitter API Credentials Setup")
    print("=" * 60)
    print()
    print("You'll need to obtain these from the Twitter Developer Portal:")
    print("https://developer.twitter.com/en/portal/dashboard")
    print()
    
    credentials = {}
    
    # Get credentials
    credentials['TWITTER_API_KEY'] = input("Enter API Key: ").strip()
    credentials['TWITTER_API_SECRET'] = input("Enter API Secret: ").strip()
    credentials['TWITTER_ACCESS_TOKEN'] = input("Enter Access Token: ").strip()
    credentials['TWITTER_ACCESS_TOKEN_SECRET'] = input("Enter Access Token Secret: ").strip()
    
    # Validate
    if not all(credentials.values()):
        print("\nError: All fields are required", file=sys.stderr)
        sys.exit(1)
    
    # Save options
    print("\n" + "=" * 60)
    print("How would you like to store these credentials?")
    print("=" * 60)
    print("1. Export as environment variables (temporary, for current session)")
    print("2. Save to .env file (recommended)")
    print("3. Display only (you'll copy and save manually)")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == '1':
        # Export environment variables
        print("\n# Add these to your shell session:")
        for key, value in credentials.items():
            print(f'export {key}="{value}"')
        print("\nOr run: source <(cat above_output)")
        
    elif choice == '2':
        # Save to .env file
        env_file = '.env'
        with open(env_file, 'w') as f:
            for key, value in credentials.items():
                f.write(f'{key}="{value}"\n')
        print(f"\n✅ Credentials saved to {env_file}")
        print("\nTo use: source .env or load with python-dotenv")
        
    else:
        # Display
        print("\n# Copy these credentials:")
        print(json.dumps(credentials, indent=2))
    
    print("\n" + "=" * 60)
    print("Setup complete!")
    print("=" * 60)


if __name__ == '__main__':
    setup_credentials()