from google import genai
import re
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("API_KEY"))

async def get_bulk_ai_rates(jobs_list, user_skills):
    if not jobs_list or not user_skills:
        return ["0%"] * len(jobs_list)

    jobs_formatted = ""
    for i, job in enumerate(jobs_list):
        jobs_formatted += f"\nID {i}: {job['position']} at {job['company']}. Description: {job['description'][:1000]}\n"

    prompt = f"""
    You are a recruiter. Rate the match (0-100) between candidate skills: {", ".join(user_skills)} 
    and the following list of jobs.
    
    Jobs list:
    {jobs_formatted}
    
    Return the result as a simple list of numbers corresponding to IDs, separated by commas. 
    Example: 85, 40, 0, 95
    Return ONLY the numbers.
    """
    
    try:

        response = await asyncio.to_thread(
            client.models.generate_content, 
            model='gemini-3.1-flash-lite-preview', 
            contents=prompt
        )
        
        raw_text = response.text.strip()
        
        rates = re.findall(r'\d+', raw_text)
        
        result = [f"{rates[i]}%" if i < len(rates) else "0%" for i in range(len(jobs_list))]
        return result
        
    except Exception as e:
        print(f"AI Bulk Error: {e}")
        return ["N/A"] * len(jobs_list)