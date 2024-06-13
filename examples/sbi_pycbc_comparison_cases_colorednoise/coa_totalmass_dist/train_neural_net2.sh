#! /bin/bash
export PATH=$PATH:/home/mactodd315/Projects/machine_learning_sbi/PEWSBI/bin

train_neural_network --verbose \
    --output-file gw150914_neural_net_withcoa.pickle \
    --input-file gw150914_training_samples.hdf \
    --training-parameters 'total_mass' 'distance' 'coa_phase'\
    --n-simulations $1 \
    --add-noise ../gw150914_noise.hdf \
    --DNRF 5e20 \
    --IFO H1  \
    --batch-size 500 \
    --stop-after-epochs 20 \
    --learning-rate 1e-4 \
    --show-summary
