#!/bin/bash

#use sbi_env environment
source ~/Projects/machine_learning_sbi/sbi_env/bin/activate

#train neural_network
python ~/Projects/machine_learning_sbi/PEWSBI/bin/train_neural_network.py \
   --sim-filename training_simulations5e4 \
   --output-folder ~/Projects/machine_learning_sbi/PEWSBI/examples/variable_distance/neural_nets \
   --n-simulations 1000 \
   --ini-filename injection1d \
   --batch-size 1000 \
   --learning-rate 5e-4 \
   --show-summary 
#    --verbose