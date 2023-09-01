#!/bin/bash

source /home/mrtodd/miniconda3/bin/activate sbi_env

bash /home/mrtodd/PEWSBI/code/simulate/create_injection.sh \
            /home/mrtodd/PEWSBI/code/simulate/injection1d.ini \
            $2 \
            /home/mrtodd/PEWSBI/datafiles/subfiles/local_injection$1.hdf

python  /home/mrtodd/PEWSBI/code/simulate/simulate_data.py \
        /home/mrtodd/PEWSBI/datafiles/subfiles/local_injection$1.hdf \
        /home/mrtodd/PEWSBI/datafiles/subfiles/local_simulation$1.hdf \
        --signal-length 1200 \
        --monitor-rate 40 \
        --pool-number 1 \
        -v
        
