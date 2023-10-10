#!/bin/bash

#use sbi_env environment
source ~/Projects/machine_learning_sbi/sbi_env/bin/activate

python ~/Projects/machine_learning_sbi/PEWSBI/bin/plot.py \
    --posteriors-folder ~/Projects/machine_learning_sbi/PEWSBI/examples/no_noise/posteriors/ \
    --output ~/Projects/machine_learning_sbi/PEWSBI/examples/no_noise/plots/tracesLR1e-5_BS1000.hdf \
    --plot-content 'pptest' \
    --config-file  ~/Projects/machine_learning_sbi/PEWSBI/examples/no_noise/injection1d.ini \
    --sample-parameter 'distance' \
    --num-posteriors 1000 