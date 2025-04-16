# app/core/logging.py
import logging
import sys
from typing import Dict, Any

from loguru import logger
from pydantic import BaseModel

from app.core.config import settings


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


class LoggingSettings(BaseModel):
    LEVEL: str = settings.LOG_LEVEL
    FORMAT: str = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )


def setup_logging() -> None:
    log_config = LoggingSettings()

    # Remove default handlers
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(log_config.LEVEL)

    # Remove every other logger's handlers and propagate to root logger
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    # Configure loguru
    logger.configure(
        handlers=[
            {
                "sink": sys.stdout,
                "level": log_config.LEVEL,
                "format": log_config.FORMAT,
            }
        ]
    )

    logger.info("Logging is configured.")
