#!/bin/bash
pycbc_create_injections --verbose \
        --config-files $1 \
        --ninjections $2 \
        --seed 0 \
	--output-file $3 \
        --variable-params-section variable_params \
        --static-params-section static_params \
        --dist-section prior \
        --force
