import os
import time
import statistics
import pytest
import concurrent.futures
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

class TestDeepSeekPerformanceAndRateLimiting:
    def setup_method(self):
        """Initialize OpenAI client with NVIDIA endpoint"""
        self.client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=os.getenv('NVIDIA_API_KEY')
        )
        
        # Performance thresholds
        self.PERFORMANCE_THRESHOLDS = {
            'max_response_time_ms': 5000,  # 5 seconds
            'avg_response_time_ms': 2000,  # 2 seconds
            'max_tokens_per_second': 100,
            'concurrent_requests': 10
        }
    
    def generate_response(self, prompt):
        """Generate response and measure performance"""
        start_time = time.time()
        response = self.client.chat.completions.create(
            model="deepseek-ai/deepseek-r1",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200
        )
        end_time = time.time()
        
        return {
            'response': response,
            'response_time_ms': (end_time - start_time) * 1000,
            'token_count': len(response.choices[0].message.content.split())
        }
    
    def test_individual_response_performance(self):
        """Test performance of individual API calls"""
        prompts = [
            "Explain quantum computing in simple terms",
            "Write a short Python function to reverse a string",
            "Describe the impact of AI on modern society"
        ]
        
        response_times = []
        token_counts = []
        
        for prompt in prompts:
            result = self.generate_response(prompt)
            
            # Validate individual response time
            assert result['response_time_ms'] < self.PERFORMANCE_THRESHOLDS['max_response_time_ms'], \
                f"Response time exceeded threshold: {result['response_time_ms']} ms"
            
            response_times.append(result['response_time_ms'])
            token_counts.append(result['token_count'])
        
        # Check average response time
        avg_response_time = statistics.mean(response_times)
        assert avg_response_time < self.PERFORMANCE_THRESHOLDS['avg_response_time_ms'], \
            f"Average response time too high: {avg_response_time} ms"
    
    def test_concurrent_request_performance(self):
        """Test performance under concurrent requests"""
        prompts = [
            "Explain machine learning algorithms",
            "Describe blockchain technology",
            "Compare functional and object-oriented programming",
            "Discuss the future of renewable energy",
            "Explain the basics of cryptography"
        ]
        
        def make_request(prompt):
            return self.generate_response(prompt)
        
        # Simulate concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.PERFORMANCE_THRESHOLDS['concurrent_requests']) as executor:
            futures = [executor.submit(make_request, prompt) for prompt in prompts]
            
            response_times = []
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                response_times.append(result['response_time_ms'])
                
                # Validate individual concurrent response
                assert result['response_time_ms'] < self.PERFORMANCE_THRESHOLDS['max_response_time_ms'], \
                    f"Concurrent response time exceeded threshold: {result['response_time_ms']} ms"
        
        # Additional concurrent performance checks
        assert len(response_times) == len(prompts), "Not all concurrent requests completed"
    
    def test_rate_limiting_behavior(self):
        """Test API's rate limiting and graceful handling"""
        # Rapid successive requests to test rate limiting
        excessive_requests = 50
        response_times = []
        
        for _ in range(excessive_requests):
            try:
                result = self.generate_response("Short test prompt")
                response_times.append(result['response_time_ms'])
                time.sleep(0.1)  # Small delay between requests
            except Exception as e:
                # Check for rate limit specific exceptions
                assert "rate limit" in str(e).lower(), "Unexpected error during rate limit test"
        
        # Validate response times don't degrade significantly
        if response_times:
            max_rate_limited_time = max(response_times)
            assert max_rate_limited_time < self.PERFORMANCE_THRESHOLDS['max_response_time_ms'] * 1.5, \
                "Response times degraded significantly under load"
    
    def test_token_generation_rate(self):
        """Validate token generation rate"""
        prompt = "Generate a detailed explanation of a complex topic"
        result = self.generate_response(prompt)
        
        # Calculate tokens per second
        tokens_per_second = result['token_count'] / (result['response_time_ms'] / 1000)
        
        assert tokens_per_second <= self.PERFORMANCE_THRESHOLDS['max_tokens_per_second'], \
            f"Token generation rate too high: {tokens_per_second} tokens/second"

if __name__ == "__main__":
    pytest.main([__file__])
