# Job Matching & Recommendation Flow

## Neural-Semantic Matching Algorithm

```mermaid
flowchart TD
    Profile["👤 Candidate Profile<br/>from Resume"]
    Jobs["💼 Available Jobs<br/>from Platforms"]
    
    Profile --> ExtractFeatures["🔍 Extract Features<br/>- Skills<br/>- Experience<br/>- Preferences"]
    Jobs --> ParseJobs["📄 Parse Job Data<br/>- Title<br/>- Requirements<br/>- Description"]
    
    ExtractFeatures --> Embed1["🧮 Generate Embeddings<br/>using OpenAI"]
    ParseJobs --> Embed2["🧮 Generate Embeddings<br/>using OpenAI"]
    
    Embed1 --> SemanticDb["💾 Store in<br/>Vector Database"]
    Embed2 --> SemanticDb
    
    SemanticDb --> Calculate["📊 Calculate Similarity<br/>Cosine Distance"]
    Calculate --> Filter["🔗 Filter Matches<br/>threshold > 0.7"]
    
    Filter --> Rank["📈 Rank by<br/>Relevance Score"]
    Rank --> Deduplicate["🔄 Remove<br/>Duplicates"]
    
    Deduplicate --> Result["✅ Ranked Job<br/>Recommendations"]
    
    style Profile fill:#90EE90
    style Jobs fill:#90EE90
    style ExtractFeatures fill:#FFE082
    style ParseJobs fill:#FFE082
    style Embed1 fill:#BA68C8
    style Embed2 fill:#BA68C8
    style SemanticDb fill:#BA68C8
    style Calculate fill:#64B5F6
    style Filter fill:#64B5F6
    style Rank fill:#64B5F6
    style Result fill:#90EE90
```

---

## Matching Stages

```mermaid
flowchart TD
    Input["🎯 Candidate + Jobs"] 
    
    Input --> Stage1["Stage 1: Keyword Match<br/>Fast, Rule-based"]
    Stage1 --> S1Result["Candidate has 5+ keywords<br/>from job description"]
    
    S1Result --> Stage2["Stage 2: Skill Matching<br/>Semantic Analysis"]
    Stage2 --> S2Result["Core skills overlap > 60%"]
    
    S2Result --> Stage3["Stage 3: Experience Match<br/>Level Alignment"]
    Stage3 --> S3Result["Years of experience<br/>within range"]
    
    S3Result --> Stage4["Stage 4: Domain Match<br/>Industry Fit"]
    Stage4 --> S4Result["Industry experience<br/>matches role"]
    
    S4Result --> FinalScore["📊 Combine Scores<br/>Weighted Average"]
    FinalScore --> Output["✅ Final<br/>Compatibility Score"]
    
    style Input fill:#FFE082
    style Stage1 fill:#E3F2FD
    style Stage2 fill:#FFE082
    style Stage3 fill:#FFE082
    style Stage4 fill:#FFE082
    style FinalScore fill:#BA68C8
    style Output fill:#90EE90
```

---

## Ranking Algorithm

```mermaid
flowchart TD
    Candidates["📋 Filtered Job<br/>Candidates"]
    
    Candidates --> Score1["💯 Relevance<br/>Score 0-100"]
    Score1 --> Score2["💼 Experience<br/>Match 0-100"]
    Score2 --> Score3["🎯 Skill<br/>Match 0-100"]
    Score3 --> Score4["📍 Location<br/>Preference 0-100"]
    Score4 --> Score5["💰 Salary<br/>Expectation 0-100"]
    
    Score1 --> Weights["⚖️ Apply Weights<br/>40% + 25% + 20% + 10% + 5%"]
    Score2 --> Weights
    Score3 --> Weights
    Score4 --> Weights
    Score5 --> Weights
    
    Weights --> Calculate["🧮 Calculate<br/>Weighted Sum"]
    Calculate --> Rank["📊 Sort by<br/>Final Score"]
    
    Rank --> Top10["🏆 Select Top 10<br/>Matches"]
    Top10 --> Display["📱 Display to<br/>User"]
    
    style Candidates fill:#90EE90
    style Score1 fill:#E3F2FD
    style Score2 fill:#E3F2FD
    style Score3 fill:#E3F2FD
    style Score4 fill:#E3F2FD
    style Score5 fill:#E3F2FD
    style Weights fill:#FFE082
    style Calculate fill:#64B5F6
    style Top10 fill:#BA68C8
    style Display fill:#90EE90
```

---

## Recommendation Engine

```mermaid
flowchart TD
    User["👤 User Profile"]
    History["📊 User History<br/>- Viewed jobs<br/>- Applied jobs<br/>- Saved jobs"]
    
    User --> Extract["Extract Preferences<br/>- Salary range<br/>- Location<br/>- Job type"]
    History --> Analyze["Analyze Patterns<br/>- Popular sectors<br/>- Preferred companies<br/>- Common skills"]
    
    Extract --> Factors["📈 Combine Factors<br/>Profile + History"]
    Analyze --> Factors
    
    Factors --> Query["🔍 Generate Search<br/>Optimized Query"]
    Query --> Fetch["🔗 Fetch Jobs<br/>from Platforms"]
    Fetch --> Candidates["📋 Job Candidates<br/>200+ jobs"]
    
    Candidates --> Filter1["Filter by<br/>Requirements"]
    Filter1 --> Filter2["Filter by<br/>Preferences"]
    Filter2 --> Match["🎯 Run<br/>Matching Algorithm"]
    
    Match --> Candidates2["📊 Scored<br/>Candidates 50+ jobs"]
    Candidates2 --> Personalize["🎨 Personalize<br/>Order"]
    Personalize --> Result["✅ Recommended<br/>Jobs 1-20"]
    
    style User fill:#90EE90
    style History fill:#90EE90
    style Candidates fill:#E3F2FD
    style Candidates2 fill:#FFE082
    style Result fill:#90EE90
```

---

## Real-time Matching Flow

```mermaid
flowchart TD
    Job["💼 New Job Posted"]
    Profiles["👥 Candidate Profiles<br/>in Database"]
    
    Job --> Parse["Parse Job<br/>Requirements"]
    Parse --> Embed["Generate Job<br/>Embeddings"]
    Embed --> Query["🔍 Query Vector DB<br/>Similar Candidates"]
    
    Query --> Matches["👥 Potential Matches<br/>100+ profiles"]
    Matches --> Score["💯 Score Each<br/>Match"]
    Score --> Rank["📊 Rank by<br/>Score"]
    
    Rank --> Filter["Filter by<br/>Threshold"]
    Filter --> Notify["📧 Notify<br/>Candidates"]
    
    Notify --> Feedback["📊 Collect<br/>Feedback"]
    Feedback --> Refine["🔄 Refine<br/>Algorithm"]
    
    style Job fill:#90EE90
    style Profiles fill:#90EE90
    style Matches fill:#FFE082
    style Rank fill:#BA68C8
    style Notify fill:#64B5F6
    style Feedback fill:#E3F2FD
```

---

## Feedback Loop

```mermaid
flowchart TD
    User["👤 User Views<br/>Recommendation"]
    User --> Action{User<br/>Action?}
    
    Action -->|Click Job| Click["✅ Clicked"]
    Action -->|Apply| Apply["✅ Applied"]
    Action -->|Save| Save["⭐ Saved"]
    Action -->|Skip| Skip["⏭️ Skipped"]
    Action -->|Downvote| Down["👎 Not Interested"]
    
    Click --> Record["📊 Record<br/>Interaction"]
    Apply --> Record
    Save --> Record
    Skip --> Record
    Down --> Record
    
    Record --> Update["🔄 Update User<br/>Profile"]
    Update --> Retrain["🤖 Retrain<br/>Matching Model"]
    Retrain --> Improve["📈 Improve Future<br/>Recommendations"]
    
    style User fill:#90EE90
    style Click fill:#E3F2FD
    style Apply fill:#90EE90
    style Save fill:#90EE90
    style Skip fill:#FFB6C6
    style Down fill:#FF6B6B
    style Record fill:#FFE082
    style Update fill:#64B5F6
    style Retrain fill:#BA68C8
    style Improve fill:#90EE90
```

---

## Filtering Strategy

```mermaid
flowchart TD
    AllJobs["💼 All Available<br/>Jobs 1000+"]
    
    AllJobs --> LocationFilter["📍 Location<br/>Filter"]
    LocationFilter --> L1["Jobs in<br/>preferred location"]
    
    L1 --> SalaryFilter["💰 Salary<br/>Filter"]
    SalaryFilter --> S1["Within salary<br/>range"]
    
    S1 --> ExperienceFilter["📈 Experience<br/>Filter"]
    ExperienceFilter --> E1["Match experience<br/>level"]
    
    E1 --> SkillFilter["🎯 Skill<br/>Filter"]
    SkillFilter --> SK1["Has required<br/>skills"]
    
    SK1 --> CompanyFilter["🏢 Company<br/>Filter"]
    CompanyFilter --> C1["Preferred<br/>companies"]
    
    C1 --> Result["✅ Filtered<br/>Jobs 50+"]
    
    style AllJobs fill:#FFE082
    style LocationFilter fill:#E3F2FD
    style SalaryFilter fill:#E3F2FD
    style ExperienceFilter fill:#E3F2FD
    style SkillFilter fill:#E3F2FD
    style CompanyFilter fill:#E3F2FD
    style Result fill:#90EE90
```

---

## See Also

- [System Flow Diagram](system_flow.md)
- [Resume Processing Flow](resume_processing.md)
- [Data Interoperability Flow](data_interoperability.md)

