#!/bin/bash

#use sbi_env environment
source ~/Projects/machine_learning_sbi/sbi_env/bin/activate

# python ~/Projects/machine_learning_sbi/PEWSBI/bin/plot.py \
#     --samples-folder ~/Projects/machine_learning_sbi/PEWSBI/examples/variable_distance/posteriors/ \
#     --plot-folder ~/Projects/machine_learning_sbi/PEWSBI/examples/variable_distance/plots \
#     --plot-content 'pptest' \
#     --config-file  ~/Projects/machine_learning_sbi/PEWSBI/examples/variable_distance/code/injection1d.ini \
#     --sample-parameter 'distance' \
#     --num-posteriors 100

python ~/Projects/machine_learning_sbi/PEWSBI/bin/plot.py \
    --samples-folder ~/Projects/machine_learning_sbi/PEWSBI/examples/variable_distance/posteriors/ \
    --plot-folder ~/Projects/machine_learning_sbi/PEWSBI/examples/variable_distance/plots \
    --plot-content 'posterior' \
    --config-file  ~/Projects/machine_learning_sbi/PEWSBI/examples/variable_distance/code/injection1d.ini \
    --sample-parameter 'mass1' \
    --posterior-index 0 \
    --plot-true