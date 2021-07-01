import os
import yaml
import logging
logger = logging.getLogger(__name__)

from .helpers import dict_to_Command_input



class Command:
    """ Construct a command in the form:
    executable 
        input_file
        -flag_arg1 arg1
        --flag_arg2 arg2
        --flag3
        --flag4
        ...

    """
    def __init__(self, executable, input_file, args):
        self.executable = executable
        self.input_file = input_file
        self.args = args
        self.full_command = " ".join([self.executable] + [self.input_file] + self.args)
        
    def run(self):
        os.system(self.full_command)

    def __repr__(self):
        r = "\n{}\n\t{}\n\t".format(self.executable, self.input_file) + "\n\t".join(self.args)
        return r


class Routine:
    """ Takes a list of Command objects and run them in order
    """
    def __init__(self, commands=None):
        if not commands:
            self.commands = []
        else:
            self.commands = commands

    def run(self):
        for command in self.commands:
            command.run()

    def __repr__(self):
        return "\n".join([repr(command) for command in self.commands])


class XSRoutine(Routine):
    """ Given a YAML file like the ones provided e.g. in metadata/xscans, create a Routine that executes
    the following commands:
    - combine + ... for the global fit
    - a combineTool.py for each parameter of interest (to perform the single scans)
    """
    def __init__(self, category, input_dir, yaml_file, single_poi=None):
        self.commands = []

        # Read YAML file
        with open(yaml_file) as fl:
            full_dict = yaml.load(fl, Loader=yaml.FullLoader)
        
        # Global fit command
        global_fit_args = dict_to_Command_input(full_dict)
        global_fit_args.insert(0, "--name _POSTFIT_{}".format(category))
        global_fit_command = Command(
            executable="combine",
            input_file="{}/{}".format(input_dir, full_dict["path_to_root_file"]),
            args=global_fit_args    
        )
        self.commands.append(global_fit_command)

        # Individual fits commands
        if single_poi:
            logger.warning("Creating command in single_poi mode for poi {}".format(single_poi))
            pois = [single_poi]
        else:
            pois = list(full_dict["fit_per_bin"].keys())
        for poi in pois:
            fit_per_bin_args = dict_to_Command_input(full_dict, poi)
            fit_per_bin_args.insert(0, "--name _SCAN_{}_{}".format(poi, category))
            fit_per_bin_args.append("--task-name _SCAN_{}_{}".format(poi, category))
            self.commands.append(
                Command(
                    executable="combineTool.py",
                    input_file="higgsCombine_POSTFIT_{}.{}.mH125.root".format(
                        category, 
                        full_dict["global_fit"]["options"]["method"]
                        ),
                    args=fit_per_bin_args
                )
            )