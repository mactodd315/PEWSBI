#!/bin/bash

source /home/mrtodd/miniconda3/bin/activate sbi_env

bash /home/mrtodd/PEWSBI/code/simulate/create_injection.sh \
            /home/mrtodd/PEWSBI/code/simulate/injection1d.ini \
            $1 \
            /home/mrtodd/PEWSBI/datafiles/local_injection.hdf

python  /home/mrtodd/PEWSBI/bin/simulate_data.py \
        /home/mrtodd/PEWSBI/datafiles/local_injection.hdf \
        /home/mrtodd/PEWSBI/datafiles/local_simulation.hdf \
        --signal-length 1200 \
        --monitor-rate 40 \
        --pool-number 1 \
        -v
        
