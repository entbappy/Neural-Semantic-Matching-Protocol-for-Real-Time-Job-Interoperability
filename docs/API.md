# API Documentation

## Overview

This document describes the API functions and modules available in the Real-Time Job Interoperability System.

---

## Core Modules

### 1. Helper Module (`src/helper.py`)

#### `extract_text_from_pdf(uploaded_file)`

Extracts text content from a PDF file.

**Parameters**:
- `uploaded_file` (file-like object): Uploaded PDF file from Streamlit

**Returns**:
- `str`: Extracted text from all PDF pages

**Example**:
```python
from src.helper import extract_text_from_pdf
import streamlit as st

uploaded_file = st.file_uploader("Upload PDF")
if uploaded_file:
    text = extract_text_from_pdf(uploaded_file)
    print(text)
```

**Error Handling**:
```python
try:
    text = extract_text_from_pdf(uploaded_file)
except Exception as e:
    print(f"Error extracting PDF: {e}")
```

---

#### `ask_openai(prompt, max_tokens=500)`

Sends a prompt to OpenAI GPT-4o and returns the response.

**Parameters**:
- `prompt` (str): The prompt to send to OpenAI
- `max_tokens` (int, optional): Maximum tokens in response (default: 500)

**Returns**:
- `str`: Response from GPT-4o

**Example**:
```python
from src.helper import ask_openai

# Summarize resume
prompt = f"Summarize this resume in 100 words:\n{resume_text}"
summary = ask_openai(prompt, max_tokens=200)
print(summary)
```

**Available Models**:
- `gpt-4o`: Latest GPT-4 Omni model (recommended)

**Rate Limiting**:
- Subject to OpenAI API plan
- Implement backoff strategy for rate limits

**Cost Estimation**:
- Input: ~$0.003/1K tokens
- Output: ~$0.006/1K tokens
- Track usage in OpenAI dashboard

---

### 2. Job API Module (`src/job_api.py`)

#### `fetch_linkedin_jobs(search_query, location="india", rows=60)`

Fetches job listings from LinkedIn via Apify.

**Parameters**:
- `search_query` (str): Job title or keywords to search
- `location` (str, optional): Job location (default: "india")
- `rows` (int, optional): Number of jobs to fetch (default: 60, max: 300)

**Returns**:
- `List[Dict]`: List of job dictionaries with keys:
  - `title`: Job title
  - `company`: Company name
  - `location`: Job location
  - `link`: Job posting URL
  - `description`: Job description
  - `salary`: Salary information (if available)

**Example**:
```python
from src.job_api import fetch_linkedin_jobs

jobs = fetch_linkedin_jobs("Python Developer", location="India", rows=30)
for job in jobs:
    print(f"{job['title']} at {job['company']}")
```

**Error Handling**:
```python
try:
    jobs = fetch_linkedin_jobs("Python Developer")
except Exception as e:
    print(f"Error fetching LinkedIn jobs: {e}")
    # Fallback or retry logic
```

**Response Example**:
```json
{
  "title": "Senior Python Developer",
  "company": "Tech Corp",
  "location": "Bangalore",
  "link": "https://linkedin.com/jobs/...",
  "description": "We are looking for...",
  "salary": "₹15,00,000 - ₹25,00,000"
}
```

---

#### `fetch_naukri_jobs(search_query, location="india", rows=60)`

Fetches job listings from Naukri.com via Apify.

**Parameters**:
- `search_query` (str): Job keywords to search
- `location` (str, optional): Job location (default: "india")
- `rows` (int, optional): Number of jobs to fetch (default: 60, max: 300)

**Additional Parameters**:
- `freshness`: "all" (all jobs) or recent
- `sortBy`: "relevance" (default) or "recency"
- `experience`: "all" (all levels) or specific range

**Returns**:
- `List[Dict]`: List of job dictionaries

**Example**:
```python
from src.job_api import fetch_naukri_jobs

jobs = fetch_naukri_jobs(
    search_query="Machine Learning Engineer",
    location="India",
    rows=50
)
for job in jobs:
    print(f"{job.get('title')} - {job.get('company')}")
```

**Response Example**:
```json
{
  "title": "ML Engineer - Python",
  "company": "AI Startup",
  "location": "Remote",
  "link": "https://naukri.com/job/...",
  "description": "Looking for ML Engineer...",
  "experience_range": "2-5 years"
}
```

---

## Advanced Usage

### Combining Multiple Job Sources

```python
from src.job_api import fetch_linkedin_jobs, fetch_naukri_jobs

def get_all_jobs(query, location="India", limit=50):
    """Fetch jobs from both platforms"""
    linkedin_jobs = fetch_linkedin_jobs(query, location, limit)
    naukri_jobs = fetch_naukri_jobs(query, location, limit)
    
    all_jobs = linkedin_jobs + naukri_jobs
    return sorted(
        all_jobs, 
        key=lambda x: x.get('relevance_score', 0),
        reverse=True
    )

jobs = get_all_jobs("Python Developer")
```

---

### Resume Analysis Pipeline

```python
from src.helper import extract_text_from_pdf, ask_openai
from src.job_api import fetch_linkedin_jobs

def analyze_and_recommend(pdf_file):
    """Complete analysis pipeline"""
    
    # Step 1: Extract resume
    resume_text = extract_text_from_pdf(pdf_file)
    
    # Step 2: Summarize
    summary_prompt = f"Summarize this resume:\n{resume_text}"
    summary = ask_openai(summary_prompt)
    
    # Step 3: Extract skills
    skills_prompt = f"List the top 5 technical skills:\n{resume_text}"
    skills = ask_openai(skills_prompt)
    
    # Step 4: Get job recommendations
    jobs = fetch_linkedin_jobs(skills.split('\n')[0])
    
    return {
        'summary': summary,
        'skills': skills,
        'jobs': jobs
    }
```

---

### Skill Gap Analysis

```python
from src.helper import ask_openai

def analyze_skill_gap(resume_text, job_description):
    """Analyze missing skills"""
    prompt = f"""
    Resume: {resume_text}
    
    Job Description: {job_description}
    
    Identify:
    1. Skills from job that candidate has
    2. Missing skills
    3. Learning recommendations
    """
    return ask_openai(prompt, max_tokens=500)
```

---

### Career Roadmap Generation

```python
from src.helper import ask_openai

def generate_career_roadmap(current_profile, target_role):
    """Generate career development path"""
    prompt = f"""
    Current Profile: {current_profile}
    Target Role: {target_role}
    
    Create a 2-year career roadmap including:
    1. Skills to develop
    2. Projects to build
    3. Timeline and milestones
    4. Resources to learn from
    """
    return ask_openai(prompt, max_tokens=1000)
```

---

## Utility Modules

### Pydantic Models (`all-utils/utilities/pydantic_models.py`)

Data validation models for request/response handling.

**Usage**:
```python
from pydantic import BaseModel

class JobPosting(BaseModel):
    title: str
    company: str
    location: str
    salary: Optional[str] = None
    description: str

# Validate job data
job = JobPosting(
    title="Software Engineer",
    company="Tech Corp",
    location="Bangalore",
    description="Great job opportunity"
)
```

---

### Query Validation (`all-utils/utilities/query_validation_transformation.py`)

Validates and transforms user queries.

**Functions**:
- `validate_query(query: str) -> bool`: Check if query is valid
- `transform_query(query: str) -> str`: Optimize query for search

**Example**:
```python
from all_utils.utilities.query_validation_transformation import validate_query, transform_query

user_input = "python developer jobs"
if validate_query(user_input):
    optimized = transform_query(user_input)
    print(optimized)
```

---

### Logging (`all-utils/utilities/logging_example.py`)

Structured logging for debugging and monitoring.

**Configuration**:
```python
import logging
from all_utils.utilities.logging_example import setup_logging

# Setup logging
logger = setup_logging("app", level="INFO")

# Log events
logger.info("Application started")
logger.error("Error occurred", exc_info=True)
```

---

## MCP Server (`mcp_server.py`)

The Model Context Protocol server exposes job fetching as tools.

**Available Tools**:
- `fetch_linkedin_jobs`: Get LinkedIn job listings
- `fetch_naukri_jobs`: Get Naukri job listings

**Starting the Server**:
```bash
python mcp_server.py
```

**Tool Invocation Example**:
```python
# Tools can be called via MCP protocol
# See mcp_server.py for implementation details
```

---

## Environment Configuration

### Required Environment Variables

```env
# OpenAI API
OPENAI_API_KEY=sk-...

# Apify API
APIFY_API_TOKEN=apify_api_...

# Optional
LOG_LEVEL=INFO
```

### Loading Configuration

```python
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
```

---

## Error Codes & Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `InvalidAPIKey` | Wrong API key | Check `.env` file |
| `RateLimitError` | Too many requests | Implement exponential backoff |
| `PDFParseError` | Corrupted PDF | Verify file format |
| `NetworkError` | Connection issue | Check internet connection |

### Retry Logic

```python
import time
from functools import wraps

def retry_with_backoff(max_retries=3, backoff_factor=2):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    wait_time = backoff_factor ** attempt
                    print(f"Retry attempt {attempt + 1}, waiting {wait_time}s")
                    time.sleep(wait_time)
        return wrapper
    return decorator

@retry_with_backoff()
def fetch_jobs(query):
    # Your API call here
    pass
```

---

## Rate Limiting & Throttling

### OpenAI Limits

- Token limit per minute: Depends on plan
- Requests per minute: 3,500 (free tier) to unlimited
- Batch processing: Available via batch API

### Apify Limits

- Actor runs: Depends on plan
- Concurrent runs: Limited by plan
- Data retention: 7 days (free tier)

### Implementation

```python
from datetime import datetime, timedelta

class RateLimiter:
    def __init__(self, calls_per_minute=10):
        self.calls_per_minute = calls_per_minute
        self.calls = []
    
    def __call__(self, func):
        def wrapper(*args, **kwargs):
            now = datetime.now()
            # Remove old calls outside the window
            self.calls = [c for c in self.calls 
                         if now - c < timedelta(minutes=1)]
            
            if len(self.calls) >= self.calls_per_minute:
                wait_time = 60 - (now - self.calls[0]).seconds
                time.sleep(wait_time)
            
            self.calls.append(now)
            return func(*args, **kwargs)
        return wrapper
```

---

## Testing API Functions

### Unit Tests

```python
import unittest
from src.helper import ask_openai

class TestAPIFunctions(unittest.TestCase):
    def test_openai_api(self):
        response = ask_openai("Say hello", max_tokens=10)
        self.assertIsInstance(response, str)
        self.assertGreater(len(response), 0)
    
    def test_job_fetch(self):
        jobs = fetch_linkedin_jobs("Python", rows=5)
        self.assertIsInstance(jobs, list)
        self.assertGreater(len(jobs), 0)

if __name__ == '__main__':
    unittest.main()
```

---

## Best Practices

1. **Always validate input** before API calls
2. **Use environment variables** for sensitive data
3. **Implement error handling** and retries
4. **Monitor API usage** and costs
5. **Cache results** when appropriate
6. **Use logging** for debugging
7. **Test thoroughly** before deployment

---

## See Also

- [Architecture Documentation](ARCHITECTURE.md)
- [Configuration Guide](CONFIGURATION.md)
- [Installation Guide](INSTALLATION.md)

