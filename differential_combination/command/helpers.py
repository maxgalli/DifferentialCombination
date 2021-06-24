import logging
logger = logging.getLogger(__name__)



def get_arg_format(k, v):
    """ Given a pair of values e.g. 'a', 'b' return a string in the format '--a b'
    If the second value is a boolean:
        if True, return '--a'

    This is meant to be used inside config_file_to_Command_input 
    """
    if k in ["sub-opts"]:
        return "--{}={}".format(k, v)
    if isinstance(v, bool):
        return "--{}".format(k)
    else:
        return "--{} {}".format(k, v)


def build_setParameterRanges(dct):
    """Given a dictionary in the form
    dct = {
        "par1": {
            "range": [a, b]
        },
        "par2": {
            "range": [c, d]
        }
    }
    return "par1=a,b:par2=c,d"
    """
    single_param_format = "{}={},{}"
    string = ":".join([
        single_param_format.format(k, v["range"][0], v["range"][1]) for k, v in dct.items()
    ])
    return string


def dict_to_Command_input(full_dict, poi=None):
    """ Given a dictionary in the following format:
    full_dict = {
        'global_fit': {
            'options': {
                ...
            }
        },
        'fit_per_bin': {
            'par1': {
                'options': {
                    ...
                }
            },
            ...
        }
    }
    convert it to a list of arguments to feed Command.
    If poi is None, 'global_fit' is assumed
    Otherwise get the specific key in 'fit_per_bin'
    """
    args = []

    if poi:
        par_dict = full_dict["fit_per_bin"][poi]["options"]
        for k, v in par_dict.items():
            args.append(get_arg_format(k, v))
        args.append("-P {}".format(poi))
        # Append --setParameterRanges flag
        args.append("--setParameterRanges " + build_setParameterRanges(full_dict["fit_per_bin"]))
        # Append batch related options
        for k, v in full_dict["batch_config"].items():
            args.append(get_arg_format(k, v))
    else:
        var_dict = full_dict["global_fit"]["options"]
        for k, v in var_dict.items():
            args.append(get_arg_format(k, v))

    return args