# Data Interoperability & Integration Flow

## Multi-Platform Job Aggregation

```mermaid
flowchart TD
    SearchQuery["🔍 User Search<br/>Query"]
    
    SearchQuery --> LinkedInBranch["LinkedIn Jobs"]
    SearchQuery --> NaukriBranch["Naukri Jobs"]
    
    LinkedInBranch --> ApifyLinkedIn["🔗 Apify Actor<br/>BHzefUZlZRKWxkTck"]
    NaukriBranch --> ApifyNaukri["🔗 Apify Actor<br/>alpcnRV9YI9lYVPWk"]
    
    ApifyLinkedIn --> ConfigLinkedIn["⚙️ Configure<br/>- Title: {query}<br/>- Location: India<br/>- Rows: 60<br/>- Proxy: Residential"]
    
    ApifyNaukri --> ConfigNaukri["⚙️ Configure<br/>- Keyword: {query}<br/>- MaxJobs: 60<br/>- Freshness: all<br/>- SortBy: relevance"]
    
    ConfigLinkedIn --> FetchLinkedIn["🌐 Fetch from<br/>LinkedIn<br/>via Residential Proxy"]
    ConfigNaukri --> FetchNaukri["🌐 Fetch from<br/>Naukri<br/>via Apify"]
    
    FetchLinkedIn --> ParseLinkedIn["📄 Parse<br/>LinkedIn HTML"]
    FetchNaukri --> ParseNaukri["📄 Parse<br/>Naukri HTML"]
    
    ParseLinkedIn --> Normalize1["📋 Normalize to<br/>Standard Format"]
    ParseNaukri --> Normalize2["📋 Normalize to<br/>Standard Format"]
    
    Normalize1 --> Schema["
    Standard Schema:
    - title
    - company
    - location
    - salary
    - description
    - url
    - posted_date
    "]
    
    Normalize2 --> Schema
    Schema --> Deduplicate["🔄 Remove<br/>Duplicates"]
    
    Deduplicate --> Combine["📦 Combine<br/>All Jobs"]
    Combine --> Clean["🧹 Clean Data<br/>Remove nulls"]
    
    Clean --> Count["📊 Statistics<br/>LinkedIn: X jobs<br/>Naukri: Y jobs<br/>Total: X+Y"]
    
    Count --> Result["✅ Aggregated<br/>Job List<br/>120+ jobs"]
    
    style SearchQuery fill:#90EE90
    style ApifyLinkedIn fill:#FF8A65
    style ApifyNaukri fill:#FF8A65
    style ConfigLinkedIn fill:#FFE082
    style ConfigNaukri fill:#FFE082
    style Normalize1 fill:#E3F2FD
    style Normalize2 fill:#E3F2FD
    style Schema fill:#E3F2FD
    style Combine fill:#BA68C8
    style Result fill:#90EE90
```

---

## Data Synchronization Pipeline

```mermaid
flowchart TD
    LocalDB["💾 Local Vector DB<br/>Chroma SQLite"]
    LinkedInAPI["🔗 LinkedIn Jobs"]
    NaukriAPI["🔗 Naukri Jobs"]
    
    LocalDB --> CheckSync["🔄 Check Sync<br/>Status"]
    CheckSync --> NeedSync{Needs<br/>Update?}
    
    NeedSync -->|Yes| Fetch1["Fetch from<br/>LinkedIn"]
    NeedSync -->|Yes| Fetch2["Fetch from<br/>Naukri"]
    NeedSync -->|No| UseCached["Use Cached<br/>Data"]
    
    LinkedInAPI --> Fetch1
    NaukriAPI --> Fetch2
    
    Fetch1 --> Transform1["Transform<br/>to Standard"]
    Fetch2 --> Transform2["Transform<br/>to Standard"]
    
    Transform1 --> Validate1["✓ Validate<br/>Data Quality"]
    Transform2 --> Validate2["✓ Validate<br/>Data Quality"]
    
    Validate1 --> Merge["📦 Merge<br/>Datasets"]
    Validate2 --> Merge
    
    Merge --> UpdateDB["💾 Update Local<br/>Vector DB"]
    UpdateDB --> GenerateEmbed["🧮 Generate<br/>Embeddings"]
    GenerateEmbed --> Index["📑 Create<br/>Indices"]
    
    Index --> Ready["✅ Data Ready<br/>for Matching"]
    UseCached --> Ready
    
    style LocalDB fill:#BA68C8
    style LinkedInAPI fill:#FF8A65
    style NaukriAPI fill:#FF8A65
    style CheckSync fill:#E3F2FD
    style Fetch1 fill:#FFE082
    style Fetch2 fill:#FFE082
    style Merge fill:#E3F2FD
    style UpdateDB fill:#BA68C8
    style GenerateEmbed fill:#BA68C8
    style Ready fill:#90EE90
```

---

## API Integration Architecture

```mermaid
flowchart LR
    App["🎨 Streamlit<br/>Application"]
    
    App -->|Search Query| JobFetcher["🔗 Job Fetcher<br/>Module<br/>src/job_api.py"]
    
    JobFetcher -->|LinkedIn| ApifyLinkedIn["Apify Actor<br/>LinkedIn"]
    JobFetcher -->|Naukri| ApifyNaukri["Apify Actor<br/>Naukri"]
    
    ApifyLinkedIn -->|HTTP| LinkedIn["🌐 LinkedIn<br/>Job Platform"]
    ApifyNaukri -->|HTTP| Naukri["🌐 Naukri<br/>Job Platform"]
    
    LinkedIn -->|HTML Response| Parse1["Parse & Extract<br/>Job Data"]
    Naukri -->|HTML Response| Parse2["Parse & Extract<br/>Job Data"]
    
    Parse1 --> Normalize["Normalize Data<br/>to Standard Format"]
    Parse2 --> Normalize
    
    Normalize --> Deduplicate["Remove Duplicates<br/>& Clean"]
    
    Deduplicate -->|Job Data| VectorDB["💾 Vector Database<br/>Chroma"]
    
    VectorDB -->|Embedding| Match["🎯 Matching<br/>Engine"]
    Match -->|Recommendations| App
    
    style App fill:#FFE082
    style JobFetcher fill:#E3F2FD
    style ApifyLinkedIn fill:#FF8A65
    style ApifyNaukri fill:#FF8A65
    style LinkedIn fill:#64B5F6
    style Naukri fill:#64B5F6
    style VectorDB fill:#BA68C8
    style Match fill:#BA68C8
```

---

## Data Transformation Pipeline

```mermaid
flowchart TD
    RawLinkedIn["🔗 Raw LinkedIn<br/>HTML Response"]
    RawNaukri["🔗 Raw Naukri<br/>HTML Response"]
    
    RawLinkedIn --> ExtractLI["Extract Fields<br/>- title<br/>- company<br/>- location<br/>- salary<br/>- description"]
    
    RawNaukri --> ExtractNK["Extract Fields<br/>- jobtitle<br/>- companyname<br/>- joblocation<br/>- salaryrange<br/>- jobdescription"]
    
    ExtractLI --> CleanLI["Clean Data<br/>- Trim spaces<br/>- Fix encoding<br/>- Remove HTML"]
    
    ExtractNK --> CleanNK["Clean Data<br/>- Trim spaces<br/>- Fix encoding<br/>- Remove HTML"]
    
    CleanLI --> MapLI["Map Fields<br/>to Standard<br/>Schema"]
    
    CleanNK --> MapNK["Map Fields<br/>to Standard<br/>Schema"]
    
    MapLI --> Standard["
    ✅ Standard Format:
    {
      'title': str,
      'company': str,
      'location': str,
      'salary': str,
      'description': str,
      'url': str,
      'platform': str,
      'posted_date': str
    }
    "]
    
    MapNK --> Standard
    
    Standard --> Validate["✓ Validate<br/>Required fields"]
    Validate --> Output["📤 Ready for<br/>Storage & Matching"]
    
    style RawLinkedIn fill:#FF8A65
    style RawNaukri fill:#FF8A65
    style ExtractLI fill:#FFE082
    style ExtractNK fill:#FFE082
    style CleanLI fill:#E3F2FD
    style CleanNK fill:#E3F2FD
    style MapLI fill:#E3F2FD
    style MapNK fill:#E3F2FD
    style Standard fill:#90EE90
    style Validate fill:#E3F2FD
    style Output fill:#90EE90
```

---

## Caching & Optimization

```mermaid
flowchart TD
    Request["🔍 Search Request<br/>{query, location}"]
    
    Request --> HashQuery["🔐 Hash Query<br/>Generate unique key"]
    HashQuery --> CheckCache["💾 Check Cache<br/>Redis/Local"]
    
    CheckCache --> CacheHit{Cache<br/>Hit?}
    
    CacheHit -->|Yes| ReturCached["⚡ Return<br/>Cached Results"]
    CacheHit -->|No| Fetch["🌐 Fetch from<br/>APIs"]
    
    Fetch --> Process["🔄 Process<br/>& Transform"]
    Process --> Store["💾 Store in<br/>Cache"]
    Store --> TTL["⏱️ Set TTL<br/>1 hour"]
    
    TTL --> Validate["✓ Validate<br/>Freshness"]
    Validate --> Return["📤 Return<br/>Results"]
    
    ReturCached --> Return
    
    Return --> Log["📊 Log<br/>Statistics<br/>- Cache hit rate<br/>- API calls saved"]
    
    style Request fill:#90EE90
    style CheckCache fill:#BA68C8
    style Fetch fill:#FF8A65
    style Store fill:#BA68C8
    style Return fill:#90EE90
```

---

## Error Handling & Fallback

```mermaid
flowchart TD
    Request["📥 Job Fetch<br/>Request"]
    
    Request --> Try1["Try LinkedIn<br/>Apify"]
    Try1 --> Success1{Success?}
    
    Success1 -->|Yes| LI["✅ LinkedIn<br/>Jobs Fetched"]
    Success1 -->|No| Error1["⚠️ LinkedIn<br/>Failed"]
    
    Error1 --> Retry1["🔄 Retry with<br/>Backoff"]
    Retry1 --> Success2{Success?}
    
    Success2 -->|Yes| LI
    Success2 -->|No| Fallback1["⏭️ Skip LinkedIn<br/>Use Naukri Only"]
    
    Try1 --> Try2["Try Naukri<br/>Apify"]
    Try2 --> Success3{Success?}
    
    Success3 -->|Yes| NK["✅ Naukri<br/>Jobs Fetched"]
    Success3 -->|No| Error2["⚠️ Naukri<br/>Failed"]
    
    Error2 --> Retry2["🔄 Retry with<br/>Backoff"]
    Retry2 --> Success4{Success?}
    
    Success4 -->|Yes| NK
    Success4 -->|No| Fallback2["⏭️ Skip Naukri<br/>Use LinkedIn Only"]
    
    LI --> Combine["📦 Combine<br/>Results"]
    NK --> Combine
    Fallback1 --> Combine
    Fallback2 --> Combine
    
    Combine --> Final{Any<br/>Results?}
    
    Final -->|Yes| Return["✅ Return<br/>Available Jobs"]
    Final -->|No| Error3["❌ No Results<br/>Show Error"]
    
    style Request fill:#90EE90
    style LI fill:#90EE90
    style NK fill:#90EE90
    style Return fill:#90EE90
    style Error1 fill:#FF6B6B
    style Error2 fill:#FF6B6B
    style Error3 fill:#FF6B6B
    style Fallback1 fill:#FFB6C6
    style Fallback2 fill:#FFB6C6
```

---

## Rate Limiting & Throttling

```mermaid
flowchart TD
    Request["📥 API Request"]
    
    Request --> Check["Check Rate<br/>Limit Status"]
    Check --> AllowedQ{Requests<br/>Available?}
    
    AllowedQ -->|Yes| Execute["✅ Execute<br/>Request"]
    AllowedQ -->|No| Queue["⏳ Queue<br/>Request"]
    
    Execute --> Wait["⏱️ Wait<br/>Min Interval"]
    Wait --> Send["📤 Send to<br/>Apify"]
    
    Queue --> CheckAgain["Recheck<br/>Limits"]
    CheckAgain --> WaitTime{Wait<br/>Time OK?}
    
    WaitTime -->|No| Queue
    WaitTime -->|Yes| Execute
    
    Send --> Response["📥 Get<br/>Response"]
    Response --> UpdateLimits["🔄 Update<br/>Rate Limits"]
    UpdateLimits --> Done["✅ Complete"]
    
    style Request fill:#FFE082
    style AllowedQ fill:#E3F2FD
    style Queue fill:#FFB6C6
    style Execute fill:#90EE90
    style Done fill:#90EE90
```

---

## See Also

- [System Flow Diagram](system_flow.md)
- [Resume Processing Flow](resume_processing.md)
- [Job Matching Flow](job_matching.md)

