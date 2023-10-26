#!/bin/bash

#use sbi_env environment
source ~/Projects/machine_learning_sbi/sbi_env/bin/activate

python ~/Projects/machine_learning_sbi/PEWSBI/bin/sample_test.py \
    --neural-net ~/Projects/machine_learning_sbi/PEWSBI/examples/var_dis_totalmass/neural_nets/NN_TS3e+05_LR5e-04_BS1e+03.pickle \
    --output-folder ~/Projects/machine_learning_sbi/PEWSBI/examples/var_dis_totalmass/samples \
    --observation-file ~/Projects/machine_learning_sbi/PEWSBI/examples/var_dis_totalmass/simulations/observations1e2.hdf \
    --config-file  ~/Projects/machine_learning_sbi/PEWSBI/examples/var_dis_totalmass//code/injection2d.ini \
    --observation-num 100 \
    --n-samples 10000 \
    --n-bins 500 \
    -v