#!/bin/bash

source /home/mrtodd/miniconda3/bin/activate sbi_env

bash /home/mrtodd/PEWSBI/code/simulate/create_injection.sh \
            /home/mrtodd/PEWSBI/code/simulate/injection.ini \
            100 \
            /home/mrtodd/PEWSBI/code/simulate/test_injection.hdf

python  /home/mrtodd/PEWSBI/code/simulate/simulate_data.py \
        /home/mrtodd/PEWSBI/code/simulate/test_injection.hdf \
        /home/mrtodd/PEWSBI/code/simulate/test_training_data.hdf \
        --signal-length 1200 \
        --monitor-rate 40 \
        -v
