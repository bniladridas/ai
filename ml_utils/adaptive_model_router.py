import os
import json
import sqlite3
from datetime import datetime
from typing import Dict, List, Any
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

class AdaptiveModelSelector:
    """
    Intelligent model selection framework that dynamically chooses 
    the most appropriate AI model based on task characteristics 
    and historical performance.
    """
    
    def __init__(self, performance_db_path='reports/model_performance.db'):
        """
        Initialize the adaptive model selector with performance database.
        
        :param performance_db_path: Path to SQLite performance tracking database
        """
        self.performance_db_path = performance_db_path
        self.models = [
            'gpt-3.5-turbo', 
            'deepseek-r1', 
            'claude-2', 
            'palm-2'
        ]
        
        # Task complexity mapping
        self.task_complexity_weights = {
            'low': 0.2,
            'medium': 0.5,
            'high': 0.8,
            'extreme': 1.0
        }
    
    def _load_historical_performance(self) -> pd.DataFrame:
        """
        Load historical performance metrics from SQLite database.
        
        :return: DataFrame with performance metrics
        """
        try:
            conn = sqlite3.connect(self.performance_db_path)
            df = pd.read_sql_query("SELECT * FROM performance_metrics", conn)
            conn.close()
            return df
        except Exception as e:
            print(f"Error loading performance data: {e}")
            return pd.DataFrame()
    
    def _calculate_model_score(self, model_metrics: Dict[str, float], task_complexity: str) -> float:
        """
        Calculate a comprehensive score for a model based on various metrics.
        
        :param model_metrics: Dictionary of model performance metrics
        :param task_complexity: Complexity level of the task
        :return: Composite performance score
        """
        complexity_weight = self.task_complexity_weights.get(task_complexity, 0.5)
        
        # Weighted scoring components
        response_time_score = 1 / (model_metrics.get('avg_response_time', 1000))
        token_efficiency_score = model_metrics.get('avg_token_generation_rate', 50) / 100
        success_rate_score = model_metrics.get('task_success_rate', 50) / 100
        error_rate_penalty = 1 - (model_metrics.get('error_rate', 10) / 100)
        
        # Composite score calculation
        composite_score = (
            (0.3 * response_time_score) +
            (0.3 * token_efficiency_score) +
            (0.2 * success_rate_score) +
            (0.2 * error_rate_penalty)
        ) * complexity_weight
        
        return composite_score
    
    def select_optimal_model(self, task_description: str, task_complexity: str = 'medium') -> str:
        """
        Select the most appropriate model for a given task.
        
        :param task_description: Natural language description of the task
        :param task_complexity: Complexity level of the task
        :return: Recommended model name
        """
        historical_data = self._load_historical_performance()
        
        if historical_data.empty:
            # Fallback to random selection if no historical data
            return np.random.choice(self.models)
        
        # Calculate scores for each model
        model_scores = {}
        for model in self.models:
            model_metrics = historical_data[historical_data['model_name'] == model].iloc[-1].to_dict()
            model_scores[model] = self._calculate_model_score(model_metrics, task_complexity)
        
        # Select model with highest score
        recommended_model = max(model_scores, key=model_scores.get)
        
        # Log model selection
        self._log_model_selection(recommended_model, task_description, task_complexity)
        
        return recommended_model
    
    def _log_model_selection(self, selected_model: str, task_description: str, task_complexity: str):
        """
        Log model selection details for future analysis.
        
        :param selected_model: Name of the selected model
        :param task_description: Task description
        :param task_complexity: Task complexity level
        """
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'selected_model': selected_model,
            'task_description': task_description,
            'task_complexity': task_complexity
        }
        
        # Ensure logs directory exists
        os.makedirs('logs', exist_ok=True)
        
        # Append to model selection log
        log_file = 'logs/model_selection.jsonl'
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    def visualize_model_performance(self):
        """
        Create interactive visualizations of model performance.
        Generates HTML reports in the reports directory.
        """
        historical_data = self._load_historical_performance()
        
        if historical_data.empty:
            print("No performance data available for visualization.")
            return
        
        # Response Time Comparison
        fig_response_time = go.Figure()
        for model in self.models:
            model_data = historical_data[historical_data['model_name'] == model]
            fig_response_time.add_trace(go.Bar(
                x=[model],
                y=[model_data['avg_response_time'].mean()],
                name='Avg Response Time'
            ))
        fig_response_time.update_layout(
            title='Average Model Response Time',
            yaxis_title='Response Time (ms)'
        )
        pio.write_html(fig_response_time, file='reports/model_response_time.html')
        
        # Token Generation Rate
        fig_token_rate = go.Figure()
        for model in self.models:
            model_data = historical_data[historical_data['model_name'] == model]
            fig_token_rate.add_trace(go.Bar(
                x=[model],
                y=[model_data['avg_token_generation_rate'].mean()],
                name='Avg Token Generation Rate'
            ))
        fig_token_rate.update_layout(
            title='Average Token Generation Rate',
            yaxis_title='Tokens per Second'
        )
        pio.write_html(fig_token_rate, file='reports/token_generation_rate.html')

def main():
    """
    Demonstration of Adaptive Model Selector
    """
    selector = AdaptiveModelSelector()
    
    # Example task scenarios
    tasks = [
        {"description": "Generate technical documentation", "complexity": "medium"},
        {"description": "Complex code generation", "complexity": "high"},
        {"description": "Multilingual translation", "complexity": "extreme"},
        {"description": "Simple text summarization", "complexity": "low"}
    ]
    
    print("🤖 Adaptive Model Selector Demonstration 🤖")
    for task in tasks:
        recommended_model = selector.select_optimal_model(
            task['description'], 
            task['complexity']
        )
        print(f"Task: {task['description']} (Complexity: {task['complexity']})")
        print(f"Recommended Model: {recommended_model}\n")
    
    # Generate performance visualizations
    selector.visualize_model_performance()

if __name__ == "__main__":
    main()
