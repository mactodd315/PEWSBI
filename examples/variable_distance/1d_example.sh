#!/bin/bash

#use sbi_env environment
source ~/miniconda3/bin/activate sbi_env

#generate injection parameters file
# pycbc_create_injections --verbose \
#     --config-files ~/PEWSBI/examples/variable_distance/injection1d.ini \
#     --ninjections 100 \
#     --seed 0 \
#     --output-file ~/PEWSBI/examples/variable_distance/injection1d.hdf \
#     --variable-params-section variable_params \
#     --static-params-section static_params \
#     --dist-section prior \
#     --force

# #generate simulation data
# python ~/PEWSBI/bin/simulate_data.py \
#     --verbose \
#     --signal-length 1200 \
#     --monitor-rate 50 \
#     --injfile ~/PEWSBI/examples/variable_distance/injection1d.hdf \
#     --output_file ~/PEWSBI/examples/variable_distance/training_simulations.hdf
    
#train neural_network
python ~/PEWSBI/bin/train_neural_network.py \
   --simfile ~/PEWSBI/examples/variable_distance/training_simulations.hdf \
   --output-file ~/PEWSBI/examples/variable_distance/neural_network_1d.pickle \
   --n-simulations 100 \
   --inifile ~/PEWSBI/examples/variable_distance/injection1d.ini \
   --noisefile ~/PEWSBI/noise/noise.hdf \
   --add-noise \
   --monitor-rate 20 \
   
# #sample posterior estimate with generated 'observations'
# pycbc_create_injections --verbose \
#     --config-files ~/PEWSBI/examples/variable_distance/injection1d.ini \
#     --ninjections 10 \
#     --seed 0 \
#     --output-file ~/PEWSBI/examples/variable_distance/injection1d.hdf \
#     --variable-params-section variable_params \
#     --static-params-section static_params \
#     --dist-section prior \
#     --force
    
# python ~/PEWSBI/bin/simulate_data.py \
#     --verbose \
#     --signal-length 1200 \
#     --monitor-rate 50 \
#     --injfile ~/PEWSBI/examples/variable_distance/injection1d.hdf \
#     --output_file ~/PEWSBI/examples/variable_distance/observation_simulations.hdf
    
# python ~/PEWSBI/bin/sample.py \
#     --neural-net ~/PEWSBI/examples/variable_distance/neural_network_1d.pickle \
#     --output-file ~/PEWSBI/examples/variable_distance/posterior_1d.hdf \
#     --observation-file ~/PEWSBI/examples/variable_distance/observation_simulations.hdf \
#     --config-file  ~/PEWSBI/examples/variable_distance/injection1d.ini \
#     --sample-parameter 'distance' \
#     --training-number 1000 \
#     --observation-num 10 \
#     --n-samples 10000 \
#     --n-bins 300 \
#     -v
    
#plot pptest of posterior along with posterior estimate of first posterior

# python ~/PEWSBI/bin/plot.py \
#     --posterior ~/PEWSBI/examples/variable_distance/posterior_1d.hdf \
#     --output ~/PEWSBI/examples/variable_distance/pptest.png \
#     --plot-content 'pptest' \
#     --config-file  ~/PEWSBI/examples/variable_distance/injection1d.ini \
#     --sample-parameter 'distance' \
#     --num-posteriors 10 \
#     --plot-title 'PPTEST-distance for TrainSim:1000 ObsSim:10'
    
# python ~/PEWSBI/bin/plot.py \
#     --posterior ~/PEWSBI/examples/variable_distance/posterior_1d.hdf \
#     --output ~/PEWSBI/examples/variable_distance/posterior0.png \
#     --plot-content 'posterior' \
#     --config-file  ~/PEWSBI/examples/variable_distance/injection1d.ini \
#     --sample-parameter 'distance' \
#     --posterior-index 0 \
#     --plot-true \
#     --plot-title 'Posterior Estimate 0 for TrainSim:1000 ObsSim:10'
    