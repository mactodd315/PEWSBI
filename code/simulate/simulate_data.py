from  pycbc.inject import InjectionSet
from pycbc.types import TimeSeries, zeros
import argparse, h5py
import numpy as np
from multiprocessing import Pool

####################################################################################################
parser = argparse.ArgumentParser(
                    prog = "Create Simulation Data: ",
                    description = "Takes in injection file and simulates a desired number of signals with specified parameters.",
                    )

parser.add_argument("injfile", type=str,
                   help="Path to the injection file, should be .hdf format.")
parser.add_argument("output_file", type=str,
                    help = "Path for output file to be written, should be .hdf format.")
parser.add_argument("--signal-length", type=int, default = 4096)
parser.add_argument("--delta-f", type=int, default = 1024)
parser.add_argument("--epoch", type=float, default = 0)
parser.add_argument("-v", "--verbose", action="store_true", default=False)
parser.add_argument("--monitor-rate", type=int, default=10)
parser.add_argument("--pool-number", type=int, default=1)

args = parser.parse_args()
####################################################################################################
def injection_to_signal(injection, args):
    signal = np.zeros((ninjections,args.signal_length))
        if args.verbose:   print("Injecting signals...")
        for i in range(ninjections):
            a = TimeSeries(zeros(args.signal_length), epoch=args.epoch, delta_t=1.0/args.delta_f)
            injector.apply(a, 'H1', simulation_ids=[i])
            signal[i,:] = a
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
            with Pool(args.pool_number) as pool:
                sub_injection_size = len(f1[f1.keys()[0]])//args.pool_size
                injector = InjectionSet(injfile)
                signals = pool.map(injection_to_signal, injections_list)



        injector = InjectionSet(injfile)
        ninjections = len(injector.table)


            signal = np.zeros((ninjections,args.signal_length))
            if args.verbose:
                print("Injecting signals...")
            for i in range(ninjections):
                if args.verbose and i%args.monitor_rate == 0:
                    print(str(i) + " signals injected...")
                a = TimeSeries(zeros(args.signal_length), epoch=args.epoch, delta_t=1.0/args.delta_f)
                injector.apply(a, 'H1', simulation_ids=[i])
                signal[i,:] = a

            f['signals'] = signal
    if args.verbose:
        print("Done.")
