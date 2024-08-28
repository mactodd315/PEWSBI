#!/bin/env python
""" A minimal ml_sbi workflow example """
############################   Functions   #################################
def get_list_of_varied_params(config_file):
    parser = configparser.ConfigParser()
    parser.read(config_file)
    variable_params = list(parser['variable_params'])
    params_to_permute = []
    for each in variable_params:
        if each != 'total_mass':
            params_to_permute.append(each)
        else:
            continue
    def all_sublists(lst):
        # Generate all possible sublists
        sublists = []
        for r in range(len(lst) + 1):
            sublists.extend(itertools.combinations(lst, r))
        # Convert tuples to lists
        return [list(sublist) for sublist in sublists]
    hidden_param_perms = all_sublists(params_to_permute)
    learned_and_hidden_params = []
    for i in range(len(hidden_param_perms)):
        hidden = hidden_param_perms[i]
        learned = []
        for param in variable_params:
            if param not in hidden:
                learned.append(param)
        learned_and_hidden_params.append([learned, hidden])

    return learned_and_hidden_params
############################################################################


############################   Preamble   ##################################
import os, argparse, configparser, itertools
import pycbc, h5py
import pycbc.workflow as wf

parser = argparse.ArgumentParser(description=__doc__[1:])
parser.add_argument('--verbose', '-v', action='count',
                    default=0)
parser.add_argument('--n-simulations', type=int, default=1000,
                    help="Number of simulations to create injection  \
                        to pass simulate_data.")
parser.add_argument('--n-trainings', type=int, default=2000,
                    help="Number of training samples to create for  \
                        neural network training from simulations+noise.")
parser.add_argument("--working-folder", type=str,
                    help="Subfolder to save work.")
# parser.add_argument('--training-config-file', type=str,
#                     help="Path/name of training config file (.ini)")
# parser.add_argument('--pycbc-config-file', type=str,
#                     help="Path/name of pycbc inference config file (.ini)")
parser.add_argument('--observation-injection', type=str,
                    help='Path to observation injection file \
                        with values of each parameter (.hdf)')
parser.add_argument('--noise-file', type=str, default=None,
                    help="Path/name of noise samples (.hdf). If None, \
                        will default to creating from generate_noise \
                        options set in wf .ini file.")
wf.add_workflow_command_line_group(parser)
wf.add_workflow_settings_cli(parser)
args = parser.parse_args()
############################################################################


##########################   Workflow init   ###############################
pycbc.init_logging(args.verbose)

workflow = wf.Workflow(args, 'cont')

training_ini_file_path = os.path.join(
    args.working_folder, 'training_injections.ini'
)
pycbc_ini_file_path = os.path.join(
    args.working_folder, 'pycbc_inference.ini'
)
############################################################################


########################   Create Noise File   #############################
if args.noise_file == None:
    exe0 = wf.Executable(workflow.cp, 'generate_noise')

    node0 = exe0.create_node()

    noise_file = node0.new_output_file_opt(
        workflow.analysis_time, '.hdf',
        '--output-file', tags=['1'])
    
    workflow += node0

else:
    noise_file = wf.resolve_url_to_file(args.noise_file)
############################################################################


####################   Create Training Injection   #########################

training_input_file = wf.resolve_url_to_file(training_ini_file_path)
exe1 = wf.Executable(workflow.cp, 'create_injections')

node1 = exe1.create_node()

node1.add_input_opt('--config-files', training_input_file)
node1.add_opt('--ninjections', args.n_simulations)
training_inj_file = node1.new_output_file_opt(
                                workflow.analysis_time, '.hdf',
                                '--output-file', tags=['1'])

workflow += node1
############################################################################


#####################   Create Training Dataset   ##########################
exe2 = wf.Executable(workflow.cp, 'simulate_data')

node2 = exe2.create_node()

node2.add_input_opt('--injection-file', training_inj_file)
node2.add_opt("--snr")
training_hdf_file = node2.new_output_file_opt(
                                workflow.analysis_time, '.hdf',
                                '--output-file', tags=['2'])

workflow += node2
############################################################################


###################   Train, Sample, Get Posterior   #######################

# first get list of parameters we will vary
learned_and_hidden = get_list_of_varied_params(training_ini_file_path)

# get pycbc inference .ini file
pycbc_input_file = wf.resolve_url_to_file(pycbc_ini_file_path)

for i in range(len(learned_and_hidden)):
    learned = learned_and_hidden[i][0]
    hidden = learned_and_hidden[i][1]

    if len(hidden) == 0:
        output_folder = 'learned_all'
    else:
        output_folder = 'hide_'+'_'.join(hidden)

    out_dir = os.path.join(os.curdir, output_folder)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # Train Neural Net
    exe3 = wf.Executable(workflow.cp, 'train_nn',
                         out_dir = out_dir)

    node3 = exe3.create_node()

    node3.add_input_opt('--input-file', training_hdf_file)
    node3.add_list_opt('--training-parameters', learned)
    node3.add_opt('--n-simulations', args.n_trainings)
    node3.add_opt('--add-noise', noise_file)
    trained_nn = node3.new_output_file_opt(
                                    workflow.analysis_time, '.hdf',
                                    '--output-file', tags=['3'])
    workflow += node3

    # Sample Neural Net
    exe4 = wf.Executable(workflow.cp, 'sample',
                         out_dir = out_dir)

    node4 = exe4.create_node()

    node4.add_input_opt('--neural-net', trained_nn)
    node4.add_list_opt('--sample-parameters', learned)
    node4.add_opt("--injection-file", args.observation_injection)
    samples = node4.new_output_file_opt(
                                    workflow.analysis_time, '.hdf',
                                    '--output-file', tags=['4'])
    posterior_samples = node4.new_output_file_opt(
                                    workflow.analysis_time, '.hdf',
                                    '--write-pycbc-posterior', tags=['41'])

    workflow += node4

    # Run PYCBC inference
    exe5 = wf.Executable(workflow.cp, 'pycbc_inference',
                         out_dir = out_dir)

    node5 = exe5.create_node()

    node5.add_input_opt('--config-files', pycbc_input_file)
    node5.add_list_opt('--sample-parameters', learned)
    node5.add_opt('--verbose')
    node5.add_opt('--force')
    pycbc_samples = node5.new_output_file_opt(
                                    workflow.analysis_time, '.hdf',
                                    '--output-file', tags=['5'])

    workflow += node5

    # Plot Posterior
    expected_params = []
    with h5py.File(args.observation_injection, 'r') as obs:
        for each_param in learned:
            expected_params.append(each_param+":" \
                                   + str(obs.attrs[each_param]))
    exe6 = wf.Executable(workflow.cp, 'plot_posterior',
                         out_dir = out_dir)

    node6 = exe6.create_node()


    node6.add_input_list_opt('--input-file', [posterior_samples,
                                              pycbc_samples])
    node6.add_list_opt('--parameters', learned)
    node6.add_list_opt('--expected-parameters', expected_params)
    node6.add_opt("--plot-contours")
    samples = node6.new_output_file_opt(
                                    workflow.analysis_time, '.hdf',
                                    '--output-file', tags=['6'])

    workflow += node6
############################################################################
# # Create Injection .hdf file ###
# exe1 = wf.Executable(workflow.cp, 'create_injections')

# node1 = exe1.create_node()

# node1.add_input_opt('--config-files', input_file)
# node1.add_opt('--ninjections', args.ninjections)
# injfile = node1.new_output_file_opt(workflow.analysis_time, '.hdf',
#                                 '--output-file', tags=['1'])

# workflow += node1
# ################################


# # Write TimeSeries from Inj Set #
# exe2 = wf.Executable(workflow.cp, 'write_sims')

# node2 = exe2.create_node()
# node2.add_input_opt('--injfile', injfile)
# simulations = node2.new_output_file_opt(workflow.analysis_time, '.hdf',
#         '--output-file', tags=['2'])
# workflow += node2
# ################################


# # Generate Noise ##############
# exe3 = wf.Executable(workflow.cp, 'make_noise')

# node3 = exe3.create_node()
# node3.add_input_opt('--ini-file', input_file)
# noise = node3.new_output_file_opt(workflow.analysis_time, '.hdf',
#         '--output-file', tags=['3'])
# workflow += node3
# ###############################


# # Train Neural Net #############
# exe4 = wf.Executable(workflow.cp, 'train_nn')

# node4 = exe4.create_node()
# node4.add_input_opt('--simulation-file', simulations)
# node4.add_opt('--training-parameters', args.training_parameters)
# node4.add_opt('--n-simulations', args.ninjections) # should change later
# node4.add_opt('--add-noise')
# node4.add_input_opt('--noise-file', noise)
# neural_net = node4.new_output_file_opt(workflow.analysis_time,
#         '.pickle', '--output-file', tags=['4'])

# workflow += node4
# #################################


# # Make Observations for samping  ########
# observation_num = 100
# node5 = exe1.create_node()
# node5.add_input_opt('--config-files', input_file)
# node5.add_opt('--ninjections', observation_num) # number of observations!
# obs_inj = node5.new_output_file_opt(workflow.analysis_time, '.hdf',
#                                 '--output-file', tags=['1'])

# node6 = exe2.create_node()
# node6.add_input_opt('--injfile', obs_inj)
# node6.add_opt('--add-noise')
# node6.add_input_opt('--noise-file', noise)
# observations = node6.new_output_file_opt(workflow.analysis_time, '.hdf',
#         '--output-file', tags=['5'])

# workflow += node5
# workflow += node6
# ########################################


# # Sample from Neural Net ###############
# exe5 = wf.Executable(workflow.cp, 'sample')

# node7 = exe5.create_node()
# node7.add_input_opt('--neural-net', neural_net)
# node7.add_input_opt('--observation-file', observations)
# node7.add_opt('--sample-parameters', args.training_parameters)
# node7.add_opt('--observation-num', observation_num)
# samples = node7.new_output_file_opt(workflow.analysis_time, '.hdf',
#         '--output-file', tags=['6'])
# pycbc_samples = node7.new_output_file_opt(workflow.analysis_time,
#         '.hdf', '--write-pycbc-posterior', tags = ['7'])

# workflow += node7
# #######################################


# # Plot PyCBC posterior ################
# exe6 = wf.Executable(workflow.cp, 'pycbc_plot')

# node8 = exe6.create_node()
# node8.add_input_opt('--input-file', pycbc_samples)
# node8.add_opt('--parameters', args.training_parameters)
# # !!! add expected parameters here!!!
# pycbc_plot = node8.new_output_file_opt(workflow.analysis_time,
#         '.png', '--output-file', tags = ['8'])

# workflow += node8
# ########################################

# # Plot PPtest ########################
# exe7 = wf.Executable(workflow.cp, 'plot')

# node9 = exe7.create_node()
# node9.add_input_opt('--samples-file', samples)
# node9.new_output_file_opt(workflow.analysis_time, '.png',
#                           '--output-plot', tags=['9'])
# node9.add_opt('--plot-content', 'pptest')
# node9.add_opt('--sample-parameters', 'total_mass')

# workflow+=node9
# ########################################

# Save workflow ##############
workflow.save()