from mcp.server.fastmcp import FastMCP
from src.job_api import fetch_linkedin_jobs, fetch_naukri_jobs
import os

mcp = FastMCP("JobSearchServer")

@mcp.tool()
async def search_linkedin(role: str, location: str = "India"):
    """Search for jobs on LinkedIn based on role and location."""
    return fetch_linkedin_jobs(role, location)

@mcp.tool()
async def search_naukri(role: str, location: str = "India"):
    """Search for jobs on Naukri based on role and location."""
    return fetch_naukri_jobs(role, location)

if __name__ == "__main__":
    mcp.run()