#!/bin/bash

source ~/miniconda3/bin/activate sbi_env

python plot/plot.py sample/posteriors.hdf \
                    plot/pp_plot.png \
                    'pptest' \
                    --num-posteriors 10 \
                    -v