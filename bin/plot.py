import matplotlib.pyplot as plt
import argparse, h5py, numpy, sys, os




#####################################################################
#Argument Parsing
parser = argparse.ArgumentParser(prog="Plotter"
                                    )


#------------------
parser.add_argument("--samples-file", required=True, nargs='+',
                    help = "Path to file containing posteriors to be plotted.")
parser.add_argument("--plot-folder", required=True)
parser.add_argument("--plot-content", choices = ["pptest", "posterior"], required=True,
                    help = "Decision to either plot a pptest or just plot one posterior.")
parser.add_argument("--config-file", type=str, required=True,
                        help="Path to config file (.ini).")
parser.add_argument("--sample-parameters", nargs='+',
                        help="Parameter names to sample for pptest.")
parser.add_argument("--sample-parameter", 
                        help="Parameter name to sample for posterior.")

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
def is_true(credibility, dataset, parameter):
    mid = len(dataset)//2
    cutoff = int(credibility*len(dataset))//2
    if parameter <= dataset[mid+cutoff] and parameter >= dataset[mid-cutoff]:
        return True
    else:
        return False
#--------------------------------

def run_pp_test(hdffile, key, args, s1, n_intervals = 101, **kwargs):
    """This pp_test function initializes linearly spaced credible intervals,
     and then evaluates the cumulative distribution function to determine
     the "credibility" at that interval. It generates the plot WITHIN this
     function, so plt.show() must be called after the function is called.
    """
    dataset = hdffile['samples/'+key][:argsd['num_posteriors']]
    parameters = hdffile['true_parameters/'+key][:argsd['num_posteriors']]

    print(f"Plotting {key}\r", end='')

    credible_intervals = numpy.linspace(0,1,n_intervals)
    trues_in_intervals = numpy.zeros(n_intervals)
    for i in range(1,n_intervals-1):
        credibility = credible_intervals[i]
        trues_list = [1 if is_true(credibility, numpy.sort(dataset[j]), parameters[j]) else 0 for j in range(len(dataset)) ]
        trues_in_intervals[i] = sum(trues_list)/len(dataset)
    trues_in_intervals[-1] = 1
    
    
    if argsd['save_traces']:
        trace_name = "traces"+key
        with h5py.File(argsd['parent_folder']+'/'+'plots/'+trace_name, 'w') as f:
            f['traces'] = (credible_intervals, trues_in_intervals)
            f['label'] = key
    s1.plot(credible_intervals, trues_in_intervals, label=key)
    return s1


#----------------------
def plot_posterior(file, key, argsd, s1):
    """Saves posterior traces to designated file

    Args:
        file (hd5 object): .hdf file object containing posterior data
        args (_type_): _description_
    """
    samples = file['samples/'+key][argsd['posterior_index'],:]
    s1.hist(samples, bins=150, density=True)
    s1.set_xlabel(key)
    s1.set_ylabel('Probability')

    return s1
#--------------------------------------------------------------------------

if __name__ == "__main__":
    if not os.path.exists(args.plot_folder):
            os.makedirs(args.plot_folder)

    argsd = vars(args)
    argsd["parent_folder"] = os.path.join(args.plot_folder,'..')
    
    # if not argsd['sample_name'] == None:
    #     samples = [os.path.join(argsd["samples_folder"], argsd["sample_name"])]
    # else:
    #     samples = [os.path.join(argsd['samples_folder'], f) for f in os.listdir(args.samples_folder) if f.split('.')[1]=='hdf']

    fig, s1 = plt.subplots(1,1)
    if argsd['plot_content'] == "pptest":
        for each in args.samples_file:
            with h5py.File(each, 'r') as f:
                keys = argsd['sample_parameters']
                for key in keys:
                    s1 = run_pp_test(f, key, argsd, s1)
        s1.set_title(f"PP Test")
        
        s1.set_xlabel("Credible Interval")
        s1.set_ylabel("Credibility")
        s1.grid(True)
        plt.legend()
        plt.savefig(os.path.join(args.plot_folder,'pptest.png'))
   
    if args.plot_content == "posterior":
        for each in args.samples_file:
            argsd['sample_name'] = each
            with h5py.File(each, 'r') as f:
                s1 = plot_posterior(f,argsd["sample_parameter"],argsd,s1)
            if argsd['plot_true']:
                with h5py.File(each, 'r') as f:
                    print(f['true_parameters/'+argsd['sample_parameter']][int(argsd['posterior_index'])])
                    s1.axvline(f['true_parameters/'+argsd['sample_parameter']][int(argsd['posterior_index'])], color='k')
        plt.savefig(f'{argsd["plot_folder"]}/posterior{argsd["posterior_index"]}_{argsd["sample_parameter"]}.png')  
    
