# In this example, we run the workflow generation script and immediately
# submit it to the compute cluster

# The env is modified only only so that the executables in the bin
# can be executed
export PATH=$PATH:$PWD/../../../bin

python pewsbi.py \
--workflow-name test \
--config-files pewsbi.ini \
--input-file injection.ini \
--training-parameters 'total_mass' \
--ninjections 1000 \
--submit-now