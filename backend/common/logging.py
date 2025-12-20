import logging

logger = logging.getLogger("filechat")

def log_info(message, **kwargs):
    logger.info(message, extra=kwargs)

def log_error(message, **kwargs):
    logger.error(message, extra=kwargs)
