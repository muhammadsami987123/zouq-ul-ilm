
import PyPDF2
import os
import fitz # PyMuPDF
import io
from PIL import Image
import time
import google.generativeai as genai
import random

# Removed hardcoded API key and global summary_length

def extract_text_and_images_from_pdf(pdf_file, summary_type, gen_config):
    models = ['models/gemini-2.0-flash', 'models/gemini-2.0-flash-exp', 'gemini-2.5-flash-lite', 'models/gemini-1.5-flash', 'models/gemini-2.0-flash-live-001']

    # API key rotation handled in app.py
    # The genai.configure(api_key=api_key) call should be outside this function or handled higher up if rotating. 
    # For now, it's assumed app.py handles overall API key configuration.

    reader = PyPDF2.PdfReader(open(pdf_file, "rb"))
    doc = fitz.open(pdf_file)

    extracted_content = []  # List of ("text", value) or ("image", path)
    
    # Add title page
    extracted_content.append(("title", "PDF Summarization"))

    for i, page in enumerate(reader.pages):
        original_text = page.extract_text()

        if original_text:
            # Add page header
            extracted_content.append(("page_header", f"Page {i+1} Summarization"))
            
            # Define length mapping based on passed summary_type
            length_instruction = ""
            length_type = summary_type

            if summary_type == "short":
                length_instruction = "short: maximum 3 sentences"
            elif summary_type == "medium":
                length_instruction = "medium: one detailed paragraph (6-8 sentences)"
            elif summary_type == "long":
                length_instruction = "detailed: 2-3 well-structured paragraphs covering all context"
            else:
                length_instruction = "medium: one detailed paragraph (6-8 sentences)" # Default

            prompt = f"""
You are a **summary helper**.  
I will give you some text.  
You must do the thinking in **two steps in your mind** (don’t show them),  
and only give me the **final summary**.The summary must be in **Easy wording** follow STRICLY these rules.

-----------------------------------
✍️ Text to Summarize:
{original_text}
-----------------------------------

🧠 THINKING STEPS (keep inside, don’t show):
1. **Find the important parts**:
   - What is the main idea?  
   - What examples or proof are given?  
   - Any names, dates, or special facts?  
   - How does the writer feel (tone)?  
   - What background is needed to understand it?  

2. **Make the summary**:
   - Keep only the most useful points  
   - Remove extra details or repeats  
   - Write it in clear, simple words  
   - Match the length I asked for  

-----------------------------------
📋 FINAL SUMMARY RULES:
1. The summary must be **{length_instruction}**  
2. Use **easy, clear, neutral language** (unless the text is very emotional)  
3. Focus only on the **main points**  
4. Always follow this format:  

-----------------------------------
✅ FINAL OUTPUT FORMAT:
**Summary (Length: {length_type})**

[Write your summary here – follow the length exactly]


"""

            # Using gen_config from parameter for model generation
            model_instance = genai.GenerativeModel(
                model_name=models[i % len(models)], # Rotate models
                generation_config=gen_config,
            )
            response = model_instance.generate_content(prompt)
            rewritten_text = response.text

            # Add the summarized text
            extracted_content.append(("text", rewritten_text))

        # Add page footer
        extracted_content.append(("page_footer", f"Page {i+1} Summary"))

        time.sleep(1)

    # pdf.create_word_document(extracted_content) # This should be handled in app.py or by a dedicated service
    return {"extracted_content": extracted_content, "summary_type": summary_type}

# Removed if __name__ == "__main__" block

