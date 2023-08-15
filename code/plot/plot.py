import matplotlib.pyplot as plt
import argparse, h5py, numpy, sys

sys.path.append("/home/mrtodd/PEWSBI/code/train")

from train_neural_network import get_bounds_from_config


#####################################################################
#Argument Parsing
parser = argparse.ArgumentParser(prog="Plotter"
                                    )


#------------------
parser.add_argument("posteriors", nargs='+',
                    help = "Path to file containing posteriors to be plotted.")
parser.add_argument("output", type=str,
                    help = "Path for produced plot.")
parser.add_argument("plot_content", choices = ["pptest", "posterior"],
                    help = "Decision to either plot a pptest or just plot one posterior.")
parser.add_argument("config_file", type=str,
                        help="Path to config file (.ini).")
parser.add_argument("sample_parameter", type=str,
                        help="Parameter name to sample.")

parser.add_argument("--num-posteriors", type=int,
                    help = "Number of posteriors to include in the pptest analysis.")
parser.add_argument("--posterior-index", type=int,
                    help = "Location of posterior desired when choosing to plot one posterior.")
parser.add_argument("--plot-true", action="store_true",
                    help = "If plotting posterior, plot true parameter or not.")
parser.add_argument("--plot-title", type=str,
                    help = "Title to put on plot.")
parser.add_argument("-v", "--verbose", action="store_true", default=False)

args = parser.parse_args()

######################################################################
def is_true(credibility, cumulative, parameter, config_file, config_parameter):
    bounds = get_bounds_from_config(config_file, config_parameter)
    theta = numpy.linspace(bounds[0],bounds[1],200)
    credibility_bounds = theta[numpy.searchsorted(cumulative,[0,credibility])]
    if parameter<= credibility_bounds[1] and parameter >= credibility_bounds[0]:
        return True
    else:
        return False
#--------------------------------

def run_pp_test(dataset, parameters, n_intervals = 21, **kwargs):
    """This pp_test function initializes linearly spaced credible intervals, and then evaluates the cumulative distribution function to determine the "credibility" at that interval. It generates the plot WITHIN this function, so plt.show() must be called after the function is called.
    """
    n_intervals = 21
    credible_intervals = numpy.linspace(0,1,n_intervals)
    trues_in_intervals = numpy.zeros(n_intervals)
    cumulatives = [dataset[j,:].cumsum() for j in range(len(dataset))]
    for i in range(1,n_intervals-1):
        credibility = credible_intervals[i]
        trues_list = [1 if is_true(credibility, cumulatives[j], parameters[:,j], config_file=kwargs['config_file'], config_parameter= kwargs['parameter']) else 0 for j in range(len(dataset)) ]
        trues_in_intervals[i] = sum(trues_list)/dataset.shape[0]
    trues_in_intervals[-1] = 1
    if 'label' in kwargs.keys():
        labeltxt = str(kwargs['label'])
    plt.plot(credible_intervals, trues_in_intervals, label = labeltxt)
    return 0
#----------------------
def plot_posterior(file, posterior_num, plot_true = True):
    posterior = file['posteriors'][posterior_num,:]
    plt.plot(posterior)
    if plot_true:
        plt.axvline(file["true_parameters"][:,posterior_num])
    return 0
#--------------------------------------------------------------------------

if __name__ == "__main__":
    if args.plot_content == "pptest":
        for each in args.posteriors:
            with h5py.File(each, 'r') as f:
                run_pp_test(f['posteriors'][:args.num_posteriors,:], f['true_parameters'][:args.num_posteriors], verbose = args.verbose, label = f['posteriors'].attrs['training_size'], config_file = args.config_file, parameter = args.sample_parameter)
    if args.plot_content == "posterior":
        with h5py.File(args.posteriors, 'r') as f:
            plot_posterior(f,args.posterior_index, plot_true = args.plot_true)
    plt.legend()
    plt.savefig(args.output)
