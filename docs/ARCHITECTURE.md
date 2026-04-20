# System Architecture Documentation

## Overview

The Real-Time Job Interoperability System is built on a **three-layer neural-semantic architecture** that intelligently bridges candidate profiles with job opportunities through AI-powered semantic matching.

---

## Architecture Overview

```
┌────────────────────────────────────────────────────────────────┐
│                        USER INTERFACE LAYER                     │
│                     (Streamlit Web Application)                 │
└────────────────────────────────────────────────────────────────┘
                               ↓
┌────────────────────────────────────────────────────────────────┐
│                    DATA PROCESSING LAYER                        │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ Resume Parser │ PDF Extraction │ Text Normalization      │  │
│  └──────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────┘
                               ↓
┌────────────────────────────────────────────────────────────────┐
│                   AI INTELLIGENCE LAYER                         │
│  ┌─────────────┬──────────────┬────────────┬────────────────┐  │
│  │   Profile   │  Skill Gap   │   Career   │  Semantic      │  │
│  │Summarization│  Analysis    │  Roadmap   │  Search Engine │  │
│  └─────────────┴──────────────┴────────────┴────────────────┘  │
│                    (OpenAI GPT-4o)                             │
└────────────────────────────────────────────────────────────────┘
                               ↓
┌────────────────────────────────────────────────────────────────┐
│                   INTEGRATION LAYER                             │
│  ┌────────────────┬────────────────┬──────────────────────┐   │
│  │ LinkedIn Jobs  │ Naukri Jobs    │ Vector Database      │   │
│  │ (Apify)        │ (Apify)        │ (Chroma)             │   │
│  └────────────────┴────────────────┴──────────────────────┘   │
└────────────────────────────────────────────────────────────────┘
```

---

## Component Architecture

### 1. **User Interface Layer**

#### Streamlit Web Application (`app.py`)

The frontend interface providing:

- 📄 **Resume Upload**: PDF file upload and preview
- 🎯 **Resume Analysis**: Display AI-generated insights
- 💼 **Job Recommendations**: Interactive job browsing
- 🗺️ **Career Insights**: Personalized career suggestions
- ⚙️ **Settings**: API configuration and preferences

**Technology Stack**:
- Streamlit >= 1.45.1
- Python 3.13+

---

### 2. **Data Processing Layer**

#### Resume Parser Module (`src/helper.py`)

Responsible for:

- **PDF Extraction**: Uses PyMuPDF (fitz) to extract text from PDF documents
- **Text Normalization**: Cleans and standardizes extracted text
- **OpenAI Integration**: Communicates with GPT-4o API

**Key Functions**:

```python
def extract_text_from_pdf(uploaded_file)
    # Extract raw text from PDF
    # Returns: str (full document text)

def ask_openai(prompt, max_tokens=500)
    # Send prompt to OpenAI GPT-4o
    # Returns: str (AI-generated response)
```

**Technology Stack**:
- PyMuPDF >= 1.26.0
- OpenAI >= 1.84.0
- python-dotenv >= 1.1.0

---

### 3. **AI Intelligence Layer**

The brain of the system - performs semantic analysis using OpenAI's GPT-4o.

#### Key Capabilities

1. **Profile Summarization**
   - Extract key information from resume
   - Generate professional summary
   - Identify core competencies

2. **Skill Gap Analysis**
   - Compare candidate skills with job requirements
   - Identify missing skills
   - Suggest learning paths

3. **Career Roadmap Generation**
   - Analyze current profile
   - Suggest next career moves
   - Recommend skill development areas

4. **Semantic Search Engine**
   - Transform job descriptions into search queries
   - Optimize keyword matching
   - Rank job relevance

**Technology Stack**:
- OpenAI GPT-4o API
- Prompt Engineering

---

### 4. **Integration Layer**

#### Job API Module (`src/job_api.py`)

Integrates with multiple job sources:

##### LinkedIn Jobs Integration
```python
def fetch_linkedin_jobs(search_query, location="india", rows=60)
    # Fetch jobs from LinkedIn via Apify
    # Uses: BHzefUZlZRKWxkTck actor
    # Returns: List[dict] (job listings)
```

##### Naukri Jobs Integration
```python
def fetch_naukri_jobs(search_query, location="india", rows=60)
    # Fetch jobs from Naukri via Apify
    # Uses: alpcnRV9YI9lYVPWk actor
    # Returns: List[dict] (job listings)
```

**Technology Stack**:
- Apify Client >= 1.10.0
- Residential Proxies for reliable scraping

#### Vector Database (`all-utils/db/`)

Stores and retrieves semantic representations:

- **Chroma SQLite3**: Vector similarity search
- **Database Path**: `all-utils/db/chroma.sqlite3`

---

## Data Flow Architecture

### Resume to Job Matching Flow

```
1. User Upload
   ├─ PDF File
   └─ → Streamlit Upload Handler

2. Text Extraction
   ├─ PyMuPDF Processing
   └─ → Raw Text

3. AI Analysis (GPT-4o)
   ├─ Profile Summarization
   ├─ Skill Extraction
   ├─ Experience Analysis
   └─ → Structured Profile Data

4. Semantic Transformation
   ├─ Generate Search Keywords
   ├─ Identify Job Preferences
   └─ → Optimized Queries

5. Job Aggregation
   ├─ LinkedIn Jobs (Apify)
   ├─ Naukri Jobs (Apify)
   └─ → Combined Job List

6. Semantic Matching
   ├─ Calculate Relevance Score
   ├─ Rank Results
   └─ → Ranked Recommendations

7. Presentation
   ├─ Display Insights
   ├─ Show Job Matches
   └─ → User Interface
```

---

## Module Dependency Graph

```
┌──────────────┐
│  app.py      │  (Main Web App)
│ (Streamlit)  │
└──────┬───────┘
       │
       ├──────────────────┬──────────────────┐
       ↓                  ↓                  ↓
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ helper.py    │  │ job_api.py   │  │ Guardrails   │
│ (PDF/OpenAI) │  │ (Job Fetch)  │  │ (Validation) │
└──────────────┘  └──────────────┘  └──────────────┘
       │                  │
       └──────────┬───────┘
                  ↓
         ┌──────────────────┐
         │ .env             │
         │ (Config)         │
         └──────────────────┘
```

---

## Technology Stack

### Frontend
- **Streamlit**: Interactive web framework
- **Python**: 3.13+

### Backend
- **OpenAI GPT-4o**: AI analysis engine
- **PyMuPDF**: PDF processing
- **Apify**: Web scraping platform

### Data Storage
- **Chroma**: Vector database
- **SQLite3**: Vector store backend

### Infrastructure
- **python-dotenv**: Environment management
- **MCP**: Model Context Protocol (for tools)

---

## Security Considerations

### API Key Management

1. **Environment Variables**: Keys stored in `.env` (never committed)
2. **Secure Loading**: Using `python-dotenv`
3. **Access Control**: Keys isolated per function

### Data Privacy

1. **Resume Data**: Processed locally first
2. **API Communication**: Encrypted HTTPS only
3. **No Data Storage**: User data not persisted unnecessarily

### Validation

1. **Guardrails AI**: Response validation
2. **Input Validation**: Resume format checking
3. **Output Validation**: Response verification

---

## Scalability Considerations

### Current Architecture

- Single-user Streamlit app
- Direct API calls (no caching)
- Local vector database

### Future Scalability Improvements

1. **API Gateway**: Replace Streamlit with REST API
2. **Caching Layer**: Redis for response caching
3. **Distributed Processing**: Async job processing
4. **Load Balancing**: Multiple server instances
5. **Advanced Vector DB**: Managed cloud service (Pinecone, Weaviate)

---

## Integration Points

### OpenAI API

**Endpoint**: `https://api.openai.com/v1/chat/completions`

**Models Used**:
- `gpt-4o`: For analysis and matching

**Rate Limits**: Subject to OpenAI plan

### Apify API

**Endpoint**: `https://api.apify.com`

**Actors Used**:
- `BHzefUZlZRKWxkTck`: LinkedIn Jobs
- `alpcnRV9YI9lYVPWk`: Naukri Jobs

**Features**:
- Residential Proxies
- Real-time Data
- Custom Parsing

---

## Error Handling & Monitoring

### Error Types

1. **API Errors**: Invalid keys, rate limits, network issues
2. **Parsing Errors**: Corrupted PDFs, unsupported formats
3. **Processing Errors**: LLM failures, timeout issues

### Logging

- Configured via `LOG_LEVEL` in `.env`
- Logs stored in utility modules
- Debug enabled via environment variable

---

## Performance Metrics

### Expected Performance

| Operation | Time | Notes |
|-----------|------|-------|
| PDF Upload & Parse | 2-5s | Depends on file size |
| AI Analysis | 10-30s | Depends on resume length |
| Job Fetching | 15-45s | Apify processing time |
| Display Results | 1-3s | Rendering |

---

## Deployment Considerations

### Containerization

Recommended Docker setup:

```dockerfile
FROM python:3.13-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["streamlit", "run", "app.py"]
```

### Environment Variables

Required for deployment:
- `OPENAI_API_KEY`
- `APIFY_API_TOKEN`
- `STREAMLIT_SERVER_PORT` (optional)

---

## Next Steps

1. 📖 Review [API Documentation](API.md)
2. ⚙️ Check [Configuration Guide](CONFIGURATION.md)
3. 🔄 Explore [Workflow Diagrams](../workflows/)
4. 🚀 Start development with provided components

