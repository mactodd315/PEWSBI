#!/bin/bash

#use sbi_env environment
source ~/Projects/machine_learning_sbi/sbi_env/bin/activate

# #generate injection parameters file
# pycbc_create_injections --verbose \
#     --config-files ~/Projects/machine_learning_sbi/PEWSBI/examples/no_noise/injection1d.ini \
#     --ninjections 1000 \
#     --seed 0 \
#     --output-file ~/Projects/machine_learning_sbi/PEWSBI/examples/no_noise/injection1d.hdf \
#     --variable-params-section variable_params \
#     --static-params-section static_params \
#     --dist-section prior \
#     --force

# #generate simulation data
# python ~/Projects/machine_learning_sbi/PEWSBI/bin/simulate_data.py \
#     --verbose \
#     --signal-length 2048 \
#     --delta-f 512 \
#     --monitor-rate 100 \
#     --injfile ~/Projects/machine_learning_sbi/PEWSBI/examples/no_noise/injection1d.hdf \
#     --output_file ~/Projects/machine_learning_sbi/PEWSBI/examples/no_noise/training_simulations1e3.hdf

# #generate noise
# python ~/Projects/machine_learning_sbi/PEWSBI/bin/generate_noise.py \
#     --output-file ~/Projects/machine_learning_sbi/PEWSBI/examples/no_noise/noise.hdf \
#     --ini-file ~/Projects/machine_learning_sbi/PEWSBI/examples/no_noise/injection1d.ini \
#     --verbose 

#train neural_network
# python ~/Projects/machine_learning_sbi/PEWSBI/bin/train_neural_network.py \
#    --simfile ~/Projects/machine_learning_sbi/PEWSBI/examples/no_noise/training_simulations1e3.hdf \
#    --output-file ~/Projects/machine_learning_sbi/PEWSBI/examples/no_noise/neural_network_1d_no_noise_1e3_LR_1e-10_BS_1000.pickle \
#    --n-simulations 1000 \
#    --inifile ~/Projects/machine_learning_sbi/PEWSBI/examples/no_noise/injection1d.ini \
#    --noisefile ~/Projects/machine_learning_sbi/PEWSBI/noise/noise.hdf \
#    --add-noise \
#    --monitor-rate 100 \
#    --batch-size 1000 \
#    --learning-rate 1e-10 \
#    --logfile ~/Projects/machine_learning_sbi/PEWSBI/examples/no_noise/traininglog.log \
#    --verbose

#  #sample posterior estimate with generated 'observations'
#  pycbc_create_injections --verbose \
#      --config-files ~/Projects/machine_learning_sbi/PEWSBI/examples/no_noise/injection1d.ini \
#      --ninjections 50 \
#      --seed 0 \
#      --output-file ~/Projects/machine_learning_sbi/PEWSBI/examples/no_noise/injection1d.hdf \
#      --variable-params-section variable_params \
#      --static-params-section static_params \
#      --dist-section prior \
#      --force

# python ~/Projects/machine_learning_sbi/PEWSBI/bin/simulate_data.py \
#      --verbose \
#      --signal-length 2048 \
#      --delta-f 512 \
#      --monitor-rate 10 \
#      --injfile ~/Projects/machine_learning_sbi/PEWSBI/examples/no_noise/injection1d.hdf \
#      --output_file ~/Projects/machine_learning_sbi/PEWSBI/examples/no_noise/observation_simulations_5e1.hdf

# sample from neuralnets and make posteriors    
python ~/Projects/machine_learning_sbi/PEWSBI/bin/sample.py \
    --neural-net ~/Projects/machine_learning_sbi/PEWSBI/examples/no_noise/neural_nets/neural_network_1d_no_noise_1e3_LR_1e-10_BS_1000.pickle \
    --output-file ~/Projects/machine_learning_sbi/PEWSBI/examples/no_noise/posteriors/posterior_1d_LR_1e-10_BS_1000.hdf \
    --observation-file ~/Projects/machine_learning_sbi/PEWSBI/examples/no_noise/observation_simulations_5e1.hdf \
    --config-file  ~/Projects/machine_learning_sbi/PEWSBI/examples/no_noise/injection1d.ini \
    --sample-parameter 'distance' \
    --training-number 1000 \
    --observation-num 50 \
    --n-samples 10000 \
    --n-bins 300 \
    -v

# plot pptest of posterior along with posterior estimate of first posterior

# python ~/Projects/machine_learning_sbi/PEWSBI/bin/plot.py \
#     --posterior ~/Projects/machine_learning_sbi/PEWSBI/examples/no_noise/posteriors/posterior_1d.hdf \
#     --output ~/Projects/machine_learning_sbi/PEWSBI/examples/no_noise/plots/traces.hdf \
#     --plot-content 'pptest' \
#     --config-file  ~/Projects/machine_learning_sbi/PEWSBI/examples/no_noise/injection1d.ini \
#     --sample-parameter 'distance' \
#     --num-posteriors 1000 
python ~/Projects/machine_learning_sbi/PEWSBI/bin/plot.py \
    --posterior ~/Projects/machine_learning_sbi/PEWSBI/examples/no_noise/posteriors/posterior_1d_LR_1e-10_BS_1000.hdf \
    --output ~/Projects/machine_learning_sbi/PEWSBI/examples/no_noise/plots/tracesLR1E-10BS1000.hdf \
    --plot-content 'pptest' \
    --config-file  ~/Projects/machine_learning_sbi/PEWSBI/examples/no_noise/injection1d.ini \
    --sample-parameter 'distance' \
    --num-posteriors 1000 
# python ~/Projects/machine_learning_sbi/PEWSBI/bin/plot.py \
#     --posterior ~/Projects/machine_learning_sbi/PEWSBI/examples/no_noise/posteriors/posterior_1d_LR_1e-6.hdf \
#     --output ~/Projects/machine_learning_sbi/PEWSBI/examples/no_noise/plots/tracesLR1e-6.hdf \
#     --plot-content 'pptest' \
#     --config-file  ~/Projects/machine_learning_sbi/PEWSBI/examples/no_noise/injection1d.ini \
#     --sample-parameter 'distance' \
#     --num-posteriors 1000 \

# python ~/Projects/machine_learning_sbi/PEWSBI/bin/plot.py \
#     --posterior ~/Projects/machine_learning_sbi/PEWSBI/examples/no_noise/posterior_1d.hdf \
#     --output ~/Projects/machine_learning_sbi/PEWSBI/examples/no_noise/posterior0_1e3_no_noise_DTP.png \
#     --plot-content 'posterior' \
#     --config-file  ~/Projects/machine_learning_sbi/PEWSBI/examples/no_noise/injection1d.ini \
#     --sample-parameter 'distance' \
#     --posterior-index 0 \
#     --plot-true \
#     --plot-title 'NoNoise Posterior Estimate 0 for TrainSim:1000'