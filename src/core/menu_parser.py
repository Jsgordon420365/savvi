"""
PDF menu text extraction module.

This module provides functionality to extract text from restaurant menu PDFs,
handling both native text-based PDFs and preserving document structure.
"""

import logging
from pathlib import Path
from typing import Dict, Optional, Any
from PyPDF2 import PdfReader
from PyPDF2.errors import PdfReadError

from src.utils.logger import get_logger
from src.utils.validators import validate_pdf_file

logger = get_logger(__name__)


class MenuParser:
    """
    Extract text from restaurant menu PDFs.
    
    This class handles:
    - Text extraction from native PDFs
    - Multi-page document processing
    - Section structure preservation
    - Metadata extraction
    - Error handling for corrupted PDFs
    """
    
    def __init__(self, pdf_path: str):
        """
        Initialize MenuParser with a PDF file path.
        
        Args:
            pdf_path: Path to the PDF file to parse
            
        Raises:
            FileNotFoundError: If PDF file doesn't exist
            ValueError: If PDF file is invalid or cannot be read
        """
        self.pdf_path = Path(pdf_path)
        
        # Validate PDF file
        is_valid, error_msg = validate_pdf_file(str(self.pdf_path))
        if not is_valid:
            logger.error(f"Invalid PDF file: {error_msg}")
            raise ValueError(f"Invalid PDF file: {error_msg}")
        
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")
        
        self._reader: Optional[PdfReader] = None
        self._metadata: Optional[Dict[str, Any]] = None
        
        logger.info(f"Initialized MenuParser for: {self.pdf_path}")
    
    def _get_reader(self) -> PdfReader:
        """
        Get or create PdfReader instance.
        
        Returns:
            PdfReader instance for the PDF file
            
        Raises:
            PdfReadError: If PDF is corrupted or cannot be read
        """
        if self._reader is None:
            try:
                logger.debug(f"Opening PDF file: {self.pdf_path}")
                self._reader = PdfReader(str(self.pdf_path))
                logger.info(f"Successfully opened PDF with {len(self._reader.pages)} pages")
            except PdfReadError as e:
                logger.error(f"Failed to read PDF: {e}")
                raise ValueError(f"Corrupted or invalid PDF file: {e}") from e
            except Exception as e:
                logger.error(f"Unexpected error reading PDF: {e}", exc_info=True)
                raise ValueError(f"Error reading PDF file: {e}") from e
        
        return self._reader
    
    def extract_text(self) -> str:
        """
        Extract all text from the PDF.
        
        Handles multi-page PDFs and preserves section structure by marking
        page breaks. Returns full text with page breaks indicated.
        
        Returns:
            Full extracted text with page breaks marked as "\\n--- Page N ---\\n"
            
        Raises:
            ValueError: If PDF cannot be read or is corrupted
        """
        reader = self._get_reader()
        full_text = []
        
        logger.debug(f"Extracting text from {len(reader.pages)} pages")
        
        for page_num, page in enumerate(reader.pages, start=1):
            try:
                page_text = page.extract_text()
                
                if page_text.strip():
                    # Mark page breaks for structure preservation
                    if page_num > 1:
                        full_text.append(f"\n--- Page {page_num} ---\n")
                    full_text.append(page_text)
                    logger.debug(f"Extracted {len(page_text)} characters from page {page_num}")
                else:
                    logger.warning(f"Page {page_num} appears to be empty or image-based")
                    if page_num > 1:
                        full_text.append(f"\n--- Page {page_num} (no text) ---\n")
            except Exception as e:
                logger.error(f"Error extracting text from page {page_num}: {e}", exc_info=True)
                # Continue with other pages even if one fails
                full_text.append(f"\n--- Page {page_num} (extraction error) ---\n")
        
        result = "".join(full_text)
        logger.info(f"Extracted {len(result)} total characters from PDF")
        
        return result
    
    def extract_by_page(self) -> Dict[int, str]:
        """
        Extract text from each page separately.
        
        Returns a dictionary mapping page numbers to their text content.
        Useful for layout analysis and page-by-page processing.
        
        Returns:
            Dictionary mapping page_number (int) -> text (str)
            
        Raises:
            ValueError: If PDF cannot be read or is corrupted
        """
        reader = self._get_reader()
        page_texts = {}
        
        logger.debug(f"Extracting text by page from {len(reader.pages)} pages")
        
        for page_num, page in enumerate(reader.pages, start=1):
            try:
                page_text = page.extract_text()
                page_texts[page_num] = page_text
                logger.debug(f"Page {page_num}: {len(page_text)} characters")
            except Exception as e:
                logger.error(f"Error extracting text from page {page_num}: {e}", exc_info=True)
                page_texts[page_num] = ""  # Empty string for failed pages
        
        logger.info(f"Extracted text from {len(page_texts)} pages")
        return page_texts
    
    def extract_metadata(self) -> Dict[str, Any]:
        """
        Extract PDF metadata and document information.
        
        Returns:
            Dictionary containing:
            - title: PDF title (if available)
            - author: PDF author (if available)
            - creator: PDF creator application
            - producer: PDF producer application
            - creation_date: PDF creation date
            - modification_date: PDF modification date
            - page_count: Number of pages
            - file_size: File size in bytes
            
        Raises:
            ValueError: If PDF cannot be read or is corrupted
        """
        if self._metadata is not None:
            return self._metadata
        
        reader = self._get_reader()
        metadata = reader.metadata
        
        result = {
            "title": metadata.get("/Title", "").strip() if metadata and "/Title" in metadata else "",
            "author": metadata.get("/Author", "").strip() if metadata and "/Author" in metadata else "",
            "creator": metadata.get("/Creator", "").strip() if metadata and "/Creator" in metadata else "",
            "producer": metadata.get("/Producer", "").strip() if metadata and "/Producer" in metadata else "",
            "creation_date": str(metadata.get("/CreationDate", "")) if metadata and "/CreationDate" in metadata else "",
            "modification_date": str(metadata.get("/ModDate", "")) if metadata and "/ModDate" in metadata else "",
            "page_count": len(reader.pages),
            "file_size": self.pdf_path.stat().st_size,
        }
        
        self._metadata = result
        logger.info(f"Extracted metadata: {result['page_count']} pages, {result['file_size']} bytes")
        
        return result
    
    def get_page_count(self) -> int:
        """
        Get the number of pages in the PDF.
        
        Returns:
            Number of pages
            
        Raises:
            ValueError: If PDF cannot be read or is corrupted
        """
        reader = self._get_reader()
        return len(reader.pages)
    
    def is_text_based(self) -> bool:
        """
        Determine if the PDF is text-based (vs. image-based/scanned).
        
        Checks if the PDF contains extractable text by examining the first page.
        If the first page has substantial text (>50 characters), considers it text-based.
        
        Returns:
            True if PDF appears to be text-based, False if likely scanned/image-based
        """
        try:
            reader = self._get_reader()
            if len(reader.pages) == 0:
                return False
            
            first_page_text = reader.pages[0].extract_text()
            text_length = len(first_page_text.strip())
            
            is_text = text_length > 50
            logger.debug(f"PDF text-based check: {text_length} chars on first page -> {is_text}")
            return is_text
        except Exception as e:
            logger.warning(f"Error checking if PDF is text-based: {e}")
            return False

