"""
Enhanced main entry point for PPT Generation system.
Uses the new modular architecture with proper separation of concerns.
"""

import os
import sys
import time
from pathlib import Path
from typing import Optional

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

from config import get_settings
from models import ProcessingConfig, ProcessingResult, PresentationData
from services import AIService, TemplateService, ContentService, PresentationService
from utils import setup_logging, get_logger, ensure_directory_exists, is_supported_file


class PPTGenerator:
    """Main PPT Generator class using the new architecture."""
    
    def __init__(self):
        self.settings = get_settings()
        self.logger = get_logger("ppt_generator")
        
        # Initialize services
        self.ai_service = AIService()
        self.template_service = TemplateService()
        self.content_service = ContentService()
        self.presentation_service = PresentationService()
        
        # Setup logging
        log_file = os.path.join(self.settings.logs_dir, "ppt_generator.log")
        setup_logging(
            log_level=self.settings.log_level,
            log_file=log_file
        )
        
        self.logger.info("PPT Generator initialized successfully")
    
    def process_document(
        self,
        input_file: str,
        template_name: Optional[str] = None,
        output_dir: Optional[str] = None,
        config: Optional[ProcessingConfig] = None
    ) -> ProcessingResult:
        """
        Process a document and generate a PowerPoint presentation.
        
        Args:
            input_file: Path to input PDF file
            template_name: Name of template to use
            output_dir: Output directory for generated files
            config: Processing configuration
            
        Returns:
            ProcessingResult with success status and generated data
        """
        start_time = time.time()
        
        try:
            self.logger.info(f"Starting document processing: {input_file}")
            
            # Validate input file
            if not os.path.exists(input_file):
                return ProcessingResult(
                    success=False,
                    message=f"Input file not found: {input_file}",
                    processing_time=time.time() - start_time
                )
            
            if not is_supported_file(input_file):
                return ProcessingResult(
                    success=False,
                    message=f"Unsupported file format: {input_file}",
                    processing_time=time.time() - start_time
                )
            
            # Create processing configuration
            if not config:
                config = ProcessingConfig(
                    input_file_path=input_file,
                    template_name=template_name,
                    output_directory=output_dir or self.settings.output_dir
                )
            
            # Ensure output directory exists
            ensure_directory_exists(config.output_directory)
            
            # Process the document
            result = self._process_document_with_config(config)
            result.processing_time = time.time() - start_time
            
            self.logger.info(f"Document processing completed: {result.success}")
            return result
            
        except Exception as e:
            self.logger.error(f"Error processing document: {e}", exc_info=True)
            return ProcessingResult(
                success=False,
                message=f"Processing failed: {str(e)}",
                error=str(e),
                processing_time=time.time() - start_time
            )
    
    def _process_document_with_config(self, config: ProcessingConfig) -> ProcessingResult:
        """Process document with given configuration."""
        try:
            # Step 1: Extract topics from document
            self.logger.info("Step 1: Extracting topics from document")
            topics = self.content_service.extract_topics_from_pdf(
                config.input_file_path,
                max_pages=config.max_pages
            )
            
            if not topics:
                return ProcessingResult(
                    success=False,
                    message="No topics found in document",
                    topics_processed=0
                )
            
            self.logger.info(f"Extracted {len(topics)} topics")
            
            # Step 2: Detect subject area
            self.logger.info("Step 2: Detecting subject area")
            subject_area = self.ai_service.detect_subject_area([t.text for t in topics])
            self.logger.info(f"Detected subject area: {subject_area}")
            
            # Step 3: Generate slide content
            self.logger.info("Step 3: Generating slide content")
            presentation_data = self.content_service.generate_presentation_content(
                topics,
                subject_area,
                config
            )
            
            if not presentation_data:
                return ProcessingResult(
                    success=False,
                    message="Failed to generate presentation content",
                    topics_processed=len(topics)
                )
            
            # Step 4: Create PowerPoint presentation
            self.logger.info("Step 4: Creating PowerPoint presentation")
            output_file = self.presentation_service.create_presentation(
                presentation_data,
                config.template_name,
                config.output_directory
            )
            
            if not output_file:
                return ProcessingResult(
                    success=False,
                    message="Failed to create PowerPoint presentation",
                    topics_processed=len(topics),
                    slides_generated=presentation_data.get_total_slides()
                )
            
            # Success
            return ProcessingResult(
                success=True,
                message=f"Presentation created successfully: {output_file}",
                data=presentation_data,
                topics_processed=len(topics),
                slides_generated=presentation_data.get_total_slides()
            )
            
        except Exception as e:
            self.logger.error(f"Error in document processing: {e}", exc_info=True)
            return ProcessingResult(
                success=False,
                message=f"Processing error: {str(e)}",
                error=str(e)
            )
    
    def get_available_templates(self) -> list:
        """Get list of available templates."""
        return self.template_service.get_all_templates_info()
    
    def get_template_info(self, template_name: str) -> Optional[dict]:
        """Get information about a specific template."""
        return self.template_service.get_template_preview_info(template_name)
    
    def validate_template(self, template_name: str) -> bool:
        """Validate that a template exists and is accessible."""
        return self.template_service.validate_template(template_name)
    
    def get_ai_usage_stats(self) -> dict:
        """Get AI service usage statistics."""
        return self.ai_service.get_api_usage_stats()
    
    def get_system_info(self) -> dict:
        """Get system information and statistics."""
        return {
            "templates": self.template_service.get_template_statistics(),
            "ai_usage": self.ai_service.get_api_usage_stats(),
            "settings": {
                "output_dir": self.settings.output_dir,
                "templates_dir": self.settings.templates_dir,
                "logs_dir": self.settings.logs_dir,
                "debug_mode": self.settings.debug_mode
            }
        }


def main():
    """Main entry point for command-line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate PowerPoint presentations from PDF documents")
    parser.add_argument("input_file", help="Path to input PDF file")
    parser.add_argument("-t", "--template", help="Template name to use")
    parser.add_argument("-o", "--output", help="Output directory")
    parser.add_argument("--max-pages", type=int, help="Maximum pages to process")
    parser.add_argument("--max-slides", type=int, help="Maximum slides to generate")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    
    args = parser.parse_args()
    
    # Initialize generator
    generator = PPTGenerator()
    
    # Create processing configuration
    config = ProcessingConfig(
        input_file_path=args.input_file,
        template_name=args.template,
        output_directory=args.output,
        max_pages=args.max_pages,
        max_slides=args.max_slides
    )
    
    # Process document
    result = generator.process_document(
        input_file=args.input_file,
        template_name=args.template,
        output_dir=args.output,
        config=config
    )
    
    # Print results
    if result.success:
        print(f"✅ {result.message}")
        print(f"📊 Topics processed: {result.topics_processed}")
        print(f"📄 Slides generated: {result.slides_generated}")
        print(f"⏱️ Processing time: {result.processing_time:.2f}s")
    else:
        print(f"❌ {result.message}")
        if result.error:
            print(f"Error: {result.error}")
        sys.exit(1)


if __name__ == "__main__":
    main()
