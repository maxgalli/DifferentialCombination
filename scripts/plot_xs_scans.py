import argparse
import matplotlib.pyplot as plt
import os

from differential_combination.utils import setup_logging, extract_from_yaml_file
from differential_combination.plot.scan import Scan, DifferentialSpectrum
from differential_combination.plot.figures import XSNLLsPerPOI


def parse_arguments():
    parser = argparse.ArgumentParser(
            description="Produce XS plots"
            )

    parser.add_argument(
            "--variable",
            required=True,
            type=str,
            help="Variable to produce XS plots for"
            )

    parser.add_argument(
        "--input-dir",
        type=str,
        default="outputs",
        help="Directory where the .root files with 'limit' trees are stored"
    )

    parser.add_argument(
        "--metadata-dir",
        type=str,
        default="outputs",
        help="Directory where the .yaml files with metadata are stored"
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
    variable = args.variable
    input_dir = args.input_dir
    metadata_dir = args.metadata_dir
    output_dir = args.output_dir
    logger.info("Plotting session for variable {}".format(variable))

    # First produce NLL plots, one for each category
    # Each containing the NLL curves for each POI
    for fl in os.listdir(metadata_dir):
        full_path_to_file = "{}/{}".format(metadata_dir, fl)
        # Based on the assumption that we have a config file for each category called 'category_name.yaml'
        category = fl.split(".")[0]
        metadata_dct = extract_from_yaml_file(full_path_to_file)

        # metadata_dct has the format {"binning": {"poi1": [], "poi2": []}}
        pois = list(metadata_dct["binning"].keys())

        diff_spectrum = DifferentialSpectrum(variable, category, pois, input_dir)

        plot_to_dump = XSNLLsPerPOI(diff_spectrum)
        plot_to_dump.dump(output_dir)


if __name__ == "__main__":
    args = parse_arguments()
    main(args)