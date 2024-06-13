#! /bin/bash
export PATH=$PATH:/home/mactodd315/Projects/machine_learning_sbi/PEWSBI/bin

generate_noise --verbose \
    --sample-rate  512 \
    --strain-high-pass 5 \
    --fake-strain aLIGOZeroDetHighPower \
    --fake-strain-seed 1234 \
    --fake-strain-sample-rate 512 \
    --fake-strain-flow 10 \
    --gps-start-time 1126253200 \
    --gps-end-time 1126363592 \
    --output-file gw150914_noise.hdf