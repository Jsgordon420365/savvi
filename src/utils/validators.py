"""
Input validation utilities for SAVVI application.

This module provides validation functions for user inputs including:
- PDF file validation (format, size, existence)
- Dietary preference validation
- Allergen list validation
- Configuration validation
"""

import os
from pathlib import Path
from typing import Tuple, List, Optional
from .config import get_config
from .logger import get_logger

logger = get_logger(__name__)


def validate_pdf_file(file_path: str, max_size_mb: Optional[int] = None) -> Tuple[bool, str]:
    """
    Validate that a file path points to a valid PDF file.
    
    Checks:
    - File exists
    - File is readable
    - File extension is .pdf
    - File size is within limits (default: 50MB from config)
    
    Args:
        file_path: Path to the file to validate
        max_size_mb: Maximum file size in MB (defaults to config value)
    
    Returns:
        Tuple of (is_valid: bool, error_message: str)
        If valid, error_message will be empty string
    """
    try:
        # Check if file path is provided
        if not file_path or not isinstance(file_path, str):
            return False, "File path must be a non-empty string"
        
        # Convert to Path object for easier manipulation
        path = Path(file_path)
        
        # Check if file exists
        if not path.exists():
            return False, f"File does not exist: {file_path}"
        
        # Check if it's a file (not a directory)
        if not path.is_file():
            return False, f"Path is not a file: {file_path}"
        
        # Check file extension
        if path.suffix.lower() != '.pdf':
            return False, f"File must be a PDF (.pdf extension). Found: {path.suffix}"
        
        # Check file size
        if max_size_mb is None:
            config = get_config()
            pdf_settings = config.get_pdf_settings()
            max_size_mb = pdf_settings.get('max_file_size_mb', 50)
        
        file_size_mb = path.stat().st_size / (1024 * 1024)
        if file_size_mb > max_size_mb:
            return False, (
                f"File size ({file_size_mb:.2f} MB) exceeds maximum allowed size "
                f"({max_size_mb} MB)"
            )
        
        # Check if file is readable
        if not os.access(path, os.R_OK):
            return False, f"File is not readable: {file_path}"
        
        # Check if file is not empty
        if path.stat().st_size == 0:
            return False, "File is empty"
        
        logger.debug(f"PDF file validation passed: {file_path} ({file_size_mb:.2f} MB)")
        return True, ""
    
    except PermissionError:
        return False, f"Permission denied accessing file: {file_path}"
    except OSError as e:
        return False, f"OS error accessing file: {file_path} - {str(e)}"
    except Exception as e:
        logger.error(f"Unexpected error validating PDF file: {e}", exc_info=True)
        return False, f"Unexpected error validating file: {str(e)}"


def validate_dietary_prefs(prefs: List[str]) -> Tuple[bool, str]:
    """
    Validate a list of dietary preferences against configured options.
    
    Valid dietary preferences are defined in config/savvi_config.yaml:
    - vegan
    - vegetarian
    - gluten_free
    - keto
    
    Args:
        prefs: List of dietary preference strings to validate
    
    Returns:
        Tuple of (is_valid: bool, error_message: str)
        If valid, error_message will be empty string
    """
    try:
        # Check if input is a list
        if not isinstance(prefs, list):
            return False, "Dietary preferences must be a list"
        
        # Get valid preferences from config
        config = get_config()
        dietary_config = config.get_dietary_preferences()
        valid_prefs = set(dietary_config.keys())
        
        # Normalize input (handle case-insensitive, spaces, underscores)
        normalized_prefs = []
        for pref in prefs:
            if not isinstance(pref, str):
                return False, f"All dietary preferences must be strings. Found: {type(pref).__name__}"
            
            # Normalize: lowercase, strip whitespace, replace spaces with underscores
            normalized = pref.lower().strip().replace(' ', '_')
            normalized_prefs.append(normalized)
        
        # Check for duplicates
        if len(normalized_prefs) != len(set(normalized_prefs)):
            duplicates = [p for p in normalized_prefs if normalized_prefs.count(p) > 1]
            return False, f"Duplicate dietary preferences found: {set(duplicates)}"
        
        # Validate each preference
        invalid_prefs = []
        for pref in normalized_prefs:
            if pref not in valid_prefs:
                invalid_prefs.append(pref)
        
        if invalid_prefs:
            return False, (
                f"Invalid dietary preferences: {', '.join(invalid_prefs)}. "
                f"Valid options are: {', '.join(sorted(valid_prefs))}"
            )
        
        logger.debug(f"Dietary preferences validation passed: {normalized_prefs}")
        return True, ""
    
    except Exception as e:
        logger.error(f"Error validating dietary preferences: {e}", exc_info=True)
        return False, f"Error validating dietary preferences: {str(e)}"


def validate_allergen_list(allergens: List[str]) -> Tuple[bool, str]:
    """
    Validate a list of allergens against configured allergen categories.
    
    Valid allergens are defined in config/savvi_config.yaml under allergen_categories:
    - Critical: peanuts, tree nuts, shellfish, fish, sesame, milk, eggs, wheat, soy
    - Moderate: gluten, processed in shared facilities
    - Mild: high sodium, spicy
    
    Args:
        allergens: List of allergen strings to validate
    
    Returns:
        Tuple of (is_valid: bool, error_message: str)
        If valid, error_message will be empty string
    """
    try:
        # Check if input is a list
        if not isinstance(allergens, list):
            return False, "Allergens must be a list"
        
        # Get valid allergens from config
        config = get_config()
        allergen_rules = config.get_allergen_rules()
        
        # Build set of all valid allergens (from all categories)
        valid_allergens = set()
        for category, allergen_list in allergen_rules.items():
            if isinstance(allergen_list, list):
                valid_allergens.update(allergen.lower() for allergen in allergen_list)
        
        # Normalize input (handle case-insensitive, spaces)
        normalized_allergens = []
        for allergen in allergens:
            if not isinstance(allergen, str):
                return False, f"All allergens must be strings. Found: {type(allergen).__name__}"
            
            # Normalize: lowercase, strip whitespace
            normalized = allergen.lower().strip()
            if normalized:
                normalized_allergens.append(normalized)
        
        # Check for duplicates
        if len(normalized_allergens) != len(set(normalized_allergens)):
            duplicates = [a for a in normalized_allergens if normalized_allergens.count(a) > 1]
            return False, f"Duplicate allergens found: {set(duplicates)}"
        
        # Validate each allergen
        invalid_allergens = []
        for allergen in normalized_allergens:
            if allergen not in valid_allergens:
                invalid_allergens.append(allergen)
        
        if invalid_allergens:
            # Provide helpful suggestions for common misspellings
            suggestions = []
            for invalid in invalid_allergens:
                # Simple fuzzy matching for common variations
                close_matches = [
                    valid for valid in valid_allergens
                    if invalid in valid or valid in invalid
                ]
                if close_matches:
                    suggestions.append(f"{invalid} (did you mean: {', '.join(close_matches[:2])}?)")
            
            error_msg = f"Invalid allergens: {', '.join(invalid_allergens)}"
            if suggestions:
                error_msg += f"\nSuggestions: {'; '.join(suggestions)}"
            error_msg += f"\nValid allergens: {', '.join(sorted(valid_allergens))}"
            
            return False, error_msg
        
        logger.debug(f"Allergen list validation passed: {normalized_allergens}")
        return True, ""
    
    except Exception as e:
        logger.error(f"Error validating allergen list: {e}", exc_info=True)
        return False, f"Error validating allergen list: {str(e)}"


def validate_file_path(file_path: str, must_exist: bool = True) -> Tuple[bool, str]:
    """
    Validate a general file path (not necessarily a PDF).
    
    Args:
        file_path: Path to validate
        must_exist: Whether the file must exist (default: True)
    
    Returns:
        Tuple of (is_valid: bool, error_message: str)
    """
    try:
        if not file_path or not isinstance(file_path, str):
            return False, "File path must be a non-empty string"
        
        path = Path(file_path)
        
        if must_exist and not path.exists():
            return False, f"File does not exist: {file_path}"
        
        if must_exist and not path.is_file():
            return False, f"Path is not a file: {file_path}"
        
        # Check if parent directory exists (for output paths)
        if not must_exist:
            parent = path.parent
            if parent and not parent.exists():
                return False, f"Parent directory does not exist: {parent}"
        
        return True, ""
    
    except Exception as e:
        logger.error(f"Error validating file path: {e}", exc_info=True)
        return False, f"Error validating file path: {str(e)}"


def validate_confidence_threshold(threshold: float) -> Tuple[bool, str]:
    """
    Validate a confidence threshold value.
    
    Args:
        threshold: Confidence threshold to validate (must be between 0.0 and 1.0)
    
    Returns:
        Tuple of (is_valid: bool, error_message: str)
    """
    try:
        if not isinstance(threshold, (int, float)):
            return False, f"Confidence threshold must be a number. Found: {type(threshold).__name__}"
        
        threshold_float = float(threshold)
        
        if threshold_float < 0.0 or threshold_float > 1.0:
            return False, f"Confidence threshold must be between 0.0 and 1.0. Found: {threshold_float}"
        
        return True, ""
    
    except (ValueError, TypeError) as e:
        return False, f"Invalid confidence threshold value: {str(e)}"
    except Exception as e:
        logger.error(f"Error validating confidence threshold: {e}", exc_info=True)
        return False, f"Error validating confidence threshold: {str(e)}"

