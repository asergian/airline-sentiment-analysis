"""Response parsing utilities for experiment results.

This module provides functions for parsing and cleaning responses from language models,
including handling different response formats and error cases.
"""

import json
from typing import List, Dict

def parse_entity_response_clean(response: str) -> List[str]:
    """Parse and clean entity extraction response.
    
    Args:
        response: Raw response from the language model
        
    Returns:
        List of extracted airline names
    """
    try:
        if response.startswith('```'):
            lines = response.split('\n')
            json_lines = [line for line in lines if line.strip() and not line.strip().startswith('```')]
            if json_lines:
                response = '\n'.join(json_lines)
        data = json.loads(response)
        airlines = data.get("airlines", [])
        if isinstance(airlines, str):
            airlines = [airlines]
        return airlines
    except Exception:
        return []

def parse_sentiment_response(response: str) -> str:
    """Parse sentiment analysis response.
    
    Args:
        response: Raw response from the language model
        
    Returns:
        Extracted sentiment ('positive', 'negative', or 'neutral')
    """
    try:
        if response.startswith('```'):
            lines = response.split('\n')
            json_lines = [line for line in lines if line.strip() and not line.strip().startswith('```')]
            if json_lines:
                response = '\n'.join(json_lines)
        data = json.loads(response)
        sentiment = data.get("sentiment", "").lower().strip()
        if sentiment in ["positive", "negative", "neutral"]:
            return sentiment
        else:
            return "unknown"
    except Exception:
        response_lower = response.lower().strip()
        if "positive" in response_lower:
            return "positive"
        elif "negative" in response_lower:
            return "negative"
        elif "neutral" in response_lower:
            return "neutral"
        else:
            return "unknown"

def parse_batch_response(response: str, tweets: List[str]) -> List[Dict]:
    """Parse the response from the API for each tweet in the batch.
    
    Args:
        response: Raw response from the API
        tweets: Original list of tweets
        
    Returns:
        List[Dict]: List of results for each tweet, containing only airlines and sentiment
    """
    try:
        # Handle potential markdown formatting
        if "```json" in response:
            response = response.split("```json")[1].split("```")[0].strip()
        elif "```" in response:
            response = response.split("```")[1].strip()
            
        results = json.loads(response)
        
        # Validate results
        if not isinstance(results, list):
            raise ValueError("Response is not a list")
            
        # Ensure we have results for all tweets
        if len(results) != len(tweets):
            raise ValueError(f"Expected {len(tweets)} results, got {len(results)}")
            
        # Extract only airlines and sentiment from each result
        parsed_results = []
        for result in results:
            if not isinstance(result, dict):
                raise ValueError("Result is not a dictionary")
            if "airlines" not in result or "sentiment" not in result:
                raise ValueError("Missing required fields in result")
            if not isinstance(result["airlines"], list):
                raise ValueError("airlines field must be a list")
            if result["sentiment"] not in ["positive", "negative", "neutral"]:
                raise ValueError("Invalid sentiment value")
                
            parsed_results.append({
                "airlines": result["airlines"],
                "sentiment": result["sentiment"]
            })
                
        return parsed_results
        
    except Exception as e:
        print(f"Error parsing batch response: {str(e)}")
        # Return empty results for failed batch
        return [{"airlines": [], "sentiment": "neutral"} for _ in tweets] 