import numpy as np
from dlsio import pyio # @UnresolvedImport

DEFAULT_BL_DIR = "/dls/i11/data"

def find_mythen_files(scan, visit=None, year=None, bl_dir=DEFAULT_BL_DIR, ending=("mac[-_][0-9]*.dat", "mythen[-_][0-9]*.dat")):
    return pyio.find_scan_files(scan, bl_dir, visit=visit, year=year, ending=ending)

def rebin(mashed, angle, delta, summed, files, progress=None, weights=True):
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

    abeg = (max(0, amin - angle) // delta) * delta + angle
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
        if progress:
            progress.setValue(progress.value() + 1)
            if progress.wasCanceled():
                break

        min_index = np.searchsorted(a, abeg) # slice out angles below start
        if min_index > 0:
            a = a[min_index:]
            c = c[min_index:]
            e = e[min_index:]

        # need to linearly interpolate?
        inds = np.floor((a - abeg + 0.5*delta) / delta).astype(np.int)
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
            if wmax > 0:
                mul  = np.where(nnweight == 0, 0, wmax/nnweight)
                nresult[1:3] *= mul
            else:
                nresult[1:3] *= 0
            nresult[2] = np.sqrt(nresult[2])
            _save_file(files[i], nresult, weights)
            
    # correct for lower weights
    wmax = nweight.max()
    mul  = np.where(nweight == 0, 0, wmax/nweight)
    result[1:3] *= mul
    return result

def load_all(files, visit, year, progress=None):
    data = []
    found = []
    for f in files:
        if progress:
            progress.setValue(progress.value() + 1)
            if progress.wasCanceled():
                break
        try:
            d = pyio.load(f)
            data.append(d)
            found.append(f)
        except:
            nfiles = find_mythen_files(int(f), visit=visit, year=year)
            dl = [pyio.load(f) for f in nfiles]
            data.extend(dl)
            found.extend(nfiles)
    return data, found

import os.path as path
import os
def parse_metadata(f):
    import re
    mythen_reg = r'^\d+[-_](mac|mythen)[-_]\d*\.dat$' # Unused
    dir, dat_file = path.split(f)
    d = pyio.load(f)
    mythen_files = []
    for k in d.keys():
        if k is not 'metadata':
            for v in d[k]:
                match = re.match(r'.*\.dat', str(v))
                if match: mythen_files.append(path.join(dir, match.group(0)))

    if not mythen_files: 
        print 'WARNING: The file %s contains no names of .dat files' % f
    return mythen_files

def parse_metadata_and_load(files):
    nfiles = parse_metadata(files)
    data = load_all(nfiles, visit=None, year=None)[0]
    return data, nfiles

def preserve_filesystem(dpath, output):
    dpath = path.realpath(dpath)
    def split_at_visit(dpath): # Split at the visit directory by finding the first /data/ directory
        spath = dpath.split('/')
        try:
            di = spath.index('data')
        except ValueError:
            print 'Cannot save the data into a directory data/year/visit/processed/ if input is not under data/year/visit/'
            raise
        br = di + 3
        dir, file = '/'.join(spath[:br]), '/'.join(spath[br:])
        return dir, file

    data_dir, file = split_at_visit(dpath)
    local_dir, file = path.split(file)
    out = path.join(data_dir, 'processed/' + local_dir) + '/'

    if output: out = path.join(out, output)
    out_dir = path.split(out)[0]
    if not path.exists(out_dir):
        os.makedirs(out_dir)
    return out


def process_and_save(data, angle, delta, rebinned, summed, files, output, progress=None, weights=True):
    mashed = [ (d[0], d[1], np.square(d[2])) for d in data ]

    if output:
        out_dir, fname = path.split(output)
        i = fname.rfind(".")
        ext = fname[i:] if i >= 0 else ''
        prefix = path.join(out_dir, fname[:i]) if i >= 0 else output
    else:
        out_dir = ''

    # format of delta in output filenames 
    sd = "%03d" % int(1000*delta) if delta > 1 else ("%.3f" % delta).replace('.', '')

    nfiles = []
    fbases = []
    # work out prefix and new rebin file names
    for f in files:
        _h, t  = path.split(f)
        i = t.rfind("-") # find and use tail only
        j = t.rfind("_") # find and use tail only
        if j > i:
            i = j
        if i >= 0:
            fbase = t[:i]
            t = t[i:]
            fbases.append(fbase)
        if rebinned:
            i = t.rfind(".") # find extension
            if i >= 0:
                e = t[i:]
                t = t[:i]
            else:
                e = None
            t += '_reb_' + sd # append delta
            if e: # append extension
                t += e
            nfiles.append(path.join(out_dir, fbase + t))


    result = rebin(mashed, angle, delta, summed, nfiles, progress, weights)
    if summed and (progress is None or not progress.wasCanceled()):
        result[2] = np.sqrt(result[2])
        # Work out an output filename of summed data 
        # It should be possible to determine which files where used by the name of the output file
        if not output or not path.split(output)[1]:
            fbase = set(fbases)
            if len(fbase) is 1: # If all the prefixes are identical just use it
                prefix = fbase.pop()
            else:
                prefix = '_'.join([path.splitext(path.split(f)[1])[0] for f in files])
            ext =  path.splitext(files[0])[1] # Use the filename extension of the first file
            prefix = path.join(out_dir, prefix)

        summed_out = prefix + '_summed_' + sd + ext
        _save_file(summed_out, result, weights)

    return prefix

def report_processing(files, output, angle, deltas):
    # report processing as txt file
    h, t  = path.split(output)
    i = t.rfind(".")
    t = t[:i] if i >= 0 else t
    proc = path.join(h, t + ".txt")

    try:
        p = open(proc, "w")
        p.write("# Output starting at %f with bin sizes: " % angle)
        for delta in deltas[:-1]:
            p.write("%f,  " % delta) 
        p.write("%f\n" % deltas[-1])
        p.write("# Used files:\n")
        for f in files:
            p.write("#    %s\n" % f)
    finally:
        p.close()


def process_and_save_all(data, angle, deltas, rebinned, summed, files, output, progress=None, weights=True):

    prefix = ''
    for delta in deltas:
        prefix = process_and_save(data, angle, delta, rebinned, summed, files, output, progress=None, weights=True)

    if not output:
        output = prefix
    if output.endswith('/'):
        output = output + 'out'
    report_processing(files, output, angle, deltas) 


def _save_file(output, result, fourth=True):
    if fourth:
        np.savetxt(output, result.T, fmt=["%f", "%f", "%f", "%d"])
    else:
        np.savetxt(output, result[:3,].T, fmt=["%f", "%f", "%f"])

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
