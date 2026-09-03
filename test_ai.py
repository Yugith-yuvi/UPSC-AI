from app.llm import ask_upsc_ai

print("🔍 Running UPSC Engine Execution Test...\n")

try:
    response = ask_upsc_ai("Give me a 1-line definition of Article 356 of the Indian Constitution.")
    print("--------------------------------------------------")
    print("🎉 SUCCESS! Output Generated:")
    print(response)
    print("--------------------------------------------------")
except Exception as e:
    print(f"❌ Execution error: {e}")