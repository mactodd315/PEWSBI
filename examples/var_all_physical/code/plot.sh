#!/bin/bash

#use sbi_env environment
source ~/Projects/machine_learning_sbi/sbi_env/bin/activate

current_folder="/home/mactodd315/Projects/machine_learning_sbi/PEWSBI"
example_folder="/examples/var_all_physical"

python $current_folder/bin/plot.py \
    --samples-file $current_folder$example_folder/samples/samples1.hdf \
    --plot-folder   $current_folder$example_folder/plots \
    --plot-content 'pptest' \
    --config-file    $current_folder$example_folder/code/injection.ini \
    --sample-parameters 'total_mass' \
    --num-posteriors 10

python $current_folder/bin/plot.py \
    --samples-file  $current_folder$example_folder/samples/samples1.hdf \
    --plot-folder  $current_folder$example_folder/plots \
    --plot-content 'posterior' \
    --config-file   $current_folder$example_folder/code/injection.ini \
    --sample-parameter 'total_mass' \
    --posterior-index 7 \
    --plot-true

# python $current_folder/bin/plot.py \
#     --samples-folder  $current_folder$example_folder/samples/ \
#     --sample-name samples_TS1e+04_LR5e-05_BS1e+03.hdf \
#     --plot-folder  $current_folder$example_folder/plots_1e4 \
#     --plot-content 'posterior' \
#     --config-file   $current_folder$example_folder/code/injection.ini \
#     --sample-parameter 'mass1' \
#     --posterior-index 10 \
#     --plot-true
# python $current_folder/bin/plot.py \
#     --samples-folder  $current_folder$example_folder/samples/ \
#     --sample-name samples_TS1e+04_LR5e-05_BS1e+03.hdf \
#     --plot-folder  $current_folder$example_folder/plots_1e4 \
#     --plot-content 'posterior' \
#     --config-file   $current_folder$example_folder/code/injection.ini \
#     --sample-parameter 'mass2' \
#     --posterior-index 10 \
#     --plot-true
# python $current_folder/bin/plot.py \
#     --samples-folder  $current_folder$example_folder/samples/ \
#     --sample-name samples_TS1e+04_LR5e-05_BS1e+03.hdf \
#     --plot-folder  $current_folder$example_folder/plots_1e4 \
#     --plot-content 'posterior' \
#     --config-file   $current_folder$example_folder/code/injection.ini \
#     --sample-parameter 'inclination' \
#     --posterior-index 10 \
#     --plot-true