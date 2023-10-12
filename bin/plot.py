import matplotlib.pyplot as plt
import argparse, h5py, numpy, sys, os

sys.path.append("/home/mrtodd/PEWSBI/code/train")

from train_neural_network import get_bounds_from_config


#####################################################################
#Argument Parsing
parser = argparse.ArgumentParser(prog="Plotter"
                                    )


#------------------
parser.add_argument("--posteriors-folder", required=True,
                    help = "Path to file containing posteriors to be plotted.")
parser.add_argument("--plot-folder", required=True)
parser.add_argument("--plot-content", choices = ["pptest", "posterior"], required=True,
                    help = "Decision to either plot a pptest or just plot one posterior.")
parser.add_argument("--config-file", type=str, required=True,
                        help="Path to config file (.ini).")
parser.add_argument("--sample-parameters", type=str,
                        help="Parameter name to sample.")
parser.add_argument("--sample-parameter")

parser.add_argument("--save-traces", action='store_true', default=False)
parser.add_argument("--num-posteriors", type=int, default=None,
                    help = "Number of posteriors to include in the pptest analysis.")
parser.add_argument("--posterior-index", type=int, default=0,
                    help = "Location of posterior desired when choosing to plot one posterior.")
parser.add_argument("--plot-true", action="store_true", default=False,
                    help = "If plotting posterior, plot true parameter or not.")
parser.add_argument("--plot-title", type=str,
                    help = "Title to put on plot.")
parser.add_argument("--legend", action="store_true", default=False)
parser.add_argument("-v", "--verbose", action="store_true", default=False)

args = parser.parse_args()

######################################################################
def is_true(credibility, cumulative, parameter, bounds, bins):
    theta = numpy.linspace(bounds[0],bounds[1],bins)
    credibility_bounds = theta[numpy.searchsorted(cumulative,[0,credibility])]
    if parameter<= credibility_bounds[1] and parameter >= credibility_bounds[0]:
        return True
    else:
        return False
#--------------------------------

def run_pp_test(hdffile, key, args, s1, n_intervals = 21, **kwargs):
    """This pp_test function initializes linearly spaced credible intervals, and then evaluates the cumulative distribution function to determine the "credibility" at that interval. It generates the plot WITHIN this function, so plt.show() must be called after the function is called.
    """
    dataset = hdffile['posteriors/'+key][:argsd['num_posteriors'],:]
    parameters = hdffile['true_parameters/'+key][:argsd['num_posteriors']]
    bounds = hdffile['bounds/'+key][:]

    credible_intervals = numpy.linspace(0,1,n_intervals)
    trues_in_intervals = numpy.zeros(n_intervals)
    cumulatives = [dataset[j,:].cumsum() for j in range(len(dataset))]
    for i in range(1,n_intervals-1):
        credibility = credible_intervals[i]
        trues_list = [1 if is_true(credibility, cumulatives[j], parameters[j],
                                    bounds,
                                    bins=dataset.shape[1]) else 0 for j in range(len(dataset)) ]
        trues_in_intervals[i] = sum(trues_list)/dataset.shape[0]
    trues_in_intervals[-1] = 1
    
    details = argsd['posterior_name'][10:-4]+'_'+key
    if argsd['save_traces']:
        trace_name = "traces"+details
        with h5py.File(argsd['parent_folder']+'/'+'plots/'+trace_name, 'w') as f:
            f['traces'] = (credible_intervals, trues_in_intervals)
            f['label'] = details
    s1.plot(credible_intervals, trues_in_intervals, label=details)
    return s1


#----------------------
def plot_posterior(file,s1, argsd):
    """Saves posterior traces to designated file

    Args:
        file (hd5 object): .hdf file object containing posterior data
        args (_type_): _description_
    """
    posterior = file['posteriors/'+argsd['sample_parameter']][argsd['posterior_index'],:]
    bounds = file['bounds/'+argsd['sample_parameter']]
    theta = numpy.linspace(bounds[0],bounds[1],len(posterior))
    s1.plot(theta, posterior, label=argsd['posterior_name'][10:-4])
    s1.set_xlabel(argsd['sample_parameter'])
    s1.set_ylabel('Probability')

    return s1
#--------------------------------------------------------------------------

if __name__ == "__main__":
    if not os.path.exists(args.plot_folder):
            os.makedirs(args.plot_folder)

    argsd = vars(args)
    argsd["parent_folder"] = os.path.join(args.plot_folder,'..')

    posteriors = [f for f in os.listdir(args.posteriors_folder) if f.split('.')[1]=='hdf']

    fig, s1 = plt.subplots(1,1)
    if argsd['plot_content'] == "pptest":
        for each in posteriors:
            argsd['posterior_name'] = each
            with h5py.File(args.posteriors_folder+'/'+each, 'r') as f:
                keys = argsd['sample_parameters'].split(',')
                for key in keys:
                    s1 = run_pp_test(f, key, argsd, s1)
        plt.legend()
        plt.savefig(os.path.join(args.plot_folder,'pptest.png'))
    if args.plot_content == "posterior":
        for each in posteriors:
            argsd['posterior_name'] = each
            with h5py.File(os.path.join(args.posteriors_folder,each), 'r') as f:
                plot_posterior(f,s1,argsd)
        if argsd['plot_true']:
            with h5py.File(os.path.join(args.posteriors_folder,posteriors[0]), 'r') as f:
                s1.axvline(f['true_parameters/'+argsd['sample_parameter']][int(argsd['posterior_index'])], color='k')
        plt.legend()
        plt.savefig(argsd['parent_folder']+f'/plots/posterior{argsd["posterior_index"]}_{argsd["sample_parameter"]}.png')  
    
