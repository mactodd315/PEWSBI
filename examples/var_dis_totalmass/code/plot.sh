#!/bin/bash

#use sbi_env environment
source ~/miniconda3/bin/activate sbi_env

# python ~/PEWSBI/bin/plot.py \
#     --posteriors-folder ~/PEWSBI/examples/var_dis_totalmass/posteriors/ \
#     --plot-folder ~/PEWSBI/examples/var_dis_totalmass/plots \
#     --plot-content 'pptest' \
#     --config-file  ~/PEWSBI/examples/var_dis_totalmass/code/injection2d.ini \
#     --sample-parameters 'distance,mass1' \
#     --num-posteriors 100

python ~/PEWSBI/bin/plot.py \
    --posteriors-folder ~/PEWSBI/examples/var_dis_totalmass/posteriors/ \
    --plot-folder ~/PEWSBI/examples/var_dis_totalmass/plots \
    --plot-content 'posterior' \
    --config-file  ~/PEWSBI/examples/var_dis_totalmass/code/injection12.ini \
    --sample-parameter 'distance' \
    --posterior-index 0 \
    --plot-true