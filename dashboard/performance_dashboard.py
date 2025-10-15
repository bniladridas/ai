import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sqlite3
from datetime import datetime, timedelta

class AIModelPerformanceDashboard:
    def __init__(self, db_path='../tests/reports/model_performance.db'):
        self.conn = sqlite3.connect(db_path)
        self.load_performance_data()
    
    def load_performance_data(self):
        """Load performance metrics from SQLite database"""
        self.df = pd.read_sql_query(
            "SELECT * FROM performance_metrics ORDER BY timestamp", 
            self.conn
        )
        self.df['timestamp'] = pd.to_datetime(self.df['timestamp'])
    
    def render_overview_section(self):
        """Create overview section with key performance insights"""
        st.title("🤖 AI Model Performance Dashboard")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Total Models Tracked", 
                len(self.df['model_name'].unique())
            )
        
        with col2:
            st.metric(
                "Average Task Success Rate",
                f"{self.df['task_success_rate'].mean():.2f}%"
            )
        
        with col3:
            st.metric(
                "Median Response Time",
                f"{self.df['avg_response_time'].median():.2f} ms"
            )
    
    def render_model_comparison(self):
        """Create comparative visualizations across models"""
        st.header("🔍 Model Performance Comparison")
        
        # Response Time Comparison
        fig_response_time = px.bar(
            self.df, 
            x='model_name', 
            y='avg_response_time',
            title='Average Response Time by Model',
            labels={'avg_response_time': 'Response Time (ms)'}
        )
        st.plotly_chart(fig_response_time)
        
        # Token Generation Rate
        fig_token_rate = px.bar(
            self.df, 
            x='model_name', 
            y='avg_token_generation_rate',
            title='Token Generation Rate by Model',
            labels={'avg_token_generation_rate': 'Tokens per Second'}
        )
        st.plotly_chart(fig_token_rate)
    
    def render_historical_trends(self):
        """Show performance trends over time"""
        st.header("📈 Historical Performance Trends")
        
        # Time series for each model
        models = self.df['model_name'].unique()
        
        for metric in ['avg_response_time', 'task_success_rate']:
            fig = go.Figure()
            for model in models:
                model_data = self.df[self.df['model_name'] == model]
                fig.add_trace(go.Scatter(
                    x=model_data['timestamp'], 
                    y=model_data[metric],
                    mode='lines+markers',
                    name=model
                ))
            
            fig.update_layout(
                title=f'{metric.replace("_", " ").title()} Over Time',
                xaxis_title='Timestamp',
                yaxis_title=metric.replace('_', ' ').title()
            )
            st.plotly_chart(fig)
    
    def render_error_analysis(self):
        """Detailed error rate and performance analysis"""
        st.header("⚠️ Error Rate and Performance Insights")
        
        fig_error_rate = px.bar(
            self.df, 
            x='model_name', 
            y='error_rate',
            title='Error Rate by Model',
            labels={'error_rate': 'Error Rate (%)'}
        )
        st.plotly_chart(fig_error_rate)
    
    def run(self):
        """Main dashboard rendering method"""
        self.render_overview_section()
        self.render_model_comparison()
        self.render_historical_trends()
        self.render_error_analysis()

def main():
    dashboard = AIModelPerformanceDashboard()
    dashboard.run()

if __name__ == "__main__":
    main()
