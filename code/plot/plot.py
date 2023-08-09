import matplotlib.pyplot as plt
import argparse, h5py

parser = argparse.ArgumentParser(
                                    )

parser.add_argument("posterior", type=str,
                    help = "Path to posterior to be plotted (.hdf).")
parser.add_argument("output", type=str,
                    help = "Path for produced plot.")
parser.add_argument("--plot-true", action="store_true", default = False)

args = parser.parse_args()

with h5py.File(args.posterior, 'r') as f:
    posterior = f['posterior'][:]
    plt.plot(posterior)
    if args.plot_true:
        plt.axvline(f['true_parameters'][:])
    plt.savefig(args.output)
