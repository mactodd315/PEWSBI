import argparse, h5py, torch, pickle, logging, time, os
import numpy as np
import sbi.utils as utils
from sbi.inference import SNPE, SNLE, SNRE
from sbi.utils.user_input_checks import process_prior

import configparser
def parse_arguments():
    parser = argparse.ArgumentParser(
                        prog = "Trains a Neural Network: ",
                        description = "Takes in simulation data and desired \
                            training parameters, and trains a neural network,\
                            which is then pickled in indicated output file \
                            (.pickle).",)
    
    parser.add_argument("--training-parameters", nargs="+")
    parser.add_argument("--simulation-file", type=str, required=True,
                       help="Filename of the datafile containing the \
                        simulations for training, assumes it is found in simulations/\
                         folder.\nIf not, specify fullpath name.")
    parser.add_argument("--output-file", type=str, required=True,
                        help = "Path to output file to store pickled neural networks.")
    parser.add_argument("--n-simulations", type=int, required=True,
                        help = "Number of simulations to use in training procedure. \
                              Cannot exceed number of simulations in datafile.")

    parser.add_argument("--add-noise", action="store_true", default = False)
    parser.add_argument("--noise-file", type=str,
                        help = "Path to noise file.")
    
    parser.add_argument("--device", default='cpu',
                        help="Decision to train on gpu, if available. Neural net is brought \
                              to cpu after training for pickling.")
    parser.add_argument("--training-method", type=str, default='SNPE',
                        choices=["SNPE", "SNLE", "SNRE"],
                        help="Training method to use, see https://github.com/sbi-dev/sbi \
                            for more details.")
    parser.add_argument("--batch-size", type = int, default=50)
    parser.add_argument("--learning-rate", type = float, default=5.0e-4)
    parser.add_argument("--show-summary", action='store_true', default=False)

    parser.add_argument("-v", "--verbose", action="store_true", default=False)
    parser.add_argument("--monitor-rate", type=int, default=20)
    parser.add_argument("--logfile", type=str)

    args = parser.parse_args()
    return args

def get_training_data(sim_filename, device, args):
    
    with h5py.File(sim_filename, 'r') as f:
            
        if args.verbose: logging.info("Fetching training samples...")
        training_samples = torch.as_tensor(f['signals'][:args.n_simulations,:],
                                            dtype=torch.float32, device=device)
        
        if args.verbose:    logging.info("Fetching parameters...")
        training_parameters = torch.zeros((args.n_simulations, len(args.training_parameters)),
                                           device=device)
        
        variable_parameter_names = args.training_parameters
        n_dim = len(variable_parameter_names)
        for i in range(n_dim):
            training = f['parameters/'+variable_parameter_names[i]][:args.n_simulations]
            training_parameters[:,i] = torch.as_tensor(training, device=device)
    return training_samples,training_parameters, variable_parameter_names
            
def add_noise(training_samples, device, args):
           
    samples_length = training_samples.shape[1]
    
    if args.verbose:  print("Adding noise...")
    start = time.perf_counter()   
    with h5py.File(args.noise_file, 'r') as f:
        noise = torch.as_tensor(f["noise"][()], dtype=torch.float32, device=device)
    indices = np.random.choice(list(range(len(noise)-samples_length)),
                                size = len(training_samples))
    for i in range(len(training_samples)):
        tic = time.perf_counter()
        training_samples[i,:] += noise[indices[i]:indices[i]+samples_length]
        if args.verbose and i%args.monitor_rate==0:
            toc = time.perf_counter()
            
            message = f"\rNoise added to {i} out of {args.n_simulations}"
            message += f" signals. Time-passed: {toc-tic:.6f} "
            message += f"  ETA:  {eta(toc-tic,i,len(training_samples))}"
            print(message, end='')
                    
    end = time.perf_counter()
    if args.verbose:     print("\nTotal time: {:.2f} s".format(end-start))
    if args.verbose:     print("Noise added.")
    return
        
        
def train(training_samples,training_parameters, device, args):
            
    if args.device == 'gpu':
        if args.training_method == "SNPE":
            inference = SNPE(device='cuda')
        elif args.training_method == "SNLE":
            inference = SNLE(device='cuda')
        else:
            inference = SNRE(device='cuda')
    else:
        if args.training_method == "SNPE":
            inference = SNPE()
        elif args.training_method == "SNLE":
            inference = SNLE()
        else:
            inference = SNRE()
    if args.verbose: print("Training...")
    inference = inference.append_simulations(training_parameters, training_samples)
    density_estimator = inference.train(training_batch_size=args.batch_size,
                                        learning_rate=args.learning_rate,
                                        show_train_summary=args.show_summary)
    neural_net = inference.build_posterior(density_estimator)
    return neural_net
    

# def get_bounds_from_config(filepath, parameter):
#     cp = configparser.ConfigParser()
#     cp.read(filepath)
#     for sect in cp.sections():
#         if parameter in sect.split('-'):
#             param_prior = sect
#     bounds = [float(cp[param_prior]['min-'+parameter]),
#                float(cp[param_prior]['max-'+parameter])]
#     return bounds

def eta(timing, current, total):
    eta = timing*(total-current)
    hrs = eta//3600
    mins = (eta%3600)//60
    secs = (eta%3600)%60
    eta = "{:.2f}h {:.2f}m {:.2f}s".format(hrs,mins,secs)
    return eta


if __name__ == "__main__":
    args = parse_arguments()
    
    
    logging.basicConfig(filename=args.logfile, level=logging.DEBUG)
    if args.device == 'gpu':
        print(f"GPU available: {torch.cuda.is_available()}")
        device = torch.device('cuda')

    else:
        device = torch.device('cpu')

    simfile = args.simulation_file
    training_samples, training_parameters, \
          variable_parameter_names = get_training_data(simfile, device, args)
    
    if args.add_noise: add_noise(training_samples, device, args)
        

    # if args.verbose:  logging.info("Getting bounds...")
    # inifile = args.ini_file
    
    if args.verbose: logging.info("Training...")
    neural_net = train(training_samples,training_parameters,device,args)
    
    torch.save(neural_net, args.output_file)
    # with open(args.output_file, 'wb') as f:
    #     pickle.dump(neural_net, f)
        
    if args.verbose:  logging.info("Neural network trained.")
