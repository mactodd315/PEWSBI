#!/bin/bash

#use sbi_env environment
source ~/Projects/machine_learning_sbi/sbi_env/bin/activate # change to your env dir.

current_folder="/home/mactodd315/Projects/machine_learning_sbi/PEWSBI"
example_folder="/examples/variable_totalmass"

#train neural_network
python $current_folder/bin/train_neural_network.py \
   --simulation-file $current_folder$example_folder/simulations/training_simulations.hdf \
   --output-file $current_folder$example_folder/neural_nets/NN_totalmass2.pickle \
   --n-simulations 10000 \
   --training-parameters 'total_mass' \
   --batch-size 1000 \
   --learning-rate 5e-5 \
   --training-method SNLE \
   --show-summary \
   --add-noise \
   --noise-file $current_folder$example_folder/simulations/noise.hdf \
   --verbose