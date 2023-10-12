from sbi.inference import SNPE
import torch, numpy, pickle, h5py, argparse, sys, configparser, os

sys.path.append("/home/mrtodd/PEWSBI/code/train")

from train_neural_network import get_bounds_from_config
def details(neuralnet):
    dets = {}
    neuralnet = neuralnet.split('.')[0]
    neuralnet = neuralnet.split('/')[-1]
    l = neuralnet.split('_')
    dets['training_number'] = l[1][2:]
    dets['learning_rate'] = l[2][2:]
    dets['batch_size'] = l[3][2:]
    return dets


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
    parser.add_argument("--sample-parameter", type=str, required=True,
                        help="Parameter name to sample.")
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

    if args.verbose:
        print("Loading neural network...")
    with open(args.neural_net, 'rb') as f:
        net = pickle.load(f)

    if args.verbose:
        print("Fetching observations...")
    with h5py.File(args.observation_file, 'r') as f:
        observations = torch.as_tensor(f['signals'][:args.observation_num,:])
        true_parameters = [f['parameters'][key][:args.observation_num] for key in f['parameters'].keys()]
    if args.verbose:
        print("Sampling...")
    samples = [net.sample((args.n_samples,), x=each).cpu() for each in observations]
    bounds = get_bounds_from_config(args.config_file, args.sample_parameter)
    counts = [numpy.histogramdd(each, args.n_bins, range=(bounds[0],bounds[1]), density=True)[0] for each in samples]
    posteriors = [each*(bounds[1]-bounds[0])/args.n_bins for each in counts]
    nn_params = details(args.neural_net)
    posteriorname = f"posterior_TS{nn_params['training_number']}_LR{nn_params['learning_rate']}_BS{nn_params['batch_size']}.hdf"
    with h5py.File(args.output_folder+'/'+posteriorname, 'w') as f:
        f['posteriors'] = posteriors
        f['posteriors'].attrs['training_size'] = nn_params['training_number']
        f['true_parameters'] = true_parameters
        if args.write_samples:
            f['raw_samples'] = samples
    if args.verbose:
        print("All posterior estimates written.")
