# In this example, we run the workflow generation script and immediately
# submit it to the compute cluster

# The env is modified only only so that the executables in the bin
# can be executed
export PATH=$PATH:$PWD/../../bin

python ml_inference.py \
	--workflow-name ml_inference \
	--config-files ml_inference.ini \
	--working-folder $1 \
	--n-simulations 10 \
    --n-trainings 10 \
	--submit-now
