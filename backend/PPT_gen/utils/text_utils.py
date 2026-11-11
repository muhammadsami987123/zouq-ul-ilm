"""
Text processing utilities.
"""

import re
from typing import List, Tuple, Optional
from difflib import SequenceMatcher


def clean_text_lines(text: str) -> List[str]:
    """
    Clean and normalize lines extracted from AI response with improved regex.
    
    Args:
        text: Raw text to clean
        
    Returns:
        List of cleaned text lines
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


def normalize_for_comparison(text: str) -> str:
    """
    Normalize text for comparison by removing punctuation and converting to lowercase.
    
    Args:
        text: Text to normalize
        
    Returns:
        Normalized text
    """
    if not text:
        return ""
    
    # Convert to lowercase
    text = text.lower()
    
    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)
    
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def are_similar(text1: str, text2: str, threshold: float = 0.7) -> bool:
    """
    Check if two texts are similar based on word overlap.
    
    Args:
        text1: First text
        text2: Second text
        threshold: Similarity threshold (0.0 to 1.0)
        
    Returns:
        True if texts are similar, False otherwise
    """
    if not text1 or not text2:
        return False
    
    # Normalize texts
    norm1 = normalize_for_comparison(text1)
    norm2 = normalize_for_comparison(text2)
    
    if not norm1 or not norm2:
        return False
    
    # Get word sets
    words1 = set(norm1.split())
    words2 = set(norm2.split())
    
    if not words1 or not words2:
        return False
    
    # Calculate Jaccard similarity
    intersection = len(words1.intersection(words2))
    union = len(words1.union(words2))
    
    similarity = intersection / union if union > 0 else 0.0
    
    return similarity >= threshold


def extract_keywords(text: str, max_keywords: int = 10) -> List[str]:
    """
    Extract keywords from text using simple frequency analysis.
    
    Args:
        text: Text to extract keywords from
        max_keywords: Maximum number of keywords to return
        
    Returns:
        List of keywords
    """
    if not text:
        return []
    
    # Normalize text
    normalized = normalize_for_comparison(text)
    
    # Remove common stop words
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
        'should', 'may', 'might', 'must', 'can', 'this', 'that', 'these',
        'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him',
        'her', 'us', 'them', 'my', 'your', 'his', 'her', 'its', 'our', 'their'
    }
    
    # Split into words and filter
    words = [word for word in normalized.split() if word not in stop_words and len(word) > 2]
    
    # Count word frequency
    word_freq = {}
    for word in words:
        word_freq[word] = word_freq.get(word, 0) + 1
    
    # Sort by frequency and return top keywords
    sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
    keywords = [word for word, freq in sorted_words[:max_keywords]]
    
    return keywords


def validate_content_quality(
    content: str,
    min_length: int = 50,
    max_length: int = 200,
    min_words: int = 8
) -> Tuple[bool, List[str]]:
    """
    Validate content quality and return issues found.
    
    Args:
        content: Content to validate
        min_length: Minimum character length
        max_length: Maximum character length
        min_words: Minimum word count
        
    Returns:
        Tuple of (is_valid, list_of_issues)
    """
    issues = []
    
    if not content or not content.strip():
        issues.append("Content is empty")
        return False, issues
    
    content = content.strip()
    
    # Check length
    if len(content) < min_length:
        issues.append(f"Content too short (minimum {min_length} characters)")
    
    if len(content) > max_length:
        issues.append(f"Content too long (maximum {max_length} characters)")
    
    # Check word count
    word_count = len(content.split())
    if word_count < min_words:
        issues.append(f"Too few words (minimum {min_words} words)")
    
    # Check for generic phrases
    generic_phrases = [
        'very important', 'quite useful', 'extremely helpful', 'it is noted that',
        'as we can see', 'it should be noted', 'it is important to', 'we can observe'
    ]
    
    content_lower = content.lower()
    for phrase in generic_phrases:
        if phrase in content_lower:
            issues.append(f"Contains generic phrase: '{phrase}'")
    
    # Check for repetitive content
    words = content.split()
    if len(words) > 10:  # Only check for longer content
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        # Check for overused words
        for word, freq in word_freq.items():
            if freq > len(words) * 0.2:  # Word appears more than 20% of the time
                issues.append(f"Word '{word}' overused ({freq} times)")
    
    is_valid = len(issues) == 0
    return is_valid, issues


def calculate_text_similarity(text1: str, text2: str) -> float:
    """
    Calculate similarity between two texts using SequenceMatcher.
    
    Args:
        text1: First text
        text2: Second text
        
    Returns:
        Similarity score between 0.0 and 1.0
    """
    if not text1 or not text2:
        return 0.0
    
    return SequenceMatcher(None, text1, text2).ratio()


def remove_duplicates_preserve_order(texts: List[str], threshold: float = 0.7) -> List[str]:
    """
    Remove duplicate texts while preserving order.
    
    Args:
        texts: List of texts
        threshold: Similarity threshold for considering texts as duplicates
        
    Returns:
        List of unique texts
    """
    if not texts:
        return []
    
    unique_texts = []
    
    for text in texts:
        is_duplicate = False
        
        for unique_text in unique_texts:
            if are_similar(text, unique_text, threshold):
                is_duplicate = True
                break
        
        if not is_duplicate:
            unique_texts.append(text)
    
    return unique_texts


def format_bullet_point(text: str, max_length: int = 200) -> str:
    """
    Format text as a proper bullet point.
    
    Args:
        text: Text to format
        max_length: Maximum length of bullet point
        
    Returns:
        Formatted bullet point
    """
    if not text:
        return ""
    
    # Clean and normalize
    text = text.strip()
    
    # Remove existing bullet points
    text = re.sub(r'^[\s•\-\*\d+\.]+', '', text)
    
    # Ensure it starts with a capital letter
    if text and text[0].islower():
        text = text[0].upper() + text[1:]
    
    # Ensure it ends with proper punctuation
    if text and not text[-1] in '.!?':
        text += '.'
    
    # Truncate if too long
    if len(text) > max_length:
        text = text[:max_length-3] + '...'
    
    return text


def extract_subject_keywords(text: str) -> List[str]:
    """
    Extract subject-related keywords from text.
    
    Args:
        text: Text to analyze
        
    Returns:
        List of subject keywords
    """
    if not text:
        return []
    
    # Subject-specific keywords
    subject_keywords = {
        'computer_science': ['programming', 'algorithm', 'software', 'database', 'network', 'code'],
        'biology': ['cell', 'organism', 'dna', 'protein', 'evolution', 'genetics'],
        'chemistry': ['molecule', 'atom', 'reaction', 'compound', 'element', 'bond'],
        'physics': ['force', 'energy', 'wave', 'particle', 'quantum', 'motion'],
        'mathematics': ['equation', 'theorem', 'calculus', 'algebra', 'geometry', 'statistics'],
        'history': ['war', 'empire', 'revolution', 'century', 'ancient', 'civilization'],
        'economics': ['market', 'economy', 'trade', 'finance', 'money', 'business'],
        'psychology': ['behavior', 'cognitive', 'mental', 'brain', 'social', 'personality']
    }
    
    text_lower = text.lower()
    found_keywords = []
    
    for subject, keywords in subject_keywords.items():
        for keyword in keywords:
            if keyword in text_lower:
                found_keywords.append(subject)
                break
    
    return list(set(found_keywords))  # Remove duplicates
