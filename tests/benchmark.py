import os
import json
import sqlite3
import time
from datetime import datetime
import plotly.graph_objects as go
import plotly.io as pio
import numpy as np
from dataclasses import dataclass, asdict
from typing import List, Dict, Any
from dotenv import load_dotenv
from openai import OpenAI
import anthropic  # Added for Claude support
import google.generativeai as palm  # Added for PaLM support

# Load environment variables
load_dotenv()

@dataclass
class ModelPerformanceMetrics:
    timestamp: str
    model_name: str
    total_queries: int
    avg_response_time: float
    median_response_time: float
    avg_token_generation_rate: float
    task_success_rate: float
    error_rate: float
    total_execution_time: float

class AdvancedModelBenchmark:
    def __init__(self, models: List[Dict[str, Any]]):
        """Initialize benchmark with multiple models and their configurations"""
        self.models = models
        self.clients = self._initialize_clients()
        
        # Expanded real-world use case scenarios
        self.scenarios = [
            {
                "name": "Technical Documentation",
                "prompt": "Generate a comprehensive technical documentation for a RESTful API with authentication and rate limiting.",
                "complexity": "high"
            },
            {
                "name": "Code Generation",
                "prompt": "Create a Python class for managing a distributed task queue with error handling and retry mechanisms.",
                "complexity": "very high"
            },
            {
                "name": "Complex Reasoning",
                "prompt": "Analyze the potential economic, social, and ethical implications of AI-driven automation in various industry sectors over the next decade.",
                "complexity": "extreme"
            },
            {
                "name": "Multilingual Technical Translation",
                "prompt": "Translate a complex academic paper about quantum machine learning from English to Mandarin, maintaining technical precision.",
                "complexity": "high"
            }
        ]
        
        # Ensure reports directory exists
        os.makedirs('reports', exist_ok=True)
        
        # Initialize SQLite database
        self._initialize_database()
    
    def _initialize_clients(self) -> Dict[str, Any]:
        """Initialize clients for different models"""
        clients = {}
        for model_config in self.models:
            model_type = model_config['type']
            
            if model_type == 'openai':
                clients[model_config['name']] = OpenAI(
                    api_key=os.getenv('OPENAI_API_KEY')
                )
            elif model_type == 'anthropic':
                clients[model_config['name']] = anthropic.Anthropic(
                    api_key=os.getenv('ANTHROPIC_API_KEY')
                )
            elif model_type == 'google':
                palm.configure(api_key=os.getenv('GOOGLE_API_KEY'))
                clients[model_config['name']] = palm
            elif model_type == 'deepseek':
                clients[model_config['name']] = OpenAI(
                    base_url="https://integrate.api.nvidia.com/v1",
                    api_key=os.getenv('NVIDIA_API_KEY')
                )
        
        return clients
    
    def _initialize_database(self):
        """Create SQLite database for performance tracking"""
        self.conn = sqlite3.connect('reports/model_performance.db')
        cursor = self.conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS performance_metrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            model_name TEXT,
            total_queries INTEGER,
            avg_response_time REAL,
            median_response_time REAL,
            avg_token_generation_rate REAL,
            task_success_rate REAL,
            error_rate REAL,
            total_execution_time REAL
        )
        ''')
        self.conn.commit()
    
    def _log_performance_to_database(self, metrics: ModelPerformanceMetrics):
        """Log performance metrics to SQLite database"""
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO performance_metrics (
            timestamp, model_name, total_queries, avg_response_time, 
            median_response_time, avg_token_generation_rate, 
            task_success_rate, error_rate, total_execution_time
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            metrics.timestamp, metrics.model_name, metrics.total_queries,
            metrics.avg_response_time, metrics.median_response_time,
            metrics.avg_token_generation_rate, metrics.task_success_rate,
            metrics.error_rate, metrics.total_execution_time
        ))
        self.conn.commit()
    
    def _generate_performance_visualization(self, all_metrics: List[ModelPerformanceMetrics]):
        """Create interactive Plotly visualizations"""
        # Response Time Comparison
        fig_response_time = go.Figure()
        for metrics in all_metrics:
            fig_response_time.add_trace(go.Bar(
                x=[metrics.model_name],
                y=[metrics.avg_response_time],
                name='Avg Response Time (ms)'
            ))
        fig_response_time.update_layout(
            title='Average Response Time Across Models',
            yaxis_title='Response Time (ms)'
        )
        pio.write_html(fig_response_time, file='reports/response_time_comparison.html')
        
        # Token Generation Rate
        fig_token_rate = go.Figure()
        for metrics in all_metrics:
            fig_token_rate.add_trace(go.Bar(
                x=[metrics.model_name],
                y=[metrics.avg_token_generation_rate],
                name='Avg Token Generation Rate'
            ))
        fig_token_rate.update_layout(
            title='Token Generation Rate Across Models',
            yaxis_title='Tokens per Second'
        )
        pio.write_html(fig_token_rate, file='reports/token_generation_rate.html')
    
    def run_benchmark(self) -> List[ModelPerformanceMetrics]:
        """Run comprehensive benchmarking across models and scenarios"""
        all_metrics = []
        timestamp = datetime.now().isoformat()
        
        for model_config in self.models:
            model_name = model_config['name']
            model_results = {
                "response_times": [],
                "success_count": 0,
                "error_count": 0,
                "total_time": 0
            }
            
            for scenario in self.scenarios:
                try:
                    result = self._evaluate_model(model_name, scenario)
                    model_results['response_times'].extend(result['response_times'])
                    model_results['success_count'] += result['success_count']
                    model_results['error_count'] += result['error_count']
                    model_results['total_time'] += result['total_time']
                except Exception as e:
                    print(f"Error evaluating {model_name}: {e}")
                    model_results['error_count'] += len(self.scenarios)
            
            metrics = ModelPerformanceMetrics(
                timestamp=timestamp,
                model_name=model_name,
                total_queries=len(self.scenarios),
                avg_response_time=np.mean(model_results['response_times']) if model_results['response_times'] else 0,
                median_response_time=np.median(model_results['response_times']) if model_results['response_times'] else 0,
                avg_token_generation_rate=len(model_results['response_times']) / model_results['total_time'] if model_results['total_time'] > 0 else 0,
                task_success_rate=(model_results['success_count'] / len(self.scenarios)) * 100,
                error_rate=(model_results['error_count'] / len(self.scenarios)) * 100,
                total_execution_time=model_results['total_time']
            )
            
            all_metrics.append(metrics)
            self._log_performance_to_database(metrics)
        
        # Generate visualizations
        self._generate_performance_visualization(all_metrics)
        
        return all_metrics
    
    def _evaluate_model(self, model_name: str, scenario: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate a specific model's performance on a scenario"""
        # Implementation similar to previous version, adapted for multiple model types
        # Would include specific logic for each model type's API call
        pass

def main():
    models = [
        {"name": "gpt-3.5-turbo", "type": "openai"},
        {"name": "deepseek-r1", "type": "deepseek"},
        {"name": "claude-2", "type": "anthropic"},
        {"name": "palm-2", "type": "google"}
    ]
    
    benchmark = AdvancedModelBenchmark(models)
    results = benchmark.run_benchmark()
    
    # Generate comprehensive JSON report
    with open('reports/comprehensive_benchmark_report.json', 'w') as f:
        json.dump([asdict(result) for result in results], f, indent=2)

if __name__ == "__main__":
    main()
