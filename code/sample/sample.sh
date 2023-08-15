#!/bin/bash

source ~/miniconda3/bin/activate sbi_env

bash /home/mrtodd/PEWSBI/code/simulate/create_injection.sh \
	/home/mrtodd/PEWSBI/code/simulate/injection.ini \
	1000 \
	/home/mrtodd/PEWSBI/code/simulate/simulation_injection.hdf

python /home/mrtodd/PEWSBI/code/simulate/simulate_data.py \
	/home/mrtodd/PEWSBI/code/simulate/simulation_injection.hdf \
	/home/mrtodd/PEWSBI/code/simulate/simulations.hdf \
	--signal-length 1200 \
	-v

python /home/mrtodd/PEWSBI/code/sample/sample.py \
	/home/mrtodd/PEWSBI/code/train/neural_network.pickle \
        /home/mrtodd/PEWSBI/code/sample/posteriors.hdf \
        /home/mrtodd/PEWSBI/code/simulate/simulations.hdf \
        /home/mrtodd/PEWSBI/code/simulate/injection.ini \
        'distance' \
        --observation-num 1000 \
        -v
