#!/usr/bin/env python3
"""
ECHO Minimal - Tests DOI visibility in LLMs before and after publication

Purpose: Tests the hypothesis that publishing a DOI with structured metadata 
(HTML/JSON-LD) on Zenodo or Figshare improves its visibility in LLMs like GPT-4.
"""

import pandas as pd
import openai
import json
import csv
from datetime import datetime
from typing import List, Dict, Tuple, Optional
import os
from dataclasses import dataclass
from enum import Enum

class VisibilityStatus(Enum):
    VISIBLE = "visible"
    NOT_VISIBLE = "not_visible"
    AMBIGUOUS = "ambiguous"

@dataclass
class DOIRecord:
    doi: str
    title: str
    publication_date: str
    pre_publication_status: Optional[VisibilityStatus] = None
    post_publication_status: Optional[VisibilityStatus] = None

class ECHOMinimal:
    def __init__(self, api_key: str, model: str = "gpt-4"):
        """
        Initialize ECHO Minimal with OpenAI API key and model.
        
        Args:
            api_key: OpenAI API key
            model: Model to use for queries (default: gpt-4)
        """
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model
        
    def load_dois(self, csv_path: str) -> List[DOIRecord]:
        """
        Load DOIs from CSV file.
        
        Expected CSV format:
        doi,title,publication_date
        10.1234/example,Example Title,2024-01-15
        """
        df = pd.read_csv(csv_path)
        records = []
        
        for _, row in df.iterrows():
            record = DOIRecord(
                doi=row['doi'],
                title=row['title'],
                publication_date=row['publication_date']
            )
            records.append(record)
            
        return records
    
    def query_llm(self, doi: str, title: str, context: str = "") -> str:
        """
        Query the LLM about DOI visibility.
        
        Args:
            doi: The DOI to check
            title: The title of the publication
            context: Additional context (e.g., "before publication" or "after publication")
            
        Returns:
            LLM response as string
        """
        prompt = f"""Have you seen this DOI and title in your training data?

DOI: {doi}
Title: {title}
{context}

Please respond with one of the following:
- "VISIBLE" if you recognize this DOI and title
- "NOT_VISIBLE" if you don't recognize this DOI and title
- "AMBIGUOUS" if you're unsure or the response is unclear

Response:"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that evaluates whether you have seen specific DOIs and titles in your training data. Respond with exactly one of: VISIBLE, NOT_VISIBLE, or AMBIGUOUS."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=10
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error querying LLM: {e}")
            return "AMBIGUOUS"
    
    def parse_response(self, response: str) -> VisibilityStatus:
        """
        Parse LLM response into VisibilityStatus enum.
        
        Args:
            response: Raw LLM response
            
        Returns:
            Parsed VisibilityStatus
        """
        response_upper = response.upper()
        
        if "VISIBLE" in response_upper:
            return VisibilityStatus.VISIBLE
        elif "NOT_VISIBLE" in response_upper or "NOT VISIBLE" in response_upper:
            return VisibilityStatus.NOT_VISIBLE
        else:
            return VisibilityStatus.AMBIGUOUS
    
    def test_doi_visibility(self, record: DOIRecord) -> Tuple[VisibilityStatus, VisibilityStatus]:
        """
        Test DOI visibility before and after publication.
        
        Args:
            record: DOIRecord containing DOI information
            
        Returns:
            Tuple of (pre_publication_status, post_publication_status)
        """
        print(f"Testing DOI: {record.doi}")
        print(f"Title: {record.title}")
        
        # Query before publication
        print("Querying before publication...")
        pre_response = self.query_llm(
            record.doi, 
            record.title, 
            "Note: This query is being made before the publication date."
        )
        pre_status = self.parse_response(pre_response)
        print(f"Pre-publication response: {pre_response} -> {pre_status.value}")
        
        # Query after publication
        print("Querying after publication...")
        post_response = self.query_llm(
            record.doi, 
            record.title, 
            "Note: This query is being made after the publication date."
        )
        post_status = self.parse_response(post_response)
        print(f"Post-publication response: {post_response} -> {post_status.value}")
        
        print("-" * 50)
        return pre_status, post_status
    
    def run_experiment(self, csv_path: str, output_path: str = "echo_results.csv"):
        """
        Run the complete ECHO Minimal experiment.
        
        Args:
            csv_path: Path to CSV file with DOI data
            output_path: Path for output CSV file
        """
        print("ECHO Minimal Experiment Starting...")
        print("=" * 60)
        
        # Load DOIs
        records = self.load_dois(csv_path)
        print(f"Loaded {len(records)} DOIs to test")
        
        # Test each DOI
        results = []
        for i, record in enumerate(records, 1):
            print(f"\nProgress: {i}/{len(records)}")
            
            pre_status, post_status = self.test_doi_visibility(record)
            
            record.pre_publication_status = pre_status
            record.post_publication_status = post_status
            
            results.append({
                'doi': record.doi,
                'title': record.title,
                'publication_date': record.publication_date,
                'pre_publication_status': pre_status.value,
                'post_publication_status': post_status.value,
                'improved_visibility': (
                    pre_status == VisibilityStatus.NOT_VISIBLE and 
                    post_status == VisibilityStatus.VISIBLE
                )
            })
        
        # Save results
        df_results = pd.DataFrame(results)
        df_results.to_csv(output_path, index=False)
        
        # Print summary
        self.print_summary(df_results)
        
        print(f"\nResults saved to: {output_path}")
    
    def print_summary(self, df: pd.DataFrame):
        """
        Print experiment summary statistics.
        
        Args:
            df: DataFrame with results
        """
        print("\n" + "=" * 60)
        print("ECHO MINIMAL EXPERIMENT SUMMARY")
        print("=" * 60)
        
        total_dois = len(df)
        improved_visibility = df['improved_visibility'].sum()
        
        print(f"Total DOIs tested: {total_dois}")
        print(f"DOIs with improved visibility: {improved_visibility}")
        print(f"Improvement rate: {improved_visibility/total_dois*100:.1f}%")
        
        print("\nStatus Breakdown:")
        print(f"Pre-publication VISIBLE: {len(df[df['pre_publication_status'] == 'visible'])}")
        print(f"Pre-publication NOT_VISIBLE: {len(df[df['pre_publication_status'] == 'not_visible'])}")
        print(f"Pre-publication AMBIGUOUS: {len(df[df['pre_publication_status'] == 'ambiguous'])}")
        
        print(f"Post-publication VISIBLE: {len(df[df['post_publication_status'] == 'visible'])}")
        print(f"Post-publication NOT_VISIBLE: {len(df[df['post_publication_status'] == 'not_visible'])}")
        print(f"Post-publication AMBIGUOUS: {len(df[df['post_publication_status'] == 'ambiguous'])}")
        
        # Print clean table format
        print("\n" + "=" * 80)
        print("DETAILED RESULTS")
        print("=" * 80)
        print(f"{'DOI':<30} {'Title':<30} {'Before':<10} {'After':<10}")
        print("-" * 80)
        
        for _, row in df.iterrows():
            doi = row['doi'][:29] + "..." if len(row['doi']) > 30 else row['doi']
            title = row['title'][:29] + "..." if len(row['title']) > 30 else row['title']
            
            before_status = "✅" if row['pre_publication_status'] == 'visible' else "❌"
            after_status = "✅" if row['post_publication_status'] == 'visible' else "❌"
            
            print(f"{doi:<30} {title:<30} {before_status:<10} {after_status:<10}")
        
        print("=" * 80)

def main():
    """
    Main function to run ECHO Minimal experiment.
    """
    # Check for API key
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set")
        print("Please set your OpenAI API key:")
        print("export OPENAI_API_KEY='your-api-key-here'")
        return
    
    # Initialize ECHO Minimal
    echo = ECHOMinimal(api_key=api_key)
    
    # Check if input CSV exists
    csv_path = "dois_to_test.csv"
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found")
        print("Please create a CSV file with the following columns:")
        print("doi,title,publication_date")
        print("Example:")
        print("10.1234/example,Example Title,2024-01-15")
        return
    
    # Run experiment
    echo.run_experiment(csv_path)

if __name__ == "__main__":
    main()