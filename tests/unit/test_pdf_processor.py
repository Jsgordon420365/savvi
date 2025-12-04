"""
Unit tests for pdf_processor module.
"""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock, Mock
from PIL import Image
import pytesseract

from src.processors.pdf_processor import PDFProcessor
from src.core.menu_parser import MenuParser


class TestPDFProcessor:
    """Tests for PDFProcessor class."""
    
    def test_init_valid_pdf(self, tmp_path):
        """Test initialization with valid PDF file."""
        pdf_file = tmp_path / "test_menu.pdf"
        pdf_file.write_bytes(b"%PDF-1.4\n%fake pdf content" * 100)
        
        with patch('src.processors.pdf_processor.get_config') as mock_config:
            mock_config_instance = MagicMock()
            mock_config_instance.get_pdf_settings.return_value = {
                "ocr_enabled": True,
                "tesseract_path": None,
                "ocr_language": "eng",
                "ocr_quality_threshold": 0.75,
            }
            mock_config.return_value = mock_config_instance
            
            processor = PDFProcessor(str(pdf_file))
            assert processor.pdf_path == pdf_file
            assert processor.ocr_enabled is True
            assert processor.ocr_language == "eng"
    
    def test_init_with_tesseract_path(self, tmp_path):
        """Test initialization with custom Tesseract path."""
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"%PDF-1.4\n" * 100)
        
        with patch('src.processors.pdf_processor.get_config') as mock_config:
            mock_config_instance = MagicMock()
            mock_config_instance.get_pdf_settings.return_value = {
                "ocr_enabled": True,
                "tesseract_path": "C:\\Program Files\\Tesseract-OCR\\tesseract.exe",
                "ocr_language": "eng",
                "ocr_quality_threshold": 0.75,
            }
            mock_config.return_value = mock_config_instance
            
            processor = PDFProcessor(str(pdf_file))
            assert processor.tesseract_path == "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
    
    def test_is_scanned_menu_text_based(self, tmp_path):
        """Test is_scanned_menu returns False for text-based PDF."""
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"%PDF-1.4\n" * 100)
        
        with patch('src.processors.pdf_processor.get_config') as mock_config, \
             patch('src.processors.pdf_processor.MenuParser') as mock_parser_class:
            
            mock_config_instance = MagicMock()
            mock_config_instance.get_pdf_settings.return_value = {
                "ocr_enabled": True,
                "tesseract_path": None,
                "ocr_language": "eng",
                "ocr_quality_threshold": 0.75,
            }
            mock_config.return_value = mock_config_instance
            
            mock_parser = MagicMock()
            mock_parser.is_text_based.return_value = True
            mock_parser.extract_by_page.return_value = {1: "A" * 100}  # >50 chars
            mock_parser_class.return_value = mock_parser
            
            processor = PDFProcessor(str(pdf_file))
            assert processor.is_scanned_menu() is False
    
    def test_is_scanned_menu_scanned(self, tmp_path):
        """Test is_scanned_menu returns True for scanned PDF."""
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"%PDF-1.4\n" * 100)
        
        with patch('src.processors.pdf_processor.get_config') as mock_config, \
             patch('src.processors.pdf_processor.MenuParser') as mock_parser_class:
            
            mock_config_instance = MagicMock()
            mock_config_instance.get_pdf_settings.return_value = {
                "ocr_enabled": True,
                "tesseract_path": None,
                "ocr_language": "eng",
                "ocr_quality_threshold": 0.75,
            }
            mock_config.return_value = mock_config_instance
            
            mock_parser = MagicMock()
            mock_parser.is_text_based.return_value = False
            mock_parser.extract_by_page.return_value = {1: "  "}  # <50 chars
            mock_parser_class.return_value = mock_parser
            
            processor = PDFProcessor(str(pdf_file))
            assert processor.is_scanned_menu() is True
    
    def test_convert_to_images(self, tmp_path):
        """Test PDF to images conversion."""
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"%PDF-1.4\n" * 100)
        
        with patch('src.processors.pdf_processor.get_config') as mock_config, \
             patch('src.processors.pdf_processor.convert_from_path') as mock_convert:
            
            mock_config_instance = MagicMock()
            mock_config_instance.get_pdf_settings.return_value = {
                "ocr_enabled": True,
                "tesseract_path": None,
                "ocr_language": "eng",
                "ocr_quality_threshold": 0.75,
            }
            mock_config.return_value = mock_config_instance
            
            # Create mock images - use actual PIL Images
            mock_image1 = Image.new('RGB', (100, 100), color='white')
            mock_image2 = Image.new('RGB', (100, 100), color='white')
            mock_convert.return_value = [mock_image1, mock_image2]
            
            processor = PDFProcessor(str(pdf_file))
            images = processor.convert_to_images(dpi=150)
            
            assert len(images) == 2
            assert images[0] == mock_image1
            assert images[1] == mock_image2
            mock_convert.assert_called_once_with(
                str(pdf_file),
                dpi=150,
                fmt='png'
            )
    
    def test_convert_to_images_caching(self, tmp_path):
        """Test that converted images are cached."""
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"%PDF-1.4\n" * 100)
        
        with patch('src.processors.pdf_processor.get_config') as mock_config, \
             patch('src.processors.pdf_processor.convert_from_path') as mock_convert:
            
            mock_config_instance = MagicMock()
            mock_config_instance.get_pdf_settings.return_value = {
                "ocr_enabled": True,
                "tesseract_path": None,
                "ocr_language": "eng",
                "ocr_quality_threshold": 0.75,
            }
            mock_config.return_value = mock_config_instance
            
            mock_image = Image.new('RGB', (100, 100), color='white')
            mock_convert.return_value = [mock_image]
            
            processor = PDFProcessor(str(pdf_file))
            
            # First call
            images1 = processor.convert_to_images()
            # Second call should use cache
            images2 = processor.convert_to_images()
            
            assert images1 == images2
            # Should only call convert_from_path once
            assert mock_convert.call_count == 1
    
    def test_convert_to_images_poppler_error(self, tmp_path):
        """Test handling of poppler not installed error."""
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"%PDF-1.4\n" * 100)
        
        with patch('src.processors.pdf_processor.get_config') as mock_config, \
             patch('src.processors.pdf_processor.convert_from_path') as mock_convert:
            
            from pdf2image.exceptions import PDFInfoNotInstalledError
            
            mock_config_instance = MagicMock()
            mock_config_instance.get_pdf_settings.return_value = {
                "ocr_enabled": True,
                "tesseract_path": None,
                "ocr_language": "eng",
                "ocr_quality_threshold": 0.75,
            }
            mock_config.return_value = mock_config_instance
            
            mock_convert.side_effect = PDFInfoNotInstalledError()
            
            processor = PDFProcessor(str(pdf_file))
            
            with pytest.raises(ValueError, match="poppler-utils not installed"):
                processor.convert_to_images()
    
    def test_preprocess_image(self, tmp_path):
        """Test image preprocessing."""
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"%PDF-1.4\n" * 100)
        
        with patch('src.processors.pdf_processor.get_config') as mock_config:
            mock_config_instance = MagicMock()
            mock_config_instance.get_pdf_settings.return_value = {
                "ocr_enabled": True,
                "tesseract_path": None,
                "ocr_language": "eng",
                "ocr_quality_threshold": 0.75,
            }
            mock_config.return_value = mock_config_instance
            
            # Create a test image
            test_image = Image.new('RGB', (100, 100), color='white')
            
            processor = PDFProcessor(str(pdf_file))
            processed = processor._preprocess_image(test_image)
            
            # Should be grayscale after preprocessing
            assert processed.mode == 'L'
    
    def test_ocr_image_success(self, tmp_path):
        """Test successful OCR processing."""
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"%PDF-1.4\n" * 100)
        
        with patch('src.processors.pdf_processor.get_config') as mock_config, \
             patch('src.processors.pdf_processor.pytesseract.image_to_string') as mock_ocr:
            
            mock_config_instance = MagicMock()
            mock_config_instance.get_pdf_settings.return_value = {
                "ocr_enabled": True,
                "tesseract_path": None,
                "ocr_language": "eng",
                "ocr_quality_threshold": 0.75,
            }
            mock_config.return_value = mock_config_instance
            
            mock_ocr.return_value = "Extracted text from menu"
            
            test_image = Image.new('RGB', (100, 100), color='white')
            processor = PDFProcessor(str(pdf_file))
            
            text = processor.ocr_image(test_image)
            
            assert text == "Extracted text from menu"
            mock_ocr.assert_called_once()
            # Check that language was passed
            call_args = mock_ocr.call_args
            assert call_args[1]['lang'] == 'eng'
    
    def test_ocr_image_tesseract_not_found(self, tmp_path):
        """Test handling of Tesseract not found error."""
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"%PDF-1.4\n" * 100)
        
        with patch('src.processors.pdf_processor.get_config') as mock_config, \
             patch('src.processors.pdf_processor.pytesseract.image_to_string') as mock_ocr:
            
            mock_config_instance = MagicMock()
            mock_config_instance.get_pdf_settings.return_value = {
                "ocr_enabled": True,
                "tesseract_path": None,
                "ocr_language": "eng",
                "ocr_quality_threshold": 0.75,
            }
            mock_config.return_value = mock_config_instance
            
            mock_ocr.side_effect = pytesseract.TesseractNotFoundError()
            
            test_image = Image.new('RGB', (100, 100), color='white')
            processor = PDFProcessor(str(pdf_file))
            
            with pytest.raises(RuntimeError, match="Tesseract OCR not found"):
                processor.ocr_image(test_image)
    
    def test_ocr_image_disabled(self, tmp_path):
        """Test OCR when disabled in config."""
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"%PDF-1.4\n" * 100)
        
        with patch('src.processors.pdf_processor.get_config') as mock_config:
            mock_config_instance = MagicMock()
            mock_config_instance.get_pdf_settings.return_value = {
                "ocr_enabled": False,
                "tesseract_path": None,
                "ocr_language": "eng",
                "ocr_quality_threshold": 0.75,
            }
            mock_config.return_value = mock_config_instance
            
            test_image = Image.new('RGB', (100, 100), color='white')
            processor = PDFProcessor(str(pdf_file))
            
            with pytest.raises(RuntimeError, match="OCR is disabled"):
                processor.ocr_image(test_image)
    
    def test_process_text_based_pdf(self, tmp_path):
        """Test processing text-based PDF (uses text extraction)."""
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"%PDF-1.4\n" * 100)
        
        with patch('src.processors.pdf_processor.get_config') as mock_config, \
             patch('src.processors.pdf_processor.MenuParser') as mock_parser_class:
            
            mock_config_instance = MagicMock()
            mock_config_instance.get_pdf_settings.return_value = {
                "ocr_enabled": True,
                "tesseract_path": None,
                "ocr_language": "eng",
                "ocr_quality_threshold": 0.75,
            }
            mock_config.return_value = mock_config_instance
            
            mock_parser = MagicMock()
            mock_parser.extract_by_page.return_value = {
                1: "Menu Item 1\nMenu Item 2" * 10,  # >50 chars per page
                2: "More menu items" * 10
            }
            mock_parser_class.return_value = mock_parser
            
            processor = PDFProcessor(str(pdf_file))
            text = processor.process()
            
            assert "Menu Item 1" in text
            assert "Page 2" in text
            # Should not call OCR
            assert not hasattr(processor, '_cached_images') or processor._cached_images is None
    
    def test_process_scanned_pdf(self, tmp_path):
        """Test processing scanned PDF (uses OCR)."""
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"%PDF-1.4\n" * 100)
        
        with patch('src.processors.pdf_processor.get_config') as mock_config, \
             patch('src.processors.pdf_processor.MenuParser') as mock_parser_class, \
             patch('src.processors.pdf_processor.convert_from_path') as mock_convert, \
             patch('src.processors.pdf_processor.pytesseract.image_to_string') as mock_ocr:
            
            mock_config_instance = MagicMock()
            mock_config_instance.get_pdf_settings.return_value = {
                "ocr_enabled": True,
                "tesseract_path": None,
                "ocr_language": "eng",
                "ocr_quality_threshold": 0.75,
            }
            mock_config.return_value = mock_config_instance
            
            # Text extraction yields low character count
            mock_parser = MagicMock()
            mock_parser.extract_by_page.return_value = {1: "  "}  # <50 chars
            mock_parser_class.return_value = mock_parser
            
            # Mock OCR - use actual PIL Image
            mock_image = Image.new('RGB', (100, 100), color='white')
            mock_convert.return_value = [mock_image]
            mock_ocr.return_value = "OCR extracted text"
            
            processor = PDFProcessor(str(pdf_file))
            text = processor.process()
            
            assert "OCR extracted text" in text
            mock_ocr.assert_called()
    
    def test_process_with_ocr_fallback(self, tmp_path):
        """Test that OCR is used as fallback if text extraction fails."""
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"%PDF-1.4\n" * 100)
        
        with patch('src.processors.pdf_processor.get_config') as mock_config, \
             patch('src.processors.pdf_processor.MenuParser') as mock_parser_class, \
             patch('src.processors.pdf_processor.convert_from_path') as mock_convert, \
             patch('src.processors.pdf_processor.pytesseract.image_to_string') as mock_ocr:
            
            mock_config_instance = MagicMock()
            mock_config_instance.get_pdf_settings.return_value = {
                "ocr_enabled": True,
                "tesseract_path": None,
                "ocr_language": "eng",
                "ocr_quality_threshold": 0.75,
            }
            mock_config.return_value = mock_config_instance
            
            # Text extraction raises exception
            mock_parser = MagicMock()
            mock_parser.extract_by_page.side_effect = Exception("Extraction failed")
            mock_parser_class.return_value = mock_parser
            
            # OCR should be used as fallback
            mock_image = Image.new('RGB', (100, 100), color='white')
            mock_convert.return_value = [mock_image]
            mock_ocr.return_value = "Fallback OCR text"
            
            processor = PDFProcessor(str(pdf_file))
            text = processor.process()
            
            assert "Fallback OCR text" in text
    
    def test_process_ocr_disabled_error(self, tmp_path):
        """Test error when OCR is required but disabled."""
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_bytes(b"%PDF-1.4\n" * 100)
        
        with patch('src.processors.pdf_processor.get_config') as mock_config, \
             patch('src.processors.pdf_processor.MenuParser') as mock_parser_class:
            
            mock_config_instance = MagicMock()
            mock_config_instance.get_pdf_settings.return_value = {
                "ocr_enabled": False,  # OCR disabled
                "tesseract_path": None,
                "ocr_language": "eng",
                "ocr_quality_threshold": 0.75,
            }
            mock_config.return_value = mock_config_instance
            
            # Text extraction yields low count (needs OCR)
            mock_parser = MagicMock()
            mock_parser.extract_by_page.return_value = {1: "  "}  # <50 chars
            mock_parser_class.return_value = mock_parser
            
            processor = PDFProcessor(str(pdf_file))
            
            with pytest.raises(RuntimeError, match="OCR is disabled but required"):
                processor.process()

