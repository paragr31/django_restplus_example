LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '(%(asctime)s)-[%(levelname)-8s]:[ThreadName: %(threadName)s, ThreadId: %(thread)d][Process Name: %(processName)s, ProcessId: %(process)d]-[FileName: %(pathname)s, FunctionName: %(funcName)s, LineNumber: %(lineno)d]-[Message:%(message)s]',
            'datefmt' : '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '(%(asctime)s)-[%(levelname)-8s] : %(message)s',
            'datefmt' : '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'level': 'DEBUG',
            'formatter': 'verbose',
            'maxBytes': 1024 * 500,
            'backupCount': 5,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'mylogging.log',
        },
    },
    'loggers': {
        'paragr': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        }
    }
}
