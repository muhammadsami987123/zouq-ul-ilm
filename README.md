# Zouq ul Ilm - AI-Powered Academic Content Generation Suite

> Frontend migration note: The project now includes a new Next.js + Tailwind frontend under `frontend-next/`. The old CRA frontend under `frontend/` is kept only for reference and can be safely deleted once you no longer need it.
>
> Frontend (Next.js) quick start:
> 
> ```powershell
> cd frontend-next
> npm install
> # Configure backend URL (default is http://localhost:5000)
> echo NEXT_PUBLIC_API_URL=http://localhost:5000 > .env.local
> npm run dev  # http://localhost:3000
> ```
>
> Expected FastAPI endpoints: `/upload`, `/generate`, `/summary`, `/slides`, `/rewrite`, `/progress/{task_id}`, `/download/{task_id}`, `/templates`. Ensure CORS allows `http://localhost:3000`.


[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![AI Powered](https://img.shields.io/badge/AI-Gemini%20Powered-orange.svg)](https://ai.google.dev)

Automated PDF Analysis: Extracts and analyzes text from PDF documents
AI-Powered Content Generation: Uses Google Gemini AI to create comprehensive slide content
Template Support: Supports custom PowerPoint templates for professional presentations
Intelligent Topic Detection: Identifies and categorizes academic subjects automatically  
Comprehensive Bullet Points: Generates detailed, educational content (15-35 words per bullet)
Duplicate Content Filtering: Removes redundant topics using similarity analysis
Multi-Model Processing: Rotates between different AI models for content variety
Subject Area Detection: Automatically detects the academic field for better context


## Table of Contents

- [Overview](#overview)
- [Problem Statement](#problem-statement)
- [Features](#features)
- [Project Architecture](#project-architecture)
- [Installation & Setup](#installation--setup)
- [How It Works](#how-it-works)
- [Real-World Applications](#real-world-applications)
- [Usage Guide](#usage-guide)
- [Technical Implementation](#technical-implementation)
- [Future Roadmap](#future-roadmap)
- [Development Team](#development-team)
- [Contributing](#contributing)
- [License](#license)

## Overview

**Zouq ul Ilm** (Arabic: ذوق العلم - "Taste of Knowledge") is a comprehensive AI-powered academic content generation suite that transforms educational materials into structured, professional presentations and study notes. Built with Google's Gemini AI models, this system automates the labor-intensive process of creating educational content from PDF documents, making it accessible to educators, students, and academic institutions worldwide.

The project consists of three specialized modules that work together to provide a complete solution for academic content creation:

- **Notes Generation Module**: Converts PDF course outlines into comprehensive study notes
- **Presentation Generation Module**: Creates professional PowerPoint presentations with custom templates
- **Summarization Module**: (In Development) Advanced content summarization and analysis

## Problem Statement

### The Challenge

Academic content creation is a time-intensive process that requires:

- **Manual Topic Extraction**: Educators spend hours identifying key concepts from lengthy course materials
- **Content Structuring**: Organizing information into logical, digestible formats for students
- **Presentation Design**: Creating visually appealing slides that maintain academic rigor
- **Template Management**: Ensuring consistent branding and professional appearance across materials
- **Scalability Issues**: Difficulty in processing large volumes of educational content efficiently

### The Solution

Zouq ul Ilm addresses these challenges through:

- **Automated PDF Analysis**: Intelligent extraction and categorization of academic topics
- **AI-Powered Content Generation**: Comprehensive bullet points and detailed explanations
- **Professional Template System**: Customizable PowerPoint templates for various academic disciplines
- **Intelligent Deduplication**: Advanced similarity detection to eliminate redundant content
- **Multi-Model Processing**: Rotation between different AI models for content variety and quality

## Features

### Core Capabilities

#### 🎯 **Intelligent Topic Detection**
- Automatic identification of academic subjects and concepts
- Smart categorization across multiple disciplines (Computer Science, Biology, Chemistry, Physics, Mathematics, etc.)
- Context-aware content generation based on detected subject areas

#### 📚 **Comprehensive Content Generation**
- Detailed bullet points (15-35 words each) for thorough explanations
- Educational language appropriate for university-level content
- Progressive content structure that builds understanding systematically
- Technical term integration with clear explanations

#### 🎨 **Professional Template System**
- Multiple PowerPoint templates (Polyhedron, Blue, Green, Silver Stone, etc.)
- Customizable design elements and branding
- Automatic template selection based on content type
- Professional formatting with consistent typography

#### 🔄 **Advanced Content Processing**
- Multi-model AI processing for content variety
- Intelligent deduplication using similarity analysis
- Rate limiting and error handling for reliable operation
- Batch processing capabilities for large documents

#### 📊 **Quality Assurance**
- Content validation and filtering
- Minimum quality thresholds for generated content
- Comprehensive error handling and logging
- Progress tracking and status reporting

### Technical Features

- **PDF Processing**: Support for complex PDF documents with text extraction
- **AI Integration**: Google Gemini 2.0 Flash, 1.5 Pro, and 1.5 Flash models
- **Template Management**: Dynamic template loading and customization
- **Output Formats**: PowerPoint presentations (.pptx) and PDF notes
- **Cross-Platform**: Windows, macOS, and Linux compatibility


## Quick links

- Backend: `backend/`
- Frontend (Next.js): `frontend-next/`
- Legacy Frontend (deprecated, optional): `frontend/`
- Presentation templates and generator: `PPT_gen/`

## How to run (development)

Below are concise, platform-correct instructions for running the backend (Python) and frontend (React) on Windows using PowerShell. These steps assume you have Python 3.7+ and Node.js/npm installed.

### Backend (Python)

1. Open a PowerShell terminal and change to the backend folder:

```powershell
cd f:\Zouq-ul-ilm\backend
```

2. Create and activate a virtual environment (recommended):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If activation fails due to execution policy, run (as Administrator):

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

3. Install backend dependencies:

```powershell
pip install -r requirements.txt
```

4. Configure environment variables:

- The `backend/PPT_gen/` folder contains `.env.example`. Copy it and add your API keys (do not commit secrets):

```powershell
Copy-Item .\PPT_gen\.env.example .\PPT_gen\.env
# Edit .\PPT_gen\.env with a text editor and set GOOGLE_API_KEY and any other keys required
```

5. Run the backend service (Flask app):

Option A — run directly with Python (recommended for development):

```powershell
python app.py
```

This starts the Flask app on port 5000 (http://localhost:5000) by default.

Option B — run with the `flask` command (alternative):

```powershell
$env:FLASK_APP = 'app.py'
flask run --host=0.0.0.0 --port=5000
```

6. Output and logs

- Generated files are written under `PPT_gen/output/` (presentations) or `Notes_gen/` output folders. Check `PPT_gen/logs/` or `backend/logs/` for runtime logs if available.

### Frontend (Next.js)

1. Open a new PowerShell terminal and change to the Next.js frontend folder:

```powershell
cd f:\Zouq-ul-ilm\frontend-next
```

2. Install dependencies:

```powershell
npm install
```

3. Configure backend URL (default):

```powershell
echo NEXT_PUBLIC_API_URL=http://localhost:5000 > .env.local
```

4. Start the development server:

```powershell
npm run dev
```

This runs the Next.js app on http://localhost:3000.

### Running both services together (developer flow)

- Start the backend in one terminal (see backend steps).
- Start the frontend in another terminal.
- Use the frontend UI to upload PDFs and trigger generation, or call backend endpoints directly.

### Common troubleshooting

- If environment variables aren't picked up, confirm `.env` files are present and the code loads them (many modules use `python-dotenv`).
- If PowerShell refuses to run activation scripts, update the execution policy for the current user as noted above.
- If the frontend can't reach the backend, check CORS settings on the backend and ensure the API base URL in `frontend/src/config.js` is correct.

## Minimal example: generate a presentation locally

1. Start backend (PowerShell):

```powershell
# Navigate to PPT_gen directory
cd PPT_gen

# Using the new architecture-based generator

2. Start frontend (PowerShell):

```powershell
python main_new.py --input "path/to/your/document.pdf" --template "Polyhedron" --output "output/presentations"
```

#### Legacy Usage

Open your browser to http://localhost:3000 and use the UI to upload or request generated content.

## Notes & next steps

- If you'd like, I can add a short `backend/README.md` and `frontend/README.md` with module-specific examples, or create `docker-compose` files to run both services with containers.
- I can also add example `.env` templates (without secrets) and a small script to launch both services concurrently.

---

If you want me to commit smaller, module-scoped run guides (for example a `frontend/README.md` and `backend/README.md`) I can add those next. 


```python
# Navigate to PPT_gen directory
cd PPT_gen

# Place your PDF file and update the path
pdf_path = r"path/to/your/document.pdf"

# Select a template
available_templates = get_available_templates()
selected_template = "Polyhedron"  # or any available template

# Run the presentation generation
python main.py
```

#### Template Selection

```python
# Available templates with categories
templates = {
    "Modern": ["Polyhedron", "gradation_green"],
    "Professional": ["blue", "silver_stone"], 
    "Academic": ["green", "yellow_subhan"]
}

# Template details
template_info = {
    "Polyhedron": "Modern geometric design - suitable for CS, Math, Engineering",
    "blue": "Professional blue theme - suitable for Business, Corporate",
    "green": "Academic green theme - suitable for Biology, Education",
    "silver_stone": "Elegant silver theme - suitable for Architecture, Design",
    "gradation_green": "Gradient green design - suitable for Technology, Innovation",
    "yellow_subhan": "Warm yellow theme - suitable for Literature, History"
}

# Use template in generation (new architecture)
python main_new.py --input "document.pdf" --template "Polyhedron"

# Use template in generation (legacy)
note(pdf_path, template_name="Polyhedron")
```

#### Advanced Configuration

```python
# Customize content generation
generation_config = {
    "temperature": 0.4,        # Balanced creativity
    "top_k": 50,              # Moderate diversity
    "top_p": 0.9,             # High quality sampling
    "max_output_tokens": 800, # Comprehensive content
}

# Adjust content quality thresholds
MIN_BULLET_LENGTH = 50
MAX_BULLET_LENGTH = 200
MIN_WORD_COUNT = 8
```

## Future Roadmap

### Phase 1: Web Interface Development (Q1 2024)

#### Frontend Development
- **Modern Web Interface**: React/Next.js-based user interface
- **Responsive Design**: Mobile and desktop compatibility
- **Real-time Processing**: Live progress tracking and status updates
- **Template Preview**: Visual template selection with previews
- **Drag-and-Drop Upload**: Intuitive file upload interface

#### Backend API Development
- **FastAPI Integration**: RESTful API for all operations
- **Asynchronous Processing**: Non-blocking operations for large files
- **File Management**: Secure file upload and storage
- **User Authentication**: JWT-based authentication system
- **API Documentation**: Comprehensive API documentation with Swagger

### Phase 2: Advanced Features (Q2 2024)

#### Enhanced AI Capabilities
- **Multi-Language Support**: Content generation in multiple languages
- **Custom AI Models**: Fine-tuned models for specific academic disciplines
- **Content Personalization**: Adaptive content based on user preferences
- **Advanced Summarization**: Intelligent content summarization module
- **Citation Integration**: Automatic citation and reference management

#### Collaboration Features
- **Team Workspaces**: Multi-user collaboration on content creation
- **Version Control**: Track changes and maintain content history
- **Sharing System**: Easy sharing of generated content
- **Comment System**: Collaborative review and feedback
- **Permission Management**: Role-based access control

### Phase 3: Enterprise Features (Q3 2024)

#### Institutional Integration
- **LMS Integration**: Canvas, Blackboard, Moodle compatibility
- **SSO Authentication**: Single sign-on for institutional users
- **Bulk Processing**: Large-scale content generation for institutions
- **Analytics Dashboard**: Usage analytics and performance metrics
- **Custom Branding**: Institution-specific templates and branding

#### Advanced Processing
- **OCR Integration**: Image and scanned document processing
- **Video Content**: Automatic video slide generation
- **Interactive Elements**: Clickable elements and multimedia integration
- **Accessibility Features**: WCAG compliance and accessibility tools
- **Export Options**: Multiple output formats (PDF, HTML, SCORM)

### Phase 4: AI Agent Integration (Q4 2024)

#### Autonomous AI Agents
- **Content Curation Agent**: Automatic content discovery and curation
- **Quality Assurance Agent**: Continuous content quality monitoring
- **Template Optimization Agent**: Automatic template improvement
- **User Assistance Agent**: Intelligent help and guidance system
- **Content Update Agent**: Automatic content updates and maintenance

#### System Integration
- **Command Line Interface**: Full CLI for power users
- **Desktop Application**: Native desktop app with offline capabilities
- **Browser Extension**: Browser-based content generation
- **API Ecosystem**: Third-party integrations and plugins
- **Cloud Deployment**: Scalable cloud infrastructure

### Long-term Vision (2025+)

#### Advanced AI Capabilities
- **Offline AI Processing**: Local AI models for privacy and speed
- **Custom Model Training**: User-specific model fine-tuning
- **Multimodal Processing**: Text, image, and audio content generation
- **Real-time Collaboration**: Live collaborative editing
- **Predictive Content**: AI-powered content suggestions

#### Global Expansion
- **Internationalization**: Full i18n support for global users
- **Regional Templates**: Culture-specific design templates
- **Language Models**: Native language AI models
- **Local Deployment**: On-premises deployment options
- **Compliance**: GDPR, FERPA, and other regulatory compliance

## Development Team

### Role Assignments

#### Frontend Development Lead
**Responsibilities:**
- **UI/UX Design**: Create intuitive and responsive user interfaces
- **Frontend Framework**: Implement using Next.js and Tailwind CSS
- **Component Development**: Build reusable React components
- **State Management**: Implement Redux or Zustand for state management
- **API Integration**: Connect frontend with FastAPI backend
- **Testing**: Implement frontend testing with Jest and React Testing Library
- **Performance Optimization**: Optimize bundle size and loading times
- **Accessibility**: Ensure WCAG compliance and accessibility features

**Technical Stack:**
- Next.js 14+ with App Router
- Tailwind CSS for styling
- TypeScript for type safety
- React Query for data fetching
- Framer Motion for animations
- React Hook Form for form management

#### Backend Development Lead
**Responsibilities:**
- **API Development**: Build robust FastAPI backend services
- **Database Design**: Design and implement database schemas
- **Authentication**: Implement JWT-based authentication system
- **File Processing**: Optimize PDF processing and content generation
- **AI Integration**: Enhance AI model integration and optimization
- **Terminal Interface**: Improve command-line interface and tools
- **Performance**: Optimize backend performance and scalability
- **Security**: Implement security best practices and data protection

**Technical Stack:**
- FastAPI for API development
- SQLAlchemy for database ORM
- PostgreSQL for data storage
- Redis for caching
- Celery for background tasks
- Docker for containerization
- Pytest for testing

### Collaboration Workflow

#### Development Process
1. **Planning Phase**: Weekly sprint planning and task assignment
2. **Development Phase**: Parallel development with regular sync meetings
3. **Integration Phase**: API integration and testing
4. **Testing Phase**: Comprehensive testing and quality assurance
5. **Deployment Phase**: Staging and production deployment

#### Communication Channels
- **Daily Standups**: Brief daily progress updates
- **Weekly Reviews**: Detailed progress review and planning
- **Code Reviews**: Peer review of all code changes
- **Documentation**: Comprehensive documentation maintenance
- **Issue Tracking**: GitHub Issues for bug tracking and feature requests

#### Quality Assurance
- **Code Standards**: Consistent coding standards and best practices
- **Testing Coverage**: Minimum 80% test coverage for all modules
- **Performance Monitoring**: Continuous performance monitoring
- **Security Audits**: Regular security assessments
- **User Feedback**: Continuous user feedback integration

## Contributing

### Getting Started

1. **Fork the Repository**: Create your own fork of the project
2. **Clone Your Fork**: Clone the repository to your local machine
3. **Create a Branch**: Create a feature branch for your changes
4. **Make Changes**: Implement your changes with proper testing
5. **Submit a Pull Request**: Submit your changes for review

### Development Guidelines

#### Code Standards
- **Python**: Follow PEP 8 style guidelines
- **JavaScript/TypeScript**: Use ESLint and Prettier configurations
- **Documentation**: Comprehensive docstrings and comments
- **Testing**: Write tests for all new functionality
- **Commits**: Use conventional commit messages

#### Pull Request Process
1. **Update Documentation**: Update relevant documentation
2. **Add Tests**: Include tests for new functionality
3. **Update CHANGELOG**: Document changes in CHANGELOG.md
4. **Request Review**: Request review from team members
5. **Address Feedback**: Address any feedback or requested changes

### Community Guidelines

#### Code of Conduct
- **Respectful Communication**: Maintain respectful and professional communication
- **Inclusive Environment**: Welcome contributors from all backgrounds
- **Constructive Feedback**: Provide constructive and helpful feedback
- **Collaborative Spirit**: Work together to improve the project

#### Support
- **Documentation**: Comprehensive documentation for all features
- **Issue Templates**: Use provided issue templates for bug reports
- **Discussion Forums**: Use GitHub Discussions for questions and ideas
- **Community Help**: Help other community members when possible

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### MIT License Summary

**Permissions:**
- Commercial use
- Modification
- Distribution
- Private use

**Conditions:**
- License and copyright notice

**Limitations:**
- Liability
- Warranty

### Third-Party Licenses

This project uses several third-party libraries and services:

- **Google Generative AI**: Subject to Google's Terms of Service
- **python-pptx**: MIT License
- **PyPDF2**: BSD License
- **FastAPI**: MIT License
- **React/Next.js**: MIT License

### Commercial Use

This project is open source and can be used for commercial purposes. However, please note:

- **API Costs**: Google AI Studio API usage may incur costs
- **Attribution**: Please provide appropriate attribution when using this project
- **Support**: Commercial support is not provided as part of this open-source project

---

## Contact and Support

- **GitHub Issues**: [Report bugs or request features](https://github.com/yourusername/Zouq-ul-ilm/issues)
- **Discussions**: [Join community discussions](https://github.com/yourusername/Zouq-ul-ilm/discussions)
- **Email**: [Contact the development team](mailto:contact@zouqulilm.com)
- **Documentation**: [Full documentation](https://docs.zouqulilm.com)

---

**Zouq ul Ilm** - Transforming education through AI-powered content generation.

*"Taste of Knowledge" - Making academic content creation accessible to everyone.*
