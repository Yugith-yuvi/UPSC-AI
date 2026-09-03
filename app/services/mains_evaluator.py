from app.llm import ask_upsc_ai

EVALUATION_SYSTEM_PROMPT = """
You are a senior UPSC Mains Answer Evaluator. Analyze the provided answer text based on:
1. Directive Alignment (Critically Analyze / Elucidate / Discuss)
2. Structure (Intro, Body Paragraphs/Points, Conclusion)
3. Factual Accuracy (Constitutional Articles, Data, Case Laws)

Format your evaluation with clear scores and actionable recommendations.
"""

def evaluate_mains_submission(question: str, student_answer_text: str) -> dict:
    prompt = f"Question: {question}\n\nStudent Answer:\n{student_answer_text}"
    ai_response = ask_upsc_ai(prompt, system_prompt=EVALUATION_SYSTEM_PROMPT)
    
    # If using fallback mode, deliver a structured mock review
    if ai_response["mode"] == "MOCK_ENGINE":
        ai_response["content"] = f"""
### Mains Answer Evaluation Report
**Question:** {question[:60]}...

* **Score:** 5.5 / 10
* **Structure & Flow (2/3):** Introduction maps well to the topic, but body paragraphs need sub-headings.
* **Content & Facts (2.5/5):** Relevant arguments presented. Missing reference to landmark Supreme Court judgements or recent committee reports.
* **Conclusion (1/2):** Forward-looking conclusion present.

**Key Improvement Tip:** Integrate relevant constitutional articles and data points in bullet form to boost content density.
        """.strip()
        
    return ai_response