from sympy import sympify
from app.llm import ask_upsc_ai

CSAT_SYSTEM_PROMPT = """
You are a CSAT Quantitative Aptitude & Reasoning Expert. 
Solve the question using shortcut methods (e.g., Unit Digit, Alligation, Work-Time ratios).
Always display:
1. Core Formula / Trick
2. 2-Step Execution
3. Final Answer
"""

def solve_csat_question(question_text: str) -> dict:
    ai_response = ask_upsc_ai(question_text, system_prompt=CSAT_SYSTEM_PROMPT)
    
    if ai_response["mode"] == "MOCK_ENGINE":
        ai_response["content"] = f"""
### CSAT Shortcut Solution
**Problem:** {question_text}

* **Core Formula:** Work = Rate × Time (LCM Method)
* **Shortcut Execution:**
  1. Let Total Work = LCM of given time parameters = 60 units.
  2. Compute combined efficiency rate = (5 + 4) = 9 units/day.
  3. Total Time = 60 / 9 = 6.67 days.

**Final Answer:** 6 2/3 Days
        """.strip()
        
    return ai_response