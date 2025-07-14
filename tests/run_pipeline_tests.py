#!/usr/bin/env python3
"""
Echo Pipeline Test Runner

This script runs the complete test suite for the echo pipeline, including
unit tests, integration tests, performance tests, and quality tests.
"""

import argparse
import asyncio
import json
import sys
from pathlib import Path
from typing import Dict, Any

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from echo_pipeline import EchoPipeline
from loguru import logger


def setup_logging():
    """Setup logging for test execution."""
    logger.remove()  # Remove default handler
    logger.add(
        "logs/test_execution.log",
        rotation="1 day",
        retention="7 days",
        level="INFO",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
    )
    logger.add(
        sys.stderr,
        level="INFO",
        format="{time:HH:mm:ss} | {level} | {message}"
    )


def run_unit_tests(pipeline: EchoPipeline) -> Dict[str, Any]:
    """Run unit tests for individual pipeline components."""
    logger.info("=" * 60)
    logger.info("RUNNING UNIT TESTS")
    logger.info("=" * 60)
    
    results = pipeline.run_tests()
    
    # Print unit test results
    for component, component_results in results['unit_tests'].items():
        logger.info(f"\n{component.upper()}:")
        for test_name, test_result in component_results.items():
            status = "✅ PASS" if test_result.get('passed', False) else "❌ FAIL"
            logger.info(f"  {test_name}: {status}")
            if 'error' in test_result:
                logger.error(f"    Error: {test_result['error']}")
    
    return results


def run_integration_tests(pipeline: EchoPipeline) -> Dict[str, Any]:
    """Run integration tests for end-to-end functionality."""
    logger.info("\n" + "=" * 60)
    logger.info("RUNNING INTEGRATION TESTS")
    logger.info("=" * 60)
    
    integration_results = pipeline._run_integration_tests()
    
    status = "✅ PASS" if integration_results.get('passed', False) else "❌ FAIL"
    logger.info(f"Integration Test: {status}")
    logger.info(f"  Execution Time: {integration_results.get('execution_time', 0):.2f}s")
    logger.info(f"  Quality Score: {integration_results.get('quality_score', 0):.2f}")
    
    if 'error' in integration_results:
        logger.error(f"  Error: {integration_results['error']}")
    
    return integration_results


def run_performance_tests(pipeline: EchoPipeline) -> Dict[str, Any]:
    """Run performance tests to measure pipeline efficiency."""
    logger.info("\n" + "=" * 60)
    logger.info("RUNNING PERFORMANCE TESTS")
    logger.info("=" * 60)
    
    performance_results = pipeline._run_performance_tests()
    
    logger.info("Performance Metrics:")
    logger.info(f"  Total Iterations: {performance_results.get('total_iterations', 0)}")
    logger.info(f"  Total Time: {performance_results.get('total_time', 0):.2f}s")
    logger.info(f"  Average Time: {performance_results.get('average_time', 0):.2f}s")
    logger.info(f"  Iterations/Second: {performance_results.get('iterations_per_second', 0):.2f}")
    
    return performance_results


def run_quality_tests(pipeline: EchoPipeline) -> Dict[str, Any]:
    """Run quality tests to validate output consistency."""
    logger.info("\n" + "=" * 60)
    logger.info("RUNNING QUALITY TESTS")
    logger.info("=" * 60)
    
    quality_results = pipeline._run_quality_tests()
    
    logger.info("Quality Metrics:")
    logger.info(f"  Average Quality: {quality_results.get('average_quality', 0):.2f}")
    logger.info(f"  Min Quality: {quality_results.get('min_quality', 0):.2f}")
    logger.info(f"  Max Quality: {quality_results.get('max_quality', 0):.2f}")
    logger.info(f"  Consistency Score: {quality_results.get('consistency_score', 0):.2f}")
    
    return quality_results


def generate_test_report(all_results: Dict[str, Any]) -> str:
    """Generate a comprehensive test report."""
    logger.info("\n" + "=" * 60)
    logger.info("GENERATING TEST REPORT")
    logger.info("=" * 60)
    
    # Calculate overall test statistics
    unit_tests = all_results.get('unit_tests', {})
    total_unit_tests = 0
    passed_unit_tests = 0
    
    for component_results in unit_tests.values():
        for test_result in component_results.values():
            total_unit_tests += 1
            if test_result.get('passed', False):
                passed_unit_tests += 1
    
    integration_passed = all_results.get('integration_tests', {}).get('passed', False)
    performance_metrics = all_results.get('performance_tests', {})
    quality_metrics = all_results.get('quality_tests', {})
    
    # Create summary
    summary = {
        'test_summary': {
            'unit_tests': {
                'total': total_unit_tests,
                'passed': passed_unit_tests,
                'failed': total_unit_tests - passed_unit_tests,
                'pass_rate': (passed_unit_tests / total_unit_tests * 100) if total_unit_tests > 0 else 0
            },
            'integration_tests': {
                'passed': integration_passed,
                'execution_time': all_results.get('integration_tests', {}).get('execution_time', 0)
            },
            'performance_tests': {
                'average_time': performance_metrics.get('average_time', 0),
                'iterations_per_second': performance_metrics.get('iterations_per_second', 0)
            },
            'quality_tests': {
                'average_quality': quality_metrics.get('average_quality', 0),
                'consistency_score': quality_metrics.get('consistency_score', 0)
            }
        },
        'detailed_results': all_results
    }
    
    # Save report to file
    reports_dir = Path('reports')
    reports_dir.mkdir(exist_ok=True)
    
    report_path = reports_dir / 'test_report.json'
    with open(report_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    logger.info(f"Test report saved to: {report_path}")
    
    # Print summary
    logger.info("\n" + "=" * 60)
    logger.info("TEST SUMMARY")
    logger.info("=" * 60)
    
    logger.info(f"Unit Tests: {passed_unit_tests}/{total_unit_tests} passed ({summary['test_summary']['unit_tests']['pass_rate']:.1f}%)")
    logger.info(f"Integration Tests: {'✅ PASS' if integration_passed else '❌ FAIL'}")
    logger.info(f"Performance: {performance_metrics.get('average_time', 0):.2f}s average execution time")
    logger.info(f"Quality: {quality_metrics.get('average_quality', 0):.2f} average quality score")
    
    return str(report_path)


def main():
    """Main test runner function."""
    parser = argparse.ArgumentParser(description='Echo Pipeline Test Runner')
    parser.add_argument('--config', type=str, help='Path to configuration file')
    parser.add_argument('--unit-only', action='store_true', help='Run only unit tests')
    parser.add_argument('--integration-only', action='store_true', help='Run only integration tests')
    parser.add_argument('--performance-only', action='store_true', help='Run only performance tests')
    parser.add_argument('--quality-only', action='store_true', help='Run only quality tests')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging()
    
    logger.info("Starting Echo Pipeline Test Suite")
    logger.info(f"Configuration: {args.config or 'default'}")
    
    # Initialize pipeline
    try:
        pipeline = EchoPipeline(args.config)
        logger.info("Pipeline initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize pipeline: {e}")
        return 1
    
    # Run tests based on arguments
    all_results = {}
    
    if args.unit_only or not any([args.integration_only, args.performance_only, args.quality_only]):
        all_results['unit_tests'] = run_unit_tests(pipeline)
    
    if args.integration_only or not any([args.unit_only, args.performance_only, args.quality_only]):
        all_results['integration_tests'] = run_integration_tests(pipeline)
    
    if args.performance_only or not any([args.unit_only, args.integration_only, args.quality_only]):
        all_results['performance_tests'] = run_performance_tests(pipeline)
    
    if args.quality_only or not any([args.unit_only, args.integration_only, args.performance_only]):
        all_results['quality_tests'] = run_quality_tests(pipeline)
    
    # Generate test report
    if all_results:
        report_path = generate_test_report(all_results)
        logger.info(f"\nTest execution completed. Report saved to: {report_path}")
    else:
        logger.warning("No tests were executed")
    
    return 0


if __name__ == '__main__':
    sys.exit(main())