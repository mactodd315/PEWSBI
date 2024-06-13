#! /bin/bash
export PATH=$PATH:/home/mactodd315/Projects/machine_learning_sbi/PEWSBI/bin

pycbc_inference_plot_posterior \
    --input-file  marg_150914.hdf samples_pycbc.hdf \
    --output-file sbi_gw150914_posterior.png \
    --parameters  total_mass distance\
    --expected-parameters total_mass:71 distance:410\
    --plot-contours