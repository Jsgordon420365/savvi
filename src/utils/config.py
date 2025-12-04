"""
Configuration management for SAVVI application.

This module handles loading and validation of environment variables and YAML configuration files.
"""

import os
from pathlib import Path
from typing import Dict, List, Optional, Any
import yaml
from dotenv import load_dotenv
from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings


class ApplicationConfig(BaseModel):
    """Application metadata configuration."""
    name: str = "SAVVI"
    version: str = "0.1.0"
    environment: str = "development"


class OCRConfig(BaseModel):
    """OCR processing configuration."""
    enabled: bool = True
    language: str = "eng"
    quality_threshold: float = 0.75


class PDFProcessingConfig(BaseModel):
    """PDF processing configuration."""
    max_file_size_mb: int = 50
    supported_formats: List[str] = Field(default_factory=lambda: ["pdf", "image"])
    ocr: OCRConfig = Field(default_factory=OCRConfig)


class RecipeSearchConfig(BaseModel):
    """Recipe search configuration."""
    confidence_threshold: float = 0.90
    max_results: int = 5
    timeout_seconds: int = 10


class OutputConfig(BaseModel):
    """Output formatting configuration."""
    format: str = "pdf_marked"
    include_confidence_scores: bool = True
    include_recipe_notes: bool = True
    editable_fields: bool = True


class YAMLConfig(BaseModel):
    """YAML configuration structure."""
    application: ApplicationConfig = Field(default_factory=ApplicationConfig)
    pdf_processing: PDFProcessingConfig = Field(default_factory=PDFProcessingConfig)
    allergen_categories: Dict[str, List[str]] = Field(default_factory=dict)
    dietary_preferences: Dict[str, Dict[str, Any]] = Field(default_factory=dict)
    recipe_search: RecipeSearchConfig = Field(default_factory=RecipeSearchConfig)
    output: OutputConfig = Field(default_factory=OutputConfig)


class EnvironmentSettings(BaseSettings):
    """Environment variable settings."""
    # Application
    app_env: str = Field(default="development", alias="APP_ENV")
    debug: bool = Field(default=True, alias="DEBUG")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    
    # Database
    db_type: str = Field(default="postgresql", alias="DB_TYPE")
    db_host: str = Field(default="localhost", alias="DB_HOST")
    db_port: int = Field(default=5432, alias="DB_PORT")
    db_name: str = Field(default="savvi_db", alias="DB_NAME")
    db_user: str = Field(default="savvi_user", alias="DB_USER")
    db_password: str = Field(default="your_secure_password", alias="DB_PASSWORD")
    
    # PDF Processing
    pdf_max_size_mb: int = Field(default=50, alias="PDF_MAX_SIZE_MB")
    ocr_enabled: bool = Field(default=True, alias="OCR_ENABLED")
    tesseract_path: Optional[str] = Field(default=None, alias="TESSERACT_PATH")
    
    # API Configuration
    api_port: int = Field(default=8000, alias="API_PORT")
    api_host: str = Field(default="0.0.0.0", alias="API_HOST")
    cors_origins: str = Field(default="http://localhost:3000,http://localhost:8000", alias="CORS_ORIGINS")
    
    # Recipe Search
    recipe_api_key: Optional[str] = Field(default=None, alias="RECIPE_API_KEY")
    ingredient_confidence_threshold: float = Field(default=0.90, alias="INGREDIENT_CONFIDENCE_THRESHOLD")
    
    # File Storage
    upload_dir: str = Field(default="data/uploaded_menus", alias="UPLOAD_DIR")
    output_dir: str = Field(default="data/processed_menus", alias="OUTPUT_DIR")
    log_dir: str = Field(default="logs", alias="LOG_DIR")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


class Config:
    """
    Main configuration class for SAVVI application.
    
    Loads configuration from both environment variables (.env) and YAML file (savvi_config.yaml).
    Provides accessors for all configuration settings.
    """
    
    def __init__(self, config_path: Optional[Path] = None, env_file: Optional[Path] = None):
        """
        Initialize configuration.
        
        Args:
            config_path: Path to savvi_config.yaml file. Defaults to config/savvi_config.yaml
            env_file: Path to .env file. Defaults to .env in project root
        """
        # Determine project root (parent of src/)
        if config_path is None:
            project_root = Path(__file__).parent.parent.parent
            config_path = project_root / "config" / "savvi_config.yaml"
        
        if env_file is None:
            project_root = Path(__file__).parent.parent.parent
            env_file = project_root / ".env"
        
        # Load environment variables
        if env_file.exists():
            load_dotenv(env_file)
        else:
            # Try loading from .env.template if .env doesn't exist
            template_file = env_file.parent / ".env.template"
            if template_file.exists():
                load_dotenv(template_file)
        
        # Load environment settings
        self.env_settings = EnvironmentSettings()
        
        # Load YAML configuration
        self._yaml_config = self._load_yaml_config(config_path)
        
        # Validate settings
        if not self.validate_settings():
            raise ValueError("Configuration validation failed. Check required settings.")
    
    def _load_yaml_config(self, config_path: Path) -> YAMLConfig:
        """
        Load YAML configuration file.
        
        Args:
            config_path: Path to YAML configuration file
            
        Returns:
            YAMLConfig object with loaded configuration
            
        Raises:
            FileNotFoundError: If config file doesn't exist
            yaml.YAMLError: If YAML file is invalid
        """
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = yaml.safe_load(f)
        
        if config_data is None:
            config_data = {}
        
        return YAMLConfig(**config_data)
    
    def validate_settings(self) -> bool:
        """
        Validate that all required settings are present and valid.
        
        Returns:
            True if validation passes, False otherwise
        """
        try:
            # Check required environment variables for production
            if self.env_settings.app_env == "production":
                if not self.env_settings.recipe_api_key or self.env_settings.recipe_api_key == "your_recipe_api_key":
                    print("WARNING: RECIPE_API_KEY not set for production environment")
                    return False
                if self.env_settings.db_password == "your_secure_password":
                    print("WARNING: DB_PASSWORD not changed from default")
                    return False
            
            # Validate PDF processing settings
            if self.env_settings.pdf_max_size_mb <= 0:
                print("ERROR: PDF_MAX_SIZE_MB must be greater than 0")
                return False
            
            # Validate API settings
            if not (1 <= self.env_settings.api_port <= 65535):
                print("ERROR: API_PORT must be between 1 and 65535")
                return False
            
            # Validate confidence threshold
            if not (0.0 <= self._yaml_config.recipe_search.confidence_threshold <= 1.0):
                print("ERROR: confidence_threshold must be between 0.0 and 1.0")
                return False
            
            return True
        except Exception as e:
            print(f"ERROR: Configuration validation failed: {e}")
            return False
    
    def get_allergen_rules(self) -> Dict[str, List[str]]:
        """
        Get allergen categories and their associated allergens.
        
        Returns:
            Dictionary mapping severity levels (critical, moderate, mild) to lists of allergens
        """
        return self._yaml_config.allergen_categories
    
    def get_dietary_preferences(self) -> Dict[str, Dict[str, Any]]:
        """
        Get dietary preference configurations.
        
        Returns:
            Dictionary mapping preference names (vegan, vegetarian, etc.) to their configurations
        """
        return self._yaml_config.dietary_preferences
    
    def get_pdf_settings(self) -> Dict[str, Any]:
        """
        Get PDF processing settings.
        
        Returns:
            Dictionary containing PDF processing configuration
        """
        return {
            "max_file_size_mb": self.env_settings.pdf_max_size_mb,
            "supported_formats": self._yaml_config.pdf_processing.supported_formats,
            "ocr_enabled": self.env_settings.ocr_enabled,
            "tesseract_path": self.env_settings.tesseract_path,
            "ocr_language": self._yaml_config.pdf_processing.ocr.language,
            "ocr_quality_threshold": self._yaml_config.pdf_processing.ocr.quality_threshold,
        }
    
    def get_recipe_search_settings(self) -> Dict[str, Any]:
        """
        Get recipe search configuration.
        
        Returns:
            Dictionary containing recipe search settings
        """
        return {
            "api_key": self.env_settings.recipe_api_key,
            "confidence_threshold": self._yaml_config.recipe_search.confidence_threshold,
            "max_results": self._yaml_config.recipe_search.max_results,
            "timeout_seconds": self._yaml_config.recipe_search.timeout_seconds,
        }
    
    def get_output_settings(self) -> Dict[str, Any]:
        """
        Get output formatting settings.
        
        Returns:
            Dictionary containing output configuration
        """
        return {
            "format": self._yaml_config.output.format,
            "include_confidence_scores": self._yaml_config.output.include_confidence_scores,
            "include_recipe_notes": self._yaml_config.output.include_recipe_notes,
            "editable_fields": self._yaml_config.output.editable_fields,
        }
    
    def get_database_settings(self) -> Dict[str, Any]:
        """
        Get database connection settings.
        
        Returns:
            Dictionary containing database configuration
        """
        return {
            "type": self.env_settings.db_type,
            "host": self.env_settings.db_host,
            "port": self.env_settings.db_port,
            "name": self.env_settings.db_name,
            "user": self.env_settings.db_user,
            "password": self.env_settings.db_password,
        }
    
    def get_api_settings(self) -> Dict[str, Any]:
        """
        Get API server settings.
        
        Returns:
            Dictionary containing API configuration
        """
        return {
            "port": self.env_settings.api_port,
            "host": self.env_settings.api_host,
            "cors_origins": self.env_settings.cors_origins.split(","),
        }
    
    def get_logging_settings(self) -> Dict[str, Any]:
        """
        Get logging configuration.
        
        Returns:
            Dictionary containing logging settings
        """
        return {
            "level": self.env_settings.log_level,
            "debug": self.env_settings.debug,
            "log_dir": self.env_settings.log_dir,
        }


# Global config instance (lazy initialization)
_config_instance: Optional[Config] = None


def get_config() -> Config:
    """
    Get the global configuration instance.
    
    Returns:
        Config instance (singleton pattern)
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = Config()
    return _config_instance

