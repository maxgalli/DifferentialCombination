import uproot4 as uproot
import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt

import logging
logger = logging.getLogger(__name__)



class Scan:
    """
    """
    def __init__(self, poi, input_dir):
        self.default_cut = "deltaNLL<990.0"
        self.file_name_tmpl = "higgsCombine_SCAN_{}*.root".format(poi)
        self.tree_name = "limit"
        self.poi = poi

        # Read the two branches we are interested in: deltaNLL and the POI one
        logger.info("Looking for files that look like {} inside {}".format(
            self.file_name_tmpl, input_dir)
            )
        branches = uproot.concatenate(
            ["{}/{}:{}".format(input_dir, self.file_name_tmpl, self.tree_name)],
            expressions=[self.poi, "deltaNLL"],
            cut=self.default_cut
        )
        logger.info("Found {} points".format(len(branches)))

        # For semplicity, make two separate arrays after sorting them
        branches_np = np.array([branches[poi], branches["deltaNLL"]])
        branches_np = branches_np[:, branches_np[0].argsort()]
        poi_values_original = branches_np[0]
        two_dnll_original = 2 * branches_np[1]

        # Interpolate and re-make arrays to have more points
        self.dNLL_func = interpolate.interp1d(poi_values_original, two_dnll_original)
        self.n_interpol = 1000000
        self.poi_boundaries = (poi_values_original[0], poi_values_original[-1])
        self.poi_values = np.linspace(self.poi_boundaries[0], self.poi_boundaries[1], self.n_interpol)
        self.two_dnll = self.dNLL_func(self.poi_values)

        # Find minimum and compute uncertainties
        self.find_minimum()
        logger.info("Found minimum at {}".format(self.minimum))
        self.compute_uncertainties()
        logger.info("Down uncertainty: {}, up uncertainty: {}".format(
            self.down_uncertainty, self.up_uncertainty))

    
    def find_minimum(self):
        min_two_dnll = np.amin(self.two_dnll)
        poi_best = self.poi_values[np.argmin(self.two_dnll)]
        self.minimum = (poi_best, min_two_dnll)


    def compute_uncertainties(self):
        level = self.minimum[1] + 1.
        level_arr = np.ones(self.n_interpol) * level
        down_idx, up_idx = np.argwhere(np.diff(np.sign(self.two_dnll - level_arr))).flatten()
        self.down = (self.poi_values[down_idx], self.dNLL_func(self.poi_values[down_idx]))
        self.up = (self.poi_values[up_idx], self.dNLL_func(self.poi_values[up_idx]))
        self.down_uncertainty = abs(self.minimum[0] - self.down[0])
        self.up_uncertainty = abs(self.minimum[0] - self.up[0])


    def plot(self, ax):
        logger.info("Plotting scan for {}".format(self.poi))
        # Restrict the plotted values to a dnll less than 3.5
        x = self.poi_values[self.two_dnll < 3.5]
        y = self.two_dnll[self.two_dnll < 3.5]
        plt.plot(x, y)
        ax.axvline(self.minimum[0])
        plt.plot([self.down[0], self.up[0]], [self.down[1], self.up[1]], "go")
        return ax