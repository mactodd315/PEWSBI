from  pycbc.inject import InjectionSet
from pycbc.types import TimeSeries, zeros
import argparse, h5py

parser = argparse.ArgumentParser(
                    prog = "Create Simulation Data: ",
                    description = "Takes in injection file and simulates a desired number of signals with specified parameters.",
                    )

parser.add_argument("injfile", type=str,
                   help="Path to the injection file, should be .hdf format.")
parser.add_argument("output_file", type=str,
                    help = "Path for output file to be written, should be .hdf format.")
parser.add_argument("-n", "--ninjections", action="store_const", const = '43')
parser.add_argument("--signal-length", type=float, default = 4096)
parser.add_argument("--delta-f", type=int, default = 1024)


args = parser.parse_args()

print(args.delta_f)


injfile = args.injfile
with h5py.File(injfile, 'r') as f1:
    injector = InjectionSet(injfile)
    print(injector.table)

    with h5py.File(args.output_file, 'w') as f:
        signal = np.zeros(0)
        distances = twod_group.create_dataset("distances", data=distance_list)
        inclinations = twod_group.create_dataset("inclinations", data=inclination_list)

        for i in range(n_distance):
            a = TimeSeries(zeros(4096), epoch=-1.0, delta_t=1.0/1024)
            injector.apply(a, 'H1', simulation_ids=[i])
            waveforms[i,:] = a
            
        f['signals'] = signal
