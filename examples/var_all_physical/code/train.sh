#!/bin/bash

#use sbi_env environment
source ~/miniconda3/bin/activate sbi_env

current_folder="/home/mrtodd/PEWSBI"
example_folder="/examples/var_all_physical"

#train neural_network
python $current_folder/bin/train_neural_network.py \
   --simulation-file $current_folder$example_folder/simulations/trainings_all.hdf \
   --output-file $current_folder$example_folder/neural_nets/NN_all.pickle \
   --n-simulations 100000 \
   --training-parameters 'total_mass' 'mass_ratio'\
   --ini-file $current_folder$example_folder/code/injection.ini \
   --add-noise \
   --noise-file $current_folder$example_folder/simulations/noise.hdf \
   --batch-size 1000 \
   --learning-rate 5e-4 \
   --show-summary \
   --verbose
