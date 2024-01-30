# How to run this example 
There are several bash scripts in contained in the subfolder `code`, and walking through these demonstrates
the flow of the modular nature of this code. **Note: You should change the current folder variable in each
of the scripts to match where your PEWSBI directory is.** All created files and subdirectories will be contained
inside this example folder.

**Before running any scripts, you must activate the installed environment**
```
conda activate sbi_env
```

All `python` scripts have `argparse` help written and can be called with
```
python /path/to/script.py -h
```

## 1. `injection.ini`
For this example, as the folder name suggests, attempts to train a neural network on varying total mass, with all other parameters held fixed, for simulated gravitational wave signals. Then, given an untrained set of observations, makes estimates of the posterior distribution for the total mass after observing that data.
The `injection.ini` file is the configuration file that describes the model we are trying to analyze. The file itself follows a basic `.ini` setup, and is used by `pycbc_create_injections`. The only variables in the `[variable_params]` section should be `mass_1` and `mass_2`, provided that there are prior sections (e.g. `[prior-mass1]`) for each and there is a `[waveform_transforms-total_mass]` section.

If one wanted to create a model with more variable parameters, simply take them from `[static_params]` and put them in the `[variable_params]` section, and defining a prior for that parameter.

## 2. `simulate_trainings.sh`
This script calls `pycbc_create_injections`, taking in the injection configuration (i.e. `injection.ini`) along with the number of desired simulations and the path to write `output_file`. This writes an `.hdf` file that will be used by `simulate_data.py` to write the simulations. `--signal-length` determines the number of points in the `TimeSeries` object, while `--signal-length` / `--delta-f` will give you the total time represented in the simulation.

The training simulations will be written to the path provided by `--output-file`.

## 3. `make_noise.sh`
This script calls `generate_noise.py` to create a simulation file of noise that can be randomly combined with simulation signals in later scripts. One note that should be made is that 1 / `--delta-t` here should be larger than `--delta-f` in the simulations made in `simulate_trainings` or `simulate_observations`.

## 5. `simulate_observations.sh`
As the name suggests, this script can be used to simulate observations, with noise already added to the simulations for later sampling from. It takes all the arguments that `simulate_trainings.sh` takes; however, usually writes fewer samples. 

Make sure that `--add-noise` and `--noise-file` arguments are included for this script.

## 4. `train.sh`
This is the main aspect of the code, in which a neural network is trained from the training simulations to construct a posterior estimate for the desired parameters (defined with `--training-parameters`). There are several arguments that can be adjusted for slower training, such as `batch_size` and `learning_rate`, as well as `training_method`. Further discussion of these parameters and their impact on training can be found at https://github.com/sbi-dev/sbi.

The number of simulations `n_simulations` can be specified if one has a file containing a large number of simulations but only wants to use a fraction of them, and `training_parameters` can be specified in any order; however they must be variable parameters or transforms of variable parameters, declared in the simulations file, in order to be trained.

Here, noise can be added to training simulations to better represent observations, using `--add-noise` and `--noise-file`.

## 6. `sample.sh`
Here, one can select a trained neural network that is to be sampled from, along with an `observation_file` (either simulated or real). Then, `sample_paramters` can be provided, which will indicate which posteriors to estimate. The samples are written to the desired `output_file`, and can also be written in `pycbc_posterior` format, which can be plotted easily later with `pycbc_inference_plot_posterior`.

## 7. `plot_pptest.sh`
This script can plot a percentile percentile test as well as a posterior estimate, with the expected value or "true parameter". In both, the `sample_parameter` must be specified, as well as the samples file. For the percentile-percentile test, the number of posteriors (`num_posteriors`) to be averaged over, contained in the samples file, must be specified as well.

## 8. `plot_pycbc_posterior.sh`
`pycbc_inference_plot_posterior` is a `pycbc` method that takes an input file which has been formatted for plotting posteriors. The output file will be an image file saved at the desired path. `parameters` to use in the posterior plotting can be specified along with their expected values, which will be plotted in red.