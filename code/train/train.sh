#!/bin/bash

source /home/mrtodd/miniconda3/bin/activate sbi_env

python /home/mrtodd/PEWSBI/code/train/train_neural_network.py \
                           /home/mrtodd/PEWSBI/code/simulate/training_simulations.hdf \
                           /home/mrtodd/PEWSBI/code/train/neural_network.pickle \
                           20000 \
                           /home/mrtodd/PEWSBI/code/simulate/injection_test.hdf \
                           /home/mrtodd/PEWSBI/code/simulate/injection.ini \
                           --noisefile /home/mrtodd/PEWSBI/code/simulate/noise.hdf \
                           --add-noise \
                           -v
