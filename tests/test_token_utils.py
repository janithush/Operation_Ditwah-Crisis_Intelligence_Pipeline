# tests/test_token_utils.py
from utils.token_utils import count_messages_tokens

def test_count_messages_tokens_basic():
    # 1. Arrange
    messages = [{"role": "user", "content": "Help us, we are stuck in the flood in Matara!"}]
    
    # 2. Act
    token_count = count_messages_tokens(messages, provider="gemini", model="gemini-2.5-flash")
    
    # 3. Assert
    assert isinstance(token_count, dict)
    
    assert "estimated_total" in token_count
    
    assert token_count["estimated_total"] > 0

def test_count_messages_tokens_empty():
    messages = [{"role": "user", "content": ""}]
    token_count = count_messages_tokens(messages, provider="gemini", model="gemini-2.5-flash")
    
    assert isinstance(token_count, dict)
    assert "estimated_total" in token_count