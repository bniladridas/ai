import os
import sys
import json
import pytest
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

class TestDeepSeekAPIResponses:
    def setup_method(self):
        """Initialize OpenAI client with NVIDIA endpoint"""
        self.client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=os.getenv('NVIDIA_API_KEY')
        )
    
    def validate_response(self, response):
        """Common response validation checks"""
        assert response is not None, "Response should not be None"
        assert hasattr(response, 'choices'), "Response missing choices"
        assert len(response.choices) > 0, "No choices in response"
        
        message = response.choices[0].message
        assert message is not None, "Message should not be None"
        assert hasattr(message, 'content'), "Message missing content"
        assert message.content is not None, "Message content should not be None"
    
    def test_reasoning_query(self):
        """Test reasoning capability"""
        reasoning_prompt = "What is 15 * 7?"
        
        response = self.client.chat.completions.create(
            model="deepseek-ai/deepseek-r1",
            messages=[{"role": "user", "content": reasoning_prompt}],
            max_tokens=50
        )
        
        self.validate_response(response)
        
        # Additional reasoning-specific checks
        content = response.choices[0].message.content
        assert len(content.split()) > 0, "Response should contain words"
        assert '105' in content, "Expected numeric result in reasoning response"
    
    def test_coding_query(self):
        """Test coding generation capability"""
        coding_prompt = "Write a Python function to calculate factorial"
        
        response = self.client.chat.completions.create(
            model="deepseek-ai/deepseek-r1",
            messages=[{"role": "user", "content": coding_prompt}],
            max_tokens=200
        )
        
        self.validate_response(response)
        
        # Additional coding-specific checks
        content = response.choices[0].message.content
        assert 'def factorial' in content, "Expected function definition"
        assert 'return' in content, "Expected return statement in function"
    
    def test_multilingual_query(self):
        """Test multilingual response capability"""
        multilingual_prompts = [
            {"lang": "French", "prompt": "Bonjour, comment ça va?"},
            {"lang": "Spanish", "prompt": "¿Cómo estás hoy?"},
            {"lang": "German", "prompt": "Wie geht es dir?"}
        ]
        
        for lang_data in multilingual_prompts:
            response = self.client.chat.completions.create(
                model="deepseek-ai/deepseek-r1",
                messages=[{"role": "user", "content": lang_data['prompt']}],
                max_tokens=100
            )
            
            self.validate_response(response)
            
            # Check response is not just echoing the input
            content = response.choices[0].message.content
            assert content.lower() != lang_data['prompt'].lower(), f"Response should not be identical to {lang_data['lang']} input"
    
    def test_token_limit(self):
        """Test response adheres to token limits"""
        long_prompt = "Explain the concept of quantum entanglement in great detail, covering its historical development, key experiments, and potential technological applications."
        
        response = self.client.chat.completions.create(
            model="deepseek-ai/deepseek-r1",
            messages=[{"role": "user", "content": long_prompt}],
            max_tokens=500
        )
        
        self.validate_response(response)
        
        # Check token limit
        content = response.choices[0].message.content
        assert len(content.split()) <= 500, "Response exceeds specified token limit"

if __name__ == "__main__":
    pytest.main([__file__])
