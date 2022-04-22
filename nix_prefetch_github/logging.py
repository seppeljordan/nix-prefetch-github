from __future__ import annotations

from dataclasses import dataclass
from logging import WARNING, Logger, StreamHandler, getLogger
from typing import Optional, Protocol, TextIO


@dataclass
class LoggingConfiguration:
    output_file: TextIO
    log_level: int = WARNING


class LoggerManager(Protocol):
    def set_logging_configuration(self, configuration: LoggingConfiguration) -> None:
        ...


class LoggerFactoryImpl:
    def __init__(self) -> None:
        self.default_configuration: Optional[LoggingConfiguration] = None

    def get_logger(self) -> Logger:
        configuration = self.default_configuration
        logger = getLogger("")
        if configuration:
            logger.addHandler(StreamHandler(configuration.output_file))
            logger.setLevel(configuration.log_level)
        return logger

    def set_logging_configuration(self, configuration: LoggingConfiguration) -> None:
        self.default_configuration = configuration
