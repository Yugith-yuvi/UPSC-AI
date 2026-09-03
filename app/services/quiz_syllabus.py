from app.llm import ask_upsc_ai

QUIZ_SYSTEM_PROMPT = """
You are a UPSC Prelims paper setter. 
Generate 1 high-quality Prelims MCQ based on the given topic.
Return output formatted as:
- Question
- Options (A, B, C, D)
- Correct Option
- Brief Analytical Explanation
"""

NOTES_SYSTEM_PROMPT = """
You are a UPSC subject-matter expert. 
Generate structured syllabus-wise notes for the given micro-topic.
Include: Core Concept, Important Constitutional/Legal Framework, Key Data/Reports, and Recent Context.
"""

def generate_prelims_quiz(topic: str) -> dict:
    prompt = f"Generate 1 UPSC Prelims MCQ for topic: {topic}"
    ai_response = ask_upsc_ai(prompt, system_prompt=QUIZ_SYSTEM_PROMPT)
    
    if ai_response["mode"] == "MOCK_ENGINE":
        ai_response["content"] = f"""
### Prelims Quiz: {topic}

**Q1. Consider the following statements regarding {topic}:**
1. It is a statutory body established under an Act of Parliament.
2. Its recommendations are legally binding on the Central Government.

**Which of the statements given above is/are correct?**
(a) 1 only
(b) 2 only
(c) Both 1 and 2
(d) Neither 1 nor 2

**Correct Answer:** (d) Neither 1 nor 2
**Explanation:** Executive bodies are formed by executive resolution, and recommendations are advisory in nature unless mandated by specific legislation.
        """.strip()
        
    return ai_response

def get_syllabus_notes(topic: str) -> dict:
    prompt = f"Provide comprehensive UPSC revision notes for: {topic}"
    ai_response = ask_upsc_ai(prompt, system_prompt=NOTES_SYSTEM_PROMPT)
    
    if ai_response["mode"] == "MOCK_ENGINE":
        ai_response["content"] = f"""
### Micro-Notes: {topic}

* **Core Overview:** Key governance framework covering rights, structural limits, and constitutional safeguards.
* **Constitutional Provision:** Relevant articles and executive mechanisms.
* **Landmark Judgements / Reports:** Refer to Supreme Court interpretations and Administrative Reforms Commission (ARC) suggestions.
* **Way Forward:** Balance between institutional autonomy and executive oversight.
        """.strip()
        
    return ai_response