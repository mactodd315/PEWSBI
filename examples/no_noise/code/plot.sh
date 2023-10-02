#!/bin/bash

#use sbi_env environment
source ~/Projects/machine_learning_sbi/sbi_env/bin/activate

python ~/Projects/machine_learning_sbi/PEWSBI/bin/plot.py \
    --posteriors-folder ~/Projects/machine_learning_sbi/PEWSBI/examples/no_noise/posteriors_TBP/ \
    --plot-folder ~/Projects/machine_learning_sbi/PEWSBI/examples/no_noise/plots \
    --plot-content 'pptest' \
    --config-file  ~/Projects/machine_learning_sbi/PEWSBI/examples/no_noise/injection1d.ini \
    --sample-parameter 'distance' \
    --num-posteriors 50

python ~/Projects/machine_learning_sbi/PEWSBI/bin/plot.py \
    --posteriors-folder ~/Projects/machine_learning_sbi/PEWSBI/examples/no_noise/posteriors_TBP/ \
    --plot-folder ~/Projects/machine_learning_sbi/PEWSBI/examples/no_noise/plots \
    --plot-content 'posterior' \
    --config-file  ~/Projects/machine_learning_sbi/PEWSBI/examples/no_noise/injection1d.ini \
    --sample-parameter 'distance' \
    --posterior-index 0 \
    --plot-true