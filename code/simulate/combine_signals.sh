#!/bin/bash

source /home/mrtodd/miniconda3/bin/activate sbi_env

python /home/mrtodd/PEWSBI/code/simulate/combine_signals.py \
       /home/mrtodd/PEWSBI/datafiles/cluster_simulation \
       /home/mrtodd/PEWSBI/datafiles/injection \
       /home/mrtodd/PEWSBI/datafiles/cluster_simulation.hdf \
       /home/mrtodd/PEWSBI/datafiles/injection.hdf \
       $1