# DeepSeek AI Exploration Project

## Model Overview: DeepSeek-R1

### Key Characteristics
- **Architecture**: Mixture of Experts (MoE)
- **Base Model**: DeepSeek-V3-Base
- **Activated Parameters**: 37 billion
- **Total Parameters**: 671 billion
- **Context Length**: 128K tokens
- **Version**: V1.0

### Model Capabilities
- State-of-the-art reasoning model
- Excels in math, code, and language tasks
- Trained using large-scale reinforcement learning (RL)
- Enhanced through supervised fine-tuning (SFT)

### Recommended Configuration
- Temperature: 0.5-0.7 (recommended: 0.6)
- Avoid system prompts
- For math problems: Include step-by-step reasoning
- Conduct multiple tests and average results

### Supported Environments
- **Runtime Engines**: vLLM and SGLang
- **Hardware**: NVIDIA Ampere, Blackwell, Jetson, Hopper, Lovelace, Pascal, Turing, Volta
- **Preferred OS**: Linux

### Licensing
- Community-driven model by DeepSeek AI
- MIT License
- Ready for research and commercial use

### Additional Resources
- [DeepSeek Website](https://www.deepseek.com/)
- [GitHub Repository](https://github.com/deepseek-ai/DeepSeek-R1)
- [Research Paper](https://arxiv.org/abs/2501.12948)

## Project Overview
This project explores the capabilities of the DeepSeek-R1 model using NVIDIA AI Enterprise's integration with multiple language runtimes.

## Prerequisites
- Python 3.8+
- Node.js 14+ (optional)
- Bash (with cURL)
- NVIDIA API Key

## Conventional Commits

This project follows conventional commit standards to maintain a clean and consistent git history.

### Setup
1. Copy the commit-msg hook to enable validation:
   ```bash
   cp scripts/commit-msg .git/hooks/commit-msg
   chmod +x .git/hooks/commit-msg
   ```

### Commit Message Format
- Start with a type: `feat:`, `fix:`, `docs:`, `style:`, `refactor:`, `test:`, `chore:`, `perf:`, `ci:`, `build:`, `revert:`
- First line lowercase, ≤30 characters
- Example: `feat: add dashboard`

### History Cleanup
To rewrite existing commit messages:
```bash
./scripts/rewrite_msg.sh
git push origin main --force
```

## Setup Instructions
1. Clone the repository
2. Create a Python virtual environment:
   ```
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Set up API Key:
   ```
   export NVIDIA_API_KEY='your_api_key_here'
   ```

## API Key Management

### Secure Configuration
We use a `.env` file to manage sensitive configuration details securely:

1. Copy the `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file and replace placeholders with your actual API keys:
   ```bash
   nano .env
   ```

### Best Practices
- Never commit `.env` file to version control
- Use environment variables for sensitive information
- Rotate API keys periodically
- Limit API key permissions

### Required Environment Variables
- `NVIDIA_API_KEY`: Your NVIDIA DeepSeek AI API key
- `DEEPSEEK_MODEL_NAME`: Model identifier
- `DEEPSEEK_DEFAULT_TEMPERATURE`: Model creativity setting
- `DEEPSEEK_DEFAULT_TOP_P`: Nucleus sampling parameter
- `DEEPSEEK_MAX_TOKENS`: Maximum response length

### Python Dependency for .env Support
Install python-dotenv to load environment variables:
```bash
pip install python-dotenv
```

### Example Usage in Python
```python
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Access API key
api_key = os.getenv('NVIDIA_API_KEY')
```

### Security Warning
Protect your API keys. Do not share them or expose them in public repositories.

## Running Examples

### Python Example
```bash
python examples/deepseek_python_example.py
```

### Node.js Example
```bash
# Install Node.js dependencies
npm init -y
npm install openai

# Run the script
node examples/deepseek_node_example.js
```

### Bash cURL Example
```bash
# Make the script executable
chmod +x examples/deepseek_curl_example.sh

# Run the script
./examples/deepseek_curl_example.sh
```

## Running the Notebook
```
jupyter notebook notebooks/DeepSeek_Exploration.ipynb
```

## Jupyter Notebook JSON Structure

### Understanding Notebook Metadata

Jupyter notebooks are stored as JSON files with a specific structure:

```json
{
    "cells": [
        {
            "cell_type": "markdown|code",
            "metadata": {},
            "source": ["Cell content as an array of strings"]
        }
    ],
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.8.5"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}
```

### Key Components
- **cells**: Array of notebook cells (markdown or code)
- **metadata**: Information about kernel and language
- **nbformat**: Notebook format version
- **nbformat_minor**: Minor version of the notebook format

### Troubleshooting Tips
- Ensure valid JSON structure
- Check for proper cell formatting
- Verify metadata is correctly defined
- Use tools like `nbconvert` to validate notebooks

## Automated Notebook Validation

### GitHub Action Workflow
We've implemented an automated Jupyter notebook validation workflow that:
- Checks all `.ipynb` files on push and pull requests
- Automatically repairs notebook JSON structure
- Ensures compatibility with GitHub rendering
- Fixes common notebook formatting issues

#### Workflow Features
- Validates notebook JSON structure
- Adds missing `outputs` property to code cells
- Resets `execution_count`
- Commits and pushes repaired notebooks

### How It Works
1. Scans all Jupyter notebooks in the repository
2. Checks for required notebook properties
3. Automatically repairs formatting issues
4. Prevents merging if critical issues are found

**Note**: This workflow helps maintain notebook quality and ensures consistent rendering across different platforms.

## API Response Validation

### Automated Testing Strategy
We've implemented comprehensive API response validation to ensure:
- Consistent and reliable AI model performance
- Robust error handling
- Quality of generated responses

#### Test Coverage
- Reasoning query validation
- Coding generation tests
- Multilingual response checks
- Token limit adherence

### Validation Workflow
- Runs daily via GitHub Actions
- Triggered on pull requests
- Checks API responses against predefined criteria

#### Key Validation Checks
- Response structure integrity
- Content relevance
- Language understanding
- Token limit compliance

### Monitoring and Alerts
- Automatic Slack notifications on test failures
- Detailed error reporting
- Continuous integration monitoring

## Advanced API Performance Validation

### Comprehensive Performance Benchmarking
Our validation strategy now includes advanced performance testing:

#### Performance Metrics
- **Response Time Tracking**
  - Maximum individual response time
  - Average response time across queries
  - Concurrent request performance

- **Token Generation Analysis**
  - Tokens generated per second
  - Consistency of token generation rate

#### Rate Limiting Validation
- Simulate high-frequency requests
- Test API's graceful handling under load
- Verify rate limit error handling

### Performance Thresholds
- Maximum response time: 5 seconds
- Average response time: 2 seconds
- Concurrent request capacity: 10 simultaneous queries
- Maximum token generation rate: 100 tokens/second

### Monitoring Capabilities
- Automated daily performance tests
- Detailed performance reports
- Slack notifications for critical issues
- Performance report artifacts for trend analysis

### Key Testing Scenarios
1. Individual query performance
2. Concurrent request handling
3. Rate limiting behavior
4. Token generation consistency

### Reporting
- JSON performance reports
- Timestamped test results
- Workflow status tracking

**Note**: Helps maintain API reliability and identify potential bottlenecks early

## Multi-Model AI Performance Benchmarking

### Comprehensive Model Comparison Framework

#### Benchmarking Objectives
- Compare performance across different AI models
- Evaluate real-world use case capabilities
- Provide data-driven model selection insights

#### Evaluated Models
- DeepSeek R1
- OpenAI GPT-3.5 Turbo
- (Expandable to more models)

### Real-World Scenario Testing

#### Scenario Categories
1. **Technical Documentation Generation**
   - Assess structured content creation
   - Evaluate technical writing capabilities

2. **Code Generation**
   - Test programming task completion
   - Analyze code quality and complexity handling

3. **Complex Reasoning**
   - Evaluate multi-dimensional problem analysis
   - Test abstract thinking capabilities

4. **Multilingual Translation**
   - Check translation accuracy
   - Assess technical terminology preservation

### Performance Metrics
- Average Response Time
- Median Response Time
- Token Generation Rate
- Task Success Rate
- Error Rate
- Total Execution Time

### Benchmarking Workflow
- Automated weekly performance tests
- Comprehensive scenario-based evaluation
- Detailed JSON performance reports

### Reporting
- Standardized performance metrics
- Comparative model analysis
- Trend tracking over time

**Note**: Provides transparent, data-driven insights into AI model capabilities

## Advanced AI Model Performance Analytics 🚀

### Comprehensive Multi-Model Benchmarking Framework

#### 🔍 Benchmarking Evolution
- Expanded beyond initial two-model comparison
- Support for multiple AI model providers
- Advanced performance tracking and visualization

#### 📊 Supported Models
- OpenAI GPT-3.5 Turbo
- DeepSeek R1
- Anthropic Claude
- Google PaLM 2
- (Easily extensible to more models)

### Performance Tracking Innovations

#### 1. Visualization Dashboard 📈
- Interactive Plotly graphs
- Real-time performance comparisons
- Stored in `reports/` directory
  - `response_time_comparison.html`
  - `token_generation_rate.html`

#### 2. Database-Driven Insights 💾
- SQLite performance logging
- Historical trend analysis
- Comprehensive metrics tracking
  - Timestamp
  - Model-specific performance
  - Scenario complexity

#### 3. Expanded Scenario Testing 🧪
- **Technical Documentation Generation**
- **Complex Code Generation**
- **Multi-dimensional Reasoning**
- **Multilingual Technical Translation**

### Performance Metrics Tracked
- Average Response Time
- Median Response Time
- Token Generation Rate
- Task Success Rate
- Error Rate
- Execution Time

### Workflow Integration
- Weekly automated benchmarks
- GitHub Actions pipeline
- Artifact generation
- Slack notifications

### Future Roadmap
- Machine learning trend prediction
- Automated model recommendation
- Continuous performance monitoring

**Note**: Provides data-driven insights into AI model capabilities across diverse scenarios

## Interactive Performance Dashboard 🖥️

### Streamlit Visualization Platform

#### 📊 Dashboard Capabilities
- Real-time AI model performance tracking
- Interactive comparative visualizations
- Comprehensive performance metrics
- Historical trend analysis

#### 🔍 Key Visualization Features
- Model Response Time Comparison
- Token Generation Rate Analysis
- Performance Trends Over Time
- Detailed Error Rate Insights

#### 🚀 Quick Start
```bash
# Navigate to dashboard directory
cd dashboard

# Install dependencies
pip install -r requirements.txt

# Launch dashboard
streamlit run performance_dashboard.py
```

#### 💡 Advanced Insights
- Machine learning trend prediction
- Predictive model performance scoring
- Customizable visualization framework

**Note**: Requires performance metrics database generated by benchmarking workflow

## Performance Evaluation

### DeepSeek Performance Notebook
The `DeepSeek_Performance_Evaluation.ipynb` provides a comprehensive assessment of the DeepSeek-R1 model's capabilities:

#### Evaluation Metrics
- **Reasoning Performance**
  - Tests across different difficulty levels
  - Measures response time and token count
  - Includes easy, medium, and hard reasoning tasks

- **Coding Performance**
  - Evaluates code generation in multiple languages
  - Assesses response time and code complexity
  - Languages tested: Python, JavaScript, Rust

#### Visualization
- Bar charts comparing response times
- Performance metrics across different task types
- Insights into model's strengths and limitations

### How to Run
```bash
jupyter notebook notebooks/DeepSeek_Performance_Evaluation.ipynb
```

### Customization
- Easily extend test cases
- Add more programming languages
- Modify difficulty levels

### Key Insights
- Quantitative analysis of AI model performance
- Benchmark DeepSeek-R1's reasoning and coding abilities
- Provides a structured approach to model evaluation

## Full Performance Evaluation Notebook Content

### Note
For the most up-to-date and interactive version, please refer to the `notebooks/DeepSeek_Performance_Evaluation.ipynb` file in the repository.

```python
# DeepSeek-R1 Performance Evaluation Notebook

# Project Overview
# This notebook provides a comprehensive performance evaluation 
# of the DeepSeek-R1 AI model across various domains and test scenarios.

# Import required libraries
from openai import OpenAI
from dotenv import load_dotenv
import os
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(
    base_url="https://integrate.api.nvidia.com/v1",
    api_key=os.getenv('NVIDIA_API_KEY')
)

# Test Case 1: Reasoning Performance
def test_reasoning_performance(prompts):
    results = []
    for difficulty, prompt in prompts.items():
        start_time = time.time()
        response = client.chat.completions.create(
            model="deepseek-ai/deepseek-r1",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        end_time = time.time()
        
        results.append({
            'difficulty': difficulty,
            'prompt': prompt,
            'response': response.choices[0].message.content,
            'response_time': end_time - start_time,
            'token_count': len(response.choices[0].message.content.split())
        })
    
    return pd.DataFrame(results)

# Reasoning test prompts
reasoning_prompts = {
    'easy': "What is 15 * 7?",
    'medium': "If a train travels 120 miles in 2 hours, what is its speed?",
    'hard': "Solve this logic puzzle: A farmer has chickens and cows. The total number of heads is 50 and the total number of legs is 140. How many chickens and cows does the farmer have?"
}

# Run reasoning performance tests
reasoning_results = test_reasoning_performance(reasoning_prompts)
print(reasoning_results)

# Test Case 2: Coding Performance
def test_coding_performance(coding_tasks):
    results = []
    for language, task in coding_tasks.items():
        start_time = time.time()
        response = client.chat.completions.create(
            model="deepseek-ai/deepseek-r1",
            messages=[{"role": "user", "content": task}],
            max_tokens=500
        )
        end_time = time.time()
        
        results.append({
            'language': language,
            'task': task,
            'solution': response.choices[0].message.content,
            'response_time': end_time - start_time,
            'code_length': len(response.choices[0].message.content.split('\n'))
        })
    
    return pd.DataFrame(results)

# Coding tasks for different languages
coding_tasks = {
    'Python': "Write a function to calculate the Fibonacci sequence up to n terms",
    'JavaScript': "Create a function that checks if a string is a palindrome",
    'Rust': "Implement a basic bubble sort algorithm"
}

# Run coding performance tests
coding_results = test_coding_performance(coding_tasks)
print(coding_results)

# Visualization of Performance Metrics
plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
reasoning_results.plot(x='difficulty', y='response_time', kind='bar')
plt.title('Reasoning Task Response Time')
plt.xlabel('Difficulty Level')
plt.ylabel('Response Time (seconds)')

plt.subplot(1, 2, 2)
coding_results.plot(x='language', y='response_time', kind='bar')
plt.title('Coding Task Response Time')
plt.xlabel('Programming Language')
plt.ylabel('Response Time (seconds)')

plt.tight_layout()
plt.show()

# Performance Summary
# This notebook provides a comprehensive evaluation of the 
# DeepSeek-R1 model's performance across reasoning and coding tasks.

## Notebook Execution Notes
- Requires NVIDIA API Key
- Depends on environment variables
- Uses OpenAI client for model interaction
- Generates performance metrics and visualizations

## Key Components
- Python script for DeepSeek AI interaction
- Node.js script for DeepSeek AI interaction
- Bash cURL script for direct API interaction
- Jupyter Notebook for interactive exploration
- Flexible API key configuration

## Notes
- The scripts are designed to work with or without an API key
- Demonstrates model interaction in multiple languages and methods
- Supports streaming responses
- Provides multiple approaches to AI model interaction

## Acknowledgments
Thanks to the NVIDIA NIM AI Software Production Team and DeepSeek AI for providing this powerful reasoning model.
```

## Improvement Plan

### Performance Optimization
- **Objective**: Enhance the overall performance of the AI model.
- **Rationale**: Improved performance will lead to faster response times and better user experience.
- **Actions**:
  - Optimize the model's architecture for faster inference.
  - Implement caching mechanisms to reduce redundant computations.
  - Fine-tune hyperparameters for optimal performance.

### Code Refactoring
- **Objective**: Improve the codebase for better maintainability and readability.
- **Rationale**: Clean and well-structured code is easier to maintain and extend.
- **Actions**:
  - Refactor the existing code to follow best practices and coding standards.
  - Modularize the codebase to separate concerns and improve reusability.
  - Add comprehensive comments and documentation to the code.

### Additional Features
- **Objective**: Introduce new features to enhance the functionality of the project.
- **Rationale**: New features will provide more value to users and expand the project's capabilities.
- **Actions**:
  - Implement new visualization tools for better data analysis.
  - Add support for additional AI models and frameworks.
  - Develop user-friendly interfaces for easier interaction with the AI model.
