from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os

import PyPDF2
import time
import re
import random
from dotenv import load_dotenv
import google.generativeai as genai # Added import
from PPT_gen.emotion import EnhancedPPTGenerator
import uuid
from Summarize_gen.ath import extract_text_and_images_from_pdf # Import summary logic
from Summarize_gen.pdf import create_word_document # Import for generating Word docs for summary
from Notes_gen.pdf_generator import pdf1 # Import for generating PDF notes (renamed)
from Notes_gen.main import send_content, engine as notes_engine # Import notes generation logic

import json # Added import for JSON parsing

load_dotenv()

# Configuration
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
TASKS = {} # To store progress and results of generation tasks

app = Flask(__name__)
CORS(app) # Enable CORS for all routes

@app.route('/')
def hello_world():
    return 'Hello, World! This is the backend.'

def clean_text_lines(text):
    """
    Clean and normalize lines extracted from AI response with improved regex
    """
    cleaned_lines = []
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        
        # Remove bullet chars or numbering at start (fixed pattern)
        line = re.sub(r'^\s*([•\-\*\d+\.]+)\s*', '', line)
        
        # Remove common prefixes like "Topic:", "Subject:", etc.
        line = re.sub(r'^\s*(Topic|Subject|Chapter|Section|Point):\s*', '', line, flags=re.IGNORECASE)
        
        # Remove trailing punctuation like ':', '.', ';'
        line = re.sub(r'[\:\.\;,]+$', '', line)
        
        # Normalize multiple spaces to single space
        line = re.sub(r'\s+', ' ', line)
        
        # Remove empty parentheses or brackets
        line = re.sub(r'\(\s*\)|\[\s*\]', '', line)
        
        final_line = line.strip()
        if final_line and len(final_line) > 3:  # Only keep meaningful content
            cleaned_lines.append(final_line)
    
    return cleaned_lines

def send_content(message):
    """
    Enhanced content analysis with better, more general prompt
    """
    num = random.randint(1, 10)
    api_key = os.getenv(f"GEMINI_API_KEY_{num}") # Use a specific API key from .env
    if not api_key:
        raise ValueError("No API key found for Gemini. Please set GEMINI_API_KEY_1 to GEMINI_API_KEY_10 in your .env file.")
    
    genai.configure(api_key=api_key)

    generation_config = {
        "temperature": 0.3,
        "top_k": 40,
        "top_p": 0.8,
        "max_output_tokens": 500,
        "response_mime_type": "text/plain",
    }
    
    model = genai.GenerativeModel(
        model_name='gemini-2.0-flash-exp',
        generation_config=generation_config,
    )
    
    chat_session = model.start_chat()
    
    enhanced_prompt = f"""
    Analyze the following academic content and extract the main topics/concepts covered.

    Content: {message}

    Instructions:
    - Identify the core topics, concepts, theories, or subjects mentioned
    - Make each topic clear and specific (3-10 words)
    - Focus on educational concepts that can be explained in a presentation
    - Include both main topics and important subtopics
    - Avoid administrative details, page numbers, references
    - Don't include generic words like "introduction", "overview", "summary"
    - Each topic should be suitable as a slide title
    - List one topic per line
    - No bullet points, numbers, or special formatting
    """
    
    try:
        response = chat_session.send_message(enhanced_prompt)
        cleaned_topics = clean_text_lines(response.text)
        return cleaned_topics
    except Exception as e:
        print(f"Error in send_content: {e}")
        return []

def engine(topic, model_name, subject_context=""):
    """
    Enhanced slide generation with comprehensive content and general prompts
    """
    num = random.randint(1, 10)
    api_key = os.getenv(f"GEMINI_API_KEY_{num}") # Use a specific API key from .env
    if not api_key:
        raise ValueError("No API key found for Gemini. Please set GEMINI_API_KEY_1 to GEMINI_API_KEY_10 in your .env file.")
    
    genai.configure(api_key=api_key)

    generation_config = {
        "temperature": 0.4,
        "top_k": 50,
        "top_p": 0.9,
        "max_output_tokens": 800,
        "response_mime_type": "text/plain",
    }
    
    model = genai.GenerativeModel(
        model_name=model_name,
        generation_config=generation_config,
    )
    
    chat_session = model.start_chat()
    
    enhanced_prompt = f"""
    Create detailed slide content for the topic: "{topic}"
    {f"Subject context: {subject_context}" if subject_context else ""}

    Generate 5-8 comprehensive bullet points that thoroughly explain this topic.

    Requirements for each bullet point:
    - 15-35 words per point (detailed explanations, not single lines)
    - Use clear, educational language appropriate for students
    - Include specific examples, definitions, or details where relevant
    - Cover different aspects of the topic (definition, importance, examples, applications)
    - Make each point informative and educational
    - Use complete sentences that provide real value
    - Include technical terms with brief explanations when needed
    - Ensure points build understanding progressively

    Format: Write each point as a complete sentence, one per line, no bullets or numbers.

    Example for "Photosynthesis Process":
    Photosynthesis is the biological process where plants convert sunlight carbon dioxide and water into glucose and oxygen
    The process occurs primarily in chloroplasts which contain chlorophyll pigments that capture light energy effectively
    Light dependent reactions take place in thylakoids where water molecules are split to release oxygen as a byproduct
    Calvin cycle occurs in the stroma where carbon dioxide is fixed into organic molecules using ATP and NADPH
    Plants produce glucose through photosynthesis which serves as their primary energy source for growth and metabolism
    This process is essential for life on Earth as it produces the oxygen that most organisms need for respiration
    Factors affecting photosynthesis rate include light intensity temperature carbon dioxide concentration and water availability
    """
    
    try:
        response = chat_session.send_message(enhanced_prompt)
        cleaned_bullets = clean_text_lines(response.text)
        
        filtered_bullets = []
        for bullet in cleaned_bullets:
            if 50 <= len(bullet) <= 200:
                generic_phrases = ['very important', 'quite useful', 'extremely helpful', 'it is noted that']
                if not any(phrase in bullet.lower() for phrase in generic_phrases):
                    word_count = len(bullet.split())
                    if word_count >= 8:
                        filtered_bullets.append(bullet)
        
        if len(filtered_bullets) < 3:
            backup_bullets = [b for b in cleaned_bullets if len(b.split()) >= 5]
            filtered_bullets = backup_bullets[:6]
        
        return filtered_bullets[:8]
        
    except Exception as e:
        print(f"Error in engine for topic {topic}: {e}")
        return [f"Detailed information and key concepts related to {topic} will be covered in this section"]

def detect_subject_area(topics_sample):
    """
    Detect the general subject area from topics to provide better context
    """
    if not topics_sample:
        return ""
    
    combined_text = " ".join(topics_sample[:5]).lower()
    
    subject_patterns = {
        "Computer Science": ["network", "algorithm", "programming", "database", "software", "computer", "data structure", "coding"],
        "Biology": ["cell", "organism", "dna", "protein", "evolution", "photosynthesis", "genetics", "anatomy"],
        "Chemistry": ["molecule", "atom", "reaction", "compound", "element", "bond", "acid", "base"],
        "Physics": ["force", "energy", "wave", "particle", "quantum", "motion", "electricity", "magnetism"],
        "Mathematics": ["equation", "theorem", "calculus", "algebra", "geometry", "probability", "statistics"],
        "History": ["war", "empire", "revolution", "century", "ancient", "medieval", "dynasty", "civilization"],
        "Economics": ["market", "economy", "trade", "finance", "money", "supply", "demand", "economic"],
        "Psychology": ["behavior", "cognitive", "mental", "brain", "psychology", "social", "personality"]
    }
    
    for subject, keywords in subject_patterns.items():
        if any(keyword in combined_text for keyword in keywords):
            return subject
    
    return "General Academic"

def get_available_templates():
    """
    Get list of available template files from templates folder
    """
    templates_folder = "PPT_gen/templates" # Adjusted path
    
    if not os.path.exists(templates_folder):
        os.makedirs(templates_folder)
        print(f"Created {templates_folder} folder. Please add your .pptx template files there.")
        return []
    
    template_files = []
    try:
        for file in os.listdir(templates_folder):
            if file.lower().endswith('.pptx') and not file.startswith('~'):
                template_files.append(file.replace('.pptx', '')) # Return name without .pptx
    except Exception as e:
        print(f"Error reading templates folder: {e}")
        return []
    
    return sorted(template_files)

def generate_presentation_task(pdf_path, template_name):
    """
    Main processing function to generate presentation, adapted for Flask
    """
    topics = []
    
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            total_pages = len(reader.pages)
            # Get the task ID from the global TASKS dictionary to update its status
            task_id_for_update = os.path.basename(pdf_path).replace('.pdf', '')
            
            TASKS[task_id_for_update].update({"progress": 5, "message": "Starting PDF analysis..."})
            print(f"Processing {total_pages} pages...")
            
            for i in range(total_pages):
                try:
                    page = reader.pages[i]
                    text1 = page.extract_text()
                    
                    if text1.strip():
                        page_topics = send_content(text1)
                        topics.extend(page_topics)
                        print(f"Page {i+1}/{total_pages}: Found {len(page_topics)} topics")
                        TASKS[task_id_for_update].update({"progress": 5 + int(30 * (i + 1) / total_pages), "message": f"Extracting topics from page {i+1}/{total_pages}..."})
                    
                    time.sleep(2)
                    
                except Exception as e:
                    print(f"Error processing page {i+1}: {e}")
                    continue
                    
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return {"status": "error", "message": f"Error reading PDF: {e}"}

    if not topics:
        print("No topics found in PDF")
        return {"status": "error", "message": "No topics found in PDF"}

    # Update progress after topic extraction
    TASKS[task_id_for_update].update({"progress": 40, "message": "Deduplicating and filtering topics..."})

    def normalize_for_comparison(text):
        text = text.lower()
        text = re.sub(r'[^\w\s]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def are_similar(text1, text2, threshold=0.7):
        words1 = set(normalize_for_comparison(text1).split())
        words2 = set(normalize_for_comparison(text2).split())
        
        if not words1 or not words2:
            return False
            
        intersection = len(words1.intersection(words2))
        union = len(words1.union(words2))
        
        return (intersection / union) >= threshold

    filtered_topics = []
    for topic in topics:
        norm_topic = normalize_for_comparison(topic)
        if len(norm_topic) > 5:
            is_duplicate = False
            for existing in filtered_topics:
                if are_similar(topic, existing):
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                filtered_topics.append(topic)

    print(f"Found {len(filtered_topics)} unique topics after deduplication")
    TASKS[task_id_for_update].update({"progress": 50, "message": "Detecting subject area..."})

    subject_context = detect_subject_area(filtered_topics)
    print(f"Detected subject area: {subject_context}")
    TASKS[task_id_for_update].update({"progress": 60, "message": "Generating content for presentation slides..."})

    model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
    
    sections = []
    
    for p, topic in enumerate(filtered_topics):
        print(f"Processing topic {p+1}/{len(filtered_topics)}: {topic}")
        try:
            slide_bullets = engine(topic, model_name, subject_context)
            if slide_bullets and len(slide_bullets) >= 3:
                sections.append({
                    "title": topic,
                    "content": slide_bullets
                })
                print(f"  Generated {len(slide_bullets)} comprehensive bullet points")
            else:
                print(f"  Insufficient quality content for: {topic}")
        except Exception as e:
            print(f"  Error generating content for {topic}: {e}")
            continue
        time.sleep(3)
        TASKS[task_id_for_update].update({"progress": 60 + int(30 * (p + 1) / len(filtered_topics)), "message": f"Generating content for topic {p+1}/{len(filtered_topics)}: {topic}..."})

    if not sections:
        print("No sections generated")
        return {"status": "error", "message": "No sections generated"}

    TASKS[task_id_for_update].update({"progress": 95, "message": "Formatting and saving presentation..."})
    presentation_title = f"{subject_context} Presentation" if subject_context != "General Academic" else "Academic Presentation"
    
    content_dict = {
        "title": presentation_title,
        "subtitle": "Generated from PDF Analysis",
        "target_slides": min(25, len(sections) + 4),
        "sections": sections,
        "call_to_action": "Questions and Discussion"
    }

    try:
        ppt_gen = EnhancedPPTGenerator(template_name=os.path.join("PPT_gen/templates", f"{template_name}.pptx")) # Adjusted path
        ppt, actual_slide_count = ppt_gen.generate_from_content(content_dict)
        
        safe_subject = re.sub(r'[^\w\s-]', '', subject_context).replace(' ', '_')
        safe_template = re.sub(r'[^\w\s-]', '', template_name).replace(' ', '_')
        output_file_name = f"{safe_subject.lower()}_{safe_template}_presentation.pptx"
        output_file_path = os.path.join("PPT_gen/output/presentations", output_file_name) # Adjusted path
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

        ppt_gen.save(output_file_path) # Save to the specified path
        
        print(f"\n✅ SUCCESS!")
        print(f"📊 Presentation saved as: {output_file_path}")
        print(f"📄 Total slides: {actual_slide_count}")
        print(f"📚 Topics covered: {len(sections)}")
        print(f"🎯 Subject area: {subject_context}")
        print(f"🎨 Template used: {template_name}")
        
        return {"status": "completed", "file_path": output_file_path, "filename": output_file_name}
        
    except Exception as e:
        print(f"❌ Error creating presentation: {e}")
        return {"status": "error", "message": f"Error creating presentation: {e}"}

def generate_notes_task(file_id, pdf_path, selected_topics, gen_config):
    TASKS[file_id].update({"progress": 5, "message": "Starting notes generation..."})
    try:
        topics = []
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            total_pages = len(reader.pages)
            
            for i in range(total_pages):
                page = reader.pages[i]
                text1 = page.extract_text()
                if text1.strip():
                    page_topics = send_content(text1) # Using send_content from Notes_gen.main
                    topics.extend(page_topics)
                time.sleep(2)
            
        if selected_topics:
            filtered_topics = [t for t in topics if t in selected_topics]
        else:
            filtered_topics = topics # Use all extracted topics if none selected

        if not filtered_topics:
            raise ValueError("No topics found or selected for notes generation.")


        ext_text = ""
        model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
        TASKS[file_id].update({"progress": 40, "message": "Generating notes content..."})
        for p, topic in enumerate(filtered_topics):
            text3 = notes_engine(topic, model_name)
            if text3:
                ext_text += text3 + "\n\n"
            time.sleep(3)
            TASKS[file_id].update({"progress": 40 + int(50 * (p + 1) / len(filtered_topics)), "message": f"Generating note for topic {p+1}/{len(filtered_topics)}..."})

        if not ext_text:
            raise ValueError("AI failed to generate notes content.")

        output_filename = f"notes_{file_id}.pdf"
        output_filepath = os.path.join(UPLOAD_FOLDER, output_filename)
        pdf1(ext_text, output_filepath) # Using pdf1 from Notes_gen.pdf

        TASKS[file_id].update({"progress": 100, "message": "Notes generated and saved.", "status": "completed", "file_path": output_filepath, "filename": output_filename})
        return {"status": "completed", "file_path": output_filepath, "filename": output_filename}
    except Exception as e:
        TASKS[file_id].update({"status": "failed", "message": str(e), "error": str(e)})
        print(f"Error generating notes for {file_id}: {e}")
        return {"status": "error", "message": str(e)}

def generate_summary_task(file_id, pdf_path, summary_type, gen_config):
    TASKS[file_id].update({"progress": 5, "message": "Starting summary generation..."})
    try:
        # Extract text from PDF using Summarize_gen.ath
        extracted_data = extract_text_and_images_from_pdf(pdf_path, summary_type, gen_config)
        full_text = extracted_data.get('text', '')

        if not full_text:
            raise ValueError("Could not extract text from PDF.")

        # Use Gemini to generate summary based on summary_type
        num = random.randint(1, 10)
        api_key = os.getenv(f"GEMINI_API_KEY_{num}")
        if not api_key:
            raise ValueError("No API key found for Gemini. Please set GEMINI_API_KEY_1 to GEMINI_API_KEY_10 in your .env file.")

        genai.configure(api_key=api_key)
        model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
        model = genai.GenerativeModel(
            model_name=model_name,
            generation_config=gen_config,
        )

        prompt = f"""
        Please provide a {summary_type} summary of the following document. 
        Focus on key points, main arguments, and conclusions. 
        The summary should be coherent, concise, and informative.

        Document:
        {full_text}
        """
        
        TASKS[file_id].update({"progress": 20, "message": "Sending content to AI for summarization..."})
        response = model.generate_content(prompt)
        summary_text = response.text

        if not summary_text:
            raise ValueError("AI failed to generate summary.")

        TASKS[file_id].update({"progress": 70, "message": "Formatting summary document..."})
        # Create a Word document using Summarize_gen.pdf
        output_filename = f"summary_{file_id}_{summary_type}.docx"
        output_filepath = os.path.join(UPLOAD_FOLDER, output_filename)
        create_word_document([summary_text], output_filepath) # Assuming create_word_document takes a list of strings

        TASKS[file_id].update({"progress": 100, "message": "Summary generated and saved.", "status": "completed", "file_path": output_filepath, "filename": output_filename})
        return {"status": "completed", "file_path": output_filepath, "filename": output_filename}
    except Exception as e:
        TASKS[file_id].update({"status": "failed", "message": str(e), "error": str(e)})
        print(f"Error generating summary for {file_id}: {e}")
        return {"status": "error", "message": str(e)}

def rewrite_document_task(file_id, pdf_path):
    TASKS[file_id].update({"progress": 5, "message": "Starting document rewrite..."})
    try:
        # Extract text from PDF
        full_text = ""
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                full_text += page.extract_text() + "\n"

        if not full_text:
            raise ValueError("Could not extract text from PDF for rewriting.")

        # Use Gemini to rewrite the document
        num = random.randint(1, 10)
        api_key = os.getenv(f"GEMINI_API_KEY_{num}")
        if not api_key:
            raise ValueError("No API key found for Gemini. Please set GEMINI_API_KEY_1 to GEMINI_API_KEY_10 in your .env file.")

        genai.configure(api_key=api_key)
        model_name = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")
        model = genai.GenerativeModel(
            model_name=model_name,
            generation_config={
                "temperature": 0.7,
                "top_k": 50,
                "top_p": 0.9,
                "max_output_tokens": 2000,
            },
        )

        prompt = f"""
        Please rewrite the following document content to improve clarity, readability, and engagement. 
        Maintain the original meaning and key information. Ensure the language is professional and academic.

        Document content to rewrite:
        {full_text}
        """
        
        TASKS[file_id].update({"progress": 30, "message": "Sending content to AI for rewriting..."})
        response = model.generate_content(prompt)
        rewritten_text = response.text

        if not rewritten_text:
            raise ValueError("AI failed to rewrite the document.")

        TASKS[file_id].update({"progress": 70, "message": "Creating rewritten document..."})
        
        output_filename = f"rewritten_document_{file_id}.pdf"
        output_filepath = os.path.join(UPLOAD_FOLDER, output_filename)

        # Create a new PDF with the rewritten content
        from fpdf import FPDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size = 12)
        # Split rewritten_text into lines and add to PDF
        for line in rewritten_text.splitlines():
            pdf.multi_cell(0, 10, txt = line)
        pdf.output(output_filepath)

        TASKS[file_id].update({"progress": 100, "message": "Document rewritten and saved.", "status": "completed", "file_path": output_filepath, "filename": output_filename})
        return {"status": "completed", "file_path": output_filepath, "filename": output_filename}
    except Exception as e:
        TASKS[file_id].update({"status": "failed", "message": str(e), "error": str(e)})
        print(f"Error rewriting document for {file_id}: {e}")
        return {"status": "error", "message": str(e)}


# API Routes
@app.route('/upload', methods=['POST'])
def upload_pdf():
    if 'pdf' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['pdf']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if file:
        file_id = str(uuid.uuid4())
        filepath = os.path.join(UPLOAD_FOLDER, file_id + '.pdf')
        file.save(filepath)
        TASKS[file_id] = {"status": "uploaded", "filepath": filepath}
        return jsonify({"message": "File uploaded successfully", "fileId": file_id}), 200

@app.route('/templates', methods=['GET'])
def get_templates():
    try:
        templates = get_available_templates()
        return jsonify(templates), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/generate', methods=['POST'])
def generate_notes_route():
    data = request.get_json()
    file_id = data.get('fileId')
    selected_topics = data.get('selectedTopics', [])
    gen_config = data.get('generation_config', {})
    
    if not file_id or file_id not in TASKS:
        return jsonify({"error": "Invalid fileId"}), 400

    TASKS[file_id]["status"] = "processing"
    
    try:
        result = generate_notes_task(file_id, TASKS[file_id]["filepath"], selected_topics, gen_config)
        TASKS[file_id].update(result)
        return jsonify({"message": "Notes generation started", "taskId": file_id}), 200
    except Exception as e:
        TASKS[file_id]["status"] = "error"
        TASKS[file_id]["message"] = str(e)
        return jsonify({"error": str(e)}), 500

@app.route('/summary', methods=['POST'])
def generate_summary_route():
    # Use request.form for FormData
    file_id = request.form.get('fileId')
    summary_type = request.form.get('summaryType', 'medium')
    gen_config_str = request.form.get('generation_config')
    
    gen_config = {}
    if gen_config_str:
        try:
            gen_config = json.loads(gen_config_str)
        except json.JSONDecodeError:
            return jsonify({"error": "Invalid generation_config JSON"}), 400

    if not file_id or file_id not in TASKS:
        return jsonify({"error": "Invalid fileId"}), 400

    TASKS[file_id]["status"] = "processing"
    
    # Run in a separate thread or process in production
    # For now, blocking call
    try:
        # Ensure we pass the gen_config to the summary task
        result = generate_summary_task(file_id, TASKS[file_id]["filepath"], summary_type, gen_config)
        TASKS[file_id].update(result)
        return jsonify({"message": "Summary generation started", "taskId": file_id}), 200
    except Exception as e:
        TASKS[file_id]["status"] = "error"
        TASKS[file_id]["message"] = str(e)
        return jsonify({"error": str(e)}), 500

@app.route('/rewrite', methods=['POST'])
def rewrite_document_route():
    data = request.get_json() # Assuming JSON for rewrite, or change to form if needed
    file_id = data.get('fileId')
    
    if not file_id or file_id not in TASKS:
        return jsonify({"error": "Invalid fileId"}), 400

    TASKS[file_id]["status"] = "processing"
    
    try:
        result = rewrite_document_task(file_id, TASKS[file_id]["filepath"])
        TASKS[file_id].update(result)
        return jsonify({"message": "Rewrite started", "taskId": file_id}), 200
    except Exception as e:
        TASKS[file_id]["status"] = "error"
        TASKS[file_id]["message"] = str(e)
        return jsonify({"error": str(e)}), 500


@app.route('/progress/<task_id>', methods=['GET'])
def check_progress(task_id):
    task = TASKS.get(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    return jsonify({"status": task["status"], "message": task.get("message"), "progress": task.get("progress", 0)}), 200

@app.route('/download/<task_id>', methods=['GET'])
def download_file(task_id):
    task = TASKS.get(task_id)
    if not task or task.get("status") != "completed":
        return jsonify({"error": "File not ready for download or task not found"}), 404
    
    file_path = task.get("file_path")
    filename = task.get("filename")
    
    if not file_path or not os.path.exists(file_path):
        return jsonify({"error": "File not found on server"}), 404

    return send_file(file_path, as_attachment=True, download_name=filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
