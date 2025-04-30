import logging
import os


def setup_logger(name: str, log_file: str) -> logging.Logger:
    """
    Sets up a logger that outputs to both console and a log file.

    Parameters:
    - name (str): Name of the logger.
    - log_file (str): File path (relative to /logs/) where logs will be saved.

    Returns:
    - logging.Logger: Configured logger instance.
    """
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        # File handler
        file_handler = logging.FileHandler(f"logs/{log_file}", mode="w")
        file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        # Console handler
        console_handler = logging.StreamHandler()
        console_formatter = logging.Formatter("%(levelname)s - %(message)s")
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    return logger
