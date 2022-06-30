from __future__ import annotations

from dataclasses import dataclass
from logging import WARNING, Formatter, Logger, StreamHandler, getLogger
from typing import Protocol, TextIO


@dataclass
class LoggingConfiguration:
    output_file: TextIO
    log_level: int = WARNING


class LoggerManager(Protocol):
    def set_logging_configuration(self, configuration: LoggingConfiguration) -> None:
        ...


class LoggerFactoryImpl:
    def __init__(self) -> None:
        self._logger = getLogger("")

    def get_logger(self) -> Logger:
        return self._logger

    def set_logging_configuration(self, configuration: LoggingConfiguration) -> None:
        self._apply_configuration_to_logger(self._logger, configuration)

    def _apply_configuration_to_logger(
        self, logger: Logger, configuration: LoggingConfiguration
    ) -> None:
        for handler in logger.handlers:
            logger.removeHandler(handler)
        handler = StreamHandler(configuration.output_file)
        handler.setFormatter(Formatter("%(levelname)s: %(message)s"))
        logger.addHandler(handler)
        logger.setLevel(configuration.log_level)
