import logging

class AppLogger:
    """Custom logger for logging messages into a log file (Singleton)."""

    _instance = None  # Singleton instance

    def __new__(cls, log_file_path: str = None):
        if cls._instance is None:
            cls._instance = super(AppLogger, cls).__new__(cls)
            cls._instance._initialize_logger(log_file_path)
        return cls._instance

    def _initialize_logger(self, log_file_path: str = None):
        self.logger = logging.getLogger("AppLogger")
        self.logger.setLevel(logging.INFO)

        if log_file_path:
            if not any(isinstance(h, logging.FileHandler) for h in self.logger.handlers):
                file_handler = logging.FileHandler(log_file_path)
                formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
                file_handler.setFormatter(formatter)
                self.logger.addHandler(file_handler)
        
        if not log_file_path:
            if not any(isinstance(h, logging.StreamHandler) for h in self.logger.handlers):
                stream_handler = logging.StreamHandler()
                formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
                stream_handler.setFormatter(formatter)
                self.logger.addHandler(stream_handler)

    def log_info(self, message: str, custom_dimensions: dict = None):
        """Logs an info message with optional custom dimensions."""
        self.logger.info(message, extra={"custom_dimensions": custom_dimensions or {}})

    def log_warning(self, message: str, custom_dimensions: dict = None):
        """Logs a warning message with optional custom dimensions."""
        self.logger.warning(message, extra={"custom_dimensions": custom_dimensions or {}})

    def log_error(self, message: str, exception: Exception = None, custom_dimensions: dict = None):
        """Logs an error message with optional exception details and custom dimensions."""
        self.logger.error(message, exc_info=exception, extra={"custom_dimensions": custom_dimensions or {}})
