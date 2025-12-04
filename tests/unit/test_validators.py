"""
Unit tests for input validation utilities.
"""

import pytest
import tempfile
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

from src.utils.validators import (
    validate_pdf_file,
    validate_dietary_prefs,
    validate_allergen_list,
    validate_file_path,
    validate_confidence_threshold,
)


class TestValidatePDFFile:
    """Tests for validate_pdf_file function."""
    
    def test_valid_pdf_file(self, tmp_path):
        """Test validation of a valid PDF file."""
        # Create a temporary PDF file
        pdf_file = tmp_path / "test_menu.pdf"
        pdf_file.write_bytes(b"%PDF-1.4\n%fake pdf content" * 100)  # ~2KB
        
        is_valid, error = validate_pdf_file(str(pdf_file))
        assert is_valid is True
        assert error == ""
    
    def test_nonexistent_file(self):
        """Test validation of non-existent file."""
        is_valid, error = validate_pdf_file("/nonexistent/file.pdf")
        assert is_valid is False
        assert "does not exist" in error.lower()
    
    def test_directory_instead_of_file(self, tmp_path):
        """Test validation when path is a directory."""
        is_valid, error = validate_pdf_file(str(tmp_path))
        assert is_valid is False
        assert "not a file" in error.lower()
    
    def test_wrong_file_extension(self, tmp_path):
        """Test validation of file with wrong extension."""
        txt_file = tmp_path / "test.txt"
        txt_file.write_text("Not a PDF")
        
        is_valid, error = validate_pdf_file(str(txt_file))
        assert is_valid is False
        assert ".pdf" in error.lower()
    
    def test_file_too_large(self, tmp_path):
        """Test validation of file exceeding size limit."""
        pdf_file = tmp_path / "large.pdf"
        # Create a file larger than 50MB (default limit)
        large_content = b"%PDF-1.4\n" * (6 * 1024 * 1024)  # ~51MB
        pdf_file.write_bytes(large_content)
        
        is_valid, error = validate_pdf_file(str(pdf_file))
        assert is_valid is False
        assert "exceeds maximum" in error.lower() or "size" in error.lower()
    
    def test_file_too_large_custom_limit(self, tmp_path):
        """Test validation with custom size limit."""
        pdf_file = tmp_path / "test.pdf"
        # Create a file that's exactly 2MB
        content = b"%PDF-1.4\n" + b"x" * (2 * 1024 * 1024 - 10)  # ~2MB
        pdf_file.write_bytes(content)
        
        # Should pass with 10MB limit
        is_valid, error = validate_pdf_file(str(pdf_file), max_size_mb=10)
        assert is_valid is True, f"Expected valid with 10MB limit, got: {error}"
        
        # Should fail with 1MB limit
        is_valid, error = validate_pdf_file(str(pdf_file), max_size_mb=1)
        assert is_valid is False, f"Expected invalid with 1MB limit, got: {error}"
    
    def test_empty_file(self, tmp_path):
        """Test validation of empty file."""
        pdf_file = tmp_path / "empty.pdf"
        pdf_file.touch()
        
        is_valid, error = validate_pdf_file(str(pdf_file))
        assert is_valid is False
        assert "empty" in error.lower()
    
    def test_invalid_path_type(self):
        """Test validation with invalid path type."""
        is_valid, error = validate_pdf_file(None)
        assert is_valid is False
        assert "string" in error.lower()
        
        is_valid, error = validate_pdf_file(123)
        assert is_valid is False
    
    def test_case_insensitive_extension(self, tmp_path):
        """Test that PDF extension is case-insensitive."""
        pdf_file = tmp_path / "test.PDF"
        pdf_file.write_bytes(b"%PDF-1.4\n" * 100)
        
        is_valid, error = validate_pdf_file(str(pdf_file))
        assert is_valid is True


class TestValidateDietaryPrefs:
    """Tests for validate_dietary_prefs function."""
    
    def test_valid_preferences(self):
        """Test validation of valid dietary preferences."""
        prefs = ["vegan", "gluten_free"]
        is_valid, error = validate_dietary_prefs(prefs)
        assert is_valid is True
        assert error == ""
    
    def test_single_valid_preference(self):
        """Test validation of single valid preference."""
        is_valid, error = validate_dietary_prefs(["vegetarian"])
        assert is_valid is True
    
    def test_all_valid_preferences(self):
        """Test validation of all valid preferences."""
        prefs = ["vegan", "vegetarian", "gluten_free", "keto"]
        is_valid, error = validate_dietary_prefs(prefs)
        assert is_valid is True
    
    def test_case_insensitive(self):
        """Test that preferences are case-insensitive."""
        prefs = ["VEGAN", "Gluten_Free"]
        is_valid, error = validate_dietary_prefs(prefs)
        assert is_valid is True
    
    def test_spaces_normalized(self):
        """Test that spaces are normalized to underscores."""
        prefs = ["gluten free", "vegan"]
        is_valid, error = validate_dietary_prefs(prefs)
        assert is_valid is True
    
    def test_invalid_preference(self):
        """Test validation with invalid preference."""
        prefs = ["vegan", "paleo"]  # paleo is not in config
        is_valid, error = validate_dietary_prefs(prefs)
        assert is_valid is False
        assert "paleo" in error.lower()
        assert "invalid" in error.lower()
    
    def test_duplicate_preferences(self):
        """Test validation with duplicate preferences."""
        prefs = ["vegan", "vegetarian", "vegan"]
        is_valid, error = validate_dietary_prefs(prefs)
        assert is_valid is False
        assert "duplicate" in error.lower()
    
    def test_empty_list(self):
        """Test validation of empty list."""
        is_valid, error = validate_dietary_prefs([])
        assert is_valid is True  # Empty list is valid
    
    def test_not_a_list(self):
        """Test validation with non-list input."""
        is_valid, error = validate_dietary_prefs("vegan")
        assert is_valid is False
        assert "list" in error.lower()
    
    def test_non_string_in_list(self):
        """Test validation with non-string in list."""
        prefs = ["vegan", 123]
        is_valid, error = validate_dietary_prefs(prefs)
        assert is_valid is False
        assert "string" in error.lower()


class TestValidateAllergenList:
    """Tests for validate_allergen_list function."""
    
    def test_valid_allergens(self):
        """Test validation of valid allergens."""
        allergens = ["peanuts", "shellfish", "milk"]
        is_valid, error = validate_allergen_list(allergens)
        assert is_valid is True
        assert error == ""
    
    def test_single_valid_allergen(self):
        """Test validation of single valid allergen."""
        is_valid, error = validate_allergen_list(["eggs"])
        assert is_valid is True
    
    def test_case_insensitive(self):
        """Test that allergens are case-insensitive."""
        allergens = ["PEANUTS", "Tree Nuts"]
        is_valid, error = validate_allergen_list(allergens)
        assert is_valid is True
    
    def test_all_categories(self):
        """Test allergens from all severity categories."""
        allergens = ["peanuts", "gluten", "high sodium"]
        is_valid, error = validate_allergen_list(allergens)
        assert is_valid is True
    
    def test_invalid_allergen(self):
        """Test validation with invalid allergen."""
        allergens = ["peanuts", "bananas"]  # bananas is not an allergen
        is_valid, error = validate_allergen_list(allergens)
        assert is_valid is False
        assert "bananas" in error.lower()
        assert "invalid" in error.lower()
    
    def test_duplicate_allergens(self):
        """Test validation with duplicate allergens."""
        allergens = ["peanuts", "shellfish", "peanuts"]
        is_valid, error = validate_allergen_list(allergens)
        assert is_valid is False
        assert "duplicate" in error.lower()
    
    def test_empty_list(self):
        """Test validation of empty list."""
        is_valid, error = validate_allergen_list([])
        assert is_valid is True  # Empty list is valid
    
    def test_not_a_list(self):
        """Test validation with non-list input."""
        is_valid, error = validate_allergen_list("peanuts")
        assert is_valid is False
        assert "list" in error.lower()
    
    def test_non_string_in_list(self):
        """Test validation with non-string in list."""
        allergens = ["peanuts", 123]
        is_valid, error = validate_allergen_list(allergens)
        assert is_valid is False
        assert "string" in error.lower()
    
    def test_whitespace_handling(self):
        """Test that whitespace is properly handled."""
        allergens = ["  peanuts  ", " tree nuts "]
        is_valid, error = validate_allergen_list(allergens)
        assert is_valid is True
    
    def test_empty_strings_filtered(self):
        """Test that empty strings are filtered out."""
        allergens = ["peanuts", "", "  ", "shellfish"]
        is_valid, error = validate_allergen_list(allergens)
        assert is_valid is True


class TestValidateFilePath:
    """Tests for validate_file_path function."""
    
    def test_valid_existing_file(self, tmp_path):
        """Test validation of existing file."""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")
        
        is_valid, error = validate_file_path(str(test_file), must_exist=True)
        assert is_valid is True
        assert error == ""
    
    def test_nonexistent_file_must_exist(self):
        """Test validation when file must exist but doesn't."""
        is_valid, error = validate_file_path("/nonexistent/file.txt", must_exist=True)
        assert is_valid is False
        assert "does not exist" in error.lower()
    
    def test_nonexistent_file_not_required(self, tmp_path):
        """Test validation when file doesn't need to exist."""
        new_file = tmp_path / "new_file.txt"
        is_valid, error = validate_file_path(str(new_file), must_exist=False)
        assert is_valid is True
    
    def test_directory_instead_of_file(self, tmp_path):
        """Test validation when path is a directory."""
        is_valid, error = validate_file_path(str(tmp_path), must_exist=True)
        assert is_valid is False
        assert "not a file" in error.lower()
    
    def test_invalid_path_type(self):
        """Test validation with invalid path type."""
        is_valid, error = validate_file_path(None)
        assert is_valid is False
        assert "string" in error.lower()


class TestValidateConfidenceThreshold:
    """Tests for validate_confidence_threshold function."""
    
    def test_valid_threshold(self):
        """Test validation of valid confidence threshold."""
        is_valid, error = validate_confidence_threshold(0.9)
        assert is_valid is True
        assert error == ""
    
    def test_boundary_values(self):
        """Test validation of boundary values (0.0 and 1.0)."""
        is_valid, error = validate_confidence_threshold(0.0)
        assert is_valid is True
        
        is_valid, error = validate_confidence_threshold(1.0)
        assert is_valid is True
    
    def test_below_minimum(self):
        """Test validation of threshold below 0.0."""
        is_valid, error = validate_confidence_threshold(-0.1)
        assert is_valid is False
        assert "between 0.0 and 1.0" in error.lower()
    
    def test_above_maximum(self):
        """Test validation of threshold above 1.0."""
        is_valid, error = validate_confidence_threshold(1.1)
        assert is_valid is False
        assert "between 0.0 and 1.0" in error.lower()
    
    def test_integer_input(self):
        """Test that integer input is accepted."""
        is_valid, error = validate_confidence_threshold(1)
        assert is_valid is True
    
    def test_non_numeric_input(self):
        """Test validation with non-numeric input."""
        is_valid, error = validate_confidence_threshold("0.9")
        assert is_valid is False
        assert "number" in error.lower()
        
        is_valid, error = validate_confidence_threshold(None)
        assert is_valid is False


class TestEdgeCases:
    """Tests for edge cases and error handling."""
    
    def test_pdf_file_permission_error(self, tmp_path):
        """Test handling of permission errors."""
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"%PDF-1.4\n" * 100)
        
        # Make file unreadable (Unix-like systems)
        if os.name != 'nt':  # Not Windows
            os.chmod(pdf_file, 0o000)
            try:
                is_valid, error = validate_pdf_file(str(pdf_file))
                assert is_valid is False
                assert "readable" in error.lower() or "permission" in error.lower()
            finally:
                os.chmod(pdf_file, 0o644)
    
    def test_config_error_handling(self):
        """Test that validators handle config errors gracefully."""
        with patch('src.utils.validators.get_config') as mock_config:
            mock_config.side_effect = Exception("Config error")
            
            # Should still validate basic structure
            is_valid, error = validate_dietary_prefs(["vegan"])
            # May fail due to config error, but should provide error message
            assert isinstance(is_valid, bool)
            assert isinstance(error, str)

