#!/bin/bash

source /home/mrtodd/miniconda3/bin/activate sbi_env

python /home/mrtodd/PEWSBI/code/simulate/combine_signals.py \
       /home/mrtodd/PEWSBI/datafiles/subfiles/local_simulation \
       /home/mrtodd/PEWSBI/datafiles/subfiles/local_injection \
       /home/mrtodd/PEWSBI/datafiles/local_simulation.hdf \
       /home/mrtodd/PEWSBI/datafiles/local_injection.hdf \
       $1 \
       '100,1200'

