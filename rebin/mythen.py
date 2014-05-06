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

def process_and_save(data, angle, delta, summed, files, output, progress=None, weights=True):
    mashed = [ (d[0], d[1], np.square(d[2])) for d in data ]
    import os.path as path

    nfiles = None
    if files: # work out prefix and new file names
        h, t = path.split(output)
        i = t.rfind(".")
        prefix = path.join(h, t[:i]) if i >= 0 else output

        nfiles = []
        for f in files:
            _h, t  = path.split(f)
            i = t.rfind("-") # find and use tail only
            j = t.rfind("_") # find and use tail only
            if j > i:
                i = j
            if i >= 0:
                t = t[i:]
            i = t.rfind(".") # find extension
            if i >= 0:
                e = t[i:]
                t = t[:i]
            else:
                e = None
            if delta < 1:
                t = "%s_reb_%03d" % (t, int(1000*delta))
            else:
                t = "%s_reb_%.3f" % (t, delta)
            if e: # append extension
                t += e

            nfiles.append(prefix + t)

    result = rebin(mashed, angle, delta, summed, nfiles, progress, weights)
    if summed and (progress is None or not progress.wasCanceled()):
        result[2] = np.sqrt(result[2])
        _save_file(output, result, weights)

    # report processing as txt file
    h, t  = path.split(output)
    i = t.rfind(".")
    t = t[:i] if i >= 0 else t
    proc = path.join(h, t + ".txt")

    try:
        p = open(proc, "w")
        p.write("# Output starting at %f with bin size of %f\n" % (angle, delta))
        p.write("# Used files:\n")
        for f in files:
            p.write("#    %s\n" % f)
    finally:
        p.close()

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
