AI Model Benchmarking and Selection Tool

This repository provides a lightweight, Python-based toolkit for benchmarking and comparing large language models across multiple providers, including OpenAI, Anthropic, Google, and NVIDIA. It is intended for developers who want a repeatable way to evaluate models using consistent tasks and measurable criteria, such as latency, success rate, and task difficulty, in order to select an appropriate model for a given use case.

The tool assumes familiarity with Python, command-line workflows, YAML configuration files, and the use of third‑party model APIs. You are expected to supply valid API credentials for any providers you benchmark.

News

Recent dependency changes were made to improve compatibility across Python versions. Version pins for numpy, pandas, scikit-learn, and matplotlib were removed because pinned versions (for example, numpy==1.26.0) required Python <3.13 and caused installation failures on newer Python releases such as Python 3.14. Allowing the latest compatible versions ensures broader compatibility without conflicts.

Weights & Biases support was removed due to protobuf import errors encountered in virtual environments. As a result, the codebase no longer depends on wandb.

Requirements

* Python 3.10 or newer
* pip
* API keys for the model providers you intend to benchmark, exposed via environment variables or a .env file

Installation

Clone the repository:

```
cd $HOME && git clone <repo-url>
cd ai
```

Install dependencies:

```
pip install -r requirements.txt
```

Model Configuration

Models are defined in `config/benchmark.yaml`. Each entry specifies the model name, provider type, and a short description. The names must match the identifiers expected by the corresponding provider integration.

Example:

```yaml
models:
  - name: new-model
    type: provider
    description: new description
```

Verify Configuration

Before running benchmarks, validate your configuration:

```
python -m utils.validate_data
```

This step checks the benchmark.yaml for required model fields.

Start Benchmarking

Basic Benchmark

Run a benchmark across all configured models:

```
python cli.py benchmark
```

Each model is evaluated on the same tasks, and aggregate metrics are reported.

Model Comparison

Compare two specific models on a focused task and complexity level:

```
python cli.py compare gpt-4o claude-3-5-sonnet --task "code generation" --complexity high
```

Custom Configuration

Benchmark behavior can be adjusted in `config/benchmark.yaml`.

Key parameters:

* `models`: list of models to benchmark
* `batch_size`: number of tasks per batch
* `eval_freq`: evaluation frequency
* `log_freq`: logging frequency

Dashboard

A Streamlit dashboard is provided to visualize benchmark results:

```
streamlit run dashboard/dashboard.py
```

Examples

Basic Benchmark

```
python cli.py benchmark
```

Example output:

```
benchmark results:
gpt-4o: 2.10s, 85.0% success
deepseek-r1: 1.80s, 92.0% success
...
```

Model Comparison

```
python cli.py compare gpt-4o gemini-2.0-flash-exp --task "math reasoning" --complexity extreme
```

Testing

Run the test suite:

```
pytest
```

FAQ

* How do I add a new model? Update `config/benchmark.yaml` with the model details.
* What metrics are used? Response time and task success rate, as implemented in the evaluation code.
* How are API limits handled? Provider integrations include basic rate limiting to reduce request failures.

License

Apache 2.0