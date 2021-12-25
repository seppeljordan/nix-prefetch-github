from __future__ import annotations

from dataclasses import dataclass
from logging import WARNING, Logger, StreamHandler, getLogger
from typing import TextIO


def get_logger(configuration: LoggingConfiguration) -> Logger:
    logger = getLogger("")
    logger.addHandler(StreamHandler(configuration.output_file))
    logger.setLevel(configuration.log_level)
    return logger


@dataclass
class LoggingConfiguration:
    output_file: TextIO
    log_level: int = WARNING
