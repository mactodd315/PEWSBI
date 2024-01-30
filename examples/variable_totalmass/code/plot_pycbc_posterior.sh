#!/bin/bash

#use sbi_env environment
source ~/Projects/machine_learning_sbi/sbi_env/bin/activate # change to your env dir.

current_folder="/home/mactodd315/Projects/machine_learning_sbi/PEWSBI"
example_folder="/examples/variable_totalmass"

INPUT_FILE=$current_folder$example_folder/samples/pycbc_posterior0.hdf
OUTPUT_FILE=$current_folder$example_folder/plots/pycbc_posterior0.png
    
pycbc_inference_plot_posterior \
    --iteration 0 \
    --input-file ${INPUT_FILE} \
    --output-file ${OUTPUT_FILE} \
    --parameters  total_mass \
    --expected-parameters total_mass:138.13