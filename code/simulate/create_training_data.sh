#!/bin/bash

source /home/mrtodd/miniconda3/bin/activate sbi_env

bash /home/mrtodd/PEWSBI/code/simulate/create_injection.sh \
       	    /home/mrtodd/PEWSBI/code/simulate/injection.ini \
	    10000 \
	    /home/mrtodd/PEWSBI/code/simulate/injection.hdf

python /home/mrtodd/PEWSBI/code/simulate/simulate_data.py \
        /home/mrtodd/PEWSBI/code/simulate/injection.hdf \
        /home/mrtodd/PEWSBI/code/simulate/training_data.hdf \
        -v
