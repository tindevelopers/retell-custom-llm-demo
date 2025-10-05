#!/usr/bin/env python3
"""
Simple test script to verify WebSocket connection and OpenAI API
"""
import asyncio
import json
import os
from dotenv import load_dotenv
from openai import AsyncOpenAI

load_dotenv()

async def test_openai_connection():
    """Test OpenAI API connection"""
    print("Testing OpenAI API connection...")
    
    client = AsyncOpenAI(
        organization=os.environ.get("OPENAI_ORGANIZATION_ID"),
        api_key=os.environ["OPENAI_API_KEY"],
    )
    
    try:
        response = await client.chat.completions.create(
            model="gpt-4-turbo-preview",
            messages=[{"role": "user", "content": "Hello, are you working?"}],
            max_tokens=50
        )
        print(f"✅ OpenAI API working: {response.choices[0].message.content}")
        return True
    except Exception as e:
        print(f"❌ OpenAI API error: {e}")
        return False

async def test_environment_variables():
    """Test environment variables"""
    print("Testing environment variables...")
    
    required_vars = ["RETELL_API_KEY", "OPENAI_API_KEY"]
    missing_vars = []
    
    for var in required_vars:
        if not os.environ.get(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing environment variables: {missing_vars}")
        return False
    else:
        print("✅ All required environment variables present")
        return True

async def main():
    print("🔍 Testing Retell Custom LLM Setup...")
    print("=" * 50)
    
    # Test environment variables
    env_ok = await test_environment_variables()
    print()
    
    # Test OpenAI API
    if env_ok:
        openai_ok = await test_openai_connection()
        print()
        
        if openai_ok:
            print("🎉 All tests passed! Your setup should be working.")
            print("\nIf Retell is still not responding, check:")
            print("1. Railway deployment logs")
            print("2. Browser console for WebSocket errors")
            print("3. Retell dashboard for any error messages")
        else:
            print("❌ OpenAI API test failed. Check your API key and organization ID.")
    else:
        print("❌ Environment variables test failed.")

if __name__ == "__main__":
    asyncio.run(main())
