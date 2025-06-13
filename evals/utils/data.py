"""Utility functions for data loading and processing.

This module provides functions for:
- Loading and sampling datasets
- Extracting true airline mentions from data
- Creating output directories for experiments
- Writing experiment results to files
"""

import pandas as pd
import json
import os
from datetime import datetime
from typing import Any

def load_dataset(dataset_type: str, n_samples: int = None) -> pd.DataFrame:
    """Load the airline sentiment dataset.
    
    Args:
        dataset_type: Type of dataset to load ('train' or 'test')
        n_samples: Optional number of samples to load. If None, loads entire dataset.
        
    Returns:
        DataFrame containing the dataset
    """
    df = pd.read_csv(f"data/airline_{dataset_type}_sentiment.csv")
    if n_samples is not None:
        df = df.sample(n=n_samples, random_state=42)
    return df

def get_true_airlines(row: pd.Series) -> list:
    """Extract true airlines from a dataset row.
    
    Args:
        row: DataFrame row containing airline mentions
        
    Returns:
        List of airline names mentioned in the row
    """
    return [a.strip() for a in row['airlines'].replace('[','').replace(']','').replace("'","").split(',') if a.strip()]

def create_output_dir(experiment: str, n_samples: int, batch_size: int, is_test: bool) -> str:
    """Create and return the output directory path for experiment results.
    
    Args:
        experiment: Name of the experiment
        n_samples: Number of samples being processed
        batch_size: Size of batches being processed
        is_test: Whether using test dataset
        
    Returns:
        Path to created output directory
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if is_test:
        prefix = "test_"
        name = "full" if n_samples is None else experiment
    else:
        prefix = ""
        name = "train_full" if n_samples is None else experiment
    
    batch_suffix = f"_batch_{batch_size}" if batch_size > 1 else ""
    output_dir = f"evals/results/{prefix}{name}{batch_suffix}_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def write_result(f, input_data: Any, ideal: Any, output: Any):
    """Write a single experiment result to the output file.
    
    Args:
        f: File object to write to
        input_data: Input data for the experiment
        ideal: Ground truth/expected output
        output: Actual output from the experiment
    """
    f.write(json.dumps({
        'input': input_data,
        'ideal': ideal,
        'output': output
    }) + '\n') 