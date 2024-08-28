#! /bin/bash
export PATH=$PATH:/home/mactodd315/Projects/machine_learning_sbi/PEWSBI/bin

generate_noise --verbose \
    --sample-rate  512 \
    --strain-high-pass 5 \
    --fake-strain aLIGOEarlyLowSensitivityP1200087 \
    --fake-strain-seed 1234 \
    --fake-strain-sample-rate 2048 \
    --fake-strain-flow 10 \
    --gps-start-time 1126253200 \
    --gps-end-time 1126363592 \
    --output-file gw150914_noise.hdf