#!/usr/bin/env python3
"""
DOI Collector - Collects real DOIs from Zenodo and Figshare APIs
for ECHO Minimal experiment controls.
"""

import requests
import pandas as pd
import json
from datetime import datetime, timedelta
from typing import List, Dict
import time

class DOICollector:
    def __init__(self):
        self.zenodo_base_url = "https://zenodo.org/api/records"
        self.figshare_base_url = "https://api.figshare.com/v2/articles"
        
    def get_zenodo_dois(self, limit: int = 50, days_back: int = 30) -> List[Dict]:
        """
        Collect recent DOIs from Zenodo API.
        
        Args:
            limit: Number of DOIs to collect
            days_back: How many days back to search
            
        Returns:
            List of DOI records
        """
        print(f"Collecting {limit} recent DOIs from Zenodo...")
        
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        params = {
            'size': limit,
            'sort': 'mostrecent',
            'status': 'published',
            'type': 'dataset'  # Focus on datasets
        }
        
        try:
            response = requests.get(self.zenodo_base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            dois = []
            for record in data.get('hits', {}).get('hits', []):
                metadata = record.get('metadata', {})
                doi = metadata.get('doi')
                title = metadata.get('title', '')
                
                if doi and title:
                    dois.append({
                        'doi': doi,
                        'title': title,
                        'publication_date': metadata.get('publication_date', ''),
                        'source': 'zenodo',
                        'control_type': 'positive'  # Real DOIs should be visible
                    })
            
            print(f"Collected {len(dois)} DOIs from Zenodo")
            return dois
            
        except Exception as e:
            print(f"Error collecting Zenodo DOIs: {e}")
            return []
    
    def get_figshare_dois(self, limit: int = 50) -> List[Dict]:
        """
        Collect recent DOIs from Figshare API.
        
        Args:
            limit: Number of DOIs to collect
            
        Returns:
            List of DOI records
        """
        print(f"Collecting {limit} recent DOIs from Figshare...")
        
        # Figshare API requires authentication for most endpoints
        # For now, we'll use a simpler approach with public data
        # In production, you'd want to use proper API authentication
        
        try:
            # Get recent articles (this is a simplified approach)
            params = {
                'page_size': limit,
                'order': 'published_date',
                'order_direction': 'desc'
            }
            
            response = requests.get(self.figshare_base_url, params=params)
            response.raise_for_status()
            data = response.json()
            
            dois = []
            for article in data:
                doi = article.get('doi')
                title = article.get('title', '')
                published_date = article.get('published_date', '')
                
                if doi and title:
                    dois.append({
                        'doi': doi,
                        'title': title,
                        'publication_date': published_date,
                        'source': 'figshare',
                        'control_type': 'positive'  # Real DOIs should be visible
                    })
            
            print(f"Collected {len(dois)} DOIs from Figshare")
            return dois
            
        except Exception as e:
            print(f"Error collecting Figshare DOIs: {e}")
            return []
    
    def generate_fake_dois(self, count: int = 20) -> List[Dict]:
        """
        Generate fake DOIs for negative controls.
        
        Args:
            count: Number of fake DOIs to generate
            
        Returns:
            List of fake DOI records
        """
        print(f"Generating {count} fake DOIs for negative controls...")
        
        fake_dois = []
        for i in range(count):
            # Generate fake Zenodo-style DOIs
            fake_zenodo_doi = f"10.5281/zenodo.{999999999 - i}"
            fake_figshare_doi = f"10.6084/m9.figshare.{999999999 - i}"
            
            fake_dois.extend([
                {
                    'doi': fake_zenodo_doi,
                    'title': f"Fake Dataset {i+1}",
                    'publication_date': '2024-01-01',
                    'source': 'fake_zenodo',
                    'control_type': 'negative'
                },
                {
                    'doi': fake_figshare_doi,
                    'title': f"Fake Article {i+1}",
                    'publication_date': '2024-01-01',
                    'source': 'fake_figshare',
                    'control_type': 'negative'
                }
            ])
        
        print(f"Generated {len(fake_dois)} fake DOIs")
        return fake_dois
    
    def create_experiment_dataset(self, output_file: str = "experiment_dois.csv"):
        """
        Create a complete experiment dataset with positive and negative controls.
        
        Args:
            output_file: Path for output CSV file
        """
        print("Creating ECHO Minimal experiment dataset...")
        
        # Collect real DOIs (positive controls)
        zenodo_dois = self.get_zenodo_dois(limit=25)
        figshare_dois = self.get_figshare_dois(limit=25)
        
        # Generate fake DOIs (negative controls)
        fake_dois = self.generate_fake_dois(count=20)
        
        # Combine all DOIs
        all_dois = zenodo_dois + figshare_dois + fake_dois
        
        # Create DataFrame
        df = pd.DataFrame(all_dois)
        
        # Save to CSV
        df.to_csv(output_file, index=False)
        
        print(f"\nExperiment dataset created: {output_file}")
        print(f"Total DOIs: {len(df)}")
        print(f"Positive controls (real DOIs): {len(df[df['control_type'] == 'positive'])}")
        print(f"Negative controls (fake DOIs): {len(df[df['control_type'] == 'negative'])}")
        
        return df

def main():
    """
    Main function to create experiment dataset.
    """
    collector = DOICollector()
    df = collector.create_experiment_dataset()
    
    # Print sample of the data
    print("\nSample of collected DOIs:")
    print(df.head(10).to_string(index=False))

if __name__ == "__main__":
    main()