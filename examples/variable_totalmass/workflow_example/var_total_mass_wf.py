#!/bin/env python
""" A minimal ml_sbi workflow example """

import os, argparse
import pycbc
import pycbc.workflow as wf

parser = argparse.ArgumentParser(description=__doc__[1:])
parser.add_argument('--verbose', '-v', action='count')
parser.add_argument('--ninjections')
parser.add_argument('--input-file')
parser.add_argument('--training-parameters')
wf.add_workflow_command_line_group(parser)
wf.add_workflow_settings_cli(parser)
args = parser.parse_args()

# Workflow init ###############
pycbc.init_logging(args.verbose)

input_file =  wf.resolve_url_to_file(args.input_file)

workflow = wf.Workflow(args, 'cont')
################################


# Create Injection .hdf file ###
exe1 = wf.Executable(workflow.cp, 'create_injections')

node1 = exe1.create_node()

node1.add_input_opt('--config-files', input_file)
node1.add_opt('--ninjections', args.ninjections)
injfile = node1.new_output_file_opt(workflow.analysis_time, '.hdf',
                                '--output-file', tags=['1'])

workflow += node1
################################


# Write TimeSeries from Inj Set #
exe2 = wf.Executable(workflow.cp, 'write_sims')

node2 = exe2.create_node()
node2.add_input_opt('--injfile', injfile)
simulations = node2.new_output_file_opt(workflow.analysis_time, '.hdf',
        '--output-file', tags=['2'])
workflow += node2
################################


# Generate Noise ##############
exe3 = wf.Executable(workflow.cp, 'make_noise')

node3 = exe3.create_node()
node3.add_input_opt('--ini-file', input_file)
noise = node3.new_output_file_opt(workflow.analysis_time, '.hdf',
        '--output-file', tags=['3'])
workflow += node3
###############################


# Train Neural Net #############
exe4 = wf.Executable(workflow.cp, 'train_nn')

node4 = exe4.create_node()
node4.add_input_opt('--simulation-file', simulations)
node4.add_opt('--training-parameters', args.training_parameters)
node4.add_opt('--n-simulations', args.ninjections) # should change later
node4.add_opt('--add-noise')
node4.add_input_opt('--noise-file', noise)
neural_net = node4.new_output_file_opt(workflow.analysis_time,
        '.pickle', '--output-file', tags=['4'])

workflow += node4
#################################


# Make Observations for samping  ########
observation_num = 100
node5 = exe1.create_node()
node5.add_input_opt('--config-files', input_file)
node5.add_opt('--ninjections', observation_num) # number of observations!
obs_inj = node5.new_output_file_opt(workflow.analysis_time, '.hdf',
                                '--output-file', tags=['1'])

node6 = exe2.create_node()
node6.add_input_opt('--injfile', obs_inj)
node6.add_opt('--add-noise')
node6.add_input_opt('--noise-file', noise)
observations = node6.new_output_file_opt(workflow.analysis_time, '.hdf',
        '--output-file', tags=['5'])

workflow += node5
workflow += node6
########################################


# Sample from Neural Net ###############
exe5 = wf.Executable(workflow.cp, 'sample')

node7 = exe5.create_node()
node7.add_input_opt('--neural-net', neural_net)
node7.add_input_opt('--observation-file', observations)
node7.add_opt('--sample-parameters', args.training_parameters)
node7.add_opt('--observation-num', observation_num)
samples = node7.new_output_file_opt(workflow.analysis_time, '.hdf',
        '--output-file', tags=['6'])
pycbc_samples = node7.new_output_file_opt(workflow.analysis_time,
        '.hdf', '--write-pycbc-posterior', tags = ['7'])

workflow += node7
#######################################


# Plot PyCBC posterior ################
exe6 = wf.Executable(workflow.cp, 'pycbc_plot')

node8 = exe6.create_node()
node8.add_input_opt('--input-file', pycbc_samples)
node8.add_opt('--parameters', args.training_parameters)
# !!! add expected parameters here!!!
pycbc_plot = node8.new_output_file_opt(workflow.analysis_time,
        '.png', '--output-file', tags = ['8'])

workflow += node8
########################################

# Plot PPtest ########################
exe7 = wf.Executable(workflow.cp, 'plot')

node9 = exe7.create_node()
node8.add_input_opt('--samples-file', samples)
node8.new_output_file_opt(workflow.analysis_time, '.png',
                          '--output-plot', tags=['9'])
node8.add_opt('--plot-content', 'pptest')
node8.add_opt('--sample-parameters', 'total_mass')
########################################

# Save workflow ##############
workflow.save()