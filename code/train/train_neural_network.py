import argparse, h5py, torch, pickle
import numpy as np
import sbi.utils as utils
from sbi.inference import SNPE
from sbi.utils.user_input_checks import process_prior

import configparser

def get_bounds_from_config(filepath, parameter):
    cp = configparser.ConfigParser()	
    cp.read(filepath)
    param_prior = 'prior-'+parameter
    bounds = [float(cp[param_prior]['min-'+parameter]), float(cp[param_prior]['max-'+parameter])]
    return bounds

parser = argparse.ArgumentParser(
                    prog = "Trains a Neural Network: ",
                    description = "Takes in simulation data and desired training parameters, and trains a neural network, which is then pickled in indicated output file (.pickle).",
                    )

parser.add_argument("simfile", type=str,
                   help="Path to the simulation datafile, should be .hdf format.")
parser.add_argument("output_file", type=str,
                    help = "Path for output file to be written, should be .pickle format.")
parser.add_argument("n-simulations", type=str,
                    help = "Number of simulations to use in training procedure.")
parser.add_argument("injfile", type=str,
                    help = "Path to .ini file used to make inserted injection.")
parser.add
parser.add_argument("--add-noise", action="store_true", default = False)
parser.add_argument("-v", "--verbose", action="store_true", default=False)


args = parser.parse_args()

training_samples = torch.as_tensor(training_file['signals'][:nsimulations,:], dtype=torch.float32)
noise = noise_file['noise']['noise'][()]

samples_length = training_samples.shape[0]

if add_noise:
    for i in range(len(training_samples)):
        index = np.random.choice(range(len(noise)-samples_length))
        training_samples[i,:] += torch.as_tensor(noise[index:index+samples_length], dtype=torch.float32)

training_parameters = torch.zeros((samples_length, len(injection_file.keys())))
variable_parameter_names = list(injection_file.keys())
n_dim = len(variable_parameter_names)
for i in range(len(training_parameters)):
    training_parameters[:,i] = injection_file[variable_parameter_names[i]][()] 

bounds = [torch.tensor([get_bounds_from_config(injfile,each)[0] for each in variable_parameter_names]),
            torch.tensor([get_bounds_from_config(injfile,each)[1] for each in variable_parameter_names])]
prior = utils.BoxUniform(low = bounds[0]*torch.ones(n_dim), high = bounds[1]*torch.ones(n_dim))
prior, _, priorr = process_prior(prior)
inference = SNPE(prior)
density_estimator = inference.append_simulations(training_parameters, training_samples).train()
neural_net = inference.build_posterior(density_estimator)
with open(outputfile, 'wb') as f:
        pickle.dump(neural_net, f)

