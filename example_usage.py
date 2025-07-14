#!/usr/bin/env python3
"""
Example Usage of Echo Pipeline

This script demonstrates how to use the echo pipeline for content generation
and testing. It shows basic pipeline execution and test suite usage.
"""

import asyncio
import json
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from echo_pipeline import EchoPipeline
from loguru import logger


def setup_logging():
    """Setup logging for the example."""
    logger.remove()  # Remove default handler
    logger.add(
        sys.stderr,
        level="INFO",
        format="{time:HH:mm:ss} | {level} | {message}"
    )


async def run_content_generation_example():
    """Example of running content generation through the pipeline."""
    logger.info("=" * 60)
    logger.info("CONTENT GENERATION EXAMPLE")
    logger.info("=" * 60)
    
    # Initialize pipeline
    pipeline = EchoPipeline()
    
    # Example input data
    input_data = {
        'topic': 'Echo Pipeline Demonstration',
        'format': 'markdown',
        'length': 'medium'
    }
    
    logger.info(f"Input data: {input_data}")
    
    # Execute pipeline
    result = await pipeline.execute(input_data, iteration=1)
    
    logger.info("Pipeline execution completed!")
    logger.info(f"Success: {result['success']}")
    logger.info(f"Execution time: {result['execution_time']:.2f}s")
    logger.info(f"Quality score: {result['quality_score']:.2f}")
    logger.info(f"Output paths: {result['output_paths']}")


async def run_testing_example():
    """Example of running the test suite."""
    logger.info("\n" + "=" * 60)
    logger.info("TESTING EXAMPLE")
    logger.info("=" * 60)
    
    # Initialize pipeline
    pipeline = EchoPipeline()
    
    # Run test suite
    test_results = pipeline.run_tests()
    
    logger.info("Test suite completed!")
    
    # Print summary
    unit_tests = test_results.get('unit_tests', {})
    integration_tests = test_results.get('integration_tests', {})
    performance_tests = test_results.get('performance_tests', {})
    quality_tests = test_results.get('quality_tests', {})
    
    logger.info(f"Unit tests: {len(unit_tests)} components tested")
    logger.info(f"Integration test: {'✅ PASS' if integration_tests.get('passed') else '❌ FAIL'}")
    logger.info(f"Performance test: {performance_tests.get('total_iterations', 0)} iterations")
    logger.info(f"Quality test: {quality_tests.get('average_quality', 0):.2f} average quality")


def run_configuration_example():
    """Example of using custom configuration."""
    logger.info("\n" + "=" * 60)
    logger.info("CONFIGURATION EXAMPLE")
    logger.info("=" * 60)
    
    # Initialize pipeline with custom config
    config_path = "config/pipeline_config.yaml"
    pipeline = EchoPipeline(config_path)
    
    logger.info(f"Pipeline initialized with config: {config_path}")
    logger.info(f"Generator model: {pipeline.generator.model}")
    logger.info(f"Quality threshold: {pipeline.validator.quality_threshold}")
    logger.info(f"Output directory: {pipeline.formatter.output_dir}")


def run_monitoring_example():
    """Example of pipeline monitoring capabilities."""
    logger.info("\n" + "=" * 60)
    logger.info("MONITORING EXAMPLE")
    logger.info("=" * 60)
    
    # Initialize pipeline
    pipeline = EchoPipeline()
    
    # Get health status
    health_status = pipeline.monitor.get_health_status()
    
    logger.info(f"Pipeline health: {health_status['status']}")
    logger.info(f"Metrics directory: {health_status.get('metrics_directory', 'N/A')}")
    logger.info(f"Execution history size: {health_status.get('execution_history_size', 0)}")
    
    if 'system_resources' in health_status:
        resources = health_status['system_resources']
        logger.info(f"Memory usage: {resources.get('memory_percent', 0):.1f}%")
        logger.info(f"Disk usage: {resources.get('disk_percent', 0):.1f}%")
        logger.info(f"CPU usage: {resources.get('cpu_percent', 0):.1f}%")


async def main():
    """Main example function."""
    setup_logging()
    
    logger.info("Echo Pipeline Example Usage")
    logger.info("This script demonstrates the key features of the echo pipeline.")
    
    try:
        # Run content generation example
        await run_content_generation_example()
        
        # Run testing example
        await run_testing_example()
        
        # Run configuration example
        run_configuration_example()
        
        # Run monitoring example
        run_monitoring_example()
        
        logger.info("\n" + "=" * 60)
        logger.info("ALL EXAMPLES COMPLETED SUCCESSFULLY!")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"Example execution failed: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    sys.exit(asyncio.run(main()))