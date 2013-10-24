
import scisoftpy as dnp


def load_mythen_files(scan, visit=None, year=None, bl_dir='/dls/i11/data', ending=('mythen-[0-9]*.dat')):
    files = dnp.io.find_scan_files(scan, bl_dir, visit=visit, year=year, ending=ending) #@UndefinedVariable
    return [dnp.io.load(f, format='srs') for f in files] #@UndefinedVariable

def rebin(mashed, angle, delta):
    amin = 360
    amax = 0
    for a in mashed:
        m = a[0].min()
        if m < amin:
            amin = m
        m = a[0].max()
        if m > amax:
            amax = m

    abeg = ((amin - angle) // delta) * delta + angle
    aend = (((amax - angle) // delta) + 1) * delta + angle
    from math import ceil
    alen = int(ceil((aend - abeg)/delta))
    result = dnp.zeros((4, alen), dtype=dnp.float)
    result[0] = abeg + dnp.arange(alen) * delta
    nweights = result[3]

    for m in mashed:
        # need to check angle step?
        # need to linearly interpolate?
        inds = ((m[0] - abeg) // delta).astype(dnp.int)
        for i in range(inds.size):
            idx = inds[i]
            result[1, idx] += m[1, i]
            result[2, idx] += m[2, i]
            nweights[idx] += 1

    # correct for lower weights
    wmax = nweights.max()
    mul  = dnp.where(nweights == 0, nweights, wmax/nweights)
    result[1:3] *= mul
    return result

def _main(args):
    from optparse import OptionParser
    parser = OptionParser()
    parser.usage = '%prog [options] file1 file2 (or scan numbers)'
    parser.description = 'This script will load, sum and rebin a set of PSD data files'
    parser.add_option('-a', '--angle', action='store', type='float', dest='angle', default=0., help='Specify 2theta angle for a bin edge, in degrees')
    parser.add_option('-d', '--delta', action='store', type='float', dest='delta', default=0.1, help='Specify 2theta bin size, in degrees')
    parser.add_option('-v', '--visit', action='store', type='string', dest='visit', default=None, help='Visit ID')
    parser.add_option('-y', '--year', action='store', type='int', dest='year', default=None, help='Year')
    parser.add_option('-o', '--output', action='store', type='string', dest='output', default='out.dat', help='Output file')

    opts, files = parser.parse_args(args)

    data = []
    for f in files:
        try:
            d = dnp.io.load(f, format='srs') #@UndefinedVariable
            data.append(d)
        except:
            dl = load_mythen_files(int(f), visit=opts.visit, year=opts.year)
            data.extend(dl)

    mashed = [ dnp.vstack((d[0],d[1],dnp.square(d[2]))) for d in data ]
    result = rebin(mashed, opts.angle, opts.delta)
    result[2] = dnp.sqrt(result[2])
    import numpy as np
    np.savetxt(opts.output, result.T, fmt=['%f', '%f', '%f', '%d']) #@UndefinedVariable

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        _main(sys.argv[1:])
    else:
        _main(['-v', 'cm2060-1', '-y', '2011', '-a', '0', '-d', '0.05', '78348'])
