# Differential Combination of Run 2 Data

## Set up

At the moment of writing, [Combine](https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit) only supports Python2 (in April 2021, with Python 2 end of life in late 2019 it's completely normal, isn't it?), so we're forced to write code accordingly. Hopefully, it will be ported to Python 3 in a while and we will be able to change this code as well.

To set up the environment, we use [this branch](https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit/pull/648) (that will probably be in master soon) and follow [these](https://github.com/nsmith-/HiggsAnalysis-CombinedLimit/tree/root6.22-compat#standalone-compilation-with-conda) instructions. This will create a conda environment with Python 2 and install Combine.
