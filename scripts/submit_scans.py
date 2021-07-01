""" Script to submit point scans for differential cross sections.
Following are the main parameters:
- variable: variable we are working with
- category: as can be seen in the README, it's usually something that identifies a combination of
year and decay channel, e.g. 2017_Hgg, 2018_Hzz, 2016_Combination, etc.
- metadata-dir: path to the directory where yaml files (1 per category) containing combine+combineTool
arguments specifications are stored
- input-dir: directory where workspaces are stored
- output-dir: base output directory; in this directory, the subdirectories created will be 
    xs_plots/variable/category
if category is already present, category-1, catyegory-2, etc. will be created, and the output
root files will be stored there
- single-poi: in case we want to submit scans for only one POI, specify it with this flag
"""
import argparse
import os

from differential_combination.utils import setup_logging
from differential_combination.command.command import XSRoutine
from differential_combination.utils import create_and_access_nested_dir, extract_from_yaml_file



def parse_arguments():
    parser = argparse.ArgumentParser(
            description="Submit scans"
            )

    parser.add_argument(
        "--level",
        type=str,
        default="INFO",
        choices=["INFO", "DEBUG"],
        help="Level of logger"
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
            help="Category for which submit scans"
            )
    
    parser.add_argument(
        "--metadata-dir",
        type=str,
        default="outputs",
        help="Directory where the .yaml files with metadata are stored"
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

    parser.add_argument(
        "--single-poi",
        type=str,
        help="Specify the name of the poi if the scan for only one parameter wants to be run"
    )

    return parser.parse_args()


def main(args):
    logger = setup_logging(args.level)
    logger.info("Starting scans submission")

    initial_path = os.path.abspath(os.getcwd())

    # Assign from args
    variable = args.variable
    category = args.category
    try:
        metadata_yml_file = "{}/{}.yml".format(args.metadata_dir, category)
    except:
        raise FileNotFoundError("Mismatch: category is {} but no file {}.yml found in {}".format(
            category, category, args.metadata_dir
        ))

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
    routine = XSRoutine(category, input_dir, metadata_yml_file, args.single_poi)
    logger.info("Built the following XSRoutine: \n{}".format(routine))

    # Create output subdirs and move to output dir
    output_path = "{}/xs_scans/{}/{}".format(output_dir, variable, category)
    create_and_access_nested_dir(output_path)

    # Run routine (submit jobs)
    routine.run()



if __name__ == "__main__":
    args = parse_arguments()
    main(args)
