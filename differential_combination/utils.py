import os
import logging
logger = logging.getLogger(__name__)


def setup_logging(level=logging.INFO):
    logger = logging.getLogger()

    logger.setLevel(level)
    formatter = logging.Formatter("%(levelname)s - %(filename)s:%(lineno)s - %(message)s")

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


def merge_two_dicts(x, y):
    # In Python3 we wouldn't need this shit... dioporcadiquellamadonna
    z = x.copy()
    z.update(y)
    return z


def create_and_access_nested_dir(path_to_dir):
    if path_to_dir.startswith("/"):
        final_path = path_to_dir
    else:
        current_path = os.path.abspath(os.getcwd())
        final_path = "{}/{}".format(current_path, path_to_dir)
    logger.info("Create {} if does not exist".format(final_path))
    os.system("mkdir -p {}".format(final_path))
    logger.info("Moving to {}".format(final_path))
    os.chdir(final_path)