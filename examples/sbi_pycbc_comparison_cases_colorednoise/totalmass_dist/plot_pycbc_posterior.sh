#! /bin/bash
export PATH=$PATH:/home/mactodd315/Projects/machine_learning_sbi/PEWSBI/bin

# pycbc_inference_plot_posterior \
#     --input-file  both_learned/pycbc_inference.hdf both_learned/samples_pycbc.hdf \
#     --output-file both_learned/compare_posteriors.png \
#     --parameters  total_mass distance\
#     --expected-parameters total_mass:71 distance:410\
#     --plot-contours

pycbc_inference_plot_posterior \
    --input-file  hiding_dist/pycbc_inference.hdf hiding_dist/samples_pycbc.hdf \
    --output-file hiding_dist/compare_posteriors.png \
    --parameters  total_mass \
    --expected-parameters total_mass:71 \
    --plot-contours