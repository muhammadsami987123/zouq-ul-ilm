# PPT Generation System Architecture

## Overview

The PPT Generation system has been restructured into a modular, maintainable architecture that follows software engineering best practices. This document outlines the new structure and how to use it.

## Directory Structure

```
PPT_gen/
├── config/                     # Configuration management
│   ├── __init__.py
│   ├── settings.py            # Application settings with Pydantic
│   └── constants.py           # Application constants and configurations
│
├── models/                     # Data models and schemas
│   ├── __init__.py
│   ├── content_models.py      # Content-related data models
│   ├── template_models.py     # Template-related data models
│   └── processing_models.py   # Processing-related data models
│
├── services/                   # Business logic services
│   ├── __init__.py
│   ├── ai_service.py          # AI/ML service for Gemini integration
│   ├── content_service.py     # Content processing service
│   ├── template_service.py    # Template management service
│   ├── presentation_service.py # Presentation creation service
│   └── processing_service.py  # Main processing orchestration
│
├── utils/                      # Utility functions
│   ├── __init__.py
│   ├── text_utils.py          # Text processing utilities
│   ├── file_utils.py          # File operation utilities
│   ├── ai_utils.py            # AI-related utilities
│   └── logging_utils.py       # Logging utilities
│
├── templates/                  # PowerPoint templates
│   ├── template_metadata.json # Template metadata and configuration
│   ├── polyhedron.pptx        # Modern geometric template
│   ├── blue.pptx              # Professional blue template
│   ├── green.pptx             # Academic green template
│   ├── silver_stone.pptx      # Elegant silver template
│   ├── gradation_green.pptx   # Gradient green template
│   └── yellow_subhan.pptx     # Academic yellow template
│
├── output/                     # Generated output files
│   ├── presentations/          # Generated PowerPoint files
│   ├── notes/                  # Generated notes files
│   ├── temp/                   # Temporary processing files
│   └── backups/                # Backup files
│
├── logs/                       # Log files
├── tests/                      # Unit tests
├── docs/                       # Documentation
│
├── main.py                     # Original main file (legacy)
├── main_new.py                 # New modular main file
├── emotion.py                  # Original PPT generator (legacy)
└── requirements.txt            # Python dependencies
```

## Key Components

### 1. Configuration Module (`config/`)

**Purpose**: Centralized configuration management using Pydantic for validation.

**Key Files**:
- `settings.py`: Application settings with environment variable support
- `constants.py`: Application constants, AI model configurations, and templates

**Features**:
- Environment variable integration
- Type validation with Pydantic
- API key management
- Quality thresholds and processing limits

### 2. Models Module (`models/`)

**Purpose**: Data models and schemas for type safety and validation.

**Key Models**:
- `Topic`: Represents extracted topics
- `SlideContent`: Slide content structure
- `PresentationData`: Complete presentation data
- `TemplateInfo`: Template metadata and information
- `ProcessingConfig`: Processing configuration
- `ProcessingResult`: Processing operation results

**Features**:
- Pydantic models for validation
- Type hints throughout
- Serialization support
- Business logic methods

### 3. Services Module (`services/`)

**Purpose**: Business logic and core functionality.

**Key Services**:
- `AIService`: Google Gemini AI integration
- `TemplateService`: Template management and selection
- `ContentService`: Content processing and generation
- `PresentationService`: PowerPoint creation
- `ProcessingService`: Main processing orchestration

**Features**:
- Separation of concerns
- Dependency injection ready
- Error handling and logging
- Configurable and testable

### 4. Utils Module (`utils/`)

**Purpose**: Reusable utility functions.

**Key Utilities**:
- `text_utils.py`: Text processing, cleaning, and validation
- `file_utils.py`: File operations and management
- `ai_utils.py`: AI-related helper functions
- `logging_utils.py`: Logging configuration and helpers

**Features**:
- Pure functions where possible
- Comprehensive error handling
- Performance optimizations
- Extensive documentation

## Usage Examples

### Basic Usage

```python
from PPT_gen.main_new import PPTGenerator

# Initialize generator
generator = PPTGenerator()

# Process a document
result = generator.process_document(
    input_file="path/to/document.pdf",
    template_name="polyhedron",
    output_dir="output/presentations"
)

if result.success:
    print(f"✅ Presentation created: {result.message}")
    print(f"📊 Slides generated: {result.slides_generated}")
else:
    print(f"❌ Error: {result.message}")
```

### Advanced Configuration

```python
from PPT_gen.models import ProcessingConfig
from PPT_gen.main_new import PPTGenerator

# Create custom configuration
config = ProcessingConfig(
    input_file_path="document.pdf",
    template_name="blue",
    output_directory="custom_output",
    max_pages=20,
    max_slides=30,
    temperature=0.5,
    min_bullet_length=60,
    max_bullet_length=180
)

# Initialize generator
generator = PPTGenerator()

# Process with custom config
result = generator.process_document(
    input_file="document.pdf",
    config=config
)
```

### Template Management

```python
from PPT_gen.main_new import PPTGenerator

generator = PPTGenerator()

# Get available templates
templates = generator.get_available_templates()
for template in templates:
    print(f"Template: {template['display_name']}")
    print(f"Category: {template['category']}")
    print(f"Description: {template['description']}")

# Get template info
template_info = generator.get_template_info("polyhedron")
print(f"Template details: {template_info}")

# Validate template
is_valid = generator.validate_template("blue")
print(f"Template valid: {is_valid}")
```

### Service-Level Usage

```python
from PPT_gen.services import AIService, TemplateService

# Initialize services
ai_service = AIService()
template_service = TemplateService()

# Extract topics
topics = ai_service.extract_topics("Your document text here")

# Generate slide content
bullets = ai_service.generate_slide_content(
    topic="Machine Learning",
    subject_context="Computer Science"
)

# Get suitable templates
suitable_templates = template_service.get_suitable_templates("Computer Science")
```

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# API Configuration
GOOGLE_API_KEY=your_api_key_here
API_KEY_1=backup_key_1
API_KEY_2=backup_key_2
API_KEY_3=backup_key_3

# Processing Configuration
MAX_PAGES_PER_DOCUMENT=50
RATE_LIMIT_DELAY=2.0
MAX_RETRIES=3

# Content Generation
DEFAULT_TEMPERATURE=0.4
DEFAULT_TOP_K=50
DEFAULT_TOP_P=0.9
MAX_OUTPUT_TOKENS=800

# Quality Thresholds
MIN_BULLET_LENGTH=50
MAX_BULLET_LENGTH=200
MIN_WORD_COUNT=8
SIMILARITY_THRESHOLD=0.7

# File Paths
TEMPLATES_DIR=templates
OUTPUT_DIR=output
LOGS_DIR=logs
TEMP_DIR=temp

# Logging
LOG_LEVEL=INFO
DEBUG_MODE=false
```

### Settings Customization

```python
from PPT_gen.config import get_settings

# Get current settings
settings = get_settings()

# Access configuration
print(f"Templates directory: {settings.templates_dir}")
print(f"Output directory: {settings.output_dir}")
print(f"Available API keys: {len(settings.get_api_keys())}")

# Get random API key
api_key = settings.get_random_api_key()
```

## Error Handling

The new architecture includes comprehensive error handling:

```python
from PPT_gen.models import ProcessingResult

result = generator.process_document("document.pdf")

if not result.success:
    print(f"Error: {result.message}")
    if result.error:
        print(f"Details: {result.error}")
    
    # Handle specific error types
    if "file not found" in result.message.lower():
        print("Please check the file path")
    elif "api key" in result.message.lower():
        print("Please configure your API keys")
    elif "template" in result.message.lower():
        print("Please check template availability")
```

## Logging

The system includes comprehensive logging:

```python
from PPT_gen.utils import setup_logging, get_logger

# Setup logging
setup_logging(
    log_level="DEBUG",
    log_file="logs/ppt_generator.log"
)

# Get logger
logger = get_logger("ppt_generator")

# Log messages
logger.info("Processing started")
logger.warning("Rate limit approaching")
logger.error("Processing failed", exc_info=True)
```

## Testing

The new structure is designed for easy testing:

```python
import pytest
from PPT_gen.services import AIService
from PPT_gen.models import Topic

def test_ai_service():
    ai_service = AIService()
    
    # Test topic extraction
    topics = ai_service.extract_topics("Sample text about machine learning")
    assert len(topics) > 0
    assert all(isinstance(topic, Topic) for topic in topics)

def test_content_generation():
    ai_service = AIService()
    
    # Test slide content generation
    bullets = ai_service.generate_slide_content("Machine Learning")
    assert len(bullets) > 0
    assert all(len(bullet) > 20 for bullet in bullets)
```

## Migration from Legacy Code

To migrate from the old structure:

1. **Replace imports**:
   ```python
   # Old
   from emotion import EnhancedPPTGenerator
   
   # New
   from PPT_gen.main_new import PPTGenerator
   ```

2. **Update initialization**:
   ```python
   # Old
   ppt_gen = EnhancedPPTGenerator(template_name="polyhedron")
   
   # New
   generator = PPTGenerator()
   ```

3. **Update processing calls**:
   ```python
   # Old
   ppt, slide_count = ppt_gen.generate_from_content(content_dict)
   
   # New
   result = generator.process_document("document.pdf", template_name="polyhedron")
   ```

## Performance Considerations

The new architecture includes several performance optimizations:

1. **Lazy Loading**: Services are initialized only when needed
2. **Caching**: Template information is cached after first load
3. **Rate Limiting**: Built-in API rate limiting and retry logic
4. **Memory Management**: Efficient memory usage for large documents
5. **Parallel Processing**: Ready for async/await implementation

## Future Enhancements

The modular architecture supports easy addition of:

1. **Web Interface**: FastAPI integration ready
2. **Database Support**: Easy to add database models
3. **Caching Layer**: Redis integration ready
4. **Queue System**: Celery integration ready
5. **Monitoring**: Metrics and health checks ready

## Best Practices

1. **Use Type Hints**: All functions include type hints
2. **Validate Input**: Pydantic models validate all inputs
3. **Handle Errors**: Comprehensive error handling throughout
4. **Log Everything**: Detailed logging for debugging
5. **Test Coverage**: Unit tests for all components
6. **Documentation**: Comprehensive docstrings and comments

This architecture provides a solid foundation for scaling the PPT Generation system while maintaining code quality and maintainability.
