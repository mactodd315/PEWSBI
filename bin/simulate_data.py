from  pycbc.inject import InjectionSet
from pycbc.types import TimeSeries, zeros, array
from pycbc import psd, filter, waveform
import argparse, h5py, os
import numpy as np
import matplotlib.pyplot as plt
import time


####################################################################################################
parser = argparse.ArgumentParser(
                    prog = "Create Simulation Data: ",
                    description = "Takes in injection file and simulates \
                          a desired number of signals with specified parameters.",
                    )

parser.add_argument("--injfile", type=str, required=True,
                   help="Name of injection file for simulations \
                    -- assumes same folder as output folder. \
                        \nIf not, provide full path.")
parser.add_argument("--output-file", type=str, required=True,
                    help = "Path to simulation file will be placed \
                        (will create folder if not found).")

parser.add_argument("--signal-length", type=int, default = 4096,
                    help="Number of data points in each simulation.")
parser.add_argument("--delta-f", type=int, default = 512,
                    help="1/delta_f gives the time step used for \
                          the signal simulation.")
parser.add_argument("--epoch", type=float, default = 0,
                    help="Start 'time' in the simulation, user should check tc \
                          in .ini file for appropriate overlap.")
parser.add_argument("--DNRF", type=float, default=1.0e18,
                    help="Dynamic range factor used to make training easier.")

parser.add_argument("--add-noise", action='store_true', default=False)
parser.add_argument("--noise-file")

parser.add_argument("-v", "--verbose", action="store_true", default=False)
parser.add_argument("--monitor-rate", type=int, default=10)
parser.add_argument("--timing", '-t', action="store_true", default=False)
parser.add_argument("--snr", action='store_true', default=False)

args = parser.parse_args()
####################################################################################################

def injection_to_signal(items):
    injector, args, n_simulations = items
    signal = np.ndarray((n_simulations),dtype=TimeSeries)
    if args.verbose:   print("Injecting signals...")
    for i in range(n_simulations):
        if args.timing:
            start = time.perf_counter()
        
        a = TimeSeries(np.zeros(args.signal_length, dtype=np.float32),
                        epoch=args.epoch, delta_t=1.0/args.delta_f)
        injector.apply(a, 'H1', simulation_ids=[i])
        signal[i] = a*args.DNRF
        if args.verbose and (i+1)%args.monitor_rate==0:
            s = f"\r{i+1} signals injected."
            if args.timing:
                elapsed = time.perf_counter()-start
                remaining = (n_simulations-i)*elapsed
                hrs = remaining//3600
                mins = (remaining%3600)//60
                sec = ((remaining%3600)%60)
                time_str = f" ETA: {hrs:.0f}h{mins:.0f}m{sec:.0f}s" 
                filled = len(s)+len(time_str)
                s += (70-filled)*'.'
                s += time_str
            print(s, end='')
    return signal


if __name__ == "__main__":
    
    injfile = args.injfile
    if args.verbose:
        print("Loaded injection file...")

    with h5py.File(args.output_file, 'w') as f:
        with h5py.File(injfile, 'r') as f1:
            for i in f1.attrs['static_args']:
                f['static_args/'+ i] = f1.attrs[i]
            for i in f1.keys():
                f['parameters/' + i] = f1[i][()]
            if args.verbose: print("Parameters: ", f1.keys())
        injector = InjectionSet(injfile)
        n_simulations = len(injector.table)
        items = (injector, args, n_simulations) 
        signal = injection_to_signal(items)
        #------ got signal


        if args.add_noise:
            noisysignal = np.ndarray((n_simulations),dtype=TimeSeries)
            samples_length = len(signal[0])
            with h5py.File(args.noise_file, 'r') as f2:
                noise = f2["noise"][()]
            indices = np.random.choice(list(range(len(noise)-samples_length)), size = n_simulations)
            for i in range(n_simulations):
                noisysignal[i] = signal[i] + noise[indices[i]:indices[i]+samples_length]
            signal = noisysignal
        if args.snr:
            snrs = np.zeros(n_simulations)
            f_low = 10.0
            flen = int(2048/.25) + 1
            psd_series = psd.aLIGOZeroDetHighPower(flen,signal[0].delta_f,f_low)*args.DNRF**2
            for i in range(n_simulations):
                snrs[i] = filter.sigma(noisysignal[i],
                                                psd=psd_series,low_frequency_cutoff=f_low)
            print(snrs)
            f['snrs'] = snrs
            
        f['signals'] = [each.numpy() for each in signal]
    if args.verbose:
        print("\nDone.")
