from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml.shared import OxmlElement, qn
from docx.enum.style import WD_STYLE_TYPE
from docx.oxml.ns import qn
import re
import os
from datetime import datetime

def create_word_document(content_list):
    doc = Document()
    
    # Set margins for better layout
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1.25)
        section.right_margin = Inches(1.25)
    
    # Create enhanced styles
    setup_document_styles(doc)
    
    inserted_images = set()  # Track inserted images to avoid duplicates

    for item_type, data in content_list:
        if item_type == "title":
            add_title_page(doc, data)
        elif item_type == "page_header":
            add_page_header(doc, data)
        elif item_type == "text":
            add_formatted_text(doc, data)
        elif item_type == "image":
            if data not in inserted_images:
                inserted_images.add(data)
                add_image(doc, data)

    # Save the document
    doc.save("notes.docx")

    # Remove temp images
    for item_type, data in content_list:
        if item_type == "image" and os.path.exists(data):
            os.remove(data)


def setup_document_styles(doc):
    """Setup enhanced document styles with better formatting"""
    
    # Enhanced Normal style
    normal_style = doc.styles['Normal']
    normal_font = normal_style.font
    normal_font.name = 'Calibri'
    normal_font.size = Pt(11)
    normal_para = normal_style.paragraph_format
    normal_para.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    normal_para.line_spacing = 1.15
    normal_para.space_after = Pt(6)
    normal_para.space_before = Pt(0)
    
    # Create custom heading styles
    try:
        heading1_style = doc.styles.add_style('CustomHeading1', WD_STYLE_TYPE.PARAGRAPH)
        h1_font = heading1_style.font
        h1_font.name = 'Calibri'
        h1_font.size = Pt(18)
        h1_font.bold = True
        h1_font.color.rgb = RGBColor(31, 73, 125)  # Professional blue
        h1_para = heading1_style.paragraph_format
        h1_para.space_before = Pt(18)
        h1_para.space_after = Pt(12)
        h1_para.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
        h1_para.line_spacing = 1.2
        h1_para.keep_with_next = True
    except:
        pass
    
    try:
        heading2_style = doc.styles.add_style('CustomHeading2', WD_STYLE_TYPE.PARAGRAPH)
        h2_font = heading2_style.font
        h2_font.name = 'Calibri'
        h2_font.size = Pt(16)
        h2_font.bold = True
        h2_font.color.rgb = RGBColor(68, 84, 106)  # Darker blue-gray
        h2_para = heading2_style.paragraph_format
        h2_para.space_before = Pt(15)
        h2_para.space_after = Pt(9)
        h2_para.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
        h2_para.line_spacing = 1.2
        h2_para.keep_with_next = True
    except:
        pass
    
    try:
        heading3_style = doc.styles.add_style('CustomHeading3', WD_STYLE_TYPE.PARAGRAPH)
        h3_font = heading3_style.font
        h3_font.name = 'Calibri'
        h3_font.size = Pt(14)
        h3_font.bold = True
        h3_font.color.rgb = RGBColor(89, 89, 89)  # Dark gray
        h3_para = heading3_style.paragraph_format
        h3_para.space_before = Pt(12)
        h3_para.space_after = Pt(6)
        h3_para.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
        h3_para.line_spacing = 1.2
        h3_para.keep_with_next = True
    except:
        pass
    
    # Enhanced bullet list style
    try:
        bullet_style = doc.styles.add_style('CustomBullet', WD_STYLE_TYPE.PARAGRAPH)
        bullet_font = bullet_style.font
        bullet_font.name = 'Calibri'
        bullet_font.size = Pt(11)
        bullet_para = bullet_style.paragraph_format
        bullet_para.left_indent = Inches(0.25)
        bullet_para.space_after = Pt(3)
        bullet_para.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
        bullet_para.line_spacing = 1.15
    except:
        pass


def add_title_page(doc, title):
    """Add elegant title page with professional styling"""
    # Add top spacing
    for _ in range(6):
        doc.add_paragraph()
    
    # Main title
    title_paragraph = doc.add_paragraph()
    title_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_run = title_paragraph.add_run(title)
    title_run.font.name = 'Calibri'
    title_run.font.size = Pt(28)
    title_run.font.bold = True
    title_run.font.color.rgb = RGBColor(31, 73, 125)  # Professional blue
    
    # Add decorative line
    line_paragraph = doc.add_paragraph()
    line_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    line_run = line_paragraph.add_run("─" * 40)
    line_run.font.size = Pt(14)
    line_run.font.color.rgb = RGBColor(156, 156, 156)  # Light gray
    
    # Add spacing
    for _ in range(4):
        doc.add_paragraph()
    
    # Subtitle/Description
    subtitle_paragraph = doc.add_paragraph()
    subtitle_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    subtitle_run = subtitle_paragraph.add_run("Document Notes & Analysis")
    subtitle_run.font.name = 'Calibri'
    subtitle_run.font.size = Pt(16)
    subtitle_run.font.color.rgb = RGBColor(89, 89, 89)  # Dark gray
    subtitle_run.font.italic = True
    
    # Add more spacing
    for _ in range(8):
        doc.add_paragraph()
    
    # Date section with styling
    date_paragraph = doc.add_paragraph()
    date_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    current_date = datetime.now().strftime("%B %d, %Y")
    date_run = date_paragraph.add_run(f"Generated on {current_date}")
    date_run.font.name = 'Calibri'
    date_run.font.size = Pt(12)
    date_run.font.color.rgb = RGBColor(89, 89, 89)
    
    # Add footer line
    footer_paragraph = doc.add_paragraph()
    footer_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    footer_run = footer_paragraph.add_run("• • •")
    footer_run.font.size = Pt(16)
    footer_run.font.color.rgb = RGBColor(156, 156, 156)
    
    # Add page break
    doc.add_page_break()


def add_page_header(doc, header_text):
    """Add styled page header with enhanced formatting"""
    # Add spacing before header
    spacer = doc.add_paragraph()
    spacer_format = spacer.paragraph_format
    spacer_format.space_before = Pt(18)
    
    # Add header with underline effect
    header_paragraph = doc.add_paragraph()
    header_run = header_paragraph.add_run(header_text)
    header_run.font.name = 'Calibri'
    header_run.font.size = Pt(16)
    header_run.font.bold = True
    header_run.font.color.rgb = RGBColor(31, 73, 125)
    
    # Format header paragraph
    header_format = header_paragraph.paragraph_format
    header_format.space_after = Pt(6)
    header_format.keep_with_next = True
    
    # Add subtle underline effect
    underline_paragraph = doc.add_paragraph()
    underline_run = underline_paragraph.add_run("_" * len(header_text))
    underline_run.font.size = Pt(8)
    underline_run.font.color.rgb = RGBColor(191, 191, 191)
    underline_format = underline_paragraph.paragraph_format
    underline_format.space_after = Pt(12)


def add_image(doc, img_path):
    """Add image with professional formatting and caption"""
    try:
        # Add spacing before image
        spacer = doc.add_paragraph()
        spacer.paragraph_format.space_before = Pt(12)
        
        # Add image with border effect
        img_paragraph = doc.add_paragraph()
        img_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        img_paragraph.paragraph_format.space_after = Pt(6)
        
        # Add the image
        run = img_paragraph.add_run()
        picture = run.add_picture(img_path, width=Inches(5))  # Larger image
        
        # Add caption
        caption_paragraph = doc.add_paragraph()
        caption_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        caption_run = caption_paragraph.add_run("Figure: Diagram Analysis")
        caption_run.font.name = 'Calibri'
        caption_run.font.size = Pt(10)
        caption_run.font.italic = True
        caption_run.font.color.rgb = RGBColor(89, 89, 89)
        
        # Format caption
        caption_format = caption_paragraph.paragraph_format
        caption_format.space_after = Pt(18)
        
    except Exception as e:
        print(f"Error adding image {img_path}: {e}")


def add_formatted_text(doc, text):
    """Add formatted text with enhanced styling and spacing"""
    # Clean and normalize text
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[ \t]+', ' ', text)
    
    lines = text.split('\n')
    
    # Regex patterns
    h1_pattern = re.compile(r'^#{1}\s+(.+)')
    h2_pattern = re.compile(r'^#{2}\s+(.+)')
    h3_pattern = re.compile(r'^#{3}\s+(.+)')
    bullet_pattern = re.compile(r'^\s*[-•*]\s*(.*)')
    
    for line in lines:
        line = line.strip()
        if not line:
            # Add controlled spacing
            spacer = doc.add_paragraph()
            spacer.paragraph_format.space_after = Pt(6)
            continue

        # Check for headers
        if h1_pattern.match(line):
            clean_text = re.sub(r'^#{1}\s+', '', line)
            add_heading(doc, clean_text, 1)
        elif h2_pattern.match(line):
            clean_text = re.sub(r'^#{2}\s+', '', line)
            add_heading(doc, clean_text, 2)
        elif h3_pattern.match(line):
            clean_text = re.sub(r'^#{3}\s+', '', line)
            add_heading(doc, clean_text, 3)
        elif bullet_pattern.match(line):
            bullet_text = bullet_pattern.sub(r'\1', line)
            add_bullet_point(doc, bullet_text)
        else:
            process_inline_formatting(doc, line)


def add_heading(doc, text, level):
    """Add styled heading with proper hierarchy"""
    paragraph = doc.add_paragraph()
    run = paragraph.add_run(text)
    run.font.name = 'Calibri'
    
    # Set style based on level
    if level == 1:
        try:
            paragraph.style = doc.styles['CustomHeading1']
        except:
            run.font.size = Pt(18)
            run.font.bold = True
            run.font.color.rgb = RGBColor(31, 73, 125)
            paragraph.paragraph_format.space_before = Pt(18)
            paragraph.paragraph_format.space_after = Pt(12)
    elif level == 2:
        try:
            paragraph.style = doc.styles['CustomHeading2']
        except:
            run.font.size = Pt(16)
            run.font.bold = True
            run.font.color.rgb = RGBColor(68, 84, 106)
            paragraph.paragraph_format.space_before = Pt(15)
            paragraph.paragraph_format.space_after = Pt(9)
    else:  # level 3
        try:
            paragraph.style = doc.styles['CustomHeading3']
        except:
            run.font.size = Pt(14)
            run.font.bold = True
            run.font.color.rgb = RGBColor(89, 89, 89)
            paragraph.paragraph_format.space_before = Pt(12)
            paragraph.paragraph_format.space_after = Pt(6)
    
    # Ensure proper line spacing
    paragraph.paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    paragraph.paragraph_format.line_spacing = 1.2
    paragraph.paragraph_format.keep_with_next = True


def add_bullet_point(doc, text):
    """Add styled bullet point with proper indentation"""
    paragraph = doc.add_paragraph()
    
    # Add bullet symbol manually for better control
    bullet_run = paragraph.add_run("• ")
    bullet_run.font.name = 'Calibri'
    bullet_run.font.size = Pt(11)
    bullet_run.font.color.rgb = RGBColor(31, 73, 125)  # Blue bullets
    
    # Add bullet text
    text_run = paragraph.add_run(text)
    text_run.font.name = 'Calibri'
    text_run.font.size = Pt(11)
    
    # Format paragraph
    paragraph_format = paragraph.paragraph_format
    paragraph_format.left_indent = Inches(0.25)
    paragraph_format.hanging_indent = Inches(0.2)
    paragraph_format.space_after = Pt(3)
    paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    paragraph_format.line_spacing = 1.15


def process_inline_formatting(doc, text):
    """Process inline formatting with enhanced text styling"""
    paragraph = doc.add_paragraph()
    
    # Set paragraph formatting
    paragraph_format = paragraph.paragraph_format
    paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    paragraph_format.line_spacing = 1.15
    paragraph_format.space_after = Pt(6)
    paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY  # Justified text
    
    # Process bold and italic formatting
    bold_pattern = re.compile(r'(\*\*.*?\*\*)')
    italic_pattern = re.compile(r'(\*(?!\*).*?\*(?!\*))')
    
    # Split by bold markers first
    parts = bold_pattern.split(text)
    
    for part in parts:
        if part.startswith('**') and part.endswith('**'):
            # Bold text
            clean_text = part.strip('*')
            run = paragraph.add_run(clean_text)
            run.font.name = 'Calibri'
            run.font.size = Pt(11)
            run.font.bold = True
            run.font.color.rgb = RGBColor(51, 51, 51)  # Darker text for emphasis
        else:
            # Check for italic in non-bold text
            italic_parts = italic_pattern.split(part)
            for italic_part in italic_parts:
                if italic_part.startswith('*') and italic_part.endswith('*') and not italic_part.startswith('**'):
                    clean_italic = italic_part.strip('*')
                    run = paragraph.add_run(clean_italic)
                    run.font.name = 'Calibri'
                    run.font.size = Pt(11)
                    run.font.italic = True
                    run.font.color.rgb = RGBColor(89, 89, 89)
                else:
                    # Regular text
                    if italic_part.strip():
                        run = paragraph.add_run(italic_part)
                        run.font.name = 'Calibri'
                        run.font.size = Pt(11)
                        run.font.color.rgb = RGBColor(51, 51, 51)  # Dark gray for readability