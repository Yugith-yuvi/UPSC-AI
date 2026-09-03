import socket
from google import genai
from google.genai import types
from app.config import GEMINI_API_KEY

def ask_upsc_ai(user_prompt: str, system_prompt: str = "You are an expert UPSC Civil Services mentor.") -> dict:
    """
    Returns a structured dictionary with execution mode metadata and generated text.
    """
    if GEMINI_API_KEY and GEMINI_API_KEY != "your_actual_gemini_api_key_here":
        try:
            socket.setdefaulttimeout(8.0)
            client = genai.Client(api_key=GEMINI_API_KEY)
            
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=user_prompt,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt,
                    temperature=0.2,
                ),
            )
            if response.text:
                return {"mode": "LIVE_AI", "status": "success", "content": response.text}
        except Exception as e:
            print(f"⚠️ Live API connection unavailable ({e}). Routing through Mock Engine...")
        finally:
            socket.setdefaulttimeout(None)

    # Deterministic Mock Response Fallback
    return {
        "mode": "MOCK_ENGINE",
        "status": "success",
        "content": (
            "Article 356 of the Indian Constitution empowers the President to impose President's Rule "
            "in a state if the state government cannot function in accordance with constitutional provisions."
        )
    }