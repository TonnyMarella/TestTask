import logging


def set_file_logger(file_path, name="sync", level=logging.DEBUG, format_string=None):
    if not format_string:
        format_string = "%(asctime)s %(name)s [%(levelname)s] : %(message)s"
    logger = logging.getLogger(name)
    logger.handlers.clear()
    logger.setLevel(level)
    fh = logging.FileHandler(file_path, encoding='utf-8')
    fh.setLevel(level)
    formatter = logging.Formatter(format_string)
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger
