from sbi.inference import SNPE
import torch, numpy, pickle, h5py, argparse, sys, configparser, os

sys.path.append("/home/mrtodd/PEWSBI/code/train")

def get_bounds_from_config(filepath):
    cp = configparser.ConfigParser()
    cp.read(filepath)
    param_prior = [each for each in cp.sections() if each.split('-')[0]=='prior']
    bounds = numpy.zeros((2,len(param_prior)))

    parameters = []
    for i in range(len(param_prior)):
        each = param_prior[i]
        parameter = each.split('-')[1]
        parameters.append(parameter)
        bounds[0, i] = float(cp[each]['min-'+parameter])
        bounds[1, i] = float(cp[each]['max-'+parameter])
    return bounds, parameters
def details(neuralnet):
    dets = {}
    neuralnet = neuralnet.split('.')[0]
    neuralnet = neuralnet.split('/')[-1]
    l = neuralnet.split('_')
    dets['training_number'] = l[1][2:]
    dets['learning_rate'] = l[2][2:]
    dets['batch_size'] = l[3][2:]
    return dets
def get_samples(net, observations, args):
    samples = [net.sample((args.n_samples,), x=each) for each in observations]
    
    return samples
def fetch_observation(file, args):
    observations = torch.as_tensor(f['signals'][:args.observation_num,:])
    true_parameters = [f['parameters'][key][:args.observation_num] for key in f['parameters'].keys()]
    return observations, true_parameters


if __name__ == "__main__":
    
    ################################################
    parser = argparse.ArgumentParser(
                        prog = "Estimates Posterior: ",
                        description = "Takes in trained neural network and given observation, and returns an estimated posterior \
                        to the designated output file.",
                        )

    parser.add_argument("--neural-net", type=str, required=True,
                         help="Path to the trained nerual network (.pickle).")
    parser.add_argument("--output-folder", type=str, required=True,
                         help="Path to output file (.hdf)")
    parser.add_argument("--observation-file", type=str, required=True,
                        help="Path to observation file (.hdf).")
    parser.add_argument("--config-file", type=str, required=True,
                        help="Path to config file (.ini).")
    parser.add_argument("--observation-num", type=int, default=0)
    parser.add_argument("--n-samples", type=int, default=10000,
                         help="Number of samples to draw from neural network.")
    parser.add_argument("--n-bins", type=int, default=200)
    parser.add_argument("--write-samples", action="store_true", default=False,
                         help="Option to write raw samples drawn from neural network")
    parser.add_argument("-v", "--verbose", action="store_true", default=False)

    args = parser.parse_args()
    ###############################################
    if not os.path.exists(args.output_folder):
        os.makedirs(args.output_folder)

    bounds, parameters = get_bounds_from_config(args.config_file)
    
    if args.verbose:
        print("Loading neural network...")
    with open(args.neural_net, 'rb') as f:
        net = pickle.load(f)

    if args.verbose:  print("Fetching observations...")
    with h5py.File(args.observation_file, 'r') as f:
        observations, true_parameters = fetch_observation(f, args)
    
    
    if args.verbose:  print("Sampling...")
    samples = get_samples(net, observations, args)
    samples = numpy.asanyarray(samples)

    # getting data
    nn_params = details(args.neural_net)
    samplename = f"samples_TS{nn_params['training_number']}_LR{nn_params['learning_rate']}_BS{nn_params['batch_size']}.hdf"
    
    # writing posteriors
    n_parameters = len(bounds[0])
    with h5py.File(args.output_folder+'/'+samplename, 'w') as f:
        for i in range(n_parameters):
            
            f['samples/'+parameters[i]] = samples[:,:,i]
            f['bounds/'+parameters[i]] = [bounds[0][i], bounds[1][i]]
            f['true_parameters/'+parameters[i]] = true_parameters[i]
            
    if args.verbose:  print("All samples written.")
