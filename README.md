# Differential Combination Run 2 Data

## Set up

At the moment of writing, [Combine](https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit) only supports Python2 (in April 2021, with Python 2 end of life in late 2019 it's completely normal, isn't it?), so we're forced to write code accordingly. Hopefully, it will be ported to Python 3 in a while and we will be able to change this code as well. 

To set up the environment, we use [this branch](https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit/pull/648) (that will probably be in master soon) and follow [these](https://github.com/nsmith-/HiggsAnalysis-CombinedLimit/tree/root6.22-compat#standalone-compilation-with-conda) instructions. This will create a conda environment with Python 2 and install Combine. 

## Inputs

This analysis is built using as initial inputs the datacards and workspaces used to produce the results for [this analysis](https://github.com/tklijnsma/differentialCombination2017) and available [here](https://github.com/tklijnsma/input-diffcomb-HIG17028).

The folder ```inputs/2017``` is thus filled with datacards, workspaces and root files produces following [these instructions](https://github.com/tklijnsma/differentialCombination2017/wiki). 

More specifically, we run [the commands](https://github.com/tklijnsma/differentialCombination2017/wiki/3-Running-text2workspace#t2ws-for-differential-cross-sections) to produce the workspaces and copy them to the according subfolder. The datacards used to produce the workspaces (through Combine's ```text2workspace.py```) are also copied and are printed when running the above mentioned commands. The root files that the datacards use as input are also copied.
