# Configuration Guide

## Environment Setup

### 1. Basic Configuration

Create a `.env` file in the project root directory:

```env
# OpenAI Configuration (Required)
OPENAI_API_KEY=sk-proj-your-api-key-here

# Apify Configuration (Required)
APIFY_API_TOKEN=apify_api_your-token-here

# Logging Configuration (Optional)
LOG_LEVEL=INFO
```

### 2. Getting API Keys

#### OpenAI API Key

**Steps**:
1. Visit [platform.openai.com](https://platform.openai.com)
2. Sign in or create an account
3. Navigate to **API keys** section
4. Click **Create new secret key**
5. Copy the key (you won't see it again)
6. Add to `.env`: `OPENAI_API_KEY=sk-...`

**Security**:
- ✅ Never commit `.env` to version control
- ✅ Rotate keys periodically
- ✅ Use environment variables in production
- ❌ Don't share keys in emails or chat

#### Apify API Token

**Steps**:
1. Visit [apify.com](https://apify.com)
2. Sign in or create an account
3. Go to **Settings** → **Integrations**
4. Copy your **API Token**
5. Add to `.env`: `APIFY_API_TOKEN=apify_api_...`

**Testing Token**:
```bash
# Verify token works
python -c "from apify_client import ApifyClient; print(ApifyClient('your_token').user())"
```

---

## Streamlit Configuration

### Streamlit Config File

Create `.streamlit/config.toml` for advanced settings:

```toml
[theme]
primaryColor = "#FF6B35"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

[server]
port = 8501
headless = true
runOnSave = true
maxUploadSize = 200

[logger]
level = "info"
```

### Common Streamlit Settings

| Setting | Purpose | Example |
|---------|---------|---------|
| `port` | Server port | 8501 |
| `maxUploadSize` | Max file upload (MB) | 200 |
| `headless` | Run without browser | true |
| `runOnSave` | Auto-reload on file change | true |
| `logger.level` | Log verbosity | "info" |

---

## OpenAI Configuration

### Model Selection

Current implementation uses `gpt-4o`. Other available models:

| Model | Speed | Quality | Cost | Use Case |
|-------|-------|---------|------|----------|
| `gpt-4o` | Fast | Excellent | Medium | Default (recommended) |
| `gpt-4-turbo` | Medium | Excellent | High | Complex analysis |
| `gpt-3.5-turbo` | Very Fast | Good | Low | Quick processing |

**Changing Model**:

Edit `src/helper.py`:
```python
response = client.chat.completions.create(
    model="gpt-4o",  # Change here
    messages=[...]
)
```

### Token Management

**Estimate costs**:
```python
# Input tokens: ~4 characters per token
# Output tokens: ~4 characters per token

# Example: 1000-word resume + 500-word response
# ~250 input tokens, ~125 output tokens
# Cost: (250 * 0.003 / 1000) + (125 * 0.006 / 1000) = $0.00135
```

### Rate Limiting

Configure request throttling in `src/helper.py`:

```python
import time
from functools import wraps

def rate_limit(calls_per_minute=60):
    min_interval = 60 / calls_per_minute
    last_called = [0.0]
    
    def decorator(func):
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            if elapsed < min_interval:
                time.sleep(min_interval - elapsed)
            last_called[0] = time.time()
            return func(*args, **kwargs)
        return wrapper
    return decorator

@rate_limit(calls_per_minute=20)
def ask_openai(prompt, max_tokens=500):
    # API call here
    pass
```

---

## Apify Configuration

### LinkedIn Job Scraper

Actor ID: `BHzefUZlZRKWxkTck`

**Parameters**:
```python
run_input = {
    "title": "Python Developer",          # Job title/keyword
    "location": "India",                   # Location
    "rows": 60,                            # Number of results (1-300)
    "proxy": {
        "useApifyProxy": True,
        "apifyProxyGroups": ["RESIDENTIAL"]  # Proxy type
    }
}
```

### Naukri Job Scraper

Actor ID: `alpcnRV9YI9lYVPWk`

**Parameters**:
```python
run_input = {
    "keyword": "Python",                  # Search keyword
    "maxJobs": 60,                        # Max results
    "freshness": "all",                   # "all" or recent
    "sortBy": "relevance",                # "relevance" or "recency"
    "experience": "all"                   # Experience level
}
```

### Proxy Configuration

**Residential Proxies** (recommended):
- More reliable for job sites
- Higher success rate
- Slightly more expensive

**Datacenter Proxies** (budget):
- Faster
- More likely to be blocked
- Cheaper

**Switch proxy type**:
```python
# In src/job_api.py
"proxy": {
    "useApifyProxy": True,
    "apifyProxyGroups": ["DATACENTER"]  # Change to DATACENTER
}
```

---

## Database Configuration

### Chroma Vector Database

**Location**: `all-utils/db/chroma.sqlite3`

**Configuration**:
```python
import chromadb

# Initialize Chroma client
client = chromadb.Client(
    settings=chromadb.config.Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory="all-utils/db",
        anonymized_telemetry=False
    )
)

# Create or get collection
collection = client.get_or_create_collection(
    name="resumes",
    metadata={"hnsw:space": "cosine"}
)

# Add embeddings
collection.add(
    ids=["doc1"],
    embeddings=[[1.2, 2.3, 4.5]],
    documents=["document text"],
    metadatas=[{"source": "resume"}]
)

# Query
results = collection.query(
    query_embeddings=[[1.1, 2.2, 4.4]],
    n_results=3
)
```

---

## Logging Configuration

### Python Logging Setup

**Log Levels**:
```
DEBUG (10) - Detailed diagnostic info
INFO (20) - General information
WARNING (30) - Warning messages
ERROR (40) - Error messages
CRITICAL (50) - Critical failures
```

**Example Logger**:
```python
import logging
import os
from dotenv import load_dotenv

load_dotenv()
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

logging.basicConfig(
    level=LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
```

### Configure in `.env`

```env
LOG_LEVEL=DEBUG  # For development
LOG_LEVEL=INFO   # For production
```

---

## Performance Tuning

### PDF Processing

**Optimize extraction speed**:
```python
# Fast mode (less accurate)
doc = fitz.open("file.pdf")
text = doc.get_text(option="text")

# High quality (slower)
text = doc.get_text(option="block")
```

### OpenAI Requests

**Optimize token usage**:
```python
# Fewer tokens = faster + cheaper
prompt = "Summarize in 50 words: ..."  # Constrains output

# Batch processing
# Use OpenAI Batch API for multiple requests
```

### Job Fetching

**Reduce API calls**:
```python
# Cache results locally
from functools import lru_cache

@lru_cache(maxsize=100)
def fetch_linkedin_jobs_cached(search_query, location, rows):
    return fetch_linkedin_jobs(search_query, location, rows)
```

---

## Security Configuration

### Secure Credential Storage

**On Local Machine**:
```bash
# Option 1: Environment variables
export OPENAI_API_KEY="sk-..."
export APIFY_API_TOKEN="apify_api_..."

# Option 2: .env file (excluded from git)
echo "OPENAI_API_KEY=sk-..." >> .env
```

**On Production Server**:
```bash
# Use secrets management:
# - AWS Secrets Manager
# - Azure Key Vault
# - HashiCorp Vault
# - 1Password / LastPass
```

### GitIgnore Configuration

Add to `.gitignore`:
```
# Environment variables
.env
.env.local
.env.*.local

# API keys
.credentials
secrets/

# Logs
logs/
*.log

# Cache
__pycache__/
*.pyc
.cache/

# Virtual environments
venv/
.venv/
```

### HTTPS Configuration

For production deployment:
```python
# Use SSL certificates
import ssl

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
ssl_context.load_cert_chain('cert.pem', 'key.pem')
```

---

## Deployment Configuration

### Development

```env
OPENAI_API_KEY=sk-proj-dev-key
APIFY_API_TOKEN=apify_api_dev
LOG_LEVEL=DEBUG
```

### Staging

```env
OPENAI_API_KEY=sk-proj-staging-key
APIFY_API_TOKEN=apify_api_staging
LOG_LEVEL=INFO
```

### Production

```env
OPENAI_API_KEY=${SECRET_OPENAI_KEY}
APIFY_API_TOKEN=${SECRET_APIFY_TOKEN}
LOG_LEVEL=WARNING
```

---

## Docker Configuration

### Dockerfile

```dockerfile
FROM python:3.13-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Set environment variables
ENV STREAMLIT_SERVER_HEADLESS=true
ENV STREAMLIT_SERVER_PORT=8501

# Expose port
EXPOSE 8501

# Run application
CMD ["streamlit", "run", "app.py"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8501:8501"
    environment:
      OPENAI_API_KEY: ${OPENAI_API_KEY}
      APIFY_API_TOKEN: ${APIFY_API_TOKEN}
      LOG_LEVEL: INFO
    volumes:
      - ./all-utils/db:/app/all-utils/db
```

---

## Troubleshooting Configuration

### Issue: API Key Invalid

```bash
# Verify key format
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
key = os.getenv('OPENAI_API_KEY')
print(f'Key starts with: {key[:20]}...')
print(f'Key is valid: {key.startswith(\"sk-\")}')"
```

### Issue: Rate Limiting

```python
# Add exponential backoff
import time
import openai

for attempt in range(3):
    try:
        response = client.chat.completions.create(...)
        break
    except openai.RateLimitError:
        wait_time = 2 ** attempt
        print(f"Rate limited, waiting {wait_time}s")
        time.sleep(wait_time)
```

### Issue: Proxy Issues

```python
# Check proxy connectivity
from apify_client import ApifyClient

try:
    client = ApifyClient(token)
    user = client.user()
    print(f"Connected as: {user['email']}")
except Exception as e:
    print(f"Connection error: {e}")
```

---

## Configuration Checklist

- [ ] OpenAI API key obtained
- [ ] Apify token obtained
- [ ] `.env` file created with credentials
- [ ] `.env` added to `.gitignore`
- [ ] Tested API connectivity
- [ ] Streamlit config created (optional)
- [ ] Logging configured
- [ ] Database initialized
- [ ] PDF test file uploaded successfully
- [ ] Job fetching tested

---

## See Also

- [Installation Guide](INSTALLATION.md)
- [Architecture Documentation](ARCHITECTURE.md)
- [API Documentation](API.md)

