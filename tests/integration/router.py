import os
import sqlite3
import tempfile
from unittest.mock import MagicMock, patch

import pandas as pd

from ml.router import AdaptiveModelSelector


class TestAdaptiveModelSelector:
    def setup_method(self):
        self.temp_db = tempfile.NamedTemporaryFile(delete=False)
        self.temp_db.close()
        self.selector = AdaptiveModelSelector(self.temp_db.name)

    def teardown_method(self):
        os.unlink(self.temp_db.name)

    def test_init(self):
        assert len(self.selector.models) == 4
        assert "gpt-4o" in self.selector.models
        assert "deepseek-r1" in self.selector.models
        assert self.selector.task_complexity_weights["low"] == 0.2
        assert self.selector.task_complexity_weights["extreme"] == 1.0

    def test_load_historical_performance_empty_db(self):
        df = self.selector._load_historical_performance()
        assert df.empty

    def test_load_historical_performance_with_data(self):
        conn = sqlite3.connect(self.temp_db.name)
        conn.execute("""
            CREATE TABLE performance_metrics (
                timestamp TEXT, model_name TEXT, total_queries INTEGER,
                avg_response_time REAL, median_response_time REAL,
                avg_token_generation_rate REAL, task_success_rate REAL,
                error_rate REAL, total_execution_time REAL
            )
        """)
        conn.execute("""
            INSERT INTO performance_metrics VALUES
            ('2024-01-01', 'gpt-4o', 10, 1.5, 1.4, 50.0, 95.0, 5.0, 15.0)
        """)
        conn.commit()
        conn.close()

        df = self.selector._load_historical_performance()
        assert not df.empty
        assert len(df) == 1
        assert df.iloc[0]["model_name"] == "gpt-4o"

    def test_calculate_model_score(self):
        metrics = {
            "avg_response_time": 1000.0,
            "avg_token_generation_rate": 60.0,
            "task_success_rate": 90.0,
            "error_rate": 10.0,
        }

        score = self.selector._calculate_model_score(metrics, "medium")
        assert isinstance(score, float)
        assert score > 0

    def test_select_optimal_model_no_historical_data(self):
        with patch("numpy.random.choice", return_value="gpt-4o"):
            model = self.selector.select_optimal_model("test task")
            assert model == "gpt-4o"

    def test_select_optimal_model_with_data(self):
        # Create mock historical data
        mock_df = pd.DataFrame(
            {
                "model_name": ["gpt-4o", "deepseek-r1", "gpt-4o"],
                "avg_response_time": [1000, 1500, 1200],
                "avg_token_generation_rate": [60, 40, 55],
                "task_success_rate": [95, 85, 90],
                "error_rate": [5, 15, 10],
            }
        )

        with patch.object(self.selector, "_load_historical_performance", return_value=mock_df):
            model = self.selector.select_optimal_model("test task", "medium")
            assert model in self.selector.models

    @patch("builtins.open")
    @patch("os.makedirs")
    def test_log_model_selection(self, mock_makedirs, mock_open):
        mock_file = MagicMock()
        mock_open.return_value.__enter__.return_value = mock_file

        self.selector._log_model_selection("gpt-4o", "test task", "medium")

        mock_open.assert_called_once()
        mock_file.write.assert_called_once()
        written_data = mock_file.write.call_args[0][0]
        assert "gpt-4o" in written_data
        assert "test task" in written_data

    def test_task_complexity_weights(self):
        assert self.selector.task_complexity_weights["low"] == 0.2
        assert self.selector.task_complexity_weights["high"] == 0.8

        # Test default complexity
        score_low = self.selector._calculate_model_score(
            {
                "avg_response_time": 1000.0,
                "avg_token_generation_rate": 50.0,
                "task_success_rate": 80.0,
                "error_rate": 20.0,
            },
            "low",
        )

        score_high = self.selector._calculate_model_score(
            {
                "avg_response_time": 1000.0,
                "avg_token_generation_rate": 50.0,
                "task_success_rate": 80.0,
                "error_rate": 20.0,
            },
            "high",
        )

        assert score_high > score_low  # Higher complexity should give higher score

    def test_model_list_completeness(self):
        expected_models = [
            "gpt-4o",
            "deepseek-r1",
            "claude-3-5-sonnet-20241022",
            "gemini-2.0-flash-exp",
        ]
        assert set(self.selector.models) == set(expected_models)
