#!/bin/bash

source ~/miniconda3/bin/activate sbi_env

python train_neural_network.py ../simulate/output.hdf \
                           test_nn.pickle \
                           10 \
                           ../simulate/injection.hdf \
                           ../simulate/injection.ini \
                           --noisefile ../simulate/noise.hdf \
                           --add-noise
