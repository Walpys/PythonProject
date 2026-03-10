def format_job_email(job_data):
    job_title = job_data.get('position', 'Unknown Position')
    company = job_data.get('company', 'Unknown Company')
    salary = job_data.get('salary', 'Not specified')
    job_url = job_data.get('url', 'No link available')

    subject = f"Interesting Job: {job_title} at {company}"
    
    body = (
        f"Hello,\n\n"
        f"Here is a job vacancy saved from Job Aggregator:\n\n"
        f"Position: {job_title}\n"
        f"Company: {company}\n"
        f"Salary: {salary}\n"
        f"Link: {job_url}\n\n"
        f"Good luck!"
    )
    
    return subject, body