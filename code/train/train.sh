#!/bin/bash

source /home/mrtodd/miniconda3/bin/activate sbi_env

python /home/mrtodd/PEWSBI/code/train/train_neural_network.py \
                           /home/mrtodd/PEWSBI/datafiles/cluster_simulations.hdf \
                           /home/mrtodd/PEWSBI/neural_nets/neural_network$1.pickle \
                           $1 \
                           /home/mrtodd/PEWSBI/datafiles/cluster_injections.hdf \
                           /home/mrtodd/PEWSBI/code/simulate/injection.ini \
                           --noisefile /home/mrtodd/PEWSBI/code/simulate/noise.hdf \
                           --add-noise \
                           -v
