from typing import Any
from loguru import logger as loguru_logger
import sys


class ApplicationLogger:
    _instance: "ApplicationLogger" = None  # type: ignore
    _initialized: bool = False

    def __new__(
        cls: type["ApplicationLogger"], *args: Any, **kwargs: Any
    ) -> "ApplicationLogger":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if ApplicationLogger._initialized:
            return

        # remove default handler to sys.stderr
        loguru_logger.remove()

        loguru_logger.add(
            sys.stdout,
            level="DEBUG",
            colorize=True,
            backtrace=True,
            diagnose=False,
            format=(
                "<green>{time:YYYY-MM-DD HH::mm:ss}</green> | "
                "<level>{level: <8}</level> | "
                "<cyan>{module}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
                "<level>{message}</level>"
            ),
        )

        self.logger = loguru_logger
        self.logger.info(f"Logger initialized (ApplicationLogger id={id(self)})")
        ApplicationLogger._initialized = True

    def trace(self, msg: str) -> None:
        self.logger.opt(depth=1).trace(msg)

    def debug(self, msg: str) -> None:
        self.logger.opt(depth=1).debug(msg)

    def info(self, msg: str) -> None:
        self.logger.opt(depth=1).info(msg)

    def success(self, msg: str) -> None:
        self.logger.opt(depth=1).success(msg)

    def warning(self, msg: str) -> None:
        self.logger.opt(depth=1).warning(msg)

    def error(self, msg: str) -> None:
        self.logger.opt(depth=1).error(msg)

    def critical(self, msg: str) -> None:
        self.logger.opt(depth=1).critical(msg)


def get_application_logger() -> ApplicationLogger:
    """
    Returns an instance of the ApplicationLogger class.

    This method provides a way to obtain a logger that can be used
    for logging messages within the application. The returned logger
    is an instance of the `ApplicationLogger` class, which is responsible
    for handling and formatting log messages according to the application's
    requirements.

    Returns:
        ApplicationLogger: An instance of the ApplicationLogger class,
                         ready to be used for logging.
    """
    return ApplicationLogger()
