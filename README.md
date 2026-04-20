# Real-Time Job Interoperability

This project is an AI-powered job recommender system that helps users find job opportunities based on their resume. It integrates with LinkedIn and Naukri job platforms and provides resume analysis, skill gap identification, and career roadmap suggestions.

## Features

- Resume upload and text extraction from PDF
- AI-powered resume summarization using OpenAI
- Skill gap analysis
- Career roadmap suggestions
- Job recommendations from LinkedIn and Naukri
- MCP server for job fetching tools

## Prerequisites

- Python 3.13 or higher
- OpenAI API key

## Installation

1. Clone or download this repository.

2. Navigate to the project directory:
   ```
   cd "your directory"
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the root directory and add your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

### Running the Streamlit App

To run the main job recommender application:

```
streamlit run app.py
```

This will start the web application where you can upload your resume and get job recommendations.

### Running the MCP Server

To run the MCP server for job fetching tools:

```
python mcp_server.py
```

### Running Utility Demos

To run the utility demonstrations:

```
python all-utils/main.py
```

### Running Guardrails Evaluation

To run the guardrails evaluation script:

```
python guardrails_eval.py
```

## Project Structure

- `app.py`: Main Streamlit application
- `mcp_server.py`: MCP server for job fetching
- `guardrails_eval.py`: Guardrails evaluation script
- `src/`: Source code directory
  - `helper.py`: Helper functions for PDF extraction and OpenAI integration
  - `job_api.py`: API functions for fetching jobs from LinkedIn and Naukri
- `utilities/`: Utility modules and notebooks
- `all-utils/`: Main script for running utility demos

## Dependencies

The project uses the following main dependencies:

- Streamlit: For the web interface
- OpenAI: For AI-powered analysis
- PyMuPDF: For PDF text extraction
- Apify Client: For job scraping
- Guardrails AI: For validation
- MCP: For server tools

## Contributing

Feel free to contribute to this project by submitting issues or pull requests.

## License

This project is licensed under the MIT License.