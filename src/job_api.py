import os
from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()

def fetch_indeed_jobs(position, location):
    token = os.getenv("APIFY_API_TOKEN")
    client = ApifyClient(token)
    
    # LIMITING TO 10 JOBS FOR SPEED
    run_input = {
        "position": position,
        "country": "IN",
        "location": location,
        "maxItems": 10, # Changed from 30 to 10 for faster results
        "scrapeCompanyDetails": False, # Setting this to False makes it 3x faster
        "saveOnlyUniqueItems": True,
        "followRedirectsForApplyLink": False # Disabling redirects saves time
    }

    try:
        # Calls the actor found in your screenshot
        run = client.actor("misceres/indeed-scraper").call(run_input=run_input)
        
        jobs = []
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            jobs.append({
                "title": item.get("positionName") or item.get("jobTitle"),
                "company": item.get("company"),
                "salary": item.get("salaryText") or "Market Standard",
                "url": item.get("url")
            })
        return jobs
    except Exception as e:
        print(f"Scraper error: {e}")
        return []