<p align="center">
  <strong>English</strong> | <a href="README_CN.md">中文</a>
</p>

# Claude to OpenAI Proxy Service

Use Claude models with OpenAI interface

## 🗂️ What it does
A FastAPI service that translates OpenAI requests to Claude format, so you can use Claude without changing your existing OpenAI code.

## 🚀 Getting Started

```bash
# Clone/download and navigate to the directory
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Start the service
python main.py

# Visit http://localhost:8000
```

## ⚙️ Environment Variables

```bash
# Choose one
ANTHROPIC_API_KEY=your-api-key
ANTHROPIC_AUTH_TOKEN=your-auth-token

# Model
DEFAULT_MODEL=your-model-name

# Other settings
HOST=0.0.0.0
PORT=8000
RELOAD=true
```

## 🔧 Dependencies
- **FastAPI** - Web framework
- **Anthropic SDK** - Claude official Python package
- **Uvicorn** - ASGI server
- **Pydantic** - Data validation

## 📊 Usage
After starting, visit http://localhost:8000/docs to see API documentation