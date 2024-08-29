# In this example, we run the workflow generation script and immediately
# submit it to the compute cluster

# The env is modified only only so that the executables in the bin
# can be executed
export PATH=$PATH:$PWD/../../bin

cd $1

python ../ml_inference.py \
	--workflow-name ml_inference \
	--config-files ../ml_inference.ini \
    --observation-injection /home/mrtodd/PEWSBI/examples/workflow_comparison/gw150914_injection.hdf \
	--working-folder $1 \
	--n-simulations 10 \
    --n-trainings 10 \
    --noise-file /home/mrtodd/PEWSBI/examples/workflow_comparison/gw150914_noise.hdf \
	--submit-now

cd ..