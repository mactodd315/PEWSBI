#!/bin/bash

#use sbi_env environment
source ~/miniconda3/bin/activate sbi_env

current_folder="/home/mrtodd/PEWSBI"
example_folder="/examples/var_all_physical"

#train neural_network
python $current_folder/bin/train_neural_network.py \
   --simulation-file $current_folder$example_folder/simulations/trainings_all_big.hdf \
   --output-file $current_folder$example_folder/neural_nets/NN_all_snpe_5e5.pickle \
   --n-simulations 500000 \
   --training-parameters 'total_mass' 'mass_ratio'\
   --ini-file $current_folder$example_folder/code/injection.ini \
   --add-noise \
   --noise-file $current_folder$example_folder/simulations/noise.hdf \
   --batch-size 1000 \
   --learning-rate 5e-5 \
   --show-summary \
   --verbose
