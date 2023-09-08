import argparse, h5py, torch, pickle, logging, time
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

def eta(timing, current, total):
    eta = timing*(total-current)
    hrs = eta//3600
    mins = (eta%3600)//60
    secs = (eta%3600)%60
    eta = "{:.2f}h {:.2f}m {:.2f}s".format(hrs,mins,secs)
    return eta



if __name__ == "__main__":
    ########################################################################################
    parser = argparse.ArgumentParser(
                        prog = "Trains a Neural Network: ",
                        description = "Takes in simulation data and desired training parameters, and trains a neural network, which is then pickled in indicated output file (.pickle).",
                        )

    parser.add_argument("simfile", type=str,
                       help="Path to the simulation datafile, should be .hdf format.")
    parser.add_argument("output_file", type=str,
                        help = "Path for output file to be written, should be .pickle format.")
    parser.add_argument("n_simulations", type=int,
                        help = "Number of simulations to use in training procedure.")
    parser.add_argument("inifile", type=str,
                        help = "Path to .ini filed used to make injection.")
    parser.add_argument("--noisefile", type=str,
                        help = "Path to noise file.")
    parser.add_argument("--add-noise", action="store_true", default = False)
    parser.add_argument("-v", "--verbose", action="store_true", default=False)
    parser.add_argument("--logfile", type=str)
    parser.add_argument("--monitor-rate", type=int, default=20)


    args = parser.parse_args()
    #########################################################################################
    if args.verbose:
        logging.basicConfig(filename=args.logfile, level=logging.DEBUG)
        logging.info("Fetching training samples...")
    with h5py.File(args.simfile, 'r') as f:
        if args.verbose:    logging.info("Fetching parameters...")
        training_parameters = torch.zeros((args.n_simulations, len(f['parameters'].keys())))
        variable_parameter_names = list(f['parameters'].keys())
        n_dim = len(variable_parameter_names)
        for i in range(n_dim):
            training_parameters[:,i] = torch.as_tensor(f['parameters/'+variable_parameter_names[i]][:args.n_simulations])
        
        if args.verbose:    logging.info("Fetching signals...")
        training_samples = torch.as_tensor(f['signals'][:args.n_simulations,:], dtype=torch.float32)

    samples_length = training_samples.shape[1]

    if args.add_noise:
        if args.verbose:
            logging.info("Adding noise...")
        
        start = time.perf_counter()   
        with h5py.File(args.noisefile, 'r') as f:
            noise = torch.as_tensor(f["noise"][()], dtype=torch.float32)
        indices = np.random.choice(list(range(len(noise)-samples_length)), size = len(training_samples))
        for i in range(len(training_samples)):
            tic = time.perf_counter()
            training_samples[i,:] += noise[indices[i]:indices[i]+samples_length]
            if args.verbose and i%args.monitor_rate==0:
                toc = time.perf_counter()
                logging.info("Noise added to {} out of {} signals. Time-passed: {:.6f}  ETA:  {}".format(str(i),str(args.n_simulations),toc-tic, eta(toc-tic,i,len(training_samples))))
                    
        end = time.perf_counter()
        if args.verbose:     logging.info("Total time: {}".format(end-start))
        if args.verbose:     logging.info("Noise added.")

    if args.verbose:
        logging.info("Getting bounds...")
    bounds = [torch.tensor([get_bounds_from_config(args.inifile,each)[0] for each in variable_parameter_names]),
                torch.tensor([get_bounds_from_config(args.inifile,each)[1] for each in variable_parameter_names])]
    prior = utils.BoxUniform(low = bounds[0]*torch.ones(n_dim), high = bounds[1]*torch.ones(n_dim))
    prior, _, priorr = process_prior(prior)
    inference = SNPE(prior)
    if args.verbose:
        logging.info("Training...")
    density_estimator = inference.append_simulations(training_parameters, training_samples).train()
    neural_net = inference.build_posterior(density_estimator)
    with open(args.output_file, 'wb') as f:
        pickle.dump(neural_net, f)
    if args.verbose:
        logging.info("Neural network trained.")
