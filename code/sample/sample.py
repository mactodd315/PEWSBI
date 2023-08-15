from sbi.inference import SNPE
import torch, numpy, pickle, h5py, argparse, sys, configparser

sys.path.append("/home/mrtodd/PEWSBI/code/train")

from train_neural_network import get_bounds_from_config


if __name__ == "__main__":
    
    ################################################
    parser = argparse.ArgumentParser(
                        prog = "Estimates Posterior: ",
                        description = "Takes in trained neural network and given observation, and returns an estimated posterior \
                        to the designated output file.",
                        )

    parser.add_argument("neuralnet", type=str,
                         help="Path to the trained nerual network (.pickle).")
    parser.add_argument("outputfile", type=str,
                         help="Path to output file (.hdf)")
    parser.add_argument("observationfile", type=str,
                        help="Path to observation file (.hdf).")
    parser.add_argument("config_file", type=str,
                        help="Path to config file (.ini).")
    parser.add_argument("sample_parameter", type=str,
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

    if args.verbose:
        print("Loading neural network...")
    with open(args.neuralnet, 'rb') as f:
        net = pickle.load(f)

    if args.verbose:
        print("Fetching observations...")
    with h5py.File(args.observationfile, 'r') as f:
        observations = torch.as_tensor(f['signals'][:args.observation_num,:])
        true_parameters = [f['parameters'][key][:args.observation_num] for key in f['parameters'].keys()]
    if args.verbose:
        print("Sampling...")
    samples = [net.sample((args.n_samples,), x=each) for each in observations]
    bounds = get_bounds_from_config(args.config_file, args.sample_parameter)
    counts = [numpy.histogram(each, args.n_bins, range=(bounds[0],bounds[1]), density=True)[0] for each in samples]
    posteriors = [each*(bounds[1]-bounds[0])/args.n_bins for each in counts]
    with h5py.File(args.outputfile, 'w') as f:
        f['posteriors'] = posteriors
        f['true_parameters'] = true_parameters
        if args.write_samples:
            f['raw_samples'] = samples
    if args.verbose:
        print("All posterior estimates written.")
