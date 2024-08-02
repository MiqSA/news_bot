from dataclasses import dataclass
from functools import wraps
import logging
import os
from string import Template
import sys
from typing import Callable, Any


FORMAT = '%(asctime)s %(levelname)s %(name)s %(message)s'


@dataclass
class Log:
    path: str = 'logs/'
    file: str = 'news_bot.log'
    level: int = logging.INFO

    def create_path(self) -> None:
        if not os.path.exists(self.path):
            os.mkdir(f'{self.path}')

    def format_log(self) -> None:
        logging.basicConfig(
            filename=f'{self.path}{self.file}',
            level=self.level,
            format=FORMAT,
        )

    def main(self, name: str) -> logging.Logger:
        try:
            self.create_path()
            self.format_log()
            return logging.getLogger(name)
        except Exception:
            raise

def set_log_execption_message(
    exc: Exception,
    func: Callable[[Any], Any],
    loggerf: Callable[[str], logging.Logger] = Log().main
    ) -> None:
    logger = loggerf(sys.modules[func.__module__].__name__)
    msg = Template(
        'Error in $func_name'
        ).substitute(func_name=func.__name__)
    logger.exception(msg, exc_info=exc)


def log_expections(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try: 
            return await func(*args, **kwargs)
        except Exception as err:
            set_log_execption_message(exc=err, func=func)
    return wrapper
