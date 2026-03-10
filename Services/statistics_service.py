import re

def calculate_salary_statistics(jobs):
    salary_data = {}
    
    if not jobs:
        return salary_data

    for job in jobs:
        company = job.get('company', 'Unknown')
        position = job.get('position', 'Job')
        salary_raw = job.get('salary')

        if not salary_raw or str(salary_raw).strip().lower() in ['not specified', 'n/a', 'none', '']:
            continue

        clean_str = str(salary_raw).lower().replace(' ', '').replace(',', '')
        matches = re.findall(r'(\d+)(k?)', clean_str)

        if matches:
            parsed_numbers = []
            for num_str, k_suffix in matches:
                val = int(num_str)
                if k_suffix == 'k':
                    val *= 1000
                parsed_numbers.append(val)
            
            max_salary = max(parsed_numbers)
            
            if max_salary > 100: 
                short_pos = position[:15] + '...' if len(position) > 15 else position
                label = f"{company}\n({short_pos})"
                salary_data[label] = max_salary

    sorted_salaries = dict(sorted(salary_data.items(), key=lambda item: item[1], reverse=True)[:6])
    return sorted_salaries