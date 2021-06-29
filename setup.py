import setuptools
from importlib import import_module

# Check ROOT related requirements and raise error if not found
for pkg in ['ROOT', 'cppyy', 'cppyy_backend']:
    try:
        import_module(pkg)
    except ImportError:
        raise ImportError('{} not found. You need a full working installation of ROOT to install this package.\n' \
                'For more info, see: https://root.cern/install/'.format(pkg))

# Check if Combine is installed and raise an error if not
try:
    import HiggsAnalysis.CombinedLimit
except ImportError:
    raise ImportError("Combine was not found and it is necessary. For this package, we are installing it like suggested in https://github.com/nsmith-/HiggsAnalysis-CombinedLimit/tree/root6.22-compat#standalone-compilation-with-conda")

setuptools.setup(
    name="differential_combination",
    author="Massimiliano Galli",
    author_email="massimiliano.galli.95@gmail.com",
    description="Package for Run 2 differential combination",
    packages=setuptools.find_packages(),
    scripts=[
        "scripts/combine_datacards.py", 
        "scripts/convert_datacard.py",
        "scripts/submit_scans.py",
        "scripts/plot_xs_scans.py"
        ],
    install_requires=[
        ],
    python_requires="==2.7.15"
)
