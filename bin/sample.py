from sbi.inference import SNPE
import torch, numpy, pickle, h5py, argparse, sys, configparser, os
from pycbc.inference.io import (ResultsArgumentParser, results_from_cli,
                                PosteriorFile, loadfile)

def details(neuralnet):
    dets = {}
    neuralnet = neuralnet.split('.')[0]
    neuralnet = neuralnet.split('/')[-1]
    l = neuralnet.split('_')
    dets['training_number'] = l[1][2:]
    dets['learning_rate'] = l[2][2:]
    dets['batch_size'] = l[3][2:]
    return dets
def get_samples(net, observations, num_params, args):
    samples = numpy.ndarray((len(observations), args.n_samples, num_params))
    for i in range(len(observations)):
        samples[i,:,:] = numpy.asanyarray(net.sample((args.n_samples,),
                                                      x=observations[i]))
    
    return samples
def fetch_observation(file, args):
    observations = torch.as_tensor(file['signals'][:args.observation_num,:])
    true_parameters = [file['parameters'][i][:args.observation_num] \
                       for i in args.sample_parameters]
    return observations, true_parameters


if __name__ == "__main__":
    
    ################################################
    parser = argparse.ArgumentParser(
                        prog = "Estimates Posterior: ",
                        description = "Takes in trained neural network \
                              and given observation, and returns an estimated posterior \
                            to the designated output file.",  )

    parser.add_argument("--neural-net", type=str, required=True,
                         help="Path to the trained nerual network (.pickle).")
    parser.add_argument("--output-file", type=str, required=True,
                         help="Path to output file (.hdf)")
    parser.add_argument("--observation-file", type=str, required=True,
                        help="Path to observation file (.hdf).")
    parser.add_argument("--config-file", type=str, required=True,
                        help="Path to config file (.ini).")
    parser.add_argument("--sample-parameters", required=True, nargs='+',
                        help="Parameters to make bounds for.")

    parser.add_argument("--observation-num", type=int, default=0)
    parser.add_argument("--n-samples", type=int, default=10000,
                         help="Number of samples to draw from neural network.")
    parser.add_argument("--n-bins", type=int, default=200)
    parser.add_argument("--write-samples", action="store_true", default=False,
                         help="Option to write raw samples drawn from neural network")
    
    parser.add_argument("--write-pycbc-posterior", default=None)
    parser.add_argument("-v", "--verbose", action="store_true", default=False)

    args = parser.parse_args()
    ###############################################
    # if not os.path.exists(args.output_folder):
    #     os.makedirs(args.output_folder)

    # bounds, parameter_names = get_bounds_from_config(args.config_file)
    
    if args.verbose:
        print("Loading neural network...")
    net = torch.load(args.neural_net, map_location=torch.device('cpu'))

    if args.verbose:  print("Fetching observations...")
    with h5py.File(args.observation_file, 'r') as f:
        observations, true_parameters = fetch_observation(f, args)
    
    
    if args.verbose:  print("Sampling...")
    num_params = len(true_parameters)
    samples = get_samples(net, observations, num_params, args)
    print(samples.shape)

    # getting data
    # nn_params = details(args.neural_net)
    
    
    parameter_names = args.sample_parameters
    # writing posteriors
    if not os.path.exists(os.path.dirname(args.output_file)):
        os.makedirs(os.path.dirname(args.output_file))
    with h5py.File(args.output_file, 'w') as f:
        pycbc_samples = {parameter_names[j]: samples[0,:,j] for j in range(len(parameter_names))} 
        samples = {parameter_names[j]: samples[:,:,j] for j in range(len(parameter_names))} 
        
        for key in samples.keys():
            f[f"samples/{key}"] = samples[key]
        for i in range(len(parameter_names)):    
            # f[f"bounds/{parameter_names[i]}"] = [bounds[0,i], bounds[1,i]]
            f[f"true_parameters/{parameter_names[i]}"] = true_parameters[i]
            # f.attrs['neural_net_data'] = nn_params

    if args.write_pycbc_posterior is not None:
        outtype = PosteriorFile.name
        out = loadfile(args.write_pycbc_posterior, 'w', filetype=outtype) 
        out.write_samples(pycbc_samples)
        out.attrs['static_params'] = []
    


    if args.verbose:  print("All samples written.")
