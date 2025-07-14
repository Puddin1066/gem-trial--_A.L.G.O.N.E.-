# Echo Pipeline Documentation

This directory contains comprehensive documentation for the Echo Pipeline testing and execution framework.

## Overview

The Echo Pipeline is a comprehensive system designed for testing and executing content generation workflows. It provides a complete framework for generating, transforming, validating, and formatting content across multiple formats.

## Architecture

The pipeline consists of four main components:

### 1. Content Generator
- **Purpose**: Creates initial content based on input parameters
- **Features**: 
  - Multi-format content generation (markdown, HTML, JSON-LD)
  - Configurable content length and style
  - Template-based generation
- **Configuration**: `config/pipeline_config.yaml` → `generator` section

### 2. Content Transformer
- **Purpose**: Converts content between different formats
- **Features**:
  - Bidirectional format conversion
  - Preserves content structure and metadata
  - Configurable conversion options
- **Configuration**: `config/pipeline_config.yaml` → `transformer` section

### 3. Quality Validator
- **Purpose**: Ensures content meets quality standards
- **Features**:
  - Format-specific validation rules
  - Content quality scoring
  - Consistency checking across formats
- **Configuration**: `config/pipeline_config.yaml` → `validator` section

### 4. Output Formatter
- **Purpose**: Formats and saves output files
- **Features**:
  - Multi-format output generation
  - Metadata preservation
  - Configurable naming conventions
- **Configuration**: `config/pipeline_config.yaml` → `formatter` section

## Testing Framework

The Echo Pipeline includes a comprehensive testing framework with four test types:

### Unit Tests
- **Scope**: Individual component testing
- **Coverage**: Each pipeline component
- **Execution**: `python tests/run_pipeline_tests.py --unit-only`

### Integration Tests
- **Scope**: End-to-end pipeline functionality
- **Coverage**: Complete workflow testing
- **Execution**: `python tests/run_pipeline_tests.py --integration-only`

### Performance Tests
- **Scope**: Load and efficiency testing
- **Coverage**: Execution time, memory usage, throughput
- **Execution**: `python tests/run_pipeline_tests.py --performance-only`

### Quality Tests
- **Scope**: Output validation and consistency
- **Coverage**: Content quality, format consistency
- **Execution**: `python tests/run_pipeline_tests.py --quality-only`

## Configuration

### Pipeline Configuration (`config/pipeline_config.yaml`)
Main configuration file containing settings for all pipeline components:

```yaml
generator:
  model: "default"
  max_tokens: 1000
  temperature: 0.7

transformer:
  formats: ["markdown", "html", "jsonld"]
  templates: "templates/"

validator:
  quality_threshold: 0.8
  consistency_check: true

formatter:
  output_dir: "content/"
  naming_convention: "iteration-{iteration}"
```

### Test Configuration (`config/test_config.yaml`)
Testing-specific configuration:

```yaml
unit_tests:
  enabled: true
  timeout: 30

integration_tests:
  enabled: true
  timeout: 60

performance_tests:
  enabled: true
  iterations: 5

quality_tests:
  enabled: true
  consistency_threshold: 0.7
```

## Usage Examples

### Basic Pipeline Execution
```bash
# Run content generation
python src/echo_pipeline.py --input input_data.json --iteration 1

# Run with custom configuration
python src/echo_pipeline.py --config config/custom_config.yaml --input input_data.json
```

### Testing Execution
```bash
# Run complete test suite
python tests/run_pipeline_tests.py

# Run specific test types
python tests/run_pipeline_tests.py --unit-only
python tests/run_pipeline_tests.py --performance-only

# Run with custom test configuration
python tests/run_pipeline_tests.py --config config/test_config.yaml
```

### Input Data Format
```json
{
  "topic": "Echo Pipeline Testing",
  "format": "markdown",
  "length": "medium",
  "additional_params": {
    "style": "technical",
    "tone": "professional"
  }
}
```

## Monitoring and Metrics

The pipeline provides comprehensive monitoring capabilities:

### Real-time Metrics
- Execution time tracking
- Memory usage monitoring
- CPU utilization
- Quality score tracking

### Performance Reports
- Historical execution data
- Performance trends
- Resource usage analysis
- Quality score trends

### Health Monitoring
- System resource monitoring
- Pipeline health checks
- Error tracking and reporting
- Performance alerts

## Output Structure

The pipeline generates output in the following structure:

```
content/
├── iteration-1/
│   ├── index.md          # Markdown content
│   ├── index.html        # HTML content
│   ├── index.jsonld      # JSON-LD content
│   └── metadata.json     # Generation metadata
├── iteration-2/
│   └── ...
└── ...

metrics/
├── execution_*.json      # Execution records
├── performance_*.json    # Performance reports
└── ...

reports/
├── test_report.json      # Test execution reports
└── ...
```

## Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check Python path includes src directory

2. **Configuration Errors**
   - Validate YAML syntax in configuration files
   - Check file paths in configuration

3. **Test Failures**
   - Review test logs in `logs/test_execution.log`
   - Check test configuration in `config/test_config.yaml`

4. **Performance Issues**
   - Monitor system resources during execution
   - Adjust timeout values in configuration
   - Check memory usage limits

### Debug Mode
Enable verbose logging for debugging:

```bash
python tests/run_pipeline_tests.py --verbose
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

MIT License - see LICENSE file for details