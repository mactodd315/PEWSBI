#!/bin/bash

source ~/miniconda3/bin/activate sbi_env

python /home/mrtodd/PEWSBI/code/plot/plot.py \
	/home/mrtodd/PEWSBI/code/sample/posteriors.hdf \
        /home/mrtodd/PEWSBI/code/plot/pp_plot.png \
        'pptest' \
        /home/mrtodd/PEWSBI/code/simulate/injection.ini \
        'distance' \
        --num-posteriors 1000 \
        -v
