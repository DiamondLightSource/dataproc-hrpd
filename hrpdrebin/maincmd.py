"""
Command line interface for rebinner
"""

from . import mythen


def process(args):
    output = args.output
    if args.mythen:
        for file in args.files:
            data, nfiles = mythen.parse_metadata_and_load(file)
            if args.processed:
                output = mythen.preserve_filesystem(
                    nfiles[0], output
                )  # This wont work for files in different directories
            mythen.process_and_save_all(
                data,
                args.angle,
                args.delta,
                args.rebin,
                args.sum,
                nfiles,
                output,
                weights=args.weights,
                ext=args.ext,
            )
    else:
        data, nfiles = mythen.load_all(args.files, visit=args.visit, year=args.year)
        if args.processed:
            output = mythen.preserve_filesystem(nfiles[0], output)
        mythen.process_and_save_all(
            data,
            args.angle,
            args.delta,
            args.rebin,
            args.sum,
            nfiles,
            output,
            weights=args.weights,
            ext=args.ext,
        )


def main(args=None):
    from argparse import ArgumentParser

    parser = ArgumentParser(
        usage="%(prog)s [options] file1 file2 (or scan numbers)",
        description="This script will load, sum and rebin a set of PSD/MAC data files",
        prefix_chars="-+",
    )
    parser.add_argument(
        "-e",
        "--ext",
        action="store",
        dest="ext",
        default=None,
        help="File extension to use for saving",
    )
    parser.add_argument(
        "-a",
        "--angle",
        action="store",
        type=float,
        dest="angle",
        default=0.0,
        help="Specify 2theta angle for a bin edge, in degrees",
    )
    parser.add_argument(
        "-d",
        "--delta",
        action="append",
        type=float,
        dest="delta",
        default=None,
        help="Specify 2theta bin size, in degrees",
    )
    parser.add_argument(
        "-r",
        "--rebin",
        action="store_true",
        dest="rebin",
        default=False,
        help="Output rebinned data",
    )
    parser.add_argument(
        "+r",
        "--no-rebin",
        action="store_false",
        dest="rebin",
        help="Do not output rebinned data [default]",
    )
    parser.add_argument(
        "-s",
        "--sum",
        action="store_true",
        dest="sum",
        default=True,
        help="Output summed data [default]",
    )
    parser.add_argument(
        "+s",
        "--no-sum",
        action="store_false",
        dest="sum",
        help="Do not output summed data",
    )
    parser.add_argument(
        "-v", "--visit", action="store", dest="visit", default=None, help="Visit ID"
    )
    parser.add_argument(
        "-y", "--year", action="store", type=int, dest="year", default=None, help="Year"
    )
    parser.add_argument(
        "-o",
        "--output",
        action="store",
        dest="output",
        default=None,
        help="Output file",
    )
    parser.add_argument(
        "-p",
        "--processed",
        action="store_true",
        dest="processed",
        default=None,
        help='Saves to "processed" directory',
    )
    parser.add_argument(
        "-m",
        "--mythen",
        action="store_true",
        dest="mythen",
        default=False,
        help="Searches a .dat file for mythen files to rebin",
    )
    parser.add_argument(
        "-w",
        "--weights",
        action="store_true",
        dest="weights",
        default=False,
        help="Include weights column",
    )
    parser.add_argument("files", nargs="+")
    args = parser.parse_args(args)
    if not args.delta:
        args.delta = [0.1]  # default delta value

    process(args)


if __name__ == "__main__":
    #     main(['-v', 'cm2060-1', '-y', '2011', '-a', '0', '-d', '0.05', '78348'])
    main(["-v", "cm4962-3", "-y", "2014", "-a", "0", "-d", "0.004", "-r", "320466"])
