import argparse
from differential_combination.utils import setup_logging


def parse_arguments():
    parser = argparse.ArgumentParser(
            description="Submit scans"
            )

    parser.add_argument(
            "--variable",
            required=True,
            type=str,
            help="Variable for which to run differential xs scans"
            )

    group.add_mutually_exclusive_group(required=True)
    group.add_argument(
            "--channel",
            type=str
            )
    group.add_argument(
            "--combination",
            type=bool
            )

    return parser.parse_args()


def main():
    logger = setup_logging()
    logger.info("Starting scans submission")



if __name__ == "__main__":
    main()
