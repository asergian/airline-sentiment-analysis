# Airline Sentiment Analysis

> This project was created as part of a technical interview process. It demonstrates prompt engineering and natural language processing capabilities using OpenAI's API.

## Overview
This project provides tools for running prompt engineering experiments on airline-related tweets, including entity extraction, sentiment analysis, and combined analysis.

## Features

- Entity extraction: Identify airline mentions in tweets
- Sentiment analysis: Analyze sentiment towards mentioned airlines
- Combined analysis: Perform both entity extraction and sentiment analysis in one step
- Support for both single-tweet and batch processing
- Configurable experiment parameters

## Prerequisites

- Python 3.x
- OpenAI API key

## Quick Start

1. Clone the repository:
```bash
git clone https://github.com/asergian/airline-sentiment-analysis.git
cd airline-sentiment-analysis
```

2. Make the run script executable:
```bash
chmod +x run.sh
```

3. Set up your OpenAI API key:
```bash
# The run script will create a .env file if it doesn't exist
# Edit the .env file and add your OpenAI API key:
echo "OPENAI_API_KEY=your_api_key_here" > .env
```

4. Run the setup and default experiment:
```bash
./run.sh
```

This will:
- Create a virtual environment if it doesn't exist
- Install required dependencies
- Run the default experiment (combined analysis on test dataset)

## Manual Setup

If you prefer to set up manually:

1. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run an experiment:
```bash
python experiment_runner.py --experiment <experiment_name> [options]
```

## Available Experiments

### Entity Extraction
- `entity_v1`: Basic entity extraction
- `entity_v2_standardized`: Standardized airline names
- `entity_v3_examples`: Detailed examples and edge cases

### Sentiment Analysis
- `sentiment_v1_basic`: Basic sentiment analysis
- `sentiment_v2_context_aware`: Context-aware sentiment analysis

### Combined Analysis
- `combined_v1`: Single-tweet combined analysis
- `combined_batch_v1`: Batch processing combined analysis

## Command Line Options

- `--experiment`: Experiment name (default: "combined_v1")
- `--n_samples`: Number of samples to process (default: full dataset)
- `--batch_size`: Batch size for processing (default: 1)
- `--test`: Use test dataset instead of train dataset

> **Important**: When using `--batch_size > 1`, you must use the `combined_batch_v1` experiment. The single-tweet prompts are not designed for batch processing.

## Example Usage

```bash
# Run single-tweet combined analysis on test set
python experiment_runner.py --experiment combined_v1 --test
# Output directory: evals/results/test_combined_v1_20240321_123456/

# Run batch processing on 100 samples
python experiment_runner.py --experiment combined_batch_v1 --batch_size 5 --n_samples 100
# Output directory: evals/results/combined_batch_v1_batch_5_20240321_123456/

# Run on full training set
python experiment_runner.py --experiment entity_v1
# Output directory: evals/results/train_full_20240321_123456/
```

## Project Structure

```
.
├── evals/
│   ├── prompts/
│   │   ├── entity.py      # Entity extraction prompts
│   │   ├── sentiment.py   # Sentiment analysis prompts
│   │   └── combined.py    # Combined analysis prompts
│   └── utils/
│       ├── api.py         # API interaction utilities
│       ├── data.py        # Data loading and processing
│       └── parsers.py     # Response parsing utilities
├── experiment_runner.py   # Main experiment script
├── requirements.txt       # Project dependencies
└── run.sh                # Setup and run script
```

## Results

Experiment results are saved in the `evals/results/` directory with timestamps. The directory name format is:
- Test set (full dataset): `test_full_<timestamp>/`
- Training set (full dataset): `train_full_<timestamp>/`
- Training set (sampled data): `<experiment_name>_<timestamp>/`
- Training set (sampled data w/ batch processing): `<experiment_name>_batch_<size>_<timestamp>/`

Each result file contains:
- Input tweet
- Ground truth (true airlines and sentiment)
- Model output

## Development

### Adding New Prompts

1. Add your prompt function to the appropriate file in `evals/prompts/`
2. Add the function to the corresponding `*_PROMPT_FUNCS` dictionary
3. Update the experiment runner if needed

### Adding New Experiments

1. Create your experiment function in `experiment_runner.py`
2. Add the experiment to the appropriate prompt functions dictionary
3. Update the main function to handle your experiment type

## Solution Architecture
A detailed architecture diagram is available in `experiments/solution_design_simple.md`. The diagram illustrates:
- Data flow from Twitter API and CSV sources
- Processing pipeline using GPT-4o-mini
- Entity extraction and sentiment analysis
- Data storage and business insights
- Future expansion opportunities

To view the diagram:
1. Open `experiments/solution_design_simple.md`
2. Copy the Mermaid diagram code
3. Paste into https://mermaid.live to visualize 

## License

MIT License

Copyright (c) 2024 Alexander Sergian

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.