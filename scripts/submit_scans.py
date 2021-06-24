import argparse
import os

from differential_combination.utils import setup_logging
from differential_combination.command.command import XSRoutine
from differential_combination.utils import create_and_access_nested_dir



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

    parser.add_argument(
            "--category",
            required=True,
            type=str,
            help="Category for which submit scans",
            choices=[
                "Hgg",
                "Hzz",
                "Hbb",
                "Combination",
                "CombWithHbb"
            ]
            )
    
    parser.add_argument(
        "--metadata",
        type=str,
        default="DifferentialCombination/metadata/xs_scans_specs.yml",
        help="Directory where .yaml files with metadata are stored"
    )

    parser.add_argument(
        "--input-dir",
        type=str,
        default="outputs",
        help="Directory where the .root file containing the workspaces is stored"
    )

    parser.add_argument(
        "--output-dir",
        type=str,
        default="outputs",
        help="Directory where output files will be stored"
    )

    return parser.parse_args()


def main(args):
    logger = setup_logging()
    logger.info("Starting scans submission")

    initial_path = os.path.abspath(os.getcwd())

    # Assign from args
    variable = args.variable
    category = args.category
    metadata_yml_file = args.metadata

    if args.input_dir.startswith("/"):
        input_dir = args.input_dir
    else:
        input_dir = "{}/{}".format(initial_path, args.input_dir)
    output_dir = args.output_dir

    logger.info("Variable: {}".format(variable))
    logger.info("Channel: {}".format(category))
    logger.info("Metadata: {}".format(metadata_yml_file))
    logger.info("Output Directory: {}".format(output_dir))

    # Build Routine
    routine = XSRoutine(category, input_dir, metadata_yml_file)
    logger.info("Built the following XSRoutine: \n{}".format(routine))

    # Create output subdirs and move to output dir
    output_path = "{}/xs_scans/{}/{}/".format(output_dir, variable, category)
    create_and_access_nested_dir(output_path)

    # Run routine (submit jobs)
    routine.run()



if __name__ == "__main__":
    args = parse_arguments()
    main(args)
