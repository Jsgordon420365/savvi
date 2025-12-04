"""
Unit tests for menu_parser module.
"""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
from PyPDF2.errors import PdfReadError

from src.core.menu_parser import MenuParser


class TestMenuParser:
    """Tests for MenuParser class."""
    
    def test_init_valid_pdf(self, tmp_path):
        """Test initialization with valid PDF file."""
        # Create a minimal valid PDF file
        pdf_file = tmp_path / "test_menu.pdf"
        pdf_file.write_bytes(b"%PDF-1.4\n%fake pdf content" * 100)
        
        parser = MenuParser(str(pdf_file))
        assert parser.pdf_path == pdf_file
        assert parser._reader is None  # Lazy loading
    
    def test_init_nonexistent_file(self):
        """Test initialization with non-existent file."""
        # validate_pdf_file catches this first and raises ValueError
        with pytest.raises(ValueError, match="Invalid PDF file"):
            MenuParser("/nonexistent/file.pdf")
    
    def test_init_invalid_file(self, tmp_path):
        """Test initialization with invalid file (not PDF)."""
        txt_file = tmp_path / "test.txt"
        txt_file.write_text("Not a PDF")
        
        with pytest.raises(ValueError, match="Invalid PDF file"):
            MenuParser(str(txt_file))
    
    def test_extract_text_single_page(self, tmp_path):
        """Test text extraction from single-page PDF."""
        # Note: This test requires a real PDF or mocking PyPDF2
        # For now, we'll test the structure
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"%PDF-1.4\n%fake pdf content" * 100)
        
        with patch('src.core.menu_parser.PdfReader') as mock_reader_class:
            mock_page = MagicMock()
            mock_page.extract_text.return_value = "Menu Item 1\nMenu Item 2"
            
            mock_reader = MagicMock()
            mock_reader.pages = [mock_page]
            mock_reader.metadata = {}
            mock_reader_class.return_value = mock_reader
            
            parser = MenuParser(str(pdf_file))
            text = parser.extract_text()
            
            assert "Menu Item 1" in text
            assert "Menu Item 2" in text
    
    def test_extract_text_multi_page(self, tmp_path):
        """Test text extraction from multi-page PDF."""
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"%PDF-1.4\n%fake pdf content" * 100)
        
        with patch('src.core.menu_parser.PdfReader') as mock_reader_class:
            mock_page1 = MagicMock()
            mock_page1.extract_text.return_value = "Page 1 Content"
            
            mock_page2 = MagicMock()
            mock_page2.extract_text.return_value = "Page 2 Content"
            
            mock_reader = MagicMock()
            mock_reader.pages = [mock_page1, mock_page2]
            mock_reader.metadata = {}
            mock_reader_class.return_value = mock_reader
            
            parser = MenuParser(str(pdf_file))
            text = parser.extract_text()
            
            assert "Page 1 Content" in text
            assert "Page 2 Content" in text
            assert "--- Page 2 ---" in text
    
    def test_extract_by_page(self, tmp_path):
        """Test extraction by page returns dictionary."""
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"%PDF-1.4\n%fake pdf content" * 100)
        
        with patch('src.core.menu_parser.PdfReader') as mock_reader_class:
            mock_page1 = MagicMock()
            mock_page1.extract_text.return_value = "Page 1"
            
            mock_page2 = MagicMock()
            mock_page2.extract_text.return_value = "Page 2"
            
            mock_reader = MagicMock()
            mock_reader.pages = [mock_page1, mock_page2]
            mock_reader.metadata = {}
            mock_reader_class.return_value = mock_reader
            
            parser = MenuParser(str(pdf_file))
            page_texts = parser.extract_by_page()
            
            assert isinstance(page_texts, dict)
            assert page_texts[1] == "Page 1"
            assert page_texts[2] == "Page 2"
            assert len(page_texts) == 2
    
    def test_extract_metadata(self, tmp_path):
        """Test metadata extraction."""
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"%PDF-1.4\n%fake pdf content" * 100)
        
        with patch('src.core.menu_parser.PdfReader') as mock_reader_class:
            mock_page = MagicMock()
            mock_reader = MagicMock()
            mock_reader.pages = [mock_page]
            mock_reader.metadata = {
                "/Title": "Test Menu",
                "/Author": "Test Author",
                "/Creator": "Test Creator",
                "/Producer": "Test Producer",
            }
            mock_reader_class.return_value = mock_reader
            
            parser = MenuParser(str(pdf_file))
            metadata = parser.extract_metadata()
            
            assert metadata["title"] == "Test Menu"
            assert metadata["author"] == "Test Author"
            assert metadata["page_count"] == 1
            assert "file_size" in metadata
    
    def test_extract_metadata_no_metadata(self, tmp_path):
        """Test metadata extraction when PDF has no metadata."""
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"%PDF-1.4\n%fake pdf content" * 100)
        
        with patch('src.core.menu_parser.PdfReader') as mock_reader_class:
            mock_page = MagicMock()
            mock_reader = MagicMock()
            mock_reader.pages = [mock_page]
            mock_reader.metadata = None
            mock_reader_class.return_value = mock_reader
            
            parser = MenuParser(str(pdf_file))
            metadata = parser.extract_metadata()
            
            assert metadata["title"] == ""
            assert metadata["author"] == ""
            assert metadata["page_count"] == 1
    
    def test_get_page_count(self, tmp_path):
        """Test getting page count."""
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"%PDF-1.4\n%fake pdf content" * 100)
        
        with patch('src.core.menu_parser.PdfReader') as mock_reader_class:
            mock_reader = MagicMock()
            mock_reader.pages = [MagicMock(), MagicMock(), MagicMock()]
            mock_reader.metadata = {}
            mock_reader_class.return_value = mock_reader
            
            parser = MenuParser(str(pdf_file))
            count = parser.get_page_count()
            
            assert count == 3
    
    def test_is_text_based_true(self, tmp_path):
        """Test is_text_based returns True for text-based PDF."""
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"%PDF-1.4\n%fake pdf content" * 100)
        
        with patch('src.core.menu_parser.PdfReader') as mock_reader_class:
            mock_page = MagicMock()
            mock_page.extract_text.return_value = "A" * 100  # >50 chars
            mock_reader = MagicMock()
            mock_reader.pages = [mock_page]
            mock_reader.metadata = {}
            mock_reader_class.return_value = mock_reader
            
            parser = MenuParser(str(pdf_file))
            assert parser.is_text_based() is True
    
    def test_is_text_based_false(self, tmp_path):
        """Test is_text_based returns False for image-based PDF."""
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"%PDF-1.4\n%fake pdf content" * 100)
        
        with patch('src.core.menu_parser.PdfReader') as mock_reader_class:
            mock_page = MagicMock()
            mock_page.extract_text.return_value = "  "  # <50 chars (scanned)
            mock_reader = MagicMock()
            mock_reader.pages = [mock_page]
            mock_reader.metadata = {}
            mock_reader_class.return_value = mock_reader
            
            parser = MenuParser(str(pdf_file))
            assert parser.is_text_based() is False
    
    def test_corrupted_pdf_error(self, tmp_path):
        """Test handling of corrupted PDF."""
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"%PDF-1.4\n%fake pdf content" * 100)
        
        with patch('src.core.menu_parser.PdfReader') as mock_reader_class:
            mock_reader_class.side_effect = PdfReadError("Corrupted PDF")
            
            parser = MenuParser(str(pdf_file))
            
            with pytest.raises(ValueError, match="Corrupted or invalid PDF"):
                parser.extract_text()
    
    def test_empty_page_handling(self, tmp_path):
        """Test handling of empty pages."""
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"%PDF-1.4\n%fake pdf content" * 100)
        
        with patch('src.core.menu_parser.PdfReader') as mock_reader_class:
            mock_page1 = MagicMock()
            mock_page1.extract_text.return_value = "Content"
            
            mock_page2 = MagicMock()
            mock_page2.extract_text.return_value = ""  # Empty page
            
            mock_reader = MagicMock()
            mock_reader.pages = [mock_page1, mock_page2]
            mock_reader.metadata = {}
            mock_reader_class.return_value = mock_reader
            
            parser = MenuParser(str(pdf_file))
            text = parser.extract_text()
            
            assert "Content" in text
            assert "Page 2" in text  # Should still mark page break
    
    def test_page_extraction_error_handling(self, tmp_path):
        """Test that extraction continues if one page fails."""
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"%PDF-1.4\n%fake pdf content" * 100)
        
        with patch('src.core.menu_parser.PdfReader') as mock_reader_class:
            mock_page1 = MagicMock()
            mock_page1.extract_text.return_value = "Page 1"
            
            mock_page2 = MagicMock()
            mock_page2.extract_text.side_effect = Exception("Page error")
            
            mock_reader = MagicMock()
            mock_reader.pages = [mock_page1, mock_page2]
            mock_reader.metadata = {}
            mock_reader_class.return_value = mock_reader
            
            parser = MenuParser(str(pdf_file))
            text = parser.extract_text()
            
            # Should still extract page 1 and mark page 2 error
            assert "Page 1" in text
            assert "Page 2" in text
            assert "extraction error" in text
    
    def test_metadata_caching(self, tmp_path):
        """Test that metadata is cached after first extraction."""
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"%PDF-1.4\n%fake pdf content" * 100)
        
        with patch('src.core.menu_parser.PdfReader') as mock_reader_class:
            mock_page = MagicMock()
            mock_reader = MagicMock()
            mock_reader.pages = [mock_page]
            mock_reader.metadata = {"/Title": "Test"}
            mock_reader_class.return_value = mock_reader
            
            parser = MenuParser(str(pdf_file))
            
            # First call
            metadata1 = parser.extract_metadata()
            # Second call should use cache
            metadata2 = parser.extract_metadata()
            
            assert metadata1 == metadata2
            # Should only call PdfReader once (during _get_reader)
            assert mock_reader_class.call_count == 1

