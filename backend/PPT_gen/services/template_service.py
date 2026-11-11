"""
Template service for managing PowerPoint templates.
"""

import os
from typing import List, Optional, Dict, Any
from pathlib import Path

from ..config import get_settings, TEMPLATE_CATEGORIES
from ..models import TemplateInfo, TemplateMetadata, TemplateCategory, TemplateCollection
from ..utils import list_files_in_directory, get_file_info


class TemplateService:
    """Service for managing PowerPoint templates."""
    
    def __init__(self):
        self.settings = get_settings()
        self.templates_dir = self.settings.templates_dir
        self.template_collection = TemplateCollection()
        self._load_templates()
    
    def _load_templates(self) -> None:
        """Load all available templates from the templates directory."""
        if not os.path.exists(self.templates_dir):
            print(f"Templates directory not found: {self.templates_dir}")
            return
        
        # Get all .pptx files
        template_files = list_files_in_directory(self.templates_dir, ['.pptx'])
        
        for template_file in template_files:
            try:
                template_info = self._create_template_info(template_file)
                if template_info:
                    self.template_collection.add_template(template_info)
            except Exception as e:
                print(f"Error loading template {template_file}: {e}")
    
    def _create_template_info(self, file_path: str) -> Optional[TemplateInfo]:
        """Create TemplateInfo from file path."""
        try:
            file_info = get_file_info(file_path)
            if not file_info.get('exists', False):
                return None
            
            # Extract template name from filename
            template_name = Path(file_path).stem.lower()
            
            # Create metadata
            metadata = TemplateMetadata(
                name=template_name,
                display_name=self._get_display_name(template_name),
                category=self._get_template_category(template_name),
                description=self._get_template_description(template_name),
                author="Zouq ul Ilm",
                version="1.0",
                tags=self._get_template_tags(template_name),
                file_size=file_info.get('size', 0),
                created_at=None,
                updated_at=None
            )
            
            # Create template info
            template_info = TemplateInfo(
                metadata=metadata,
                file_path=file_path,
                is_available=True,
                layout_count=None,  # Could be determined by analyzing the template
                color_scheme=None,  # Could be extracted from template
                font_family=None,   # Could be extracted from template
                supported_slide_types=["title", "content", "section"]
            )
            
            return template_info
            
        except Exception as e:
            print(f"Error creating template info for {file_path}: {e}")
            return None
    
    def _get_display_name(self, template_name: str) -> str:
        """Get display name for template."""
        display_names = {
            "polyhedron": "Polyhedron",
            "blue": "Professional Blue",
            "green": "Academic Green",
            "silver_stone": "Silver Stone",
            "gradation_green": "Gradient Green",
            "yellow_subhan": "Yellow Subhan"
        }
        return display_names.get(template_name, template_name.title())
    
    def _get_template_category(self, template_name: str) -> TemplateCategory:
        """Get template category based on name."""
        category_mapping = {
            "polyhedron": TemplateCategory.MODERN,
            "gradation_green": TemplateCategory.MODERN,
            "blue": TemplateCategory.PROFESSIONAL,
            "silver_stone": TemplateCategory.PROFESSIONAL,
            "green": TemplateCategory.ACADEMIC,
            "yellow_subhan": TemplateCategory.ACADEMIC
        }
        return category_mapping.get(template_name, TemplateCategory.PROFESSIONAL)
    
    def _get_template_description(self, template_name: str) -> str:
        """Get template description."""
        descriptions = {
            "polyhedron": "Modern geometric design with clean lines and professional appearance",
            "blue": "Classic professional blue theme suitable for business presentations",
            "green": "Academic green theme perfect for educational content",
            "silver_stone": "Elegant silver and stone color scheme for sophisticated presentations",
            "gradation_green": "Modern gradient green design with contemporary styling",
            "yellow_subhan": "Warm yellow theme with academic focus and readability"
        }
        return descriptions.get(template_name, "Professional PowerPoint template")
    
    def _get_template_tags(self, template_name: str) -> List[str]:
        """Get template tags."""
        tag_mapping = {
            "polyhedron": ["modern", "geometric", "professional", "clean"],
            "blue": ["professional", "business", "corporate", "classic"],
            "green": ["academic", "education", "nature", "growth"],
            "silver_stone": ["elegant", "sophisticated", "professional", "neutral"],
            "gradation_green": ["modern", "gradient", "contemporary", "fresh"],
            "yellow_subhan": ["academic", "warm", "readable", "educational"]
        }
        return tag_mapping.get(template_name, ["professional", "presentation"])
    
    def get_template(self, template_name: str) -> Optional[TemplateInfo]:
        """Get template by name."""
        return self.template_collection.get_template_by_name(template_name)
    
    def get_available_templates(self) -> List[TemplateInfo]:
        """Get all available templates."""
        return self.template_collection.get_available_templates()
    
    def get_templates_by_category(self, category: TemplateCategory) -> List[TemplateInfo]:
        """Get templates by category."""
        return self.template_collection.get_templates_by_category(category)
    
    def get_suitable_templates(self, subject: str) -> List[TemplateInfo]:
        """Get templates suitable for given subject."""
        return self.template_collection.get_suitable_templates(subject)
    
    def get_default_template(self) -> Optional[TemplateInfo]:
        """Get default template."""
        # Try to get Polyhedron first, then any available template
        polyhedron = self.get_template("polyhedron")
        if polyhedron and polyhedron.is_available:
            return polyhedron
        
        available = self.get_available_templates()
        return available[0] if available else None
    
    def get_template_categories(self) -> List[TemplateCategory]:
        """Get all available template categories."""
        return list(TemplateCategory)
    
    def get_template_count(self) -> int:
        """Get total number of templates."""
        return self.template_collection.get_template_count()
    
    def get_available_count(self) -> int:
        """Get number of available templates."""
        return self.template_collection.get_available_count()
    
    def refresh_templates(self) -> None:
        """Refresh template collection by reloading from disk."""
        self.template_collection = TemplateCollection()
        self._load_templates()
    
    def get_template_preview_info(self, template_name: str) -> Optional[Dict[str, Any]]:
        """Get template preview information."""
        template = self.get_template(template_name)
        if not template:
            return None
        
        return {
            "name": template.metadata.name,
            "display_name": template.metadata.display_name,
            "category": template.metadata.category.value,
            "description": template.metadata.description,
            "tags": template.metadata.tags,
            "file_size": template.metadata.file_size,
            "is_available": template.is_available,
            "supported_slide_types": template.supported_slide_types
        }
    
    def get_all_templates_info(self) -> List[Dict[str, Any]]:
        """Get information for all templates."""
        templates = self.get_available_templates()
        return [self.get_template_preview_info(t.metadata.name) for t in templates]
    
    def validate_template(self, template_name: str) -> bool:
        """Validate that template exists and is accessible."""
        template = self.get_template(template_name)
        if not template:
            return False
        
        return os.path.exists(template.file_path) and template.is_available
    
    def get_template_statistics(self) -> Dict[str, Any]:
        """Get template collection statistics."""
        templates = self.get_available_templates()
        
        # Count by category
        category_counts = {}
        for category in TemplateCategory:
            category_counts[category.value] = len(self.get_templates_by_category(category))
        
        # Calculate total file size
        total_size = sum(t.metadata.file_size or 0 for t in templates)
        
        return {
            "total_templates": len(templates),
            "category_counts": category_counts,
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2),
            "templates_dir": self.templates_dir
        }
