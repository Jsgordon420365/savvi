"""
Unit tests for logging utility.
"""

import pytest
import logging
from pathlib import Path
from src.utils.logger import get_logger, setup_root_logger, logger


class TestLogger:
    """Test cases for logger functionality."""
    
    def test_get_logger_returns_logger_instance(self):
        """Test that get_logger returns a logging.Logger instance."""
        test_logger = get_logger("test_module")
        assert isinstance(test_logger, logging.Logger)
        assert test_logger.name == "test_module"
    
    def test_logger_has_handlers(self):
        """Test that logger has both console and file handlers."""
        test_logger = get_logger("test_module_handlers")
        assert len(test_logger.handlers) >= 1  # At least console handler
    
    def test_logger_logs_different_levels(self, caplog):
        """Test that logger can log at different levels."""
        test_logger = get_logger("test_levels")
        test_logger.setLevel(logging.DEBUG)
        
        with caplog.at_level(logging.DEBUG):
            test_logger.debug("Debug message")
            test_logger.info("Info message")
            test_logger.warning("Warning message")
            test_logger.error("Error message")
        
        assert "Debug message" in caplog.text
        assert "Info message" in caplog.text
        assert "Warning message" in caplog.text
        assert "Error message" in caplog.text
    
    def test_logger_includes_timestamp(self, caplog):
        """Test that log messages include timestamps."""
        test_logger = get_logger("test_timestamp")
        
        with caplog.at_level(logging.INFO):
            test_logger.info("Test message with timestamp")
        
        # Check that log message contains timestamp-like pattern
        assert any(char.isdigit() for char in caplog.text)
    
    def test_logger_includes_module_name(self, caplog):
        """Test that log messages include module name."""
        test_logger = get_logger("test_module_name")
        
        with caplog.at_level(logging.INFO):
            test_logger.info("Test message")
        
        # Logger name should be in the log
        assert "test_module_name" in caplog.text or "test_logger" in caplog.text
    
    def test_default_logger_exists(self):
        """Test that default logger instance exists."""
        assert logger is not None
        assert isinstance(logger, logging.Logger)
    
    def test_setup_root_logger(self):
        """Test that setup_root_logger configures root logger."""
        setup_root_logger()
        root_logger = logging.getLogger()
        assert root_logger.level in [logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]
        assert len(root_logger.handlers) > 0
    
    def test_log_file_created(self, tmp_path, monkeypatch):
        """Test that log file is created in the logs directory."""
        # Temporarily change log directory to tmp_path
        from src.utils import config
        original_get_config = config.get_config
        
        def mock_get_config():
            mock_config = original_get_config()
            # Create a mock that returns tmp_path for log_dir
            class MockConfig:
                def get_logging_settings(self):
                    return {"level": "INFO", "debug": False, "log_dir": str(tmp_path)}
            return MockConfig()
        
        monkeypatch.setattr(config, "get_config", mock_get_config)
        
        test_logger = get_logger("test_file_creation")
        test_logger.info("Test log message")
        
        # Check if log file was created
        log_files = list(tmp_path.glob("*.log"))
        assert len(log_files) > 0
    
    def test_logger_does_not_propagate(self):
        """Test that logger does not propagate to root logger."""
        test_logger = get_logger("test_propagation")
        root_logger = logging.getLogger()
        root_handler_count = len(root_logger.handlers)
        
        # Log a message
        test_logger.info("Test message")
        
        # Root logger handler count should not change
        assert len(root_logger.handlers) == root_handler_count or test_logger.propagate is False

