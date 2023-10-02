#!/bin/bash

#use sbi_env environment
source ~/Projects/machine_learning_sbi/sbi_env/bin/activate

#train neural_network
python ~/Projects/machine_learning_sbi/PEWSBI/bin/train_neural_network.py \
   --simfile ~/Projects/machine_learning_sbi/PEWSBI/examples/no_noise/training_simulations5e4.hdf \
   --output-folder ~/Projects/machine_learning_sbi/PEWSBI/examples/no_noise/neural_nets \
   --n-simulations 10000 \
   --inifile ~/Projects/machine_learning_sbi/PEWSBI/examples/no_noise/injection1d.ini \
   --monitor-rate 100 \
   --batch-size 10000 \
   --learning-rate 5e-5 \
   --show-summary 
#    --verbose