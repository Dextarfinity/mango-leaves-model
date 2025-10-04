#!/usr/bin/env python3
"""
Simple debug script to test Railway deployment issues
"""
import os
import asyncio
import uvicorn
from fastapi import FastAPI

# Simple test app
debug_app = FastAPI(title="Railway Debug API")

@debug_app.get("/")
async def root():
    return {"message": "Debug API is working", "port": os.environ.get("PORT", "8000")}

@debug_app.get("/health")
async def health():
    return {"status": "ok", "port": os.environ.get("PORT", "8000")}

@debug_app.get("/env")
async def env_vars():
    return {
        "PORT": os.environ.get("PORT"),
        "RAILWAY_ENVIRONMENT": os.environ.get("RAILWAY_ENVIRONMENT"),
        "RAILWAY_PROJECT_NAME": os.environ.get("RAILWAY_PROJECT_NAME"),
        "PYTHONPATH": os.environ.get("PYTHONPATH"),
        "PWD": os.environ.get("PWD")
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"🚀 Starting debug server on port {port}")
    print(f"🌍 Environment PORT: {os.environ.get('PORT', 'Not Set')}")
    print(f"📁 Working Directory: {os.getcwd()}")
    print(f"🐍 Python Path: {os.environ.get('PYTHONPATH', 'Not Set')}")
    
    uvicorn.run(debug_app, host="0.0.0.0", port=port, log_level="debug")