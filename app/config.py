import os

# ✅ SAFE: Reads purely from environment variables with no hardcoded fallback
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
