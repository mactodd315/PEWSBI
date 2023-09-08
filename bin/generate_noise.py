"""
Generates noise from pycbc.noise and writes to noise.txt
"""
import h5py, argparse
import pycbc.psd, pycbc.noise
import numpy as np

global args

parser = argparse.ArgumentParser(
                    prog = "Create Noise File: ",
                    description = "Takes in parameters and simulates a noise file at given output path.",
                    )

parser.add_argument("output_file", type=str,
                    help = "Path for output file to be written, should be .hdf format.")
parser.add_argument("--f-low", type=float, default = 30.0)
parser.add_argument("--delta-f", type=float, default = 1/16)
parser.add_argument("--f-len", type = int, default = 2048)
parser.add_argument("--delta-t", type=float, default=1/4096)
parser.add_argument("--t-len", type = int, default = 64)
parser.add_argument("-v", "--verbose", action="store_true", default=False)


args = parser.parse_args()

def generate_noise():
    f = h5py.File(args.output_file,'w')

    
    flen = int(args.f_len/args.delta_f) + 1
    psd = pycbc.psd.aLIGOZeroDetHighPower(flen,args.delta_f,args.f_low)
    
    t_samples = int(args.t_len/args.delta_t)

    ts = pycbc.noise.noise_from_psd(t_samples,args.delta_t,psd,seed=0)
    f["noise"] = ts
    f.close()
    
if __name__ == "__main__":
    generate_noise()
