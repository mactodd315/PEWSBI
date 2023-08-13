#!/bin/bash
source ~/miniconda3/bin/activate sbi_env

bash simulate/create_injection.sh simulate/injection.ini 100 simulate/injection.hdf

python simulate/simulate_data.py simulate/injection.hdf \
                    simulate/training_data.hdf \
                    -v

python train/train_neural_network.py simulate/training_data.hdf \
                    train/neural_network.pickle \
                    100 \
                    simulate/injection.hdf \
                    simulate/injection.ini \
                    --noisefile simulate/noise.hdf \
                    --add-noise \
                    -v
                    
bash simulate/create_injection.sh simulate/injection.ini 10 simulate/injection.hdf

python simulate/simulate_data.py simulate/injection.hdf simulate/simulations.hdf -v

python sample/sample.py train/neural_network.pickle \
                    sample/posteriors.hdf \
                    simulate/simulations.hdf \
                    --observation-num 10 \
                    -v

python plot/plot.py sample/posteriors.hdf \
                    plot/pp_plot.png \
                    'pptest' \
                    --num-posteriors 10 \
                    -v
                    
