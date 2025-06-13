"""Combined entity extraction and sentiment analysis prompts.

This module provides prompts for performing both entity extraction and sentiment analysis
in a single step, including both single-tweet and batch processing variants.
"""

import json
from typing import List

def combined_prompt(tweet: str) -> str:
    """Generate a prompt for combined entity extraction and sentiment analysis on a single tweet.
    
    Args:
        tweet: The tweet to analyze
        
    Returns:
        Formatted prompt string
    """
    return f'''Extract airline names using official names then analyze the sentiment of this tweet toward the mentioned airline(s).
    
    STEP 1 - Extract Airlines:

    Examples:
    - "@AmericanAir delayed again!" → "American Airlines"
    - "USAirways" → "US Airways"  
    - "Flying United and Southwest today " → "United Airlines, Southwest Airlines"
    - "Jet Blue" → "JetBlue Airways"

    STEP 2 - Analyze Sentiment:
    Analyze the sentiment of this tweet toward the mentioned airline(s). Considerations:
    - Infer the overall sentiment of the tweet
    - Consider customer satisfaction and underlying sarcasm
    - Pay attention to sentiment indicators such as emojis, hashtags, etc.
    - If on the border of neutral/negative, lean on neutral unless overall sentiment is negative

    Sentiment can only return as positive, negative, or neutral.
    
    Focus on the customer's actual satisfaction with the airline(s).
    
    Output as JSON just the results. Example output:
    {{
        "airlines": ["Official Airline Name", "Another Airline"],
        "sentiment": "positive"
    }}
    
    If no airlines mentioned, return: {{"airlines": [], "sentiment": "negative"}}
    
    Tweet to analyze: "{tweet}"'''

def combined_prompt_batch(tweets: List[str]) -> str:
    """Generate a prompt for batch processing multiple tweets.
    
    Args:
        tweets: List of tweets to analyze
        
    Returns:
        Formatted prompt string for batch analysis
    """
    tweets_text = "\n".join([f"{i+1}. {tweet}" for i, tweet in enumerate(tweets)])
    
    return f'''For each tweet, extract airline names using official names then analyze the sentiment of these tweets toward the mentioned airline(s).

STEP 1 - Extract Airlines:

Examples:
- "@AmericanAir delayed again!" → "American Airlines"
- "USAirways" → "US Airways"  
- "Flying United and Southwest today " → "United Airlines, Southwest Airlines"
- "Jet Blue" → "JetBlue Airways"

STEP 2 - Analyze Sentiment:
Analyze the sentiment of each tweet toward the mentioned airline(s). Considerations:
- Infer the overall sentiment of the tweet
- Consider customer satisfaction and underlying sarcasm
- Pay attention to sentiment indicators such as emojis, hashtags, etc.
- If on the border of neutral/negative, lean on neutral unless overall sentiment is negative

Sentiment can only return as positive, negative, or neutral.

Focus on the customer's actual satisfaction with the airline(s).

Tweets to analyze:
{tweets_text}

Output as JSON array with results for each tweet. Example output:
[
    {{
        "tweet": "I love flying with @Delta! Great service!",
        "airlines": ["Delta Airlines"],
        "sentiment": "positive"
    }},
    {{
        "tweet": "Terrible experience with @United",
        "airlines": ["United Airlines"],
        "sentiment": "negative"
    }}
]

If no airlines mentioned in a tweet, include that tweet with: {{"airlines": [], "sentiment": "negative"}}'''

# Dictionary mapping experiment names to prompt functions
COMBINED_PROMPT_FUNCS = {
    "combined_v1": combined_prompt,
    "combined_batch_v1": combined_prompt_batch
} 