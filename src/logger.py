import logging
from logging.handlers import TimedRotatingFileHandler

class Logger:
    _instance = None

    def __init__(self, name, log_file=None, level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        if log_file:
            file_handler = TimedRotatingFileHandler(log_file, when='midnight')
            file_handler.suffix = "%Y-%m-%d.log"
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    @classmethod
    def get_instance(cls, name, log_file=None, level=logging.DEBUG):
        if cls._instance is None:
            cls._instance = cls(name, log_file, level)
        return cls._instance

    def debug(self, message) -> None:
        self.logger.debug(message)

    def info(self, message) -> None:
        self.logger.info(message)

    def warning(self, message) -> None:
        self.logger.warning(message)

    def error(self, message) -> None:
        self.logger.error(message)

    def critical(self, message) -> None:
        self.logger.critical(message)
