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
parser.add_argument('sim_shape', type=str)

args = parser.parse_args()

if __name__ == "__main__":
    sim_shape = args.sim_shape.split(',')
    args.sim_shape = [int(each) for each in sim_shape]
    with h5py.File(args.output_simfile, 'w') as f:
        signals = np.ndarray((args.n_simulations*args.sim_shape[0],args.sim_shape[1])) 
        parameters = {}
        for i in range(args.n_simulations):
            with h5py.File(args.simfile+str(i)+'.hdf', 'r') as f1:
                if i==0:
                    for j in f1['static_args'].keys():
                        f['static_args/'+ j] = f1['static_args'][j][()]
                for j in f1['parameters'].keys():
                    if j in parameters.keys():
                        parameters[j] = np.concatenate((parameters[j],f1['parameters/'+j][:]))
                    else:
                        parameters[j] = f1['parameters/'+j][:]
                signals[i*args.sim_shape[0]:(i+1)*args.sim_shape[0],:] = f1['signals'][:,:]
        
        #write results to file
        f['signals'] = signals
        for key in parameters.keys():
            f['parameters/'+key] = parameters[key]
            
    with h5py.File(args.output_injfile, 'w') as f:
        parameters = {}
        for i in range(args.n_simulations):
            with h5py.File(args.injfile+str(i)+'.hdf', 'r') as f1:
                for j in f1.keys():
                    if j in parameters.keys():
                        parameters[j] = np.concatenate((parameters[j],f1[j][:]))
                    else:
                        parameters[j] = f1[j][:]
                if i==0:
                    for j in f1.attrs.keys():
                        f.attrs[j] = f1.attrs[j]
        for key in parameters.keys():
            f[key] = parameters[key]
    for i in range(args.n_simulations):
        os.remove(args.simfile+str(i)+'.hdf')
        os.remove(args.injfile+str(i)+'.hdf')
