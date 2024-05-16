from os import environ as env

class Telegram:
    API_ID = int(env.get("TELEGRAM_API_ID", 25647912))
    API_HASH = env.get("TELEGRAM_API_HASH", "60cb4e6c107e910420f0c16f000140df")
    OWNER_ID = int(env.get("OWNER_ID", 5979279455))
    ALLOWED_USER_IDS = env.get("ALLOWED_USER_IDS", "").split()
    BOT_USERNAME = env.get("TELEGRAM_BOT_USERNAME", "Kukufm_bot")
    BOT_TOKEN = env.get("TELEGRAM_BOT_TOKEN", "2123034087:AAFVrs5SCouBglZNV_xzYc1i9GFhuCVb-rM")
    CHANNEL_ID = int(env.get("TELEGRAM_CHANNEL_ID", -1002089314495))
    SECRET_CODE_LENGTH = int(env.get("SECRET_CODE_LENGTH", 12))

class Server:
    BASE_URL = env.get("BASE_URL", "http://81.31.197.224:6776")
    BIND_ADDRESS = env.get("BIND_ADDRESS", "0.0.0.0")
    PORT = int(env.get("PORT", 6776))

# LOGGING CONFIGURATION
LOGGER_CONFIG_JSON = {
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s][%(name)s][%(levelname)s] -> %(message)s',
            'datefmt': '%d/%m/%Y %H:%M:%S'
        },
    },
    'handlers': {
        'file_handler': {
            'class': 'logging.FileHandler',
            'filename': 'event-log.txt',
            'formatter': 'default'
        },
        'stream_handler': {
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        }
    },
    'loggers': {
        'uvicorn': {
            'level': 'INFO',
            'handlers': ['file_handler', 'stream_handler']
        },
        'uvicorn.error': {
            'level': 'WARNING',
            'handlers': ['file_handler', 'stream_handler']
        },
        'bot': {
            'level': 'INFO',
            'handlers': ['file_handler', 'stream_handler']
        }
    }
}
