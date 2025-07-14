"""
Pipeline Monitor for Echo Pipeline

This module provides monitoring and metrics collection capabilities for the echo pipeline,
including performance tracking, execution history, and resource usage monitoring.
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

import psutil
from loguru import logger


class PipelineMonitor:
    """Monitors pipeline execution and collects performance metrics."""
    
    def __init__(self):
        """Initialize the pipeline monitor."""
        self.execution_history = []
        self.metrics_dir = Path('metrics/')
        self.metrics_dir.mkdir(exist_ok=True)
        
        # Performance tracking
        self.start_time = None
        self.current_execution = None
    
    def start_execution(self, execution_id: str, input_data: Dict[str, Any]):
        """Start monitoring a pipeline execution."""
        self.start_time = time.time()
        self.current_execution = {
            'execution_id': execution_id,
            'start_time': datetime.now().isoformat(),
            'input_data': input_data,
            'system_info': self._get_system_info()
        }
        
        logger.info(f"Started monitoring execution: {execution_id}")
    
    def record_execution(self, execution_data: Dict[str, Any]):
        """Record execution results and metrics."""
        if self.current_execution:
            self.current_execution.update(execution_data)
            self.current_execution['end_time'] = datetime.now().isoformat()
            self.current_execution['duration'] = time.time() - self.start_time
            
            # Add performance metrics
            self.current_execution['performance'] = self._get_performance_metrics()
            
            # Add to history
            self.execution_history.append(self.current_execution)
            
            # Save to file
            self._save_execution_record(self.current_execution)
            
            logger.info(f"Recorded execution: {self.current_execution['execution_id']}")
            
            # Reset for next execution
            self.current_execution = None
            self.start_time = None
    
    def _get_system_info(self) -> Dict[str, Any]:
        """Get current system information."""
        try:
            return {
                'cpu_count': psutil.cpu_count(),
                'memory_total': psutil.virtual_memory().total,
                'memory_available': psutil.virtual_memory().available,
                'disk_usage': psutil.disk_usage('/').percent
            }
        except Exception as e:
            logger.warning(f"Could not get system info: {e}")
            return {}
    
    def _get_performance_metrics(self) -> Dict[str, Any]:
        """Get current performance metrics."""
        try:
            process = psutil.Process()
            return {
                'cpu_percent': process.cpu_percent(),
                'memory_percent': process.memory_percent(),
                'memory_rss': process.memory_info().rss,
                'memory_vms': process.memory_info().vms
            }
        except Exception as e:
            logger.warning(f"Could not get performance metrics: {e}")
            return {}
    
    def _save_execution_record(self, execution_record: Dict[str, Any]):
        """Save execution record to file."""
        execution_id = execution_record['execution_id']
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"execution_{execution_id}_{timestamp}.json"
        filepath = self.metrics_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(execution_record, f, indent=2)
        
        logger.debug(f"Saved execution record to {filepath}")
    
    def get_execution_summary(self, limit: int = 10) -> Dict[str, Any]:
        """Get a summary of recent executions."""
        recent_executions = self.execution_history[-limit:] if self.execution_history else []
        
        if not recent_executions:
            return {'message': 'No executions recorded'}
        
        # Calculate summary statistics
        durations = [ex.get('duration', 0) for ex in recent_executions]
        quality_scores = [ex.get('content_quality', 0) for ex in recent_executions]
        
        summary = {
            'total_executions': len(recent_executions),
            'average_duration': sum(durations) / len(durations) if durations else 0,
            'average_quality': sum(quality_scores) / len(quality_scores) if quality_scores else 0,
            'min_duration': min(durations) if durations else 0,
            'max_duration': max(durations) if durations else 0,
            'min_quality': min(quality_scores) if quality_scores else 0,
            'max_quality': max(quality_scores) if quality_scores else 0,
            'recent_executions': recent_executions
        }
        
        return summary
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Generate a comprehensive performance report."""
        if not self.execution_history:
            return {'message': 'No execution history available'}
        
        # Calculate performance metrics
        durations = [ex.get('duration', 0) for ex in self.execution_history]
        quality_scores = [ex.get('content_quality', 0) for ex in self.execution_history]
        
        # Performance trends
        recent_durations = durations[-10:] if len(durations) >= 10 else durations
        recent_quality = quality_scores[-10:] if len(quality_scores) >= 10 else quality_scores
        
        report = {
            'total_executions': len(self.execution_history),
            'performance_metrics': {
                'average_duration': sum(durations) / len(durations) if durations else 0,
                'average_quality': sum(quality_scores) / len(quality_scores) if quality_scores else 0,
                'min_duration': min(durations) if durations else 0,
                'max_duration': max(durations) if durations else 0,
                'min_quality': min(quality_scores) if quality_scores else 0,
                'max_quality': max(quality_scores) if quality_scores else 0
            },
            'recent_trends': {
                'recent_avg_duration': sum(recent_durations) / len(recent_durations) if recent_durations else 0,
                'recent_avg_quality': sum(recent_quality) / len(recent_quality) if recent_quality else 0
            },
            'system_metrics': self._get_system_info(),
            'execution_history': self.execution_history[-5:]  # Last 5 executions
        }
        
        return report
    
    def save_performance_report(self, filename: Optional[str] = None):
        """Save performance report to file."""
        report = self.get_performance_report()
        
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"performance_report_{timestamp}.json"
        
        filepath = self.metrics_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Performance report saved to {filepath}")
        return str(filepath)
    
    def clear_history(self):
        """Clear execution history."""
        self.execution_history.clear()
        logger.info("Execution history cleared")
    
    def get_metrics_files(self) -> List[str]:
        """Get list of available metrics files."""
        metrics_files = list(self.metrics_dir.glob('*.json'))
        return [str(f) for f in metrics_files]
    
    def load_execution_record(self, filename: str) -> Optional[Dict[str, Any]]:
        """Load a specific execution record from file."""
        filepath = self.metrics_dir / filename
        
        if not filepath.exists():
            logger.warning(f"Metrics file not found: {filepath}")
            return None
        
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading metrics file {filepath}: {e}")
            return None
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get current health status of the monitoring system."""
        try:
            # Check if metrics directory exists and is writable
            metrics_writable = self.metrics_dir.exists() and self.metrics_dir.is_dir()
            
            # Check system resources
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            health_status = {
                'status': 'healthy',
                'metrics_directory': str(self.metrics_dir),
                'metrics_writable': metrics_writable,
                'execution_history_size': len(self.execution_history),
                'system_resources': {
                    'memory_percent': memory.percent,
                    'disk_percent': disk.percent,
                    'cpu_percent': psutil.cpu_percent()
                }
            }
            
            # Check for potential issues
            if memory.percent > 90:
                health_status['status'] = 'warning'
                health_status['warnings'] = ['High memory usage']
            
            if disk.percent > 90:
                health_status['status'] = 'warning'
                health_status['warnings'] = health_status.get('warnings', []) + ['High disk usage']
            
            if not metrics_writable:
                health_status['status'] = 'error'
                health_status['errors'] = ['Metrics directory not writable']
            
            return health_status
            
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }