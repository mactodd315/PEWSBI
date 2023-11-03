#!/bin/bash

#use sbi_env environment
source ~/Projects/machine_learning_sbi/sbi_env/bin/activate

current_folder="/home/mactodd315/Projects/machine_learning_sbi/PEWSBI"
example_folder="/examples/var_all_physical"

#train neural_network
python $current_folder/bin/train_neural_network.py \
   --simulation-file $current_folder$example_folder/simulations/trainings.hdf \
   --output-file $current_folder$example_folder/neural_nets/NN1.pickle \
   --n-simulations 10000 \
   --training-parameters 'total_mass' \
   --ini-file $current_folder$example_folder/code/injection.ini \
   --batch-size 1000 \
   --learning-rate 5e-5 \
   --show-summary 
#    --verbose