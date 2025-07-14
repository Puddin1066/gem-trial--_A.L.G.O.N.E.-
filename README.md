# ECHO Minimal

Tests the hypothesis that publishing a DOI with structured metadata (HTML/JSON-LD) on Zenodo or Figshare improves its visibility in LLMs like GPT-4.

## What It Does

- Loads a list of DOIs with their publication dates
- Sends two queries per DOI to an LLM:
  - One before publication
  - One after publication
- Asks the model: "Have you seen this DOI + title?"
- Labels each response as:
  - ✅ Visible
  - ❌ Not visible
  - Ambiguous
- Outputs a CSV showing which DOIs are recognized only after publishing

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set your OpenAI API key:
```bash
export OPENAI_API_KEY='your-api-key-here'
```

3. Prepare your DOI data in `dois_to_test.csv`:
```csv
doi,title,publication_date
10.5281/zenodo.1234567,Example Research Dataset,2024-01-15
10.6084/m9.figshare.9876543,Sample Scientific Paper,2024-02-20
```

## Usage

Run the experiment:
```bash
python echo_minimal.py
```

Generate clean output:
```bash
python generate_clean_output.py echo_results.csv
```

## Output Format

The script produces two types of output:

1. **Console output** with detailed progress and summary statistics
2. **CSV file** (`echo_results.csv`) with all results
3. **Clean text file** (optional) with the format:
```
Output: DOI
Title
Before Visible
After Visible
10.5281/zenodo.1234567
Sample A
❌
✅
```

## Files

- `echo_minimal.py` - Main experiment script
- `generate_clean_output.py` - Helper script for clean output
- `dois_to_test.csv` - Sample DOI data (create your own)
- `requirements.txt` - Python dependencies
- `README.md` - This file

## Core Tools

- `pandas` for data handling
- `openai` for querying LLMs
- Simple response parsing logic
- No embeddings, no perplexity, no deep stats — just binary recognition analysis