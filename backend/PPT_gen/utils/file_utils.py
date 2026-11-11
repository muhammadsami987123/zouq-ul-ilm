"""
File operation utilities.
"""

import os
import shutil
from pathlib import Path
from typing import Optional, List, Tuple
import mimetypes


def ensure_directory_exists(directory_path: str) -> bool:
    """
    Ensure that a directory exists, create it if it doesn't.
    
    Args:
        directory_path: Path to the directory
        
    Returns:
        True if directory exists or was created successfully
    """
    try:
        Path(directory_path).mkdir(parents=True, exist_ok=True)
        return True
    except Exception as e:
        print(f"Error creating directory {directory_path}: {e}")
        return False


def get_file_extension(file_path: str) -> str:
    """
    Get file extension from file path.
    
    Args:
        file_path: Path to the file
        
    Returns:
        File extension (including the dot)
    """
    return Path(file_path).suffix.lower()


def is_supported_file(file_path: str, supported_extensions: List[str] = None) -> bool:
    """
    Check if file has a supported extension.
    
    Args:
        file_path: Path to the file
        supported_extensions: List of supported extensions (default: ['.pdf', '.docx', '.txt'])
        
    Returns:
        True if file is supported
    """
    if supported_extensions is None:
        supported_extensions = ['.pdf', '.docx', '.txt']
    
    extension = get_file_extension(file_path)
    return extension in supported_extensions


def get_safe_filename(filename: str, max_length: int = 100) -> str:
    """
    Create a safe filename by removing invalid characters and limiting length.
    
    Args:
        filename: Original filename
        max_length: Maximum length of filename
        
    Returns:
        Safe filename
    """
    # Remove invalid characters
    invalid_chars = '<>:"/\\|?*'
    safe_name = filename
    
    for char in invalid_chars:
        safe_name = safe_name.replace(char, '_')
    
    # Remove multiple underscores
    while '__' in safe_name:
        safe_name = safe_name.replace('__', '_')
    
    # Remove leading/trailing underscores and dots
    safe_name = safe_name.strip('_.')
    
    # Limit length
    if len(safe_name) > max_length:
        name, ext = os.path.splitext(safe_name)
        safe_name = name[:max_length - len(ext)] + ext
    
    return safe_name


def get_file_size(file_path: str) -> int:
    """
    Get file size in bytes.
    
    Args:
        file_path: Path to the file
        
    Returns:
        File size in bytes, -1 if error
    """
    try:
        return os.path.getsize(file_path)
    except Exception:
        return -1


def get_file_info(file_path: str) -> dict:
    """
    Get comprehensive file information.
    
    Args:
        file_path: Path to the file
        
    Returns:
        Dictionary with file information
    """
    try:
        path = Path(file_path)
        stat = path.stat()
        
        return {
            'name': path.name,
            'stem': path.stem,
            'suffix': path.suffix,
            'size': stat.st_size,
            'size_mb': round(stat.st_size / (1024 * 1024), 2),
            'created': stat.st_ctime,
            'modified': stat.st_mtime,
            'is_file': path.is_file(),
            'is_dir': path.is_dir(),
            'exists': path.exists(),
            'mime_type': mimetypes.guess_type(str(path))[0]
        }
    except Exception as e:
        return {'error': str(e)}


def copy_file(source: str, destination: str) -> bool:
    """
    Copy file from source to destination.
    
    Args:
        source: Source file path
        destination: Destination file path
        
    Returns:
        True if copy was successful
    """
    try:
        # Ensure destination directory exists
        dest_dir = os.path.dirname(destination)
        ensure_directory_exists(dest_dir)
        
        shutil.copy2(source, destination)
        return True
    except Exception as e:
        print(f"Error copying file from {source} to {destination}: {e}")
        return False


def move_file(source: str, destination: str) -> bool:
    """
    Move file from source to destination.
    
    Args:
        source: Source file path
        destination: Destination file path
        
    Returns:
        True if move was successful
    """
    try:
        # Ensure destination directory exists
        dest_dir = os.path.dirname(destination)
        ensure_directory_exists(dest_dir)
        
        shutil.move(source, destination)
        return True
    except Exception as e:
        print(f"Error moving file from {source} to {destination}: {e}")
        return False


def delete_file(file_path: str) -> bool:
    """
    Delete a file.
    
    Args:
        file_path: Path to the file to delete
        
    Returns:
        True if deletion was successful
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception as e:
        print(f"Error deleting file {file_path}: {e}")
        return False


def list_files_in_directory(
    directory: str,
    extensions: Optional[List[str]] = None,
    recursive: bool = False
) -> List[str]:
    """
    List files in a directory with optional filtering.
    
    Args:
        directory: Directory to search
        extensions: List of file extensions to filter by
        recursive: Whether to search recursively
        
    Returns:
        List of file paths
    """
    try:
        path = Path(directory)
        if not path.exists():
            return []
        
        if recursive:
            files = list(path.rglob('*'))
        else:
            files = list(path.iterdir())
        
        # Filter for files only
        files = [str(f) for f in files if f.is_file()]
        
        # Filter by extensions if specified
        if extensions:
            files = [f for f in files if get_file_extension(f) in extensions]
        
        return sorted(files)
    except Exception as e:
        print(f"Error listing files in {directory}: {e}")
        return []


def get_unique_filename(file_path: str) -> str:
    """
    Get a unique filename by adding a number if file already exists.
    
    Args:
        file_path: Original file path
        
    Returns:
        Unique file path
    """
    if not os.path.exists(file_path):
        return file_path
    
    path = Path(file_path)
    name = path.stem
    extension = path.suffix
    directory = path.parent
    
    counter = 1
    while True:
        new_name = f"{name}_{counter}{extension}"
        new_path = directory / new_name
        
        if not new_path.exists():
            return str(new_path)
        
        counter += 1


def create_backup(file_path: str, backup_dir: str = "backups") -> Optional[str]:
    """
    Create a backup of a file.
    
    Args:
        file_path: Path to the file to backup
        backup_dir: Directory to store backups
        
    Returns:
        Path to backup file if successful, None otherwise
    """
    try:
        if not os.path.exists(file_path):
            return None
        
        # Ensure backup directory exists
        ensure_directory_exists(backup_dir)
        
        # Create backup filename with timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        path = Path(file_path)
        backup_name = f"{path.stem}_{timestamp}{path.suffix}"
        backup_path = os.path.join(backup_dir, backup_name)
        
        # Copy file to backup location
        if copy_file(file_path, backup_path):
            return backup_path
        
        return None
    except Exception as e:
        print(f"Error creating backup of {file_path}: {e}")
        return None


def clean_directory(directory: str, extensions: Optional[List[str]] = None) -> int:
    """
    Clean directory by removing files with specified extensions.
    
    Args:
        directory: Directory to clean
        extensions: List of extensions to remove (if None, removes all files)
        
    Returns:
        Number of files removed
    """
    try:
        if not os.path.exists(directory):
            return 0
        
        files = list_files_in_directory(directory, extensions)
        removed_count = 0
        
        for file_path in files:
            if delete_file(file_path):
                removed_count += 1
        
        return removed_count
    except Exception as e:
        print(f"Error cleaning directory {directory}: {e}")
        return 0


def get_directory_size(directory: str) -> int:
    """
    Get total size of directory in bytes.
    
    Args:
        directory: Directory path
        
    Returns:
        Total size in bytes
    """
    try:
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                if os.path.exists(file_path):
                    total_size += os.path.getsize(file_path)
        return total_size
    except Exception:
        return 0
