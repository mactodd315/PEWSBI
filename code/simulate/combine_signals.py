import argparse, h5py, os
import numpy as np

parser = argparse.ArgumentParser(
                    prog = "Combine Simulation Data: ",
                    description = "Takes simulation data and combines into one file.",
                    )

parser.add_argument("simfile", type=str,
                   help="Path to simulation data (without number label or .hdf).")
parser.add_argument("injfile", type=str,
                   help="Path to simulation data (without number label or .hdf).")
parser.add_argument("output_simfile", type=str,
                    help = "Path for simulation output file to be written, should be .hdf format.")
parser.add_argument("output_injfile", type=str,
                    help = "Path for injection output file to be written, should be .hdf format.")

parser.add_argument("n_simulations", type=int)

args = parser.parse_args()

if __name__ == "__main__":
    with h5py.File(args.output_simfile, 'w') as f:
        signals = []
        for i in range(args.n_simulations):
            with h5py.File(args.simfile+str(i)+'.hdf', 'r') as f1:
                if i==1:
                    for j in f1['static_args'].keys():
                        f['static_args/'+ j] = f1['static_args'][j][()]
                    for j in f1['parameters'].keys():
                        f['parameters/' + j] = f1['parameters'][j][()]
                signals.append(f1['signals'][:,:])
            
        f['signals'] = signals
    with h5py.File(args.output_injfile, 'w') as f:
        for i in range(args.n_simulations):
            with h5py.File(args.injfile+str(i)+'.hdf', 'r') as f1:
                if i==1:
                    for j in f1.keys():
                        f[j] = f1[j][()]
                    for j in f1.attrs.keys():
                        f.attrs[j] = f1.attrs[j]
    for i in range(args.n_simulations):
        os.remove(args.simfile+str(i)+'.hdf')
        os.remove(args.injfile+str(i)+'.hdf')