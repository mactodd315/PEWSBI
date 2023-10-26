#!/bin/bash

#use sbi_env environment
source ~/Projects/machine_learning_sbi/sbi_env/bin/activate

# python ~/Projects/machine_learning_sbi/PEWSBI/bin/plot.py \
#     --samples-folder  ~/Projects/machine_learning_sbi/PEWSBI/examples/var_dis_totalmass/samples/ \
#     --plot-folder  ~/Projects/machine_learning_sbi/PEWSBI/examples/var_dis_totalmass/plots \
#     --plot-content 'pptest' \
#     --config-file   ~/Projects/machine_learning_sbi/PEWSBI/examples/var_dis_totalmass/code/injection2d.ini \
#     --sample-parameters 'distance,mass1' \
#     --num-posteriors 100

python ~/Projects/machine_learning_sbi/PEWSBI/bin/plot.py \
    --samples-folder ~/Projects/machine_learning_sbi/PEWSBI/examples/var_dis_totalmass/samples/ \
    --plot-folder ~/Projects/machine_learning_sbi/PEWSBI/examples/var_dis_totalmass/plots \
    --plot-content 'posterior' \
    --config-file  ~/Projects/machine_learning_sbi/PEWSBI/examples/var_dis_totalmass/code/injection2d.ini \
    --sample-parameter 'distance' \
    --posterior-index 0 \
    --plot-true