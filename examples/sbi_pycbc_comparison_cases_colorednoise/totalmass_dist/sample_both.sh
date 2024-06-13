#! /bin/bash
export PATH=$PATH:/home/mactodd315/Projects/machine_learning_sbi/PEWSBI/bin

# first we want to create an injection file with gw150914 in it
pycbc_create_injections --verbose \
    --config-files gw150914_injection.ini \
    --ninjections 1 \
    --seed 0 \
    --output-file gw150914_injection.hdf \
    --variable-params-section variable_params \
    --static-params-section static_params \
    --dist-section prior \
    --force

sample --verbose \
    --neural-net both_learned/gw150914_neural_net.pickle \
    --sample-parameters 'total_mass' 'distance'\
    --output-file both_learned/samples_sbi.hdf \
    --observation-file gw150914_injection.hdf \
    --IFOs H1 \
    --channel-name H1:sim-strain \
    --injection-file gw150914_injection.hdf \
    --DNRF 5e20 \
    --sample-rate  512 \
    --strain-high-pass 5 \
    --fake-strain aLIGOZeroDetHighPower \
    --fake-strain-seed 1234 \
    --fake-strain-sample-rate 512 \
    --fake-strain-flow 10 \
    --gps-start-time 1126259459 \
    --gps-end-time 1126259463 \
    --write-pycbc-posterior both_learned/samples_pycbc.hdf

# now we also want to run pycbc inference for comparison
# OMP_NUM_THREADS=1 pycbc_inference \
#     --config-file marg_time_injection.ini \
#     --nprocesses 2 \
#     --processing-scheme mkl \
#     --output-file marg_150914.hdf \
#     --seed 0 \
#     --force \
#     --verbose
