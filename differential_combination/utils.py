import os
import yaml
import logging
logger = logging.getLogger(__name__)


def setup_logging(level=logging.INFO):
    logger = logging.getLogger()

    logger.setLevel(getattr(logging, level))
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
    """ Create a nested directory for path_to_dir and access it.
    First, a check is performed and last "/" removed if present.
    Then, we create and absolute if path_to_dir is relative (i.e., if it does not start with "/").
    We then split the full path into base_dir and the last nested level (want_to_create).
    Ex:
    final_path = "/aa/bb/cc/dd"
    base_dir = "/aa/bb/cc"
    want_to_create = "dd"
    We then check if want_to_create is present; if it is, instead of "want_to_create", we create 
    want_to_create-$(N+1) where N is the highest number for which we have directories called
    want_to_create-$N inside base_dir
    """
    path_to_dir = path_to_dir[:-1] if path_to_dir.endswith("/") else path_to_dir
    if path_to_dir.startswith("/"):
        final_path = path_to_dir
    else:
        current_path = os.path.abspath(os.getcwd())
        final_path = "{}/{}".format(current_path, path_to_dir)

    base_dir, want_to_create = final_path.rsplit("/", 1)
    already_in_base_dir = [s for s in os.listdir(base_dir) if want_to_create in s]
    if want_to_create in already_in_base_dir:
        logger.debug("{} already present in {}".format(want_to_create, already_in_base_dir))
        counter = 1
        while True:
            check = "{}-{}".format(want_to_create, counter)
            if check in already_in_base_dir:
                logger.debug("{} already present in {}".format(check, already_in_base_dir))
                counter += 1
                continue
            else:
                want_to_create = check
                break

    final_path = "{}/{}".format(base_dir, want_to_create)
    logger.info("Creating {}".format(final_path))
    os.system("mkdir -p {}".format(final_path))
    logger.info("Moving to {}".format(final_path))
    os.chdir(final_path)


def extract_from_yaml_file(path_to_file):
    with open(path_to_file) as fl:
        dct = yaml.load(fl, Loader=yaml.FullLoader)
    
    return dct