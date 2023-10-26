#!/bin/bash

#use sbi_env environment
source ~/Projects/machine_learning_sbi/sbi_env/bin/activate

current_folder="/home/mactodd315/Projects/machine_learning_sbi/PEWSBI"
example_folder="/examples/var_all_physical"

#train neural_network
python $current_folder/bin/train_neural_network.py \
   --sim-filename trainings_1e4 \
   --output-folder $current_folder$example_folder/neural_nets \
   --n-simulations 10000 \
   --ini-filename injection \
   --batch-size 1000 \
   --learning-rate 5e-5 \
   --show-summary 
#    --verbose