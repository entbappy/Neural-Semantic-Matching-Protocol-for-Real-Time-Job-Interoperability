# Resume Processing Pipeline

## Complete Resume Analysis Flow

```mermaid
flowchart TD
    Input["📥 Input: PDF Resume<br/>from User Upload"]
    Input --> Validate["✓ File Validation<br/>- Check format<br/>- Verify size<br/>- Scan for corruption"]
    
    Validate --> Valid{File<br/>Valid?}
    Valid -->|No| Reject["❌ Reject File<br/>Invalid Format or Size"]
    Valid -->|Yes| Extract
    
    Reject --> Error1["Return Error<br/>to User"]
    
    Extract["📄 Extract Text<br/>using PyMuPDF"]
    Extract --> CheckEmpty{Text<br/>Empty?}
    CheckEmpty -->|Yes| Error2["❌ No Readable Text<br/>File may be image-based"]
    CheckEmpty -->|No| Clean
    
    Clean["🧹 Clean & Normalize<br/>- Remove duplicates<br/>- Fix encoding<br/>- Trim whitespace"]
    Clean --> Tokenize["🔢 Tokenize Text<br/>Count tokens for API"]
    
    Tokenize --> CheckTokens{Tokens<br/>Too Many?}
    CheckTokens -->|Yes| Truncate["✂️ Truncate to<br/>Max Tokens"]
    CheckTokens -->|No| Truncate
    
    Truncate --> Summary["🤖 Generate Summary<br/>via GPT-4o"]
    
    Summary --> SummaryPrompt["
    Prompt:
    Summarize this resume
    in 100-150 words,
    highlighting key skills
    and experience
    "]
    
    SummaryPrompt --> Skills["🎯 Extract Key Skills<br/>via GPT-4o"]
    
    Skills --> SkillsPrompt["
    Prompt:
    List the top 10
    technical and
    soft skills
    "]
    
    SkillsPrompt --> Experience["📈 Analyze Experience<br/>via GPT-4o"]
    
    Experience --> ExpPrompt["
    Prompt:
    Summarize work
    experience,
    technologies,
    and achievements
    "]
    
    ExpPrompt --> Education["🎓 Extract Education<br/>via GPT-4o"]
    
    Education --> EduPrompt["
    Prompt:
    List degrees,
    certifications,
    and courses
    "]
    
    EduPrompt --> Validate2["✓ Validate Outputs<br/>using Guardrails AI"]
    
    Validate2 --> Valid2{Output<br/>Valid?}
    Valid2 -->|No| RetryGPT["🔄 Retry with<br/>Different Prompt"]
    RetryGPT --> Summary
    Valid2 -->|Yes| Combine
    
    Combine["📦 Combine Results<br/>into Profile Object"]
    
    Combine --> Store["💾 Store in<br/>Vector Database"]
    Store --> Generate["🔍 Generate Embeddings<br/>for Similarity Search"]
    
    Generate --> Output["📊 Output: Structured<br/>Resume Profile"]
    
    Output --> End(["✅ Processing<br/>Complete"])
    Error1 --> End
    Error2 --> End
    
    style Input fill:#90EE90
    style Validate fill:#E3F2FD
    style Extract fill:#E3F2FD
    style Clean fill:#E3F2FD
    style Summary fill:#FFE082
    style Skills fill:#FFE082
    style Experience fill:#FFE082
    style Education fill:#FFE082
    style Validate2 fill:#E3F2FD
    style Combine fill:#E3F2FD
    style Store fill:#BA68C8
    style Output fill:#90EE90
    style Reject fill:#FF6B6B
    style Error1 fill:#FF6B6B
    style Error2 fill:#FF6B6B
    style End fill:#90EE90
```

---

## Parallel Processing Architecture

```mermaid
flowchart TD
    Start["📥 Resume Text<br/>Ready"]
    
    Start --> Split["Split into<br/>4 Parallel Streams"]
    
    Split --> S1["Stream 1:<br/>Summary"]
    Split --> S2["Stream 2:<br/>Skills"]
    Split --> S3["Stream 3:<br/>Experience"]
    Split --> S4["Stream 4:<br/>Education"]
    
    S1 --> P1["🤖 GPT-4o<br/>Summary Analysis"]
    S2 --> P2["🤖 GPT-4o<br/>Skill Extraction"]
    S3 --> P3["🤖 GPT-4o<br/>Experience Parse"]
    S4 --> P4["🤖 GPT-4o<br/>Education Extract"]
    
    P1 --> V1["✓ Validate<br/>Output"]
    P2 --> V2["✓ Validate<br/>Output"]
    P3 --> V3["✓ Validate<br/>Output"]
    P4 --> V4["✓ Validate<br/>Output"]
    
    V1 --> Merge["Merge All<br/>Results"]
    V2 --> Merge
    V3 --> Merge
    V4 --> Merge
    
    Merge --> Profile["📊 Complete<br/>Profile"]
    
    style Start fill:#90EE90
    style S1 fill:#E3F2FD
    style S2 fill:#E3F2FD
    style S3 fill:#E3F2FD
    style S4 fill:#E3F2FD
    style P1 fill:#FFE082
    style P2 fill:#FFE082
    style P3 fill:#FFE082
    style P4 fill:#FFE082
    style Merge fill:#BA68C8
    style Profile fill:#90EE90
```

---

## Data Transformation Pipeline

```mermaid
flowchart LR
    Raw["Raw PDF<br/>Text"] --> Parse["Parse<br/>Structure"]
    Parse --> Extract["Extract<br/>Entities"]
    Extract --> Normalize["Normalize<br/>Values"]
    Normalize --> Enrich["Enrich with<br/>Context"]
    Enrich --> Validate["Validate<br/>Data"]
    Validate --> Embed["Generate<br/>Embeddings"]
    Embed --> Store["Store in<br/>Vector DB"]
    Store --> Ready["Ready for<br/>Matching"]
    
    style Raw fill:#FFE082
    style Parse fill:#E3F2FD
    style Extract fill:#E3F2FD
    style Normalize fill:#E3F2FD
    style Enrich fill:#E3F2FD
    style Validate fill:#E3F2FD
    style Embed fill:#BA68C8
    style Store fill:#BA68C8
    style Ready fill:#90EE90
```

---

## Prompt Engineering Strategy

```mermaid
flowchart TD
    Task["📋 Task Definition<br/>Extract specific info"] --> System["🎯 System Prompt<br/>Set context & role"]
    System --> Structure["📐 Structure<br/>Define output format"]
    Structure --> Examples["📝 Few-shot Examples<br/>Provide samples"]
    Examples --> Constraints["⚠️ Constraints<br/>Add limitations"]
    Constraints --> Temperature["🌡️ Temperature<br/>Control randomness"]
    
    Temperature --> Final["✅ Final Prompt<br/>Ready to Execute"]
    
    Final --> Execute["🚀 Execute with<br/>GPT-4o"]
    Execute --> Quality{Quality<br/>Check}
    
    Quality -->|Low| Refine["🔧 Refine Prompt<br/>Improve wording"]
    Quality -->|High| Success["✅ Success<br/>Use Result"]
    
    Refine --> Execute
    
    style Task fill:#FFE082
    style System fill:#FFE082
    style Structure fill:#FFE082
    style Examples fill:#FFE082
    style Constraints fill:#FFE082
    style Temperature fill:#FFE082
    style Final fill:#90EE90
    style Execute fill:#64B5F6
    style Success fill:#90EE90
    style Refine fill:#FFB6C6
```

---

## Token Management

```mermaid
flowchart TD
    Input["📥 Input Text<br/>Resume content"]
    Input --> Count["🔢 Count Tokens<br/>~4 chars = 1 token"]
    Count --> Check{Too Many<br/>Tokens?}
    
    Check -->|No| Process["✅ Process<br/>as-is"]
    Check -->|Yes| Strategy{Strategy?}
    
    Strategy -->|Truncate| S1["Truncate to<br/>max tokens"]
    Strategy -->|Summarize| S2["Pre-summarize<br/>reduce size"]
    Strategy -->|Split| S3["Split into<br/>sections"]
    
    S1 --> Process
    S2 --> Process
    S3 --> Process
    
    Process --> Estimate["💰 Estimate Cost<br/>Input × Rate"]
    Estimate --> Execute["🚀 Call API<br/>with tokens"]
    Execute --> Count2["🔢 Count Output<br/>Tokens"]
    Count2 --> Total["💰 Calculate Total<br/>Cost"]
    
    style Input fill:#90EE90
    style Count fill:#E3F2FD
    style S1 fill:#FFE082
    style S2 fill:#FFE082
    style S3 fill:#FFE082
    style Process fill:#90EE90
    style Estimate fill:#BA68C8
    style Execute fill:#64B5F6
    style Total fill:#BA68C8
```

---

## Caching Strategy

```mermaid
flowchart TD
    Input["📥 Resume Text"] --> Hash["🔐 Generate Hash<br/>of content"]
    Hash --> Check{Cache<br/>Hit?}
    
    Check -->|Yes| Retrieve["⚡ Retrieve from<br/>Cache"]
    Check -->|No| Process["🤖 Process with<br/>GPT-4o"]
    
    Process --> Validate["✓ Validate<br/>Results"]
    Validate --> Store["💾 Store in<br/>Cache"]
    
    Retrieve --> Output["📤 Return<br/>Results"]
    Store --> Output
    
    style Input fill:#90EE90
    style Hash fill:#E3F2FD
    style Check fill:#FFE082
    style Retrieve fill:#90EE90
    style Process fill:#64B5F6
    style Validate fill:#E3F2FD
    style Store fill:#BA68C8
    style Output fill:#90EE90
```

---

## See Also

- [System Flow Diagram](system_flow.md)
- [Job Matching Flow](job_matching.md)
- [Data Interoperability Flow](data_interoperability.md)

