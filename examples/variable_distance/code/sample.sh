#!/bin/bash

#use sbi_env environment
source ~/Projects/machine_learning_sbi/sbi_env/bin/activate

python ~/Projects/machine_learning_sbi/PEWSBI/bin/sample.py \
    --neural-net /home/mactodd315/Projects/machine_learning_sbi/PEWSBI/examples/variable_distance/neural_nets/NN_TS1e+04_LR5e-04_BS5e+03.pickle \
    --output-folder ~/Projects/machine_learning_sbi/PEWSBI/examples/variable_distance/posteriors \
    --observation-file ~/Projects/machine_learning_sbi/PEWSBI/examples/variable_distance/simulations/observations1e2.hdf \
    --config-file  ~/Projects/machine_learning_sbi/PEWSBI/examples/variable_distance/code/injection1d.ini \
    --observation-num 50 \
    --n-samples 10000 \
    --n-bins 500 \
    -v