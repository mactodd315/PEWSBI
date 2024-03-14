#! /bin/bash
export PATH=$PATH:$PWD/../../PEWSBI/bin


### Do marginalized time pycbc inference first ###
pycbc_create_injections --verbose \
    --config-files gw150914_injection.ini \
    --ninjections 1 \
    --seed 0 \
    --output-file gw150914_injection.hdf \
    --variable-params-section variable_params \
    --static-params-section static_params \
    --dist-section prior \
    --force

pycbc_condition_strain \
    --fake-strain aLIGOZeroDetHighPower \
    --fake-strain-seed 1234 \
    --fake-strain-flow 10 \
    --sample-rate 2048 \
    --gps-start-time 1126259456 \
    --gps-end-time 1126259468 \
    --channel-name H1:SIMULATED_STRAIN \
    --injection-file gw150914_injection.hdf \
    --output-strain-file H1:SIMULATED_STRAIN-1126259452-16.hdf 

OMP_NUM_THREADS=1 pycbc_inference \
    --config-file margtime.ini \
    --nprocesses 2 \
    --processing-scheme mkl \
    --output-file marg_150914.hdf \
    --seed 0 \
    --force \
    --verbose

# This reconstructs any marginalized parameters
OMP_NUM_THREADS=1 pycbc_inference_model_stats \
    --input-file marg_150914.hdf \
    --output-file demarg_150914.hdf \
    --nprocesses 1 \
    --reconstruct-parameters \
    --force \
    --verbose
###########################################################

###     Now run sbi_inference procedure      ###

# generate injection parameters file
pycbc_create_injections --verbose \
    --config-files margtime.ini \
    --ninjections 1000000 \
    --seed 0 \
    --output-file gw150914_training_injections.hdf \
    --variable-params-section variable_params \
    --static-params-section static_params \
    --dist-section prior \
    --force

# generate simulation data, signa-length should match
# (gps-end minus gps-start)*sample_rate in condition
# strain above.
simulate_data \
    --verbose \
    --signal-length '12*2048'\
    --delta-f 2048 \
    --monitor-rate 500 \
    --epoch 1126259456 \
    --DNRF '1e18' \
    --injfile gw150914_training_injections.hdf \
    --output-file gw150914_training_samples.hdf

train_neural_network \
 --training-parameters mass1 mass2 \
 --simulation-file gw150914_training_samples.hdf \
 --output-file gw150914_trained_nn.pickle \
 --n-simulations 100000 \
 --add-noise \
 --noise-file noise.hdf \
 --DNRF '1e18' \
 --show-summary \
 --batch-size 1000 \
 --learning-rate .00002 \
 -v

sample \
    --neural-net gw150914_trained_nn.pickle \
    --output-file sbi_gw150914_samples.hdf \
    --observation-file  H1:SIMULATED_STRAIN-1126259452-16.hdf \
    --strain-channel 'H1:SIMULATED_STRAIN' \
    --sample-parameters 'mass1' 'mass2' \
    --observation-num 1 \
    --n-samples 10000 \
    --n-bins 500 \
    --write-pycbc-posterior sbi_gw150914_posterior.hdf \
    -v

pycbc_inference_plot_posterior \
    --input-file 'demarg_150914.hdf' 'sbi_gw150914_posterior.hdf' \
    --output-file comparison_plot_150914.png \
    --parameters "primary_mass(mass1,mass2):mass1" \
                    "secondary_mass(mass1,mass2):mass2" \
    --expected-parameters "mass1:37.0" "mass2:32.0" \
    --expected-parameters-color 'red' \
    --plot-contours

