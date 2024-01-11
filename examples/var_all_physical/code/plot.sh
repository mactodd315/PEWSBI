#!/bin/bash

#use sbi_env environment
source ~/miniconda3/bin/activate sbi_env

current_folder="/home/mrtodd/PEWSBI"
example_folder="/examples/var_all_physical"

python $current_folder/bin/plot.py \
    --samples-file $current_folder$example_folder/samples/samples_all_snpe.hdf \
    --plot-folder   $current_folder$example_folder/plots \
    --plot-content 'pptest' \
    --config-file    $current_folder$example_folder/code/injection.ini \
    --n-trainings 300000 \
    --sample-parameters 'total_mass' 'mass_ratio'\
    --num-posteriors 100

python $current_folder/bin/plot.py \
    --samples-file  $current_folder$example_folder/samples/samples_all_snpe.hdf \
    --plot-folder  $current_folder$example_folder/plots \
    --plot-content 'posterior' \
    --config-file   $current_folder$example_folder/code/injection.ini \
    --sample-parameter 'total_mass' \
    --posterior-index 0 \
    --plot-true

python $current_folder/bin/plot.py \
    --samples-file  $current_folder$example_folder/samples/samples_all_snpe.hdf \
    --plot-folder  $current_folder$example_folder/plots \
    --plot-content 'posterior' \
    --config-file   $current_folder$example_folder/code/injection.ini \
    --sample-parameter 'mass_ratio' \
    --posterior-index 0 \
    --plot-true