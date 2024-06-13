#! /bin/bash
export PATH=$PATH:/home/mactodd315/Projects/machine_learning_sbi/PEWSBI/bin

# bash generate_training_samples.sh 100000

# # bash generate_noise.sh

# bash train_neural_net_both.sh 250000

# bash train_neural_net_hide_dist.sh 250000

# bash sample_both.sh

# bash sample_hide_dist.sh

bash run_pycbc_inference.sh

bash plot_pycbc_posterior.sh

# compare_posteriors --input-file samples_pycbc.hdf marg_150914.hdf 
