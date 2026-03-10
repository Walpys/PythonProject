import httpx
import asyncio
from helpers.ai_match_rate import get_bulk_ai_rates as ai_match_rate
from helpers.clean_html import clean_html
from helpers.process_jobs import process_jobs


URL = "https://remotive.com/api/remote-jobs"


async def get_table_data(category, job_title, user_skills):
    params = {
        "category": category,
        "search": job_title,
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(URL, params=params, timeout=10.0)
            response.raise_for_status()
            raw_data = response.json()
            initial_jobs = process_jobs(raw_data) 
    
            if initial_jobs:
                rates = await ai_match_rate(initial_jobs, user_skills)
    
                for job, rate in zip(initial_jobs, rates):
                    job['match_rate'] = rate

            initial_jobs.sort(
                key=lambda x: int(x['match_rate'].replace('%', '')) if x['match_rate'] != 'N/A' else -1, 
                reverse=True
                )
            for job in initial_jobs:
                job.pop('description', None)

            return initial_jobs[:5]
                
        except Exception as e:
            print(f"Critical error: {e}")
            return []


