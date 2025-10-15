# AI Benchmark

Compare DeepSeek R1, GPT-4o, Claude-3.5, Gemini-1.5.

## Quick Start

```bash
# With Docker
cp .env.example .env  # Add API keys
docker-compose up
# Visit http://localhost:8501

# Or locally
pip install -r requirements.txt
streamlit run dashboard/dashboard.py
```

## API Keys

- `NVIDIA_API_KEY` (DeepSeek)
- `OPENAI_API_KEY` (GPT)
- `ANTHROPIC_API_KEY` (Claude)
- `GOOGLE_API_KEY` (Gemini)
