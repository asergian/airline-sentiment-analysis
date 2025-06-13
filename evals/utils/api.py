"""API utilities for making calls to language models.

This module provides functions for interacting with language model APIs,
including handling API calls and responses.
"""

import openai

MODEL = "gpt-4o-mini"
client = openai.OpenAI()

def call_api(prompt: str, max_tokens: int = 150) -> str:
    """Make an API call to the language model.
    
    Args:
        prompt: The prompt to send to the model
        max_tokens: Maximum number of tokens in the response
        
    Returns:
        The model's response as a string, stripped of whitespace
    """
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"API Error: {e}")
        return "" 