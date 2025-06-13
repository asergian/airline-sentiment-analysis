"""Sentiment analysis prompts for analyzing airline-related tweets.

This module provides different prompt variants for analyzing sentiment in tweets,
with varying levels of context and guidance.
"""

def sentiment_prompt_v1_basic(tweet: str, airline: str) -> str:
    """Basic sentiment analysis prompt.
    
    Args:
        tweet: The tweet to analyze
        airline: The airline to analyze sentiment for
        
    Returns:
        Formatted prompt string
    """
    return f'''What is the sentiment of this tweet toward {airline}?
    
    Tweet: "{tweet}"
    Airline: {airline}
    
    Return as JSON: {{"sentiment": "positive"}} or {{"sentiment": "negative"}} or {{"sentiment": "neutral"}}'''

def sentiment_prompt_v2_context_aware(tweet: str, airline: str) -> str:
    """Context-aware prompt that handles sarcasm and mixed sentiment.
    
    Args:
        tweet: The tweet to analyze
        airline: The airline to analyze sentiment for
        
    Returns:
        Formatted prompt string
    """
    return f'''Analyze the sentiment of this tweet toward {airline}. Considerations:
    
    - Infer the overall sentiment of the tweet
    - Consider customer satisfaction and underlying sarcasm
    - Pay attention to sentiment indicators such as emojis, hashtags, etc.
    - If no airlines mentioned, return "neutral"
    - If on the border of neutral/negative, lean on neutral unless overall sentiment is negative
    
    Tweet: "{tweet}"
    Airline: {airline}
    
    Focus on the customer's actual satisfaction with {airline}.
    
    Return as JSON: {{"sentiment": "positive"}} or {{"sentiment": "negative"}} or {{"sentiment": "neutral"}}'''

# Dictionary mapping experiment names to prompt functions
SENTIMENT_PROMPT_FUNCS = {
    "sentiment_v1_basic": sentiment_prompt_v1_basic,
    "sentiment_v2_context_aware": sentiment_prompt_v2_context_aware,
} 