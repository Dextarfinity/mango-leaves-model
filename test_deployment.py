#!/usr/bin/env python3
"""
Test script for the Mango Disease Detection API
Run this script to test your API locally before deploying to Railway
"""

import requests
import json
import os
import sys
from pathlib import Path

def test_health_endpoint(base_url):
    """Test the health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            data = response.json()
            print("✅ Health check passed")
            print(f"   Status: {data.get('status')}")
            print(f"   Model loaded: {data.get('model_loaded')}")
            print(f"   Classes: {data.get('classes')}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_api_docs(base_url):
    """Test API documentation endpoint"""
    print("🔍 Testing API documentation...")
    try:
        response = requests.get(f"{base_url}/docs")
        if response.status_code == 200:
            print("✅ API documentation accessible")
            return True
        else:
            print(f"❌ API docs failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ API docs error: {e}")
        return False

def test_web_interface(base_url):
    """Test web interface"""
    print("🔍 Testing web interface...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Web interface accessible")
            return True
        else:
            print(f"❌ Web interface failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Web interface error: {e}")
        return False

def check_model_file():
    """Check if model file exists"""
    print("🔍 Checking for model file...")
    model_files = ["best.pt", "yolo11n.pt", "yolov8s.pt"]
    
    for model_file in model_files:
        if os.path.exists(model_file):
            print(f"✅ Found model file: {model_file}")
            return True
    
    print("⚠️  No model file found!")
    print("   Please add your trained model file (best.pt) to this directory")
    print("   Or the app will download a default YOLO model")
    return False

def check_required_files():
    """Check if all required files exist"""
    print("🔍 Checking required files...")
    required_files = [
        "main.py",
        "requirements.txt", 
        "Dockerfile",
        "railway.toml",
        "static/index.html"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path}")
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    print("✅ All required files present")
    return True

def main():
    print("🥭 Mango Disease Detection API - Deployment Test")
    print("=" * 50)
    
    # Check files first
    files_ok = check_required_files()
    model_ok = check_model_file()
    
    if not files_ok:
        print("\n❌ Missing required files. Please check the file structure.")
        sys.exit(1)
    
    print("\n🔧 To test the API locally:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. Run the server: python main.py")
    print("3. Visit: http://localhost:8000")
    
    # Test if server is running
    BASE_URL = "http://localhost:8000"
    
    print(f"\n🔍 Testing if server is running at {BASE_URL}...")
    
    health_ok = test_health_endpoint(BASE_URL)
    
    if health_ok:
        docs_ok = test_api_docs(BASE_URL)
        web_ok = test_web_interface(BASE_URL)
        
        if health_ok and docs_ok and web_ok:
            print("\n🎉 All tests passed! Your API is ready for deployment.")
        else:
            print("\n⚠️  Some tests failed, but basic functionality works.")
    else:
        print(f"\n💡 Server not running. To start the server:")
        print("   python main.py")
        print("\nThen run this test script again.")
    
    print(f"\n📋 Deployment Checklist:")
    print("✅ Upload this folder to GitHub" if files_ok else "❌ Fix missing files first")
    print("✅ Include your model file (best.pt)" if model_ok else "⚠️  Add your trained model file")
    print("✅ Deploy to Railway")
    print("✅ Test the deployed URL")
    
    print(f"\n📄 Documentation:")
    print("   Local: http://localhost:8000/docs")
    print("   GitHub: README.md")
    print("   Deployment Guide: DEPLOYMENT.md")

if __name__ == "__main__":
    main()