#!/bin/bash

#use sbi_env environment
source ~/miniconda3/bin/activate sbi_env

python ~/PEWSBI/bin/sample_test.py \
    --neural-net ~/PEWSBI/examples/var_dis_totalmass/neural_nets/NN_TS3e+05_LR5e-04_BS1e+03.pickle \
    --output-folder ~/PEWSBI/examples/var_dis_totalmass/posteriors \
    --observation-file ~/PEWSBI/examples/var_dis_totalmass/simulations/observations1e2.hdf \
    --config-file  ~/PEWSBI/examples/var_dis_totalmass//code/injection2d.ini \
    --observation-num 100 \
    --n-samples 10000 \
    --n-bins 500 \
    -v