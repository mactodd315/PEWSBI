#!/bin/bash

bash create_injection.sh injection.ini 10000 injection.hdf

python simulate_data.py injection.hdf \
                    training_data.hdf \
                    -v
