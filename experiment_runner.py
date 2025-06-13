"""Main script for running prompt engineering experiments on airline sentiment analysis.

This script provides a command-line interface to run different types of experiments:
- Entity extraction: Identifying airline mentions in tweets
- Sentiment analysis: Analyzing sentiment towards mentioned airlines
- Combined: Performing both entity extraction and sentiment analysis in one step

The script supports both single-tweet and batch processing modes, with configurable
parameters for experiment type, number of samples, and batch size.
"""

import argparse
import pandas as pd
import json
import os
import time
from typing import Callable

from evals.prompts.entity import ENTITY_PROMPT_FUNCS
from evals.prompts.sentiment import SENTIMENT_PROMPT_FUNCS
from evals.prompts.combined import COMBINED_PROMPT_FUNCS
from evals.utils.api import call_api
from evals.utils.parsers import parse_entity_response_clean, parse_sentiment_response, parse_batch_response
from evals.utils.data import load_dataset, get_true_airlines, create_output_dir, write_result

def run_entity_experiment(df: pd.DataFrame, n_samples: int, prompt_func: Callable, solution_path: str):
    """Run entity extraction experiment on tweets.
    
    Args:
        df: DataFrame containing tweets and true airline mentions
        n_samples: Number of samples to process
        prompt_func: Function to generate the prompt for each tweet
        solution_path: Path to save the results
    """
    with open(solution_path, 'w') as f:
        for i, (_, row) in enumerate(df.iterrows()):
            if i >= n_samples:
                break
            tweet = row['tweet']
            true_airlines = get_true_airlines(row)
            prompt = prompt_func(tweet)
            response = call_api(prompt)
            predicted_airlines = parse_entity_response_clean(response)
            write_result(f, tweet, true_airlines, predicted_airlines)
            print(f"{i+1}/{n_samples} | True: {true_airlines} | Pred: {predicted_airlines}")
            time.sleep(0.3)

def run_sentiment_experiment(df: pd.DataFrame, n_samples: int, prompt_func: Callable, solution_path: str):
    """Run sentiment analysis experiment on tweets.
    
    Args:
        df: DataFrame containing tweets and true sentiment labels
        n_samples: Number of samples to process
        prompt_func: Function to generate the prompt for each tweet-airline pair
        solution_path: Path to save the results
    """
    with open(solution_path, 'w') as f:
        for i, (_, row) in enumerate(df.iterrows()):
            if i >= n_samples:
                break
            tweet = row['tweet']
            true_sentiment = row['sentiment']
            true_airlines = get_true_airlines(row)
            for airline in true_airlines:
                prompt = prompt_func(tweet, airline)
                response = call_api(prompt)
                predicted_sentiment = parse_sentiment_response(response)
                write_result(f, {'tweet': tweet, 'airline': airline}, true_sentiment, predicted_sentiment)
                print(f"{i+1}/{n_samples} | Airline: {airline} | True: {true_sentiment} | Pred: {predicted_sentiment}")
                time.sleep(0.3)

def run_combined_experiment(df: pd.DataFrame, n_samples: int, batch_size: int, prompt_func: Callable, solution_path: str):
    """Run combined entity extraction and sentiment analysis experiment.
    
    Args:
        df: DataFrame containing tweets and true labels
        n_samples: Number of samples to process
        batch_size: Number of tweets to process in each batch
        prompt_func: Function to generate the prompt for tweets
        solution_path: Path to save the results
    """
    with open(solution_path, 'w') as f:
        if batch_size == 1:
            for i, (_, row) in enumerate(df.iterrows()):
                if i >= n_samples:
                    break
                tweet = row['tweet']
                true_sentiment = row['sentiment']
                true_airlines = get_true_airlines(row)
                prompt = prompt_func(tweet)
                response = call_api(prompt)
                # Clean the response: remove markdown and parse JSON
                if response.startswith('```'):
                    lines = response.split('\n')
                    json_lines = [line for line in lines if line.strip() and not line.strip().startswith('```')]
                    if json_lines:
                        response = '\n'.join(json_lines)
                try:
                    output_json = json.loads(response)
                except Exception:
                    output_json = response
                write_result(f, tweet, {'sentiment': true_sentiment, 'airlines': true_airlines}, output_json)
                print(f"{i+1}/{n_samples} | Tweet: {tweet[:50]}... | Response: {str(response)[:50]}...")
                time.sleep(0.3)
        else:
            for i in range(0, len(df), batch_size):
                if i >= n_samples:
                    break
                    
                batch_df = df.iloc[i:i+batch_size]
                batch_tweets = batch_df['tweet'].tolist()
                batch_sentiments = batch_df['sentiment'].tolist()
                batch_airlines = [get_true_airlines(row) for _, row in batch_df.iterrows()]
                
                # Get response from API
                prompt = prompt_func(batch_tweets)
                response = call_api(prompt, max_tokens=300 * len(batch_tweets))
                
                # Parse results
                batch_results = parse_batch_response(response, batch_tweets)
                
                # Save results
                for j, (tweet, true_sentiment, true_airlines, output) in enumerate(zip(batch_tweets, batch_sentiments, batch_airlines, batch_results)):
                    if i + j >= n_samples:
                        break
                        
                    write_result(f, tweet, {'sentiment': true_sentiment, 'airlines': true_airlines}, output)
                    print(f"Batch {i//batch_size+1}, {j+1}/{len(batch_tweets)} | Tweet: {tweet[:50]}... | Output: {str(output)[:50]}...")
                time.sleep(0.5)

def main():
    """Main entry point for running experiments.
    
    Parses command line arguments and runs the specified experiment type
    with the given parameters. Results are saved to a timestamped directory.
    """
    start_time = time.time()
    
    parser = argparse.ArgumentParser(description="Run prompt experiment.")
    parser.add_argument("--experiment", default="combined_v1", help="Experiment name (entity_v1, entity_v2_standardized, entity_v3_examples, sentiment_v1_basic, sentiment_v2_context_aware, combined_v1, combined_batch_v1)")
    parser.add_argument("--n_samples", type=int, default=None, help="Number of samples (default: use full dataset)")
    parser.add_argument("--batch_size", type=int, default=1, help="Batch size for processing (default: 1)")
    parser.add_argument("--test", action="store_true", help="Use test dataset instead of train dataset")
    args = parser.parse_args()

    # Create output directory
    output_dir = create_output_dir(args.experiment, args.n_samples, args.batch_size, args.test)
    solution_path = os.path.join(output_dir, "solution.jsonl")

    # Load data
    dataset_type = "test" if args.test else "train"
    df = load_dataset(dataset_type, args.n_samples)
    if args.n_samples is None:
        args.n_samples = len(df)  # Set n_samples to full dataset length

    # Run experiment
    if args.experiment in ENTITY_PROMPT_FUNCS:
        run_entity_experiment(df, args.n_samples, ENTITY_PROMPT_FUNCS[args.experiment], solution_path)
    elif args.experiment in SENTIMENT_PROMPT_FUNCS:
        run_sentiment_experiment(df, args.n_samples, SENTIMENT_PROMPT_FUNCS[args.experiment], solution_path)
    elif args.experiment in COMBINED_PROMPT_FUNCS:
        run_combined_experiment(df, args.n_samples, args.batch_size, COMBINED_PROMPT_FUNCS[args.experiment], solution_path)
    else:
        print(f"Experiment '{args.experiment}' not found. Available: "
              f"{list(ENTITY_PROMPT_FUNCS.keys()) + list(SENTIMENT_PROMPT_FUNCS.keys()) + list(COMBINED_PROMPT_FUNCS.keys())}")

    print(f"Saved solution to {output_dir}")
    print(f"Total runtime: {time.time() - start_time:.2f} seconds")

if __name__ == "__main__":
    main() 