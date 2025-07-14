"""
Echo Pipeline Package

This package contains the core components for the echo pipeline,
including content generation, transformation, validation, and output formatting.
"""

__version__ = "1.0.0"
__author__ = "Echo Pipeline Team"
__description__ = "Comprehensive testing and execution framework for content generation and processing workflows"

from .echo_pipeline import EchoPipeline
from .pipeline_components import (
    ContentGenerator,
    ContentTransformer,
    QualityValidator,
    OutputFormatter
)
from .pipeline_monitor import PipelineMonitor

__all__ = [
    'EchoPipeline',
    'ContentGenerator',
    'ContentTransformer',
    'QualityValidator',
    'OutputFormatter',
    'PipelineMonitor'
]