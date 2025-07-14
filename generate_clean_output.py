#!/usr/bin/env python3
"""
Generate clean output from ECHO Minimal results.
"""

import pandas as pd
import sys

def generate_clean_output(results_file: str, output_file: str = "clean_results.txt"):
    """
    Generate clean output from ECHO Minimal results.
    
    Args:
        results_file: Path to the CSV results file
        output_file: Path for the clean output file
    """
    df = pd.read_csv(results_file)
    
    with open(output_file, 'w') as f:
        # Header
        f.write("Output: DOI\n")
        f.write("Title\n")
        f.write("Before Visible\n")
        f.write("After Visible\n")
        
        # Results
        for _, row in df.iterrows():
            f.write(f"{row['doi']}\n")
            f.write(f"{row['title']}\n")
            
            before_status = "✅" if row['pre_publication_status'] == 'visible' else "❌"
            after_status = "✅" if row['post_publication_status'] == 'visible' else "❌"
            
            f.write(f"{before_status}\n")
            f.write(f"{after_status}\n")
            f.write("\n")  # Empty line between entries
    
    print(f"Clean output saved to: {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_clean_output.py <results_csv_file> [output_file]")
        sys.exit(1)
    
    results_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "clean_results.txt"
    
    generate_clean_output(results_file, output_file)