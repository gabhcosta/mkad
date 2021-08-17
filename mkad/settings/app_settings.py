"""
Contains methods to help the user configure the application
"""
import __main__
import logging
import os
from configparser import ConfigParser, NoOptionError, NoSectionError, ExtendedInterpolation
from logging.handlers import TimedRotatingFileHandler
from abc import ABC


class AppSettings(ABC):
    """
    Handles the reading/writing of global parameters of the application, such
    as database URLs, usernames and passwords.
    All the parameters are stored on the "app_settings.ini" file. On that file,
    each section contains parameters for a different environment, namely
    "development", "production" and "localhost".

    Please note that the `setup` method also configures the logging
    environment using a StreamHandler and a TimedRotatingFileHandler
    See: https://docs.python.org/3/library/logging.handlers.html

    ----
    Usage example:
    def main()
        AppSettings.setup(AppSettings.PRODUCTION)
        connect()

    def connect(self):
        try:
            db = mysql.connect(
                host = AppSettings.get_str('db_host'),
                user = AppSettings.get_str('db_user'),
                password = AppSettings.get_str('db_password'),
                port = AppSettings.get_int('db_port')
            )
        except:
            pass
    """
    environment = os.getenv('API_ENVIRONMENT') or 'development'

    _parser: ConfigParser = ConfigParser(interpolation=ExtendedInterpolation()) if environment == 'production' \
                            else ConfigParser()

    CONFIG_FILE_PATH = os.path.join(
        os.path.dirname(__main__.__file__),
        'app_settings.ini'
    )

    LOG_FILE_PATH = os.path.join(
        os.path.dirname(__main__.__file__), 'logs\\', '.log'
    )
    

    _initialized_parser = False
    _initialized_logger = False


    @classmethod
    def setup(cls, environment: str = None) -> None:
        """
        Initializes the settings file parser and configures the logging library
        """
        if environment:
            cls.environment = environment
            
        cls.setup_parser()
        cls.setup_logger()


    @classmethod
    def setup_parser(cls) -> None:
        """
        Initializes the settings file parser
        """
        if not os.path.exists(cls.CONFIG_FILE_PATH):
            file_name = cls.CONFIG_FILE_PATH
            msg = f'The configuration file "{file_name}" doesn\'t exist'
            raise FileNotFoundError(msg)

        cls._parser.read(cls.CONFIG_FILE_PATH)
        cls._initialized_parser = True

        cls._log('Settings file parser initialized')


    @classmethod
    def setup_logger(cls) -> None:
        app_logger = cls._build_logger()
        cls._setup_log_level(app_logger)

        formatter = cls._build_log_formatter()
        cls._setup_console_logging(app_logger, formatter)
        cls._setup_file_logging(app_logger, formatter)

        cls._initialized_logger = True
        cls._log('Logger initialized')


    @classmethod
    def _build_logger(cls) -> logging.Logger:
        logger = logging.getLogger()
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
            handler.close()

        return logger


    @classmethod
    def _setup_log_level(cls, logger: logging.Logger) -> None:
        log_level = cls.get_str('log_level', 'DEBUG').upper()
        logger.setLevel(log_level)


    @classmethod
    def _build_log_formatter(cls) -> logging.Logger:
        max_logging_length = cls.get_int('log_max_length', 200)
        format_str = '%(asctime)s: [%(levelname)s][%(module)s:%(lineno)d] ' + \
                     f'%(message).{max_logging_length}s'
        return logging.Formatter(format_str, '%Y-%m-%d %H:%M:%S')


    @classmethod
    def _setup_console_logging(cls, logger: logging.Logger,
                               formatter: logging.Formatter) -> None:
        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        logger.addHandler(sh)


    @classmethod
    def _setup_file_logging(cls, logger: logging.Logger,
                            formatter: logging.Formatter) -> None:
        file_path = cls.get_str('log_file', cls.LOG_FILE_PATH)
        fh = TimedRotatingFileHandler(file_path, 'midnight')
        fh.setFormatter(formatter)
        fh.suffix = '%Y-%m-%d'
        logger.addHandler(fh)


    @classmethod
    def _log(cls, msg: str, *args) -> None:
        if cls._initialized_logger:
            logging.debug(msg, *args)
        else:
            print(msg.replace('%s', '{}').format(*args))


    @classmethod
    def get_str(cls, param: str, default: str = None) -> str:
        cls._check_setup(default)
        try:
            if cls.environment == 'production':
                out = cls._parser.get(cls.environment, param, vars=os.environ)
            else:
                out = cls._parser.get(cls.environment, param)
        except (NoSectionError, NoOptionError):
            if default is not None:
                out = default
                msg = 'Unable to read [%s.%s] from file [%s]. Using default.'
                cls._log(msg, cls.environment, param, cls.CONFIG_FILE_PATH)
            else:
                raise

        cls._log('%s.%s="%s"', cls.environment, param, out)
        return out


    @classmethod
    def get_int(cls, param: str, default: int = None) -> int:
        cls._check_setup(default)
        try:
            if cls.environment == 'production':
                out = cls._parser.getint(cls.environment, param, vars=os.environ)
            else:
                out = cls._parser.getint(cls.environment, param)
        except (NoSectionError, NoOptionError):
            if default is not None:
                out = default
                msg = 'Unable to read [%s.%s] from file [%s]. Using default.'
                cls._log(msg, cls.environment, param, cls.CONFIG_FILE_PATH)
            else:
                raise

        cls._log('%s.%s=%s', cls.environment, param, out)
        return out


    @classmethod
    def _check_setup(cls, default: any = None) -> None:
        if not cls._initialized_parser:
            if default is None:
                msg = 'AppSettings has not been initialized. Either call ' + \
                      'AppSettings.setup(), AppSettings.setup_parser() or ' + \
                      'use a default value argument'
                raise RuntimeError(msg)
            else:
                msg = 'Parser is not ready. Call setup() or setup_parser()'
                cls._log(msg)