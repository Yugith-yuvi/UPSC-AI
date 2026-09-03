from supabase import create_client, Client
from app.config import SUPABASE_URL, SUPABASE_KEY

def get_db_client() -> Client | None:
    """Returns a Supabase client if configured, or None for offline mode."""
    if SUPABASE_URL and SUPABASE_KEY and SUPABASE_URL != "your_supabase_project_url_here":
        try:
            return create_client(SUPABASE_URL, SUPABASE_KEY)
        except Exception as e:
            print(f"⚠️ Supabase connection failed ({e}). Running in local mode.")
    return None

def log_api_activity(endpoint: str, prompt: str, mode: str):
    """Logs user request metadata asynchronously to Supabase."""
    supabase = get_db_client()
    if supabase:
        try:
            supabase.table("activity_logs").insert({
                "endpoint": endpoint,
                "prompt_summary": prompt[:100],
                "execution_mode": mode
            }).execute()
        except Exception as e:
            print(f"Failed to log activity: {e}")

def log_mains_score(question: str, score: float, feedback: str):
    """Logs Mains evaluation score to database."""
    supabase = get_db_client()
    if supabase:
        try:
            supabase.table("mains_scores").insert({
                "question": question[:150],
                "score": score,
                "feedback": feedback[:300]
            }).execute()
        except Exception as e:
            print(f"Failed to log mains score: {e}")

def get_score_history():
    """Fetches past scores for trend analysis."""
    supabase = get_db_client()
    if supabase:
        try:
            res = supabase.table("mains_scores").select("created_at, score").order("created_at", desc=False).execute()
            return res.data
        except Exception as e:
            print(f"Failed to fetch score history: {e}")
    # Local fallback sample data if Supabase isn't active
    return [
        {"created_at": "2026-08-28", "score": 4.5},
        {"created_at": "2026-08-29", "score": 5.0},
        {"created_at": "2026-08-30", "score": 5.5},
        {"created_at": "2026-08-31", "score": 6.0},
        {"created_at": "2026-09-01", "score": 6.5},
        {"created_at": "2026-09-02", "score": 7.0},
    ]