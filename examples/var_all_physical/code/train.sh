#!/bin/bash

#use sbi_env environment
source ~/miniconda3/bin/activate sbi_env

current_folder="/home/mrtodd/PEWSBI"
example_folder="/examples/var_all_physical"

#train neural_network
python $current_folder/bin/train_neural_network.py \
   --simulation-file $current_folder$example_folder/simulations/trainings.hdf \
   --output-file $current_folder$example_folder/neural_nets/NN2_all.pickle \
   --n-simulations 100000 \
   --training-parameters 'total_mass' 'mass1' 'inclination' 'ra' 'dec' \
                         'distance' 'polarization' 'tc'\
   --ini-file $current_folder$example_folder/code/injection.ini \
   --batch-size 10000 \
   --learning-rate 5e-4 \
   --show-summary \
   --verbose
