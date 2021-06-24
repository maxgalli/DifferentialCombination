# Differential Combination Run 2 Data  
  
## Set up  
  
At the moment of writing, [Combine](https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit) only supports Python2, so we're forced to write code accordingly. Hopefully, it will be ported to Python 3 in a while and we will be able to change this code as well.  
There are two possible ways to set up the environment, described below.

### Conda environment (preferred way)
To set up the environment, we use [this branch](https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit/pull/648) (that will probably be in master soon) and follow [these](https://github.com/nsmith-/HiggsAnalysis-CombinedLimit/tree/root6.22-compat#standalone-compilation-with-conda) instructions. This will create a conda environment with Python 2 and install Combine. However, at the moment of writing there is no branch in [CombineHarvester](https://github.com/cms-analysis/CombineHarvester) to install it in a Conda environment.
Installing the package in the ```site-packages``` directories can be done simply with
```
pip install -e .
``` 

### CMSSW 11_2 (ROOT 6.22)
This is supposed to use the branches called 112x in both Combine and CombineHarvester. At the moment of writing, only the first one is available, hence follow these instructions.
```
export SCRAM_ARCH=slc7_amd64_gcc900
cmsrel CMSSW_11_2_0_pre10
cd CMSSW_11_2_0_pre10/src
cmsenv
git clone -b 112x https://github.com/cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit
git clone -b root622_comp https://github.com/maxgalli/CombineHarvester.git
scramv1 b
```
Remember that running ```cmsenv``` from inside ```CMSSW_11_2_0_pre10/src``` has to be done every time a new session starts.

In this case, installing the package is a bit more complicated since we don't have privileges on the ```cvmfs``` directories.
To install in a specific directory (e.g. ```~/install_dir```) the process consists in the following:
```
source setup_cmssw112_env.sh ~/install_dir
python setup.py install --home=~/install_dir
```

### Working
The suggested way to work (at the moment of writing, 24.06.21) is to have a main directory ```DifferentialCombination_home``` that looks like:
```
.
|-- DifferentialCombination
|-- install_dir
`-- outputs
```
where ```DifferentialCombination``` is this very repo, ```install_dir``` is where we install the package (assuming we're not working with conda, because in that case we could easily install in the default directories) and ```outputs``` is all the relevant outputs end up.
The drawback is that every time a change is implemented, ```python setup.py install --home=../install_dir``` has to be re-run from inside the repo, but at least we keep the clone clean. This also allows us to run the scripts that are installed from wherever we want.


## Inputs  
  
This analysis is built using as initial inputs the datacards and workspaces used to produce the results for [this analysis](https://github.com/tklijnsma/differentialCombination2017) and  
available [here](https://github.com/tklijnsma/input-diffcomb-HIG17028).  
  
The folder ```inputs/2017``` is thus filled with datacards, workspaces and root files produces following [these instructions](https://github.com/tklijnsma/differentialCombination2017/wiki).  
  
More specifically, we run [the commands](https://github.com/tklijnsma/differentialCombination2017/wiki/3-Running-text2workspace#t2ws-for-differential-cross-sections) to produce the works  
paces and copy them to the according subfolder. The datacards used to produce the workspaces (through Combine's ```text2workspace.py```) are also copied and are printed when running the  
above mentioned commands. The root files that the datacards use as input are also copied.


## Mind-Scheme
The main challenge of this work is probably determine an efficient bookkeeping for all the possible situations. It is thus important to divide the work in "areas" that should be reflected in the output layout too.
The first macro-division is of course between ```differential spectra``` and ```interpretation```.

Inside each of them, we have to perform a few kind of operations, mostly related to:

- datacard preprocessing/production
- likelihood evaluation (with scans submission)
- plot

Now, all these operations (let's say except plotting, which we will address more in detail at a later point) have to be performed for multiple **variables of interest**.

Inside each variables we have multiple **categories**, that can be conveniently divided in the following types:

- binning-like (the name is probably inappropriate, but still...)
- decay-mode
- year

At datacard level, we will probably have one datacard for each combination of decay-mode and year categories (e.g. 2017Hzz, 2018Hgg, 2017Hgg+Htautau, etc.). Inside every datacard, every binning-like category is considered.