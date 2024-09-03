#!/bin/bash

cd $1

public_html=/home/mrtodd/public_html/ml_pycbc_comparisons/$1

if [ -e $public_html ]; then 

IFS="/"
    for file in /home/mrtodd/PEWSBI/examples/workflow_comparison/$1/*/*.png
    do
    IFS="/"
	read -a locs <<< $file
    name=$public_html/${locs[-2]}.png
	IFS=" "
    cp $file name
    done
IFS=" "
fi
