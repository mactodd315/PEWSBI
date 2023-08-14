#!/bin/bash

source ~/miniconda3/bin/activate sbi_env

bash simulate/create_injection.sh simulate/injection.ini 100 simulate/injection.hdf

python simulate/simulate_data.py simulate/injection.hdf simulate/simulations.hdf -v

python sample/sample.py train/neural_network.pickle \
                    sample/posteriors.hdf \
                    simulate/simulations.hdf \
                    simulate/injection.ini \
                    'distance' \
                    --observation-num 100 \
                    -v