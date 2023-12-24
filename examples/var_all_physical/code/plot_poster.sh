#!/bin/bash

#use sbi_env environment
source ~/miniconda3/bin/activate sbi_env

current_folder="/home/mrtodd/PEWSBI"
example_folder="/examples/var_all_physical"
INPUT_FILE=$current_folder$example_folder/samples/post1.hdf
OUTPUT_FILE=$current_folder$example_folder/plots/post0_tm_mr.png
    
pycbc_inference_plot_posterior \
    --iteration 0 \
    --input-file ${INPUT_FILE} \
    --output-file ${OUTPUT_FILE} \
    --parameters  total_mass mass_ratio