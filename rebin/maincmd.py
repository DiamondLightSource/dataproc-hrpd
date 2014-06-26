'''
Command line interface for rebinner
'''

import mythen

def main(args=None):
    from argparse import ArgumentParser
    parser = ArgumentParser(usage= '%(prog)s [options] file1 file2 (or scan numbers)',
                            description='This script will load, sum and rebin a set of PSD/MAC data files',
                            prefix_chars='-+')
    parser.add_argument('-a', '--angle', action='store', type=float, dest='angle', default=0., 
            help='Specify 2theta angle for a bin edge, in degrees')
    binning = parser.add_mutually_exclusive_group()
    binning.add_argument('-d', '--delta', action='store', type=float, dest='delta', default=0.1, help='Specify 2theta bin size, in degrees')
    binning.add_argument('-b', '--bin-ratio', action='append', type=float, dest='bin_ratios', 
            help='The number of bins in the input per bin in the result')
    binning.add_argument('-b235', action='store_true', default=False, help='Equivalent to "-b 2 -b 3 -b 5"')

    parser.add_argument('-r', '--rebin', action='store_true', dest='rebin', default=False, help='Output rebinned data')
    parser.add_argument('+r', '--no-rebin', action='store_false', dest='rebin', help='Do not output rebinned data [default]')
    parser.add_argument('-s', '--sum', action='store_true', dest='sum', default=True, help='Output summed data [default]')
    parser.add_argument('+s', '--no-sum', action='store_false', dest='sum', help='Do not output summed data')
    parser.add_argument('-v', '--visit', action='store', dest='visit', default=None, help='Visit ID')
    parser.add_argument('-y', '--year', action='store', type=int, dest='year', default=None, help='Year')
    parser.add_argument('-o', '--output', action='store', dest='output', default='out.dat', help='Output file')
    parser.add_argument('files', nargs='+')
    args = parser.parse_args(args)

    data, nfiles = mythen.load_all(args.files, visit=args.visit, year=args.year)

    if args.b235: args.bin_ratios = [2., 3., 5.]

    if not args.bin_ratios:
        mythen.process_and_save(data, args.angle, args.delta, args.sum, nfiles, args.output)
    else:
        mythen.process_and_save_all(data, args.angle, args.bin_ratios, args.sum, nfiles, args.output)

if __name__ == '__main__':
    main(['-v', 'cm2060-1', '-y', '2011', '-a', '0', '-d', '0.05', '78348'])
