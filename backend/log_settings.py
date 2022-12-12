LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'default_formatter': {
            'format': '[%(levelname)s:%(asctime)s] %(message)s'
        },
    },

    'handlers': {
        'stream_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'default_formatter',
            'level': 'INFO'
        },
        'logfile': {  # The handler name
            'formatter': 'default_formatter',  # Refer to the formatter defined above
            'class': 'logging.handlers.RotatingFileHandler',  # OUTPUT: Which class to use
            'filename': 'log.txt',  # Param for class above. Defines filename to use, load it from constant
            'backupCount': 2,  # Param for class above. Defines how many log files to keep as it grows
            'level': 'DEBUG'
        },
    },
    'loggers': {
        'root': {
            'handlers': ['stream_handler', 'logfile'],
        },
        'routers': {
            'level': 'DEBUG',
        },
        'parsers': {
            'level': 'DEBUG',
        },
        'utils': {
            'level': 'DEBUG',
        },
        'services': {
            'level': 'DEBUG',
        },
        'rocketry.task': {
            'level': 'ERROR',
        }
    }
}