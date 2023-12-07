#!/bin/bash

#use sbi_env environment
source ~/miniconda3/bin/activate sbi_env

current_folder="/home/mrtodd/PEWSBI"
example_folder="/examples/var_all_physical"

python $current_folder/bin/plot.py \
    --samples-file $current_folder$example_folder/samples/samples_all.hdf \
    --plot-folder   $current_folder$example_folder/plots \
    --plot-content 'pptest' \
    --config-file    $current_folder$example_folder/code/injection.ini \
    --sample-parameters 'total_mass' 'mass1' 'inclination' 'ra' 'dec' 'distance' 'tc' 'polarization'\
    --num-posteriors 100

python $current_folder/bin/plot.py \
    --samples-file  $current_folder$example_folder/samples/samples_all.hdf \
    --plot-folder  $current_folder$example_folder/plots \
    --plot-content 'posterior' \
    --config-file   $current_folder$example_folder/code/injection.ini \
    --sample-parameter 'polarization' \
    --posterior-index 0 \
    --plot-true

python $current_folder/bin/plot.py \
    --samples-file  $current_folder$example_folder/samples/samples_all.hdf \
    --plot-folder  $current_folder$example_folder/plots \
    --plot-content 'posterior' \
    --config-file   $current_folder$example_folder/code/injection.ini \
    --sample-parameter 'tc' \
    --posterior-index 0 \
    --plot-true