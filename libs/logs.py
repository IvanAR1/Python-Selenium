import os
import sys
import logging
from datetime import date
from .path.config_loader import env
from logging.config import dictConfig
from .path.path_utils import JoinFile
from .cmd.CheckCmd import get_type_of_param

def get_log_folder(type:str):
    route:str = "log"
    if os.path.exists("%s/log" %(get_type_of_param("--project"))):
        route = "%s/log" %(get_type_of_param("--project"))
    today = date.today()
    format_date:str = env("DATE_LOG_FORMAT") or "%Y/%m"
    route += '/%s' %(today.strftime( format_date ))
    file = JoinFile(os.getcwd(), route)
    if not os.path.exists(file):
        os.makedirs(file, exist_ok=True)
    return "%s/%s" %(route, type)

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
            'filename': get_log_folder('api.log'),
            'maxBytes': 52428800,
            'backupCount': 7
        },
        'batch-process-logger': {
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'level': logging.DEBUG,
            'filename': get_log_folder('batch_process.log'),
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
api_logger = logging.getLogger('api_logger')
batch_process_logger = logging.getLogger('batch_process_logger')