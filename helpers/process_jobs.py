from .clean_html import clean_html

def process_jobs(json_data):
    if not isinstance(json_data, dict):
        return []

    jobs = json_data.get('jobs', [])
    processed_results = []

    for job in jobs:
        raw_description = job.get('description', '')
        cleaned_description = clean_html(raw_description)
        item = {
            "position": job.get('title', 'N/A'),
            "company": job.get('company_name', 'N/A'),
            "salary": job.get('salary') if job.get('salary') else "Not specified",
            "match_rate": "Waiting for AI...",  
            "email": "Click to prepare",        
            "url": job.get('url', ''),
            "description": cleaned_description    
        }
        processed_results.append(item)
    
    return processed_results
