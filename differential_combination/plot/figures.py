import matplotlib.pyplot as plt



class Figure:
    def __init__(self):
        self.fig, _ = plt.subplots()
        self.output_name = "prototype"

    def dump(self, output_dir):
        # Dump the image in multiple formats
        self.fig.savefig("{}/{}.png".format(output_dir, self.output_name), bbox_inches="tight")
        self.fig.savefig("{}/{}.pdf".format(output_dir, self.output_name), bbox_inches="tight")


class XSNLLsPerPOI(Figure):
    """
    """
    def __init__(self, differential_spectrum):
        self.fig, self.ax = plt.subplots()
        self.output_name = "NLLs_{}_{}".format(
            differential_spectrum.variable, differential_spectrum.category
            )
        
        # Draw all the NLLs on the ax
        for poi, scan in differential_spectrum.scans.items():
            self.ax = scan.plot(self.ax)