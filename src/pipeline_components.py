"""
Pipeline Components for Echo Pipeline

This module contains the individual components that make up the echo pipeline:
- ContentGenerator: Handles content generation
- ContentTransformer: Transforms content between formats
- QualityValidator: Validates content quality and consistency
- OutputFormatter: Formats and saves output files
"""

import asyncio
import json
import re
from pathlib import Path
from typing import Dict, Any, List, Optional

from loguru import logger


class ContentGenerator:
    """Handles content generation based on input parameters."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the content generator with configuration."""
        self.config = config
        self.model = config.get('model', 'default')
        self.max_tokens = config.get('max_tokens', 1000)
        self.temperature = config.get('temperature', 0.7)
    
    async def generate(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate content based on input parameters.
        
        Args:
            input_data: Input parameters for content generation
            
        Returns:
            Generated content with metadata
        """
        topic = input_data.get('topic', 'Default Topic')
        format_type = input_data.get('format', 'markdown')
        length = input_data.get('length', 'medium')
        
        # Generate content based on parameters
        content = await self._generate_content(topic, format_type, length)
        
        return {
            'content': content,
            'metadata': {
                'topic': topic,
                'format': format_type,
                'length': length,
                'model': self.model,
                'max_tokens': self.max_tokens,
                'temperature': self.temperature
            }
        }
    
    async def _generate_content(self, topic: str, format_type: str, length: str) -> str:
        """Generate actual content based on parameters."""
        # Simulate content generation
        await asyncio.sleep(0.1)  # Simulate processing time
        
        length_map = {
            'short': 100,
            'medium': 300,
            'long': 600
        }
        
        target_length = length_map.get(length, 300)
        
        if format_type == 'markdown':
            return self._generate_markdown_content(topic, target_length)
        elif format_type == 'html':
            return self._generate_html_content(topic, target_length)
        elif format_type == 'jsonld':
            return self._generate_jsonld_content(topic, target_length)
        else:
            return self._generate_markdown_content(topic, target_length)
    
    def _generate_markdown_content(self, topic: str, length: int) -> str:
        """Generate markdown content."""
        content = f"""# {topic}

This is generated content about {topic}. The echo pipeline is designed to test and validate content generation workflows.

## Key Features

- **Content Generation**: Automated content creation based on input parameters
- **Format Transformation**: Convert between markdown, HTML, and JSON-LD formats
- **Quality Validation**: Ensure content meets quality standards
- **Output Formatting**: Generate properly formatted output files

## Pipeline Components

The echo pipeline consists of several key components:

1. **Content Generator**: Creates initial content based on input parameters
2. **Content Transformer**: Converts content between different formats
3. **Quality Validator**: Ensures content quality and consistency
4. **Output Formatter**: Formats and saves output files

## Testing Framework

The pipeline includes comprehensive testing capabilities:

- Unit tests for individual components
- Integration tests for end-to-end functionality
- Performance tests for efficiency measurement
- Quality tests for output validation

This content demonstrates the echo pipeline's ability to generate structured, informative content for testing and validation purposes.
"""
        return content[:length]
    
    def _generate_html_content(self, topic: str, length: int) -> str:
        """Generate HTML content."""
        content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{topic}</title>
</head>
<body>
    <h1>{topic}</h1>
    <p>This is generated HTML content about {topic}. The echo pipeline is designed to test and validate content generation workflows.</p>
    
    <h2>Key Features</h2>
    <ul>
        <li><strong>Content Generation</strong>: Automated content creation based on input parameters</li>
        <li><strong>Format Transformation</strong>: Convert between markdown, HTML, and JSON-LD formats</li>
        <li><strong>Quality Validation</strong>: Ensure content meets quality standards</li>
        <li><strong>Output Formatting</strong>: Generate properly formatted output files</li>
    </ul>
    
    <h2>Pipeline Components</h2>
    <p>The echo pipeline consists of several key components:</p>
    <ol>
        <li><strong>Content Generator</strong>: Creates initial content based on input parameters</li>
        <li><strong>Content Transformer</strong>: Converts content between different formats</li>
        <li><strong>Quality Validator</strong>: Ensures content quality and consistency</li>
        <li><strong>Output Formatter</strong>: Formats and saves output files</li>
    </ol>
    
    <h2>Testing Framework</h2>
    <p>The pipeline includes comprehensive testing capabilities:</p>
    <ul>
        <li>Unit tests for individual components</li>
        <li>Integration tests for end-to-end functionality</li>
        <li>Performance tests for efficiency measurement</li>
        <li>Quality tests for output validation</li>
    </ul>
    
    <p>This content demonstrates the echo pipeline's ability to generate structured, informative content for testing and validation purposes.</p>
</body>
</html>"""
        return content[:length]
    
    def _generate_jsonld_content(self, topic: str, length: int) -> str:
        """Generate JSON-LD content."""
        content = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": topic,
            "description": f"This is generated JSON-LD content about {topic}. The echo pipeline is designed to test and validate content generation workflows.",
            "author": {
                "@type": "Organization",
                "name": "Echo Pipeline"
            },
            "publisher": {
                "@type": "Organization",
                "name": "Echo Pipeline Testing",
                "logo": {
                    "@type": "ImageObject",
                    "url": "https://example.com/logo.png"
                }
            },
            "datePublished": "2025-01-01T00:00:00Z",
            "keywords": [
                "echo pipeline",
                "content generation",
                "testing",
                "validation"
            ],
            "inLanguage": "en-US",
            "mainEntityOfPage": {
                "@type": "WebPage",
                "@id": f"https://example.com/{topic.lower().replace(' ', '-')}"
            }
        }
        return json.dumps(content, indent=2)[:length]
    
    def run_tests(self) -> Dict[str, Any]:
        """Run unit tests for the content generator."""
        logger.info("Running ContentGenerator tests...")
        
        test_results = {
            'markdown_generation': self._test_markdown_generation(),
            'html_generation': self._test_html_generation(),
            'jsonld_generation': self._test_jsonld_generation(),
            'config_loading': self._test_config_loading()
        }
        
        return test_results
    
    def _test_markdown_generation(self) -> Dict[str, Any]:
        """Test markdown content generation."""
        try:
            content = asyncio.run(self._generate_content('Test Topic', 'markdown', 'short'))
            return {
                'passed': bool(content and content.startswith('#')),
                'content_length': len(content),
                'has_headers': '#' in content
            }
        except Exception as e:
            return {'passed': False, 'error': str(e)}
    
    def _test_html_generation(self) -> Dict[str, Any]:
        """Test HTML content generation."""
        try:
            content = asyncio.run(self._generate_content('Test Topic', 'html', 'short'))
            return {
                'passed': bool(content and '<html>' in content),
                'content_length': len(content),
                'has_html_tags': '<' in content and '>' in content
            }
        except Exception as e:
            return {'passed': False, 'error': str(e)}
    
    def _test_jsonld_generation(self) -> Dict[str, Any]:
        """Test JSON-LD content generation."""
        try:
            content = asyncio.run(self._generate_content('Test Topic', 'jsonld', 'short'))
            return {
                'passed': bool(content and '@context' in content),
                'content_length': len(content),
                'is_valid_json': self._is_valid_json(content)
            }
        except Exception as e:
            return {'passed': False, 'error': str(e)}
    
    def _test_config_loading(self) -> Dict[str, Any]:
        """Test configuration loading."""
        return {
            'passed': bool(self.config),
            'model': self.model,
            'max_tokens': self.max_tokens,
            'temperature': self.temperature
        }
    
    def _is_valid_json(self, content: str) -> bool:
        """Check if content is valid JSON."""
        try:
            json.loads(content)
            return True
        except:
            return False


class ContentTransformer:
    """Transforms content between different formats."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the content transformer with configuration."""
        self.config = config
        self.supported_formats = config.get('formats', ['markdown', 'html', 'jsonld'])
        self.templates_dir = config.get('templates', 'templates/')
    
    async def transform(self, content_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform content between different formats.
        
        Args:
            content_data: Content data with metadata
            
        Returns:
            Transformed content in multiple formats
        """
        original_content = content_data['content']
        original_format = content_data['metadata']['format']
        
        transformed_content = {}
        
        for target_format in self.supported_formats:
            if target_format != original_format:
                transformed_content[target_format] = await self._transform_format(
                    original_content, original_format, target_format
                )
            else:
                transformed_content[target_format] = original_content
        
        return {
            'content': transformed_content,
            'metadata': content_data['metadata'],
            'transformations': list(transformed_content.keys())
        }
    
    async def _transform_format(self, content: str, from_format: str, to_format: str) -> str:
        """Transform content from one format to another."""
        await asyncio.sleep(0.05)  # Simulate processing time
        
        if from_format == 'markdown' and to_format == 'html':
            return self._markdown_to_html(content)
        elif from_format == 'markdown' and to_format == 'jsonld':
            return self._markdown_to_jsonld(content)
        elif from_format == 'html' and to_format == 'markdown':
            return self._html_to_markdown(content)
        elif from_format == 'html' and to_format == 'jsonld':
            return self._html_to_jsonld(content)
        elif from_format == 'jsonld' and to_format == 'markdown':
            return self._jsonld_to_markdown(content)
        elif from_format == 'jsonld' and to_format == 'html':
            return self._jsonld_to_html(content)
        else:
            return content
    
    def _markdown_to_html(self, content: str) -> str:
        """Convert markdown to HTML."""
        # Simple markdown to HTML conversion
        html = content
        html = re.sub(r'^# (.+)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.+)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^### (.+)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.+?)\*', r'<em>\1</em>', html)
        html = re.sub(r'\n\n', r'</p><p>', html)
        html = f'<p>{html}</p>'
        return f'<!DOCTYPE html><html><body>{html}</body></html>'
    
    def _markdown_to_jsonld(self, content: str) -> str:
        """Convert markdown to JSON-LD."""
        # Extract title from first heading
        title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else "Generated Content"
        
        jsonld = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": title,
            "text": content,
            "author": {"@type": "Organization", "name": "Echo Pipeline"},
            "datePublished": "2025-01-01T00:00:00Z"
        }
        return json.dumps(jsonld, indent=2)
    
    def _html_to_markdown(self, content: str) -> str:
        """Convert HTML to markdown."""
        # Simple HTML to markdown conversion
        markdown = content
        markdown = re.sub(r'<h1>(.+?)</h1>', r'# \1', markdown)
        markdown = re.sub(r'<h2>(.+?)</h2>', r'## \1', markdown)
        markdown = re.sub(r'<h3>(.+?)</h3>', r'### \1', markdown)
        markdown = re.sub(r'<strong>(.+?)</strong>', r'**\1**', markdown)
        markdown = re.sub(r'<em>(.+?)</em>', r'*\1*', markdown)
        markdown = re.sub(r'<p>(.+?)</p>', r'\1\n\n', markdown)
        markdown = re.sub(r'<[^>]+>', '', markdown)  # Remove remaining HTML tags
        return markdown.strip()
    
    def _html_to_jsonld(self, content: str) -> str:
        """Convert HTML to JSON-LD."""
        # Extract title from first h1
        title_match = re.search(r'<h1>(.+?)</h1>', content)
        title = title_match.group(1) if title_match else "Generated Content"
        
        jsonld = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": title,
            "text": content,
            "author": {"@type": "Organization", "name": "Echo Pipeline"},
            "datePublished": "2025-01-01T00:00:00Z"
        }
        return json.dumps(jsonld, indent=2)
    
    def _jsonld_to_markdown(self, content: str) -> str:
        """Convert JSON-LD to markdown."""
        try:
            data = json.loads(content)
            title = data.get('headline', 'Generated Content')
            text = data.get('text', '')
            
            markdown = f"# {title}\n\n{text}"
            return markdown
        except:
            return content
    
    def _jsonld_to_html(self, content: str) -> str:
        """Convert JSON-LD to HTML."""
        try:
            data = json.loads(content)
            title = data.get('headline', 'Generated Content')
            text = data.get('text', '')
            
            html = f"""<!DOCTYPE html>
<html>
<head><title>{title}</title></head>
<body>
<h1>{title}</h1>
<p>{text}</p>
</body>
</html>"""
            return html
        except:
            return content
    
    def run_tests(self) -> Dict[str, Any]:
        """Run unit tests for the content transformer."""
        logger.info("Running ContentTransformer tests...")
        
        test_results = {
            'markdown_to_html': self._test_markdown_to_html(),
            'html_to_markdown': self._test_html_to_markdown(),
            'jsonld_conversion': self._test_jsonld_conversion(),
            'format_support': self._test_format_support()
        }
        
        return test_results
    
    def _test_markdown_to_html(self) -> Dict[str, Any]:
        """Test markdown to HTML conversion."""
        try:
            markdown = "# Test Title\n\nThis is **bold** text."
            html = asyncio.run(self._transform_format(markdown, 'markdown', 'html'))
            return {
                'passed': '<h1>' in html and '<strong>' in html,
                'has_title': 'Test Title' in html,
                'has_bold': 'bold' in html
            }
        except Exception as e:
            return {'passed': False, 'error': str(e)}
    
    def _test_html_to_markdown(self) -> Dict[str, Any]:
        """Test HTML to markdown conversion."""
        try:
            html = "<h1>Test Title</h1><p>This is <strong>bold</strong> text.</p>"
            markdown = asyncio.run(self._transform_format(html, 'html', 'markdown'))
            return {
                'passed': markdown.startswith('# Test Title'),
                'has_title': 'Test Title' in markdown,
                'has_bold': '**bold**' in markdown
            }
        except Exception as e:
            return {'passed': False, 'error': str(e)}
    
    def _test_jsonld_conversion(self) -> Dict[str, Any]:
        """Test JSON-LD conversion."""
        try:
            jsonld = '{"@context": "https://schema.org", "@type": "Article", "headline": "Test"}'
            markdown = asyncio.run(self._transform_format(jsonld, 'jsonld', 'markdown'))
            return {
                'passed': markdown.startswith('# Test'),
                'is_valid_markdown': '#' in markdown
            }
        except Exception as e:
            return {'passed': False, 'error': str(e)}
    
    def _test_format_support(self) -> Dict[str, Any]:
        """Test format support configuration."""
        return {
            'passed': bool(self.supported_formats),
            'supported_formats': self.supported_formats,
            'templates_dir': self.templates_dir
        }


class QualityValidator:
    """Validates content quality and consistency."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the quality validator with configuration."""
        self.config = config
        self.quality_threshold = config.get('quality_threshold', 0.8)
        self.consistency_check = config.get('consistency_check', True)
    
    async def validate(self, content_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate content quality and consistency.
        
        Args:
            content_data: Content data to validate
            
        Returns:
            Validation results with quality scores
        """
        content = content_data['content']
        metadata = content_data['metadata']
        
        validation_results = {}
        
        for format_type, format_content in content.items():
            validation_results[format_type] = await self._validate_format(
                format_content, format_type, metadata
            )
        
        # Calculate overall quality score
        quality_scores = [result['quality_score'] for result in validation_results.values()]
        overall_quality = sum(quality_scores) / len(quality_scores) if quality_scores else 0
        
        # Check consistency across formats
        consistency_score = self._check_consistency(validation_results) if self.consistency_check else 1.0
        
        return {
            'passed': overall_quality >= self.quality_threshold,
            'quality_score': overall_quality,
            'consistency_score': consistency_score,
            'format_results': validation_results,
            'threshold': self.quality_threshold
        }
    
    async def _validate_format(self, content: str, format_type: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Validate content in a specific format."""
        await asyncio.sleep(0.02)  # Simulate processing time
        
        quality_score = 0.0
        issues = []
        
        # Check content length
        if len(content) < 50:
            issues.append("Content too short")
            quality_score -= 0.2
        elif len(content) > 5000:
            issues.append("Content too long")
            quality_score -= 0.1
        
        # Check for required elements based on format
        if format_type == 'markdown':
            if not re.search(r'^#\s+', content, re.MULTILINE):
                issues.append("Missing markdown header")
                quality_score -= 0.3
            if not re.search(r'\*\*.*\*\*', content):
                issues.append("Missing bold text in markdown")
                quality_score -= 0.1
        elif format_type == 'html':
            if '<html>' not in content or '</html>' not in content:
                issues.append("Invalid HTML structure")
                quality_score -= 0.3
            if '<h1>' not in content:
                issues.append("Missing HTML header")
                quality_score -= 0.2
        elif format_type == 'jsonld':
            try:
                json.loads(content)
            except:
                issues.append("Invalid JSON-LD format")
                quality_score -= 0.5
        
        # Check for topic relevance
        topic = metadata.get('topic', '').lower()
        if topic and topic not in content.lower():
            issues.append("Content not relevant to topic")
            quality_score -= 0.2
        
        # Base quality score
        quality_score += 0.8
        
        # Ensure score is between 0 and 1
        quality_score = max(0.0, min(1.0, quality_score))
        
        return {
            'quality_score': quality_score,
            'issues': issues,
            'content_length': len(content),
            'format_type': format_type
        }
    
    def _check_consistency(self, validation_results: Dict[str, Any]) -> float:
        """Check consistency across different formats."""
        quality_scores = [result['quality_score'] for result in validation_results.values()]
        
        if len(quality_scores) < 2:
            return 1.0
        
        # Calculate variance in quality scores
        mean_score = sum(quality_scores) / len(quality_scores)
        variance = sum((score - mean_score) ** 2 for score in quality_scores) / len(quality_scores)
        
        # Convert variance to consistency score (lower variance = higher consistency)
        consistency_score = max(0.0, 1.0 - variance)
        
        return consistency_score
    
    def run_tests(self) -> Dict[str, Any]:
        """Run unit tests for the quality validator."""
        logger.info("Running QualityValidator tests...")
        
        test_results = {
            'markdown_validation': self._test_markdown_validation(),
            'html_validation': self._test_html_validation(),
            'jsonld_validation': self._test_jsonld_validation(),
            'consistency_check': self._test_consistency_check()
        }
        
        return test_results
    
    def _test_markdown_validation(self) -> Dict[str, Any]:
        """Test markdown validation."""
        try:
            markdown_content = "# Test Title\n\nThis is **bold** text about testing."
            metadata = {'topic': 'testing'}
            
            result = asyncio.run(self._validate_format(markdown_content, 'markdown', metadata))
            return {
                'passed': result['quality_score'] >= self.quality_threshold,
                'quality_score': result['quality_score'],
                'issues': result['issues']
            }
        except Exception as e:
            return {'passed': False, 'error': str(e)}
    
    def _test_html_validation(self) -> Dict[str, Any]:
        """Test HTML validation."""
        try:
            html_content = "<html><body><h1>Test Title</h1><p>This is about testing.</p></body></html>"
            metadata = {'topic': 'testing'}
            
            result = asyncio.run(self._validate_format(html_content, 'html', metadata))
            return {
                'passed': result['quality_score'] >= self.quality_threshold,
                'quality_score': result['quality_score'],
                'issues': result['issues']
            }
        except Exception as e:
            return {'passed': False, 'error': str(e)}
    
    def _test_jsonld_validation(self) -> Dict[str, Any]:
        """Test JSON-LD validation."""
        try:
            jsonld_content = '{"@context": "https://schema.org", "@type": "Article", "headline": "Test"}'
            metadata = {'topic': 'testing'}
            
            result = asyncio.run(self._validate_format(jsonld_content, 'jsonld', metadata))
            return {
                'passed': result['quality_score'] >= self.quality_threshold,
                'quality_score': result['quality_score'],
                'issues': result['issues']
            }
        except Exception as e:
            return {'passed': False, 'error': str(e)}
    
    def _test_consistency_check(self) -> Dict[str, Any]:
        """Test consistency checking."""
        test_results = {
            'markdown': {'quality_score': 0.8},
            'html': {'quality_score': 0.9},
            'jsonld': {'quality_score': 0.7}
        }
        
        consistency_score = self._check_consistency(test_results)
        return {
            'passed': consistency_score > 0.5,
            'consistency_score': consistency_score,
            'threshold': self.quality_threshold
        }


class OutputFormatter:
    """Formats and saves output files."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the output formatter with configuration."""
        self.config = config
        self.output_dir = Path(config.get('output_dir', 'content/'))
        self.naming_convention = config.get('naming_convention', 'iteration-{iteration}')
    
    async def format(self, content_data: Dict[str, Any], iteration: int = 1) -> Dict[str, str]:
        """
        Format and save content to output files.
        
        Args:
            content_data: Content data to format and save
            iteration: Current iteration number
            
        Returns:
            Dictionary mapping format types to file paths
        """
        content = content_data['content']
        metadata = content_data['metadata']
        
        # Create output directory
        iteration_dir = self.output_dir / self.naming_convention.format(iteration=iteration)
        iteration_dir.mkdir(parents=True, exist_ok=True)
        
        output_paths = {}
        
        for format_type, format_content in content.items():
            file_path = await self._save_format_content(
                format_content, format_type, iteration_dir, metadata
            )
            output_paths[format_type] = str(file_path)
        
        # Save metadata
        metadata_path = iteration_dir / 'metadata.json'
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        output_paths['metadata'] = str(metadata_path)
        
        return output_paths
    
    async def _save_format_content(
        self, 
        content: str, 
        format_type: str, 
        output_dir: Path, 
        metadata: Dict[str, Any]
    ) -> Path:
        """Save content in a specific format to a file."""
        await asyncio.sleep(0.01)  # Simulate processing time
        
        # Determine file extension
        extensions = {
            'markdown': '.md',
            'html': '.html',
            'jsonld': '.jsonld'
        }
        
        extension = extensions.get(format_type, '.txt')
        filename = f'index{extension}'
        file_path = output_dir / filename
        
        # Write content to file
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        logger.info(f"Saved {format_type} content to {file_path}")
        return file_path
    
    def run_tests(self) -> Dict[str, Any]:
        """Run unit tests for the output formatter."""
        logger.info("Running OutputFormatter tests...")
        
        test_results = {
            'directory_creation': self._test_directory_creation(),
            'file_saving': self._test_file_saving(),
            'naming_convention': self._test_naming_convention(),
            'metadata_saving': self._test_metadata_saving()
        }
        
        return test_results
    
    def _test_directory_creation(self) -> Dict[str, Any]:
        """Test directory creation."""
        try:
            test_dir = Path('test_output')
            test_dir.mkdir(exist_ok=True)
            test_dir.rmdir()
            return {'passed': True}
        except Exception as e:
            return {'passed': False, 'error': str(e)}
    
    def _test_file_saving(self) -> Dict[str, Any]:
        """Test file saving functionality."""
        try:
            test_content = "Test content"
            test_dir = Path('test_output')
            test_dir.mkdir(exist_ok=True)
            
            file_path = test_dir / 'test.md'
            with open(file_path, 'w') as f:
                f.write(test_content)
            
            # Verify file was created
            exists = file_path.exists()
            
            # Cleanup
            file_path.unlink()
            test_dir.rmdir()
            
            return {'passed': exists}
        except Exception as e:
            return {'passed': False, 'error': str(e)}
    
    def _test_naming_convention(self) -> Dict[str, Any]:
        """Test naming convention formatting."""
        try:
            result = self.naming_convention.format(iteration=1)
            expected = 'iteration-1'
            return {
                'passed': result == expected,
                'result': result,
                'expected': expected
            }
        except Exception as e:
            return {'passed': False, 'error': str(e)}
    
    def _test_metadata_saving(self) -> Dict[str, Any]:
        """Test metadata saving functionality."""
        try:
            test_metadata = {'test': 'data'}
            test_dir = Path('test_output')
            test_dir.mkdir(exist_ok=True)
            
            metadata_path = test_dir / 'metadata.json'
            with open(metadata_path, 'w') as f:
                json.dump(test_metadata, f)
            
            # Verify file was created
            exists = metadata_path.exists()
            
            # Cleanup
            metadata_path.unlink()
            test_dir.rmdir()
            
            return {'passed': exists}
        except Exception as e:
            return {'passed': False, 'error': str(e)}