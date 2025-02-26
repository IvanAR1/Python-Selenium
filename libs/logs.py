import sys
import logging
from datetime import date
from .path.loader import env
from logging.config import dictConfig
from .path.utils.route import JoinPath
from .cmd.CheckCmd import get_type_of_param
from config.framework import FORMAT_LOG_DATE
from .path.utils.folder import CurrentWorkingDirectory, ExistFolder, CreateFolder

def get_log_folder(log_name:str) -> str:
    """Get Filename

    Args:
        log_name (str): Name file of log.

    Returns:
        str: Final file path.
    """
    folder = "%s/log" %( get_type_of_param(["--run-project", "-rp"]) )
    if not ExistFolder(folder):
        folder = "log"
    today_ = date.today().strftime( env("DATE_LOG_FORMAT", FORMAT_LOG_DATE) )
    folder = JoinPath(CurrentWorkingDirectory(), folder, today_)
    if not ExistFolder(folder):
        CreateFolder(folder)
    return "%s/%s.log" %(folder, log_name)

logging_config = dict(
    version = 1,
    formatters={
        'verbose': {
            'format': ("[%(asctime)s] %(levelname)s "
                       "[%(name)s:%(lineno)s] %(message)s"),
            'datefmt': "%d/%b/%Y %H:%M:%S",
        },
        'simple': {
            'format': '%(levelname)s %(message)s',
        },
    },
    handlers={
        'api-logger': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'level': logging.DEBUG,
            'filename': get_log_folder('api'),
            'maxBytes': 52428800,
            'backupCount': 7
        },
        'batch-process-logger': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'level': logging.DEBUG,
            'filename': get_log_folder('batch_process'),
            'maxBytes': 52428800,
            'backupCount': 7
        },
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'simple',
            'stream': sys.stdout,
        },
    },
    loggers={
        'api_logger': {
            'handlers': ['api-logger', 'console'],
            'level': logging.DEBUG
        },
        'batch_process_logger': {
            'handlers': ['batch-process-logger', 'console'],
            'level': logging.DEBUG
        }
    }
)

dictConfig(logging_config)
api_logger:logging.Logger = logging.getLogger('api_logger')
batch_process_logger:logging.Logger = logging.getLogger('batch_process_logger')
api_logger.__doc__ = batch_process_logger.__doc__ = logging.Logger.__doc__