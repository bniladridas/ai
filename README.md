# AI Model Benchmarking System

A comprehensive framework for benchmarking and comparing multiple AI language models including DeepSeek R1, GPT-4o, Claude-3.5, and Gemini-1.5.

## Features

- **Multi-Model Support**: Compare performance across different AI providers
- **Adaptive Model Selection**: Intelligent routing based on task complexity and historical performance
- **Performance Dashboard**: Real-time visualization of model metrics
- **Comprehensive Testing**: Rate limiting, validation, and benchmarking suites
- **Docker Support**: Containerized deployment with multi-stage builds

## Quick Start

### With Docker (Recommended)

1. Clone the repository
2. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. Run with Docker Compose:
   ```bash
   docker-compose up
   ```

4. Access the dashboard at http://localhost:8501

### Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables (see .env.example)

3. Run the dashboard:
   ```bash
   streamlit run dashboard/dashboard.py
   ```

## Supported Models

- **DeepSeek R1** (via NVIDIA API)
- **GPT-4o** (OpenAI)
- **Claude-3.5 Sonnet** (Anthropic)
- **Gemini-1.5 Flash** (Google)

## API Keys Required

- `NVIDIA_API_KEY`: For DeepSeek models
- `OPENAI_API_KEY`: For GPT models
- `ANTHROPIC_API_KEY`: For Claude models
- `GOOGLE_API_KEY`: For Gemini models

## Development

- Run tests: `pytest tests/`
- Format code: Follow PEP 8
- Commit style: One-word lowercase messages enforced by git hook

## Architecture

- `ml/router.py`: Adaptive model selection logic
- `dashboard/`: Streamlit performance visualization
- `tests/`: Comprehensive test suites
- `examples/`: Usage examples in Python, Node.js, and cURL
