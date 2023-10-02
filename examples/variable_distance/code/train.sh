#!/bin/bash

#use sbi_env environment
source ~/Projects/machine_learning_sbi/sbi_env/bin/activate

#train neural_network
python ~/Projects/machine_learning_sbi/PEWSBI/bin/train_neural_network.py \
   --simfile ~/Projects/machine_learning_sbi/PEWSBI/examples/variable_distance/simulations/training_simulations5e4.hdf \
   --output-folder ~/Projects/machine_learning_sbi/PEWSBI/examples/variable_distance/neural_nets \
   --n-simulations 10000 \
   --inifile ~/Projects/machine_learning_sbi/PEWSBI/examples/variable_distance/code/injection1d.ini \
   --batch-size 5000 \
   --learning-rate 5e-4 \
   --show-summary 
#    --verbose