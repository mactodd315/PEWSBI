#! /bin/bash
export PATH=$PATH:/home/mactodd315/Projects/machine_learning_sbi/PEWSBI/bin

train_neural_network --verbose \
    --output-file both_learned/gw150914_neural_net.pickle \
    --input-file gw150914_training_samples.hdf \
    --training-parameters 'total_mass' 'distance' \
    --n-simulations $1 \
    --add-noise ../gw150914_noise.hdf \
    --DNRF 5e20 \
    --IFO H1  \
    --batch-size 500 \
    --stop-after-epochs 20 \
    --learning-rate 1e-4 \
    --show-summary
