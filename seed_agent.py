import os
import json
import google.generativeai as genai
from supabase import create_client

# Initialize Credentials
SUPABASE_URL = os.getenv("SUPABASE_URL", "YOUR_SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "YOUR_SUPABASE_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

SUBJECTS = [
    "Polity & Governance", "Economy", "Modern History", 
    "Ancient & Medieval History", "Art & Culture", 
    "Geography", "Environment & Ecology", "Science & Technology"
]

model = genai.GenerativeModel("gemini-2.5-flash")

def generate_and_seed_pyqs(subject, year_start=2006, year_end=2025):
    prompt = f"""
    Generate 5 authentic, highly accurate UPSC Civil Services Prelims questions for the subject: '{subject}' between years {year_start} and {year_end}.
    Return strictly a JSON array of objects with no markdown formatting around it:
    [
      {{
        "year": 2022,
        "exam_type": "Prelims",
        "subject": "{subject}",
        "topic": "Topic Name",
        "question": "Full Question Text",
        "options": {{"A": "Option 1", "B": "Option 2", "C": "Option 3", "D": "Option 4"}},
        "correct_option": "A",
        "explanation": "Detailed step-by-step UPSC model answer explanation."
      }}
    ]
    """
    response = model.generate_content(prompt)
    clean_json = response.text.replace("```json", "").replace("```", "").strip()
    data = json.loads(clean_json)
    
    # Upload directly to Supabase
    supabase.table("pyqs").insert(data).execute()
    print(f"✅ Successfully seeded {len(data)} questions for {subject}")

if __name__ == "__main__":
    for sub in SUBJECTS:
        generate_and_seed_pyqs(sub)