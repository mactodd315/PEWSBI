#!/bin/bash

cd $1

public_html=/home/mrtodd/public_html/ml_pycbc_comparisons/$1

if [ -e "$public_html" ]; then 
    
    cp /home/mrtodd/PEWSBI/examples/workflow_comparison/$1/*/*.png \
        -t $public_html

else 
    mkdir $public_html
    cp /home/mrtodd/PEWSBI/examples/workflow_comparison/$1/*/*.png \
        -t $public_html

fi