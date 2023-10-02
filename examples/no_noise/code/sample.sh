#!/bin/bash

#use sbi_env environment
source ~/Projects/machine_learning_sbi/sbi_env/bin/activate

python ~/Projects/machine_learning_sbi/PEWSBI/bin/sample.py \
    --neural-net /home/mactodd315/Projects/machine_learning_sbi/PEWSBI/examples/no_noise/neural_nets/NN_TS50000_LR5e-04_BS5e+04.pickle \
    --output-folder ~/Projects/machine_learning_sbi/PEWSBI/examples/no_noise/posteriors5e4 \
    --observation-file ~/Projects/machine_learning_sbi/PEWSBI/examples/no_noise/observation_simulations_5e1.hdf \
    --config-file  ~/Projects/machine_learning_sbi/PEWSBI/examples/no_noise/injection1d.ini \
    --sample-parameter 'distance' \
    --observation-num 50 \
    --n-samples 10000 \
    --n-bins 500 \
    -v