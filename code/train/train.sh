#!/bin/bash

source /home/mrtodd/miniconda3/bin/activate sbi_env

python /home/mrtodd/PEWSBI/bin/train_neural_network.py \
       /home/mrtodd/PEWSBI/datafiles/cluster_simulation.hdf \
       /home/mrtodd/PEWSBI/neural_nets/neural_network_1d_$1.pickle \
       $1 \
       /home/mrtodd/PEWSBI/code/simulate/injection1d.ini \
       --noisefile /home/mrtodd/PEWSBI/code/simulate/noise.hdf \
       --add-noise \
       --monitor-rate 1000 \
       --verbose \
       --logfile /home/mrtodd/PEWSBI/logs/cluster_training.log
