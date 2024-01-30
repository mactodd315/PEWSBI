# PEWSBI

Parameter Estimation with Simulation Based Inferencing (PEWSBI), for Gravitational-wave signals.

## How to install

1. Make sure you have `conda` installed:
```
conda --version
```
This should return something like `conda 23.X.X`

2. Change directories to the directory to place the PEWSBI package in, then `git` clone the repo:
```
cd /path/to/directory/
git clone https://github.com/mactodd315/PEWSBI.git
```

3. Install the `sbi_env` using the env `.yml` file in this repo:
```
cd PEWSBI
conda env create -f environment.yml
conda activate sbi_env
```

4. Activate the new env and check that certain packages are installed:
```
conda list -n sbi_env numpy
conda list -n sbi_env matplotlib
conda list -n sbi_env pycbc
conda list -n sbi_env sbi
conda list -n sbi_env torch
```