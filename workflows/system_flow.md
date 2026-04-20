# System Flow Diagram

## Main System Workflow

This diagram shows the complete flow of the Real-Time Job Interoperability System from user input to job recommendations.

```mermaid
flowchart TD
    Start([User Visits Application]) --> Upload[Upload Resume PDF]
    Upload --> ValidateFile{Valid PDF File?}
    ValidateFile -->|No| ErrorFile["❌ Show Error<br/>Invalid Format"]
    ErrorFile --> Upload
    ValidateFile -->|Yes| ExtractText["📄 Extract Text<br/>from PDF"]
    
    ExtractText --> CheckText{Text<br/>Extracted?}
    CheckText -->|No| ErrorText["❌ PDF Parse Error<br/>Empty Content"]
    ErrorText --> Upload
    CheckText -->|Yes| LoadEnv["⚙️ Load API Keys<br/>from .env"]
    
    LoadEnv --> CheckKeys{API Keys<br/>Valid?}
    CheckKeys -->|No| ErrorKeys["❌ Configuration Error<br/>Missing API Keys"]
    ErrorKeys --> LoadEnv
    CheckKeys -->|Yes| Analyze["🤖 AI Analysis<br/>Resume Processing"]
    
    Analyze --> ProcessingBox["
    Processing:
    ✓ Profile Summary
    ✓ Skill Extraction
    ✓ Experience Analysis
    ✓ Key Competencies
    "]
    
    ProcessingBox --> DisplayAnalysis["📊 Display Analysis<br/>to User"]
    DisplayAnalysis --> UserChoice{User Action?}
    
    UserChoice -->|View Jobs| GetKeywords["🔍 Generate Search<br/>Keywords"]
    UserChoice -->|Quit| End1([Session Ended])
    UserChoice -->|View Roadmap| GenRoadmap["🗺️ Generate Career<br/>Roadmap"]
    
    GetKeywords --> FetchJobs["🔗 Fetch Job Listings<br/>from Platforms"]
    FetchJobs --> FetchBox["
    Fetching:
    • LinkedIn Jobs
    • Naukri Jobs
    • (via Apify)
    "]
    
    FetchBox --> RankJobs["📈 Rank & Filter<br/>Job Results"]
    RankJobs --> DisplayJobs["💼 Display Recommended<br/>Jobs"]
    DisplayJobs --> UserJobChoice{User Action?}
    
    UserJobChoice -->|View Job Details| ShowDetails["📋 Show Full<br/>Job Details"]
    ShowDetails --> UserJobChoice
    UserJobChoice -->|Next Jobs| DisplayJobs
    UserJobChoice -->|Back to Menu| UserChoice
    UserJobChoice -->|Exit| End2([Application Exit])
    
    GenRoadmap --> RoadmapBox["
    Career Path:
    ✓ Current Level
    ✓ Next Roles
    ✓ Skills Needed
    ✓ Timeline
    "]
    RoadmapBox --> DisplayRoadmap["📊 Display Career<br/>Roadmap"]
    DisplayRoadmap --> UserChoice
    
    style Start fill:#90EE90
    style End1 fill:#FFB6C6
    style End2 fill:#FFB6C6
    style ErrorFile fill:#FF6B6B
    style ErrorText fill:#FF6B6B
    style ErrorKeys fill:#FF6B6B
    style ProcessingBox fill:#E3F2FD
    style FetchBox fill:#E3F2FD
    style RoadmapBox fill:#F3E5F5
```

---

## Component Interaction

```mermaid
flowchart LR
    UI["🎨 Streamlit UI<br/>app.py"]
    PDF["📄 PDF Handler<br/>PyMuPDF"]
    AI["🤖 OpenAI<br/>GPT-4o"]
    JobAPI["💼 Job Fetcher<br/>Apify"]
    DB["💾 Vector DB<br/>Chroma"]
    
    UI <-->|Upload| PDF
    UI <-->|Analyze| AI
    UI <-->|Fetch| JobAPI
    UI <-->|Store/Query| DB
    AI <-->|Embeddings| DB
    JobAPI <-->|Data| DB
    
    style UI fill:#FFE082
    style PDF fill:#81C784
    style AI fill:#64B5F6
    style JobAPI fill:#FF8A65
    style DB fill:#BA68C8
```

---

## Decision Tree

```mermaid
flowchart TD
    Start([User Starts App]) --> Q1{Has Resume?}
    Q1 -->|No| Q2["Create Resume<br/>Using Template"]
    Q1 -->|Yes| Q3["Upload<br/>Existing Resume"]
    
    Q2 --> Q4{Resume<br/>Ready?}
    Q3 --> Q4
    Q4 -->|Yes| Q5["Process<br/>with AI"]
    Q4 -->|No| Q2
    
    Q5 --> Q6{Satisfied with<br/>Analysis?}
    Q6 -->|No| Q7["Edit Resume<br/>and Reprocess"]
    Q6 -->|Yes| Q8["Search for<br/>Jobs"]
    
    Q7 --> Q6
    Q8 --> Q9{Found<br/>Matches?}
    Q9 -->|No| Q10["Adjust<br/>Criteria"]
    Q9 -->|Yes| Q11["Review<br/>Matches"]
    
    Q10 --> Q8
    Q11 --> Q12{Apply<br/>Now?}
    Q12 -->|Yes| Q13["Save Job<br/>Info"]
    Q12 -->|No| Q14["Bookmark<br/>for Later"]
    
    Q13 --> Q15["View Career<br/>Roadmap"]
    Q14 --> Q15
    Q15 --> End([Session End])
    
    style Start fill:#90EE90
    style End fill:#FFB6C6
```

---

## Error Handling Flow

```mermaid
flowchart TD
    Try["Attempt<br/>Operation"]
    Try -->|Success| Continue["✅ Continue<br/>Workflow"]
    Try -->|Failure| Catch["⚠️ Catch<br/>Exception"]
    
    Catch --> ErrType{Error<br/>Type?}
    
    ErrType -->|API Key Error| E1["❌ Invalid API Key<br/>- Check .env file<br/>- Verify credentials<br/>- Regenerate key"]
    ErrType -->|PDF Error| E2["❌ PDF Parse Error<br/>- File corrupted<br/>- Wrong format<br/>- File too large"]
    ErrType -->|Network Error| E3["❌ Network Error<br/>- Check internet<br/>- Verify proxy<br/>- Retry later"]
    ErrType -->|Rate Limit| E4["⏳ Rate Limited<br/>- Wait 60 seconds<br/>- Reduce batch size<br/>- Retry request"]
    ErrType -->|Other Error| E5["❌ Unknown Error<br/>- Check logs<br/>- Contact support<br/>- Report issue"]
    
    E1 --> Retry{"Retry<br/>Operation?"}
    E2 --> Retry
    E3 --> Retry
    E4 --> Retry
    E5 --> Retry
    
    Retry -->|Yes| Try
    Retry -->|No| Abort["⛔ Abort<br/>Operation"]
    
    Continue --> End(["✅ Success"])
    Abort --> End
    
    style Try fill:#E3F2FD
    style Continue fill:#90EE90
    style Catch fill:#FFE082
    style E1 fill:#FF6B6B
    style E2 fill:#FF6B6B
    style E3 fill:#FF6B6B
    style E4 fill:#FF6B6B
    style E5 fill:#FF6B6B
    style Abort fill:#FFB6C6
    style End fill:#90EE90
```

---

## See Also

- [Resume Processing Flow](resume_processing.md)
- [Job Matching Flow](job_matching.md)
- [Data Interoperability Flow](data_interoperability.md)

