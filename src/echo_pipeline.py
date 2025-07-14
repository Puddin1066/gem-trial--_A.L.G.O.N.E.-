#!/usr/bin/env python3
"""
Echo Pipeline - Content Generation and Processing System

This module provides the core functionality for executing the echo pipeline,
which handles content generation, transformation, and quality assurance.
"""

import argparse
import asyncio
import json
import logging
import time
from pathlib import Path
from typing import Dict, Any, List, Optional

import yaml
from loguru import logger
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from .pipeline_components import (
    ContentGenerator,
    ContentTransformer,
    QualityValidator,
    OutputFormatter
)
from .pipeline_monitor import PipelineMonitor


class EchoPipeline:
    """
    Main echo pipeline class that orchestrates content generation and processing.
    """
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the echo pipeline with configuration."""
        self.config = self._load_config(config_path)
        self.monitor = PipelineMonitor()
        self.console = Console()
        
        # Initialize pipeline components
        self.generator = ContentGenerator(self.config.get('generator', {}))
        self.transformer = ContentTransformer(self.config.get('transformer', {}))
        self.validator = QualityValidator(self.config.get('validator', {}))
        self.formatter = OutputFormatter(self.config.get('formatter', {}))
        
        # Setup logging
        self._setup_logging()
    
    def _load_config(self, config_path: Optional[str]) -> Dict[str, Any]:
        """Load pipeline configuration from YAML file."""
        if config_path and Path(config_path).exists():
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Return default pipeline configuration."""
        return {
            'generator': {
                'model': 'default',
                'max_tokens': 1000,
                'temperature': 0.7
            },
            'transformer': {
                'formats': ['markdown', 'html', 'jsonld'],
                'templates': 'templates/'
            },
            'validator': {
                'quality_threshold': 0.8,
                'consistency_check': True
            },
            'formatter': {
                'output_dir': 'content/',
                'naming_convention': 'iteration-{iteration}'
            }
        }
    
    def _setup_logging(self):
        """Configure logging for the pipeline."""
        logger.add(
            "logs/echo_pipeline.log",
            rotation="1 day",
            retention="7 days",
            level="INFO"
        )
    
    async def execute(self, input_data: Dict[str, Any], iteration: int = 1) -> Dict[str, Any]:
        """
        Execute the complete echo pipeline.
        
        Args:
            input_data: Input data for content generation
            iteration: Current iteration number
            
        Returns:
            Pipeline execution results
        """
        start_time = time.time()
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=self.console
        ) as progress:
            
            # Step 1: Generate content
            task1 = progress.add_task("Generating content...", total=None)
            generated_content = await self.generator.generate(input_data)
            progress.update(task1, completed=True)
            
            # Step 2: Transform content
            task2 = progress.add_task("Transforming content...", total=None)
            transformed_content = await self.transformer.transform(generated_content)
            progress.update(task2, completed=True)
            
            # Step 3: Validate quality
            task3 = progress.add_task("Validating quality...", total=None)
            validation_result = await self.validator.validate(transformed_content)
            progress.update(task3, completed=True)
            
            # Step 4: Format output
            task4 = progress.add_task("Formatting output...", total=None)
            output_paths = await self.formatter.format(
                transformed_content, 
                iteration=iteration
            )
            progress.update(task4, completed=True)
        
        # Record metrics
        execution_time = time.time() - start_time
        self.monitor.record_execution({
            'iteration': iteration,
            'execution_time': execution_time,
            'content_quality': validation_result.get('quality_score', 0),
            'output_paths': output_paths
        })
        
        logger.info(f"Pipeline execution completed in {execution_time:.2f}s")
        
        return {
            'success': validation_result.get('passed', False),
            'execution_time': execution_time,
            'quality_score': validation_result.get('quality_score', 0),
            'output_paths': output_paths,
            'validation_details': validation_result
        }
    
    def run_tests(self) -> Dict[str, Any]:
        """Run the complete test suite for the echo pipeline."""
        logger.info("Starting echo pipeline test suite")
        
        test_results = {
            'unit_tests': self._run_unit_tests(),
            'integration_tests': self._run_integration_tests(),
            'performance_tests': self._run_performance_tests(),
            'quality_tests': self._run_quality_tests()
        }
        
        # Generate test report
        self._generate_test_report(test_results)
        
        return test_results
    
    def _run_unit_tests(self) -> Dict[str, Any]:
        """Run unit tests for individual pipeline components."""
        logger.info("Running unit tests...")
        
        results = {
            'generator_tests': self.generator.run_tests(),
            'transformer_tests': self.transformer.run_tests(),
            'validator_tests': self.validator.run_tests(),
            'formatter_tests': self.formatter.run_tests()
        }
        
        return results
    
    def _run_integration_tests(self) -> Dict[str, Any]:
        """Run integration tests for end-to-end pipeline functionality."""
        logger.info("Running integration tests...")
        
        # Test with sample data
        sample_input = {
            'topic': 'Echo Pipeline Testing',
            'format': 'markdown',
            'length': 'medium'
        }
        
        try:
            result = asyncio.run(self.execute(sample_input, iteration=999))
            return {
                'passed': result['success'],
                'execution_time': result['execution_time'],
                'quality_score': result['quality_score']
            }
        except Exception as e:
            logger.error(f"Integration test failed: {e}")
            return {'passed': False, 'error': str(e)}
    
    def _run_performance_tests(self) -> Dict[str, Any]:
        """Run performance tests to measure pipeline efficiency."""
        logger.info("Running performance tests...")
        
        # Test execution time under load
        start_time = time.time()
        test_iterations = 5
        
        for i in range(test_iterations):
            sample_input = {
                'topic': f'Performance Test {i+1}',
                'format': 'markdown',
                'length': 'short'
            }
            asyncio.run(self.execute(sample_input, iteration=i+1))
        
        total_time = time.time() - start_time
        avg_time = total_time / test_iterations
        
        return {
            'total_iterations': test_iterations,
            'total_time': total_time,
            'average_time': avg_time,
            'iterations_per_second': test_iterations / total_time
        }
    
    def _run_quality_tests(self) -> Dict[str, Any]:
        """Run quality tests to validate output consistency."""
        logger.info("Running quality tests...")
        
        # Test content consistency across multiple runs
        test_inputs = [
            {'topic': 'Test 1', 'format': 'markdown'},
            {'topic': 'Test 2', 'format': 'html'},
            {'topic': 'Test 3', 'format': 'jsonld'}
        ]
        
        quality_scores = []
        for i, test_input in enumerate(test_inputs):
            result = asyncio.run(self.execute(test_input, iteration=i+1))
            quality_scores.append(result['quality_score'])
        
        return {
            'average_quality': sum(quality_scores) / len(quality_scores),
            'min_quality': min(quality_scores),
            'max_quality': max(quality_scores),
            'consistency_score': 1.0 - (max(quality_scores) - min(quality_scores))
        }
    
    def _generate_test_report(self, test_results: Dict[str, Any]):
        """Generate a comprehensive test report."""
        report_path = Path('reports/test_report.json')
        report_path.parent.mkdir(exist_ok=True)
        
        with open(report_path, 'w') as f:
            json.dump(test_results, f, indent=2)
        
        logger.info(f"Test report generated: {report_path}")


def main():
    """Main entry point for the echo pipeline."""
    parser = argparse.ArgumentParser(description='Echo Pipeline - Content Generation and Processing')
    parser.add_argument('--config', type=str, help='Path to configuration file')
    parser.add_argument('--test', action='store_true', help='Run test suite')
    parser.add_argument('--input', type=str, help='Input data file (JSON)')
    parser.add_argument('--iteration', type=int, default=1, help='Iteration number')
    
    args = parser.parse_args()
    
    # Initialize pipeline
    pipeline = EchoPipeline(args.config)
    
    if args.test:
        # Run test suite
        results = pipeline.run_tests()
        print("Test suite completed. Check reports/test_report.json for details.")
    else:
        # Execute pipeline
        if args.input:
            with open(args.input, 'r') as f:
                input_data = json.load(f)
        else:
            input_data = {
                'topic': 'Echo Pipeline Demo',
                'format': 'markdown',
                'length': 'medium'
            }
        
        result = asyncio.run(pipeline.execute(input_data, args.iteration))
        print(f"Pipeline execution completed: {result}")


if __name__ == '__main__':
    main()