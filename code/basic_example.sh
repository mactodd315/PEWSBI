#!/bin/bash
source ~/miniconda3/bin/activate sbi_env

bash simulate/create_injection.sh simulate/injection.ini 11 simulate/injection.hdf

python simulate/simulate_data.py simulate/injection.hdf simulate/output.hdf

python train/train_neural_network.py simulate/output.hdf \
                    train/test_nn.pickle \
                    10 \
                    simulate/injection.hdf \
                    simulate/injection.ini \
                    --noisefile simulate/noise.hdf \
                    --add-noise

python sample/sample.py train/test_nn.pickle \
                    sample/test_posterior.hdf \
                    simulate/output.hdf \
                    --observation-num 10 

python plot/plot.py sample/test_posterior.hdf \
                    plot/test_plot.png \
                    --plot-true 
