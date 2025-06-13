"""Entity extraction prompts for identifying airline mentions in tweets.

This module provides different prompt variants for extracting airline names from tweets,
with varying levels of detail and examples.
"""

def prompt_entity_v1(tweet: str) -> str:
    """Simple entity extraction prompt.
    
    Args:
        tweet: The tweet to analyze
        
    Returns:
        Formatted prompt string
    """
    return f'''Extract all airline names mentioned in this tweet.
    
    Tweet: "{tweet}"\n\n
    
    Return as JSON: {{"airlines": ["Airline Name 1", "Airline Name 2"]}}
    If no airlines mentioned, return: {{"airlines": []}}'''

def prompt_entity_v2_standardized(tweet: str) -> str:
    """Prompt with standardized official names.
    
    Args:
        tweet: The tweet to analyze
        
    Returns:
        Formatted prompt string
    """
    return f'''Extract airline names and return using these EXACT official names:
    
    Official Names to Use:
    - American Airlines
    - United Airlines
    - Southwest Airlines
    - US Airways
    - JetBlue Airways
    - Virgin America
    - Delta Air Lines
    - Air Canada
    
    For any other airline, use their official name.
    
    Tweet: "{tweet}"
    
    Return as JSON: {{"airlines": ["Official Name 1", "Official Name 2"]}}
    If no airlines mentioned, return: {{"airlines": []}}'''

def prompt_entity_v3_examples(tweet: str) -> str:
    """Prompt with few-shot examples.
    
    Args:
        tweet: The tweet to analyze
        
    Returns:
        Formatted prompt string
    """
    return f'''Extract airline names using official names. Examples:
    
    Tweet: "@AmericanAir delayed again!"
    Output: {{"airlines": ["American Airlines"]}}
    
    Tweet: "Flying United and Southwest today"
    Output: {{"airlines": ["United Airlines", "Southwest Airlines"]}}'''

# Dictionary mapping experiment names to prompt functions
ENTITY_PROMPT_FUNCS = {
    "entity_v1": prompt_entity_v1,
    "entity_v2_standardized": prompt_entity_v2_standardized,
    "entity_v3_examples": prompt_entity_v3_examples,
} 