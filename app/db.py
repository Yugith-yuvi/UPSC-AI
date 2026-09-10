from app.config import SUPABASE_URL, SUPABASE_KEY
from supabase import create_client

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def fetch_pyqs(subject: str = None, year_start: int = 2006, year_end: int = 2025, exam_type: str = "Prelims"):
    query = supabase.table("pyqs").select("*").eq("exam_type", exam_type)
    
    query = query.gte("year", year_start).lte("year", year_end)
    
    if subject and subject.lower() != "all":
        query = query.ilike("subject", f"%{subject}%")
        
    response = query.order("year", desc=True).execute()
    
    # Convert non-serializable fields (like UUIDs) to plain Python strings/dicts
    cleaned_data = []
    for item in response.data:
        item["id"] = str(item["id"])
        cleaned_data.append(item)
        
    return cleaned_data