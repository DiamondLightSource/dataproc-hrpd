#!/usr/bin/env python

import scisoftpy as np
import numpy as np2


def find_mythen_files(scan, visit=None, year=None, bl_dir='/dls/i11/data', ending=('mac-[0-9]*.dat', 'mythen-[0-9]*.dat')):
    return np.io.find_scan_files(scan, bl_dir, visit=visit, year=year, ending=ending) #@UndefinedVariable

def rebin(mashed, angle, delta, summed, files):
    '''
    mashed is list of tuples of 3 1-D arrays (angle, count, squared error)
    '''
    amin = 360
    amax = 0
    for a, _c, _e in mashed:
        t = a.min()
        if t < amin:
            amin = t
        t = a.max()
        if t > amax:
            amax = t

    abeg = ((amin - angle) // delta) * delta + angle
    aend = (((amax - angle) // delta) + 1) * delta + angle
    from math import ceil
    alen = int(ceil((aend - abeg)/delta))
    result = np.zeros((4, alen), dtype=np.float)
    result[0] = abeg + np.arange(alen) * delta
    cresult = result[1]
    eresult = result[2]
    nweight = result[3]

    a = mashed[0][0]
    d = (a[1:] - a[:-1]).min() # smallest change in angle
    assert d > 0
    use_sum = d * 10 < delta
    for i, (a, c, e) in enumerate(mashed):
        # need to linearly interpolate?
        inds = ((a - abeg) // delta).astype(np.int)
        nlen = inds.ptp() + 1
        nbeg = inds.min()
        nresult = np.zeros((4, nlen), dtype=np.float)
        nresult[0] = abeg + (nbeg + np.arange(nlen)) * delta
        ncresult = nresult[1]
        neresult = nresult[2]
        nnweight = nresult[3]
        if use_sum:
            finds = np.where(inds[1:] > inds[:-1])[0] + 1
            # use first occurrences to slice and sum
            fb = 0
            for f in finds: # 
                fa = fb
                fb = f
                u = inds[fa] - nbeg
                ncresult[u] += c[fa:fb].sum()
                neresult[u] += e[fa:fb].sum()
                nnweight[u] += fb - fa
            fa = fb
            fb = a.size
            u = inds[fa] - nbeg
            ncresult[u] += c[fa:fb].sum()
            neresult[u] += e[fa:fb].sum()
            nnweight[u] += fb - fa
        else:
            for j,u in enumerate(inds):
                nu = u - nbeg
                ncresult[nu] += c[j]
                neresult[nu] += e[j]
                nnweight[nu] += 1
        if summed:
            nend = inds.max() + 1
            cresult[nbeg:nend] += ncresult
            eresult[nbeg:nend] += neresult
            nweight[nbeg:nend] += nnweight

        if files:
            # save
            wmax = nnweight.max()
            mul  = np.where(nnweight == 0, 0, wmax/nnweight)
            nresult[1:3] *= mul
            nresult[2] = np.sqrt(nresult[2])
            np2.savetxt(files[i], nresult.T, fmt=['%f', '%f', '%f', '%d']) #@UndefinedVariable
            
    # correct for lower weights
    wmax = nweight.max()
    mul  = np.where(nweight == 0, 0, wmax/nweight)
    result[1:3] *= mul
    return result

def load_all(files, visit, year):
    data = []
    found = []
    for f in files:
        try:
            d = np.io.load(f, format='srs') #@UndefinedVariable
            data.append(d)
            found.append(f)
        except:
            nfiles = find_mythen_files(int(f), visit=visit, year=year)
            dl = [np.io.load(f, format='srs') for f in nfiles] #@UndefinedVariable
            data.extend(dl)
            found.extend(nfiles)
    return data, found

def process_and_save(data, angle, delta, summed, files, output):
    mashed = [ (d[0], d[1], np.square(d[2])) for d in data ]

    nfiles = None
    if files: # work out prefix and new file names
        import os.path as path
        h, t = path.split(output)
        i = t.rfind('.')
        prefix = path.join(h, t[:i]) if i >= 0 else output

        nfiles = []
        for f in files:
            _h, t  = path.split(f)
            i = t.rfind('-')
            if i >= 0:
                nfiles.append(prefix + t[i:])
            else:
                nfiles.append(prefix + t)

    result = rebin(mashed, angle, delta, summed, nfiles)
    if summed:
        result[2] = np.sqrt(result[2])
        np2.savetxt(output, result.T, fmt=['%f', '%f', '%f', '%d']) #@UndefinedVariable

def parse_range_list(lst):
    '''Parse a string like 0,2-7,20,35-9
    and return a list of integers [0,2,3,4,5,6,7,20,35,36,37,38,39]
    '''
    ranges = [l.split("-") for l in lst.split(",")]
    values = []
    import math
    for r in ranges:
        a = int(r[0])
        b = int(r[-1])
        if b < a:
            d = math.ceil(math.log10(b))
            f = int(math.pow(10, d))
            b += (a // f) * f
        values.extend(range(a,b+1))
    return values

def _main(args):
    from optparse import OptionParser
    parser = OptionParser()
    parser.usage = '%prog [options] file1 file2 (or scan numbers)'
    parser.description = 'This script will load, sum and rebin a set of PSD data files'
    parser.add_option('-a', '--angle', action='store', type='float', dest='angle', default=0., help='Specify 2theta angle for a bin edge, in degrees')
    parser.add_option('-d', '--delta', action='store', type='float', dest='delta', default=0.1, help='Specify 2theta bin size, in degrees')
    parser.add_option('-r', '--rebin', action='store_true', dest='rebin', default=False, help='Output rebinned data')
    parser.add_option('-R', '--no-rebin', action='store_false', dest='rebin', help='Do not output rebinned data [default]')
    parser.add_option('-s', '--sum', action='store_true', dest='sum', default=True, help='Output summed data [default]')
    parser.add_option('-S', '--no-sum', action='store_false', dest='sum', help='Do not output summed data')
    parser.add_option('-v', '--visit', action='store', type='string', dest='visit', default=None, help='Visit ID')
    parser.add_option('-y', '--year', action='store', type='int', dest='year', default=None, help='Year')
    parser.add_option('-o', '--output', action='store', type='string', dest='output', default='out.dat', help='Output file')

    opts, files = parser.parse_args(args)

    data, nfiles = load_all(files, visit=opts.visit, year=opts.year)
    if not opts.rebin:
        nfiles = None
    process_and_save(data, opts.angle, opts.delta, opts.sum, nfiles, opts.output)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        _main(sys.argv[1:])
    else:
        _main(['-h'])
#         _main(['-v', 'cm2060-1', '-y', '2011', '-a', '0', '-d', '0.05', '78348'])

