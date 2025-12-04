"""
PDF processing module for handling both text-based and scanned PDFs.

This module provides OCR capabilities for scanned menu PDFs and integrates
with the MenuParser for text-based PDFs.
"""

import logging
from pathlib import Path
from typing import List, Optional, Dict, Any
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
from pdf2image.exceptions import PDFInfoNotInstalledError, PDFPageCountError

from src.core.menu_parser import MenuParser
from src.utils.logger import get_logger
from src.utils.config import get_config

logger = get_logger(__name__)


class PDFProcessor:
    """
    Process PDF menus with support for both text-based and scanned PDFs.
    
    This class handles:
    - Detection of scanned vs text-based PDFs
    - PDF to image conversion
    - OCR processing with Tesseract
    - Image preprocessing for better OCR accuracy
    - Intelligent fallback between text extraction and OCR
    """
    
    def __init__(self, pdf_path: str, config: Optional[Any] = None):
        """
        Initialize PDFProcessor with a PDF file path.
        
        Args:
            pdf_path: Path to the PDF file to process
            config: Optional Config instance (uses get_config() if not provided)
            
        Raises:
            FileNotFoundError: If PDF file doesn't exist
            ValueError: If PDF file is invalid
        """
        self.pdf_path = Path(pdf_path)
        self.config = config or get_config()
        
        # Get PDF and OCR settings from config
        pdf_settings = self.config.get_pdf_settings()
        self.ocr_enabled = pdf_settings.get("ocr_enabled", True)
        self.tesseract_path = pdf_settings.get("tesseract_path")
        self.ocr_language = pdf_settings.get("ocr_language", "eng")
        self.ocr_quality_threshold = pdf_settings.get("ocr_quality_threshold", 0.75)
        
        # Set Tesseract path if configured
        if self.tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = self.tesseract_path
        
        # Initialize MenuParser for text extraction
        self._menu_parser: Optional[MenuParser] = None
        
        # Cache for processed images
        self._cached_images: Optional[List[Image.Image]] = None
        
        logger.info(f"Initialized PDFProcessor for: {self.pdf_path}")
    
    def _get_menu_parser(self) -> MenuParser:
        """Get or create MenuParser instance."""
        if self._menu_parser is None:
            self._menu_parser = MenuParser(str(self.pdf_path))
        return self._menu_parser
    
    def is_scanned_menu(self) -> bool:
        """
        Detect if PDF is image-based (scanned) vs text-based.
        
        Compares text extraction results with expected page size.
        If text extraction yields <50 characters per page on average,
        considers it a scanned PDF.
        
        Returns:
            True if PDF appears to be scanned/image-based, False if text-based
        """
        try:
            parser = self._get_menu_parser()
            
            # Check if it's text-based using MenuParser's method
            if parser.is_text_based():
                return False
            
            # Additional check: extract text and check character count
            page_texts = parser.extract_by_page()
            if not page_texts:
                return True  # No text found, likely scanned
            
            # Calculate average characters per page
            total_chars = sum(len(text.strip()) for text in page_texts.values())
            avg_chars_per_page = total_chars / len(page_texts) if page_texts else 0
            
            is_scanned = avg_chars_per_page < 50
            logger.debug(
                f"PDF scan detection: {avg_chars_per_page:.1f} chars/page -> "
                f"{'scanned' if is_scanned else 'text-based'}"
            )
            return is_scanned
            
        except Exception as e:
            logger.warning(f"Error detecting if PDF is scanned: {e}")
            # Default to assuming it's scanned if we can't determine
            return True
    
    def convert_to_images(self, dpi: int = 150) -> List[Image.Image]:
        """
        Convert PDF pages to images.
        
        Uses pdf2image to convert each page of the PDF to a PIL Image.
        Caches results to avoid re-conversion.
        
        Args:
            dpi: Resolution for image conversion (default: 150)
            
        Returns:
            List of PIL Image objects, one per page
            
        Raises:
            ValueError: If PDF cannot be converted
            PDFInfoNotInstalledError: If poppler is not installed
        """
        if self._cached_images is not None:
            logger.debug(f"Using cached images ({len(self._cached_images)} pages)")
            return self._cached_images
        
        try:
            logger.info(f"Converting PDF to images at {dpi} DPI")
            images = convert_from_path(
                str(self.pdf_path),
                dpi=dpi,
                fmt='png'
            )
            
            self._cached_images = images
            logger.info(f"Converted {len(images)} pages to images")
            return images
            
        except PDFInfoNotInstalledError:
            error_msg = (
                "poppler-utils not installed. Install it with:\n"
                "  Windows: choco install poppler\n"
                "  Mac: brew install poppler\n"
                "  Linux: apt-get install poppler-utils"
            )
            logger.error(error_msg)
            raise ValueError(error_msg) from None
        except PDFPageCountError as e:
            logger.error(f"Error reading PDF page count: {e}")
            raise ValueError(f"Cannot read PDF: {e}") from e
        except Exception as e:
            logger.error(f"Error converting PDF to images: {e}", exc_info=True)
            raise ValueError(f"Error converting PDF to images: {e}") from e
    
    def _preprocess_image(self, image: Image.Image) -> Image.Image:
        """
        Preprocess image for better OCR accuracy.
        
        Applies:
        - Grayscale conversion
        - Contrast enhancement
        - Noise reduction (basic)
        
        Args:
            image: PIL Image to preprocess
            
        Returns:
            Preprocessed PIL Image
        """
        # Convert to grayscale if not already
        if image.mode != 'L':
            image = image.convert('L')
        
        # Enhance contrast using point transform
        from PIL import ImageEnhance
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.5)  # Increase contrast by 50%
        
        # Enhance sharpness
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(1.2)  # Increase sharpness by 20%
        
        return image
    
    def ocr_image(self, image: Image.Image, timeout: int = 30) -> str:
        """
        Apply Tesseract OCR to a single image.
        
        Includes image preprocessing for better accuracy.
        
        Args:
            image: PIL Image to process
            timeout: Maximum seconds to wait for OCR (default: 30)
            
        Returns:
            Extracted text string
            
        Raises:
            RuntimeError: If Tesseract is not available or OCR fails
        """
        if not self.ocr_enabled:
            raise RuntimeError("OCR is disabled in configuration")
        
        try:
            # Preprocess image
            processed_image = self._preprocess_image(image)
            
            logger.debug(f"Running OCR on image ({image.size[0]}x{image.size[1]})")
            
            # Run OCR with configured language
            text = pytesseract.image_to_string(
                processed_image,
                lang=self.ocr_language,
                timeout=timeout
            )
            
            logger.debug(f"OCR extracted {len(text)} characters")
            return text
            
        except pytesseract.TesseractNotFoundError:
            error_msg = (
                "Tesseract OCR not found. Install it with:\n"
                "  Windows: choco install tesseract\n"
                "  Mac: brew install tesseract\n"
                "  Linux: apt-get install tesseract-ocr\n"
                f"Or set TESSERACT_PATH in .env to: {self.tesseract_path}"
            )
            logger.error(error_msg)
            raise RuntimeError(error_msg) from None
        except Exception as e:
            logger.error(f"OCR error: {e}", exc_info=True)
            raise RuntimeError(f"OCR processing failed: {e}") from e
    
    def process(self) -> str:
        """
        Intelligently process PDF (text-based or scanned).
        
        Tries text extraction first. If that yields <50 characters per page,
        falls back to OCR processing.
        
        Returns:
            Full extracted text from PDF
            
        Raises:
            ValueError: If PDF cannot be processed
            RuntimeError: If OCR is required but not available
        """
        try:
            parser = self._get_menu_parser()
            
            # Try text extraction first
            logger.info("Attempting text extraction from PDF")
            page_texts = parser.extract_by_page()
            
            if not page_texts:
                logger.warning("No text extracted, treating as scanned PDF")
                return self._process_with_ocr()
            
            # Check if we have enough text
            total_chars = sum(len(text.strip()) for text in page_texts.values())
            avg_chars_per_page = total_chars / len(page_texts)
            
            if avg_chars_per_page >= 50:
                # Good text extraction, use it
                logger.info(
                    f"Text extraction successful: {avg_chars_per_page:.1f} chars/page"
                )
                full_text = []
                for page_num, text in sorted(page_texts.items()):
                    if page_num > 1:
                        full_text.append(f"\n--- Page {page_num} ---\n")
                    full_text.append(text)
                return "".join(full_text)
            else:
                # Low text count, likely scanned - use OCR
                logger.info(
                    f"Low text count ({avg_chars_per_page:.1f} chars/page), "
                    "using OCR"
                )
                return self._process_with_ocr()
                
        except Exception as e:
            logger.error(f"Error processing PDF: {e}", exc_info=True)
            # Try OCR as fallback
            logger.info("Attempting OCR as fallback")
            try:
                return self._process_with_ocr()
            except Exception as ocr_error:
                raise ValueError(
                    f"Failed to process PDF with both text extraction and OCR: "
                    f"{ocr_error}"
                ) from ocr_error
    
    def _process_with_ocr(self) -> str:
        """
        Process PDF using OCR.
        
        Returns:
            Full extracted text from OCR
            
        Raises:
            RuntimeError: If OCR is disabled but required
        """
        if not self.ocr_enabled:
            raise RuntimeError("OCR is disabled but required for this PDF")
        
        logger.info("Processing PDF with OCR")
        images = self.convert_to_images()
        
        full_text = []
        for page_num, image in enumerate(images, start=1):
            try:
                page_text = self.ocr_image(image)
                if page_num > 1:
                    full_text.append(f"\n--- Page {page_num} ---\n")
                full_text.append(page_text)
                logger.debug(f"OCR completed for page {page_num}")
            except Exception as e:
                logger.error(f"OCR failed for page {page_num}: {e}")
                full_text.append(f"\n--- Page {page_num} (OCR error) ---\n")
        
        result = "".join(full_text)
        logger.info(f"OCR processing complete: {len(result)} characters extracted")
        return result

