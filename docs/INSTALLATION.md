# Installation Guide

## System Requirements

- **Operating System**: Windows, macOS, or Linux
- **Python**: 3.13 or higher
- **Memory**: Minimum 4GB RAM (8GB+ recommended for smooth operation)
- **Disk Space**: ~500MB for dependencies

---

## Step 1: Prerequisites Setup

Before installing the project, ensure you have the required API keys and tokens:

### OpenAI API Key

1. Visit [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign up or log in to your account
3. Generate a new API key
4. Copy the key (you won't be able to see it again)

### Apify API Token

1. Visit [Apify Platform](https://apify.com)
2. Create an account or log in
3. Navigate to Settings → Integrations
4. Copy your API token

---

## Step 2: Clone or Download the Repository

```bash
# Using git (if available)
git clone <repository-url>
cd "Real-Time Job Interoperability"

# Or manually download and extract the ZIP file
cd "path/to/extracted/folder"
```

---

## Step 3: Create Virtual Environment

It's recommended to use a virtual environment to avoid conflicts with other Python projects.

### On Windows:

```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate
```

### On macOS/Linux:

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate
```

---

## Step 4: Install Dependencies

### Option A: Using pip (Standard Installation)

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Option B: Using UV Package Manager (⚡ Recommended for Speed)

UV is a blazing-fast Python package manager written in Rust. It's ideal for large projects.

#### Install UV:

```bash
pip install uv
```

#### Install dependencies with UV:

```bash
uv pip install -r requirements.txt
```

**Why UV?**
- ⚡ 10-100x faster dependency resolution
- 🔒 Secure and reproducible builds
- 📦 Drop-in replacement for pip
- 🎯 Better error messages

---

## Step 5: Environment Configuration

1. **Create `.env` file** in the project root:

```bash
touch .env  # On macOS/Linux
# Or manually create .env file on Windows
```

2. **Add your API credentials** to `.env`:

```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Apify Configuration
APIFY_API_TOKEN=your_apify_api_token_here

# Optional: Logging Level (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL=INFO
```

3. **Verify the `.env` file** is in the root directory and **never** commit it to version control.

---

## Step 6: Verify Installation

Test if everything is installed correctly:

```bash
# Test Python installation
python --version  # Should show 3.13 or higher

# Test package imports
python -c "import streamlit, openai, PyMuPDF; print('All packages installed successfully!')"

# Verify environment variables are loaded
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('OPENAI_API_KEY' in os.environ)"
```

---

## Running the Application

### Start the Streamlit App

```bash
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

### Start the MCP Server

```bash
python mcp_server.py
```

### Run Utility Scripts

```bash
python all-utils/main.py
```

---

## Troubleshooting

### Issue: Python version not compatible

```bash
# Check your Python version
python --version

# Solution: Install Python 3.13 from python.org
```

### Issue: ModuleNotFoundError

```bash
# Ensure virtual environment is activated
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate

# Reinstall packages
pip install -r requirements.txt
```

### Issue: API Key not found

1. Verify `.env` file exists in the project root
2. Check that the file has `OPENAI_API_KEY=your_key` format
3. Make sure there are no extra spaces: `OPENAI_API_KEY = your_key` ❌ → `OPENAI_API_KEY=your_key` ✅

### Issue: Streamlit not found

```bash
# Reinstall Streamlit specifically
pip install streamlit>=1.45.1
```

### Issue: PyMuPDF installation fails

```bash
# Try installing from pre-compiled wheels
pip install --only-binary :all: PyMuPDF
```

---

## Using UV for Faster Installations

### Install Dependencies with UV

```bash
# Install uv first (one time)
pip install uv

# Use uv for faster installation
uv pip install -r requirements.txt

# Create a venv and install in one command
uv venv .venv
uv pip install -r requirements.txt
```

### UV Commands Cheat Sheet

```bash
# Create virtual environment
uv venv .venv

# Install specific package
uv pip install streamlit

# Install from requirements file
uv pip install -r requirements.txt

# Freeze dependencies
uv pip freeze > requirements.txt

# Show installed packages
uv pip show
```

---

## Next Steps

1. ✅ Installation complete!
2. 📖 Read the [Architecture Documentation](ARCHITECTURE.md)
3. 🔑 Configure your API keys (done in Step 5)
4. 🚀 Start the application with `streamlit run app.py`
5. 📚 Explore the [API Documentation](API.md)

---

## Getting Help

- 📖 Check the [Configuration Guide](CONFIGURATION.md)
- 🔄 Review [Workflow Diagrams](../workflows/)
- 💬 Open an issue on GitHub
- 📧 Contact the development team

