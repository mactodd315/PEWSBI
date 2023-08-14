from  pycbc.inject import InjectionSet
from pycbc.types import TimeSeries, zeros
import argparse, h5py
import numpy as np

parser = argparse.ArgumentParser(
                    prog = "Create Simulation Data: ",
                    description = "Takes in injection file and simulates a desired number of signals with specified parameters.",
                    )

parser.add_argument("injfile", type=str,
                   help="Path to the injection file, should be .hdf format.")
parser.add_argument("output_file", type=str,
                    help = "Path for output file to be written, should be .hdf format.")
parser.add_argument("--signal-length", type=float, default = 4096)
parser.add_argument("--delta-f", type=int, default = 1024)
parser.add_argument("--epoch", type=float, default = 0)
parser.add_argument("-v", "--verbose", action="store_true", default=False)
parser.add_argument("--monitor-rate", type=int, default=10)


args = parser.parse_args()


injfile = args.injfile
if args.verbose:
    print("Loaded injection file...")
with h5py.File(injfile, 'r') as f1:
    injector = InjectionSet(injfile)
    ninjections = len(injector.table)

    with h5py.File(args.output_file, 'w') as f:
        for i in f1.attrs['static_args']:
            f['static_args/'+ i] = f1.attrs[i]
        for i in f1.keys():
            f['parameters/' + i] = f1[i][()]
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
