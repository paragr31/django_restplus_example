
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'DEBUG',
            'formatter': 'verbose',
            'maxBytes': 1024 * 500,
            'backupCount': 5,
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'C:/Apache24/logs/paragr/django_logs.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console','file'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'django.request': {
            'handlers': ['console','file'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django_auth_ldap':{
            'handlers': ['console','file'],
            'level': 'INFO',
            'propagate': True,
        },
        'paragr.access': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'propagate': True,
        }
    }
}