#! /bin/bash
export PATH=$PATH:/home/mactodd315/Projects/machine_learning_sbi/PEWSBI/bin

# bash generate_training_samples.sh 100000

# bash generate_noise.sh

# bash train_neural_net.sh 250000


# bash train_neural_net2.sh 250000

# bash sample_gw150914_injection.sh

# bash sample_gw150914_injection2.sh

# bash run_pycbc_inference.sh

bash plot_pycbc_posterior.sh

# compare_posteriors --input-file samples_pycbc.hdf marg_150914.hdf 
