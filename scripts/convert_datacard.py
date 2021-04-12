import argparse
import json


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="Convert datacard to JSON file"
        )

    parser.add_argument(
        "--input-card",
        required=True,
        type=str,
        help="Datacard in .txt format"
        )

    parser.add_argument(
        "--output-dir",
        required=True,
        type=str,
        help="Output directory where JSON file is saved"
        )

    return parser.parse_args()


def main(args):
    input_card = args.input_card
    output_dir = args.output_dir

    output_file = "{}/{}.json".format(
            output_dir,
            input_card.split('/')[-1].replace('.txt', ''))

    output_dict = {
            "shapes": [],
            "bin": [],
            "observation": [],
            "process": [],
            "rate": []
            }
    shapes_fields = ["process", "channel", "file", "histogram"]

    with open(input_card, "r") as fr:
        for line in fr:
            if line.startswith("shapes"):
                output_dict["shapes"].append({k: v for k, v in zip(shapes_fields, line.split()[1:])})

    with open(output_file, "w") as fw:
        json.dump(output_dict, fw)


if __name__ == "__main__":
    args = parse_arguments()
    main(args)
