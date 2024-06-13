#! /bin/bash
export PATH=$PATH:/home/mactodd315/Projects/machine_learning_sbi/PEWSBI/bin

# generate injection parameters file
pycbc_create_injections --verbose \
    --config-files training_injections.ini \
    --ninjections $1 \
    --seed 0 \
    --output-file gw150914_training_injections.hdf \
    --variable-params-section variable_params \
    --static-params-section static_params \
    --dist-section prior \
    --force

# generate simulation data
simulate_data \
    --verbose \
    --signal-length 2048\
    --delta-f 512 \
    --monitor-rate 500 \
    --epoch 1126259459 \
    --injection-file gw150914_training_injections.hdf \
    --output-file gw150914_training_samples.hdf \
    --DNRF 5e20 \
    --timing 
