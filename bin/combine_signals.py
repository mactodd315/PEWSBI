import argparse, h5py, os
import numpy as np

def zip_signals(simfile, sim_shape):
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
    return signals,parameters

def write_signals(outputfile, simfile, sim_shape):
    with h5py.File(outputfile, 'w') as f:
        signals,parameters = zip_signals(simfile,sim_shape)
        #write results to file
        f['signals'] = signals
        for key in parameters.keys():
            f['parameters/'+key] = parameters[key]
###############################################################################################
parser = argparse.ArgumentParser(
                    prog = "Combine Simulation Data: ",
                    description = "Takes simulation data and combines into one file.",
                    )

parser.add_argument("--simfile", type=str,required=True,
                   help="Path to simulation data (without number label or .hdf).")
parser.add_argument("--injfile", type=str,required=True,
                   help="Path to simulation data (without number label or .hdf).")
parser.add_argument("--output-simfile", type=str, required=True,
                    help = "Path for simulation output file to be written, should be .hdf format.")
parser.add_argument("--output_injfile", type=str,
                    help = "Path for injection output file to be written, should be .hdf format.")

parser.add_argument("--n-simulations", type=int,required=True)
parser.add_argument('--sim-shape', type=str, required=True)

# args = parser.parse_args()
###############################################################################################

if __name__ == "__main__":
    sim_shape = args.sim_shape.split(',')
    args.sim_shape = [int(each) for each in sim_shape]
    
    write_signals(args.output_simfile, args.simfile, args.sim_shape)
    # for i in range(args.n_simulations):
    #     os.remove(args.simfile+str(i)+'.hdf')
    #     os.remove(args.injfile+str(i)+'.hdf')
