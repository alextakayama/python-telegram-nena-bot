from logger import Logger

class Debuggable:
    def __init__(self, debug: bool = False):
        self.debug = debug
        self.logger = Logger.get_instance('DEFAULT')

    def get_debug(self) -> bool:
        return self.debug

    def log_debug(self, message) -> None:
        self.logger.debug(message) if self.debug else None

    def log_error(self, message) -> None:
        self.logger.error(message) if self.debug else None

    def log_warning(self, message) -> None:
        self.logger.warning(message) if self.debug else None

    def set_debug(self, debug: bool) -> bool:
        self.debug = debug
        return self.debug
