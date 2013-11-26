###
# Copyright 2011 Diamond Light Source Ltd.
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#   http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###

'''
'''

from dictutils import DataHolder

io_exception = IOError

class PythonLoader(object):
    def __init__(self, name, togrey=False):
        self.ascolour = not togrey
        self.name = name
        self.load_metadata = True

    def setloadmetadata(self, load_metadata):
        self.load_metadata = load_metadata

from re import compile as _compile
_begin_number = _compile(r'^[-+]?[\d]?\.?\d')

class SRSLoader(PythonLoader):
    '''
    Loads an SRS dat file and returns a dataholder object
    '''
    def load(self, warn=True):
        '''
        warn        -- if True (default), print warnings about key names

        Returns a DataHolder object
        '''

        f = open(self.name)
    
        try:
            header = False
            while True:
                l = f.readline()
                if not l:
                    raise io_exception, "End of file reached unexpectedly"
                ls = l.lstrip()
                if ls.startswith("&SRS") or ls.startswith("&DLS"):
                    header = True
                    break
                if _begin_number.match(ls):
                    break
            else:
                raise io_exception, "Not an SRS file"
    
            srstext = []
            if header:
                while True:
                    l = f.readline()
                    if not l:
                        raise io_exception, "End of file reached unexpectedly"
                    ls = l.strip()
                    if ls:
                        if ls.startswith("&END"):
                            break
                        if self.load_metadata:
                            srstext.append(ls)
                else:
                    raise io_exception, "No end tag found"
    
                l = f.readline()
                if not l:
                    raise io_exception, "End of file reached unexpectedly"
                colstext = l.strip()
                datatext = []
            else:
                colstext = None
                datatext = [ls]

            while True:
                l = f.readline()
                if not l:
                    break
                ls = l.lstrip()
                if _begin_number.match(ls):
                    datatext.append(ls)
                else:
                    break
    
            data = SRSLoader._parse_data(colstext, datatext, warn)
            metadata = SRSLoader._parse_head(srstext, warn)
    
            return DataHolder(data, metadata, warn)

        finally:
            f.close()

    @staticmethod
    def _parse_head(text, warn):
        '''
        Scan header lines and extract key/value pairs. A pair contains an equals sign
        '''
        srsmeta = []
        othermeta = []
        other = False
        mdtext = "MetaDataAtStart"
        for ls in text:
            i = ls.find(mdtext)
            if i >= 0:
                other = not other
                if other:
                    i += len(mdtext) + 1 # after right angle bracket
                    r = ls[i:].strip()
                    if len(r) > 0:
                        othermeta.append(r)
                else:
                    r = ls[:i-2].strip()
                    if len(r) > 0:
                        othermeta.append(r)
                    i += len(mdtext) + 1 # after right angle bracket
                    r = ls[i:].strip()
                    if len(r) > 0:
                        srsmeta.append(r)
                continue
            if other:
                othermeta.append(ls)
            else:
                srsmeta.append(ls)
        meta = []
        for m in srsmeta:
            ss = SRSLoader._parse_srsline(m, warn)
            for s in ss:
                meta.append(s)
        for m in othermeta:
            s = m.split('=',1)
            if len(s) == 1:
                raise io_exception, "Metadata did not contain equal sign: " + m
            meta.append((s[0], SRSLoader._parse_value(s[1])))
        return meta

    @staticmethod
    def _parse_srsline(line, warn):
        '''
        Scan a SRS header line of comma-separated key/value pairs
        '''
        meta = []
        if line.startswith("SRS"):
            ki = 0
            l = len(line)
            while ki < l:
                kf = line.find('=', ki)
                if kf > 0:
                    k = line[ki:kf]
                    vi = kf+1
                    nc = line.find(',', vi)
                    if nc < vi:
                        raise io_exception, "No comma found: " + line[vi:]
                    qi = line.find('\'', vi)
                    if qi > 0 and qi < nc:
                        if qi != vi:
                            raise io_exception, "Quoted string does not follow equal sign: " + line[qi:]
                        # inside quoted string
                        qf = line.find('\'', qi+1)
                        if qf > 0 and qf != (nc-1):
                            raise io_exception, "A comma does not follow a quoted string: " + line[qi:]

                    vf = nc
                    v = line[vi:vf]
                    meta.append((k, SRSLoader._parse_value(v)))
                    ki = nc+1
                else:
                    raise io_exception, "No equal sign on line: " + line[ki:]
        else:
            s = line.split('=',1)
            if len(s) == 1:
                raise io_exception, "Metadata did not contain equal sign: " + line
            meta.append((s[0], SRSLoader._parse_value(s[1])))
        return meta

    @staticmethod
    def _parse_data(cols, text, warn):
        '''
        Convert to all data to dictionary. Keys are column headers and values are
        1D NumPy arrays 
        '''
        import re
        cs_regex = re.compile('\s+')

        if cols is None:
            # use first line
            r = cs_regex.split(text[0].strip())
            lc = len(r)
            from math import log10, ceil
            p = ceil(log10(lc))
            fmt = 'col%%0%dd' % p
            cols = [ fmt % (i+1,) for i in range(lc) ]
        else:
            if cols.count('\t') > 0: # columns separated by tabs
                cols = cols.split('\t')
            else:
                cols = cs_regex.split(cols)
            lc = len(cols)
        data = [[] for dummy in cols]
        for t in text:
            r = cs_regex.split(t.strip())
            lr = len(r)
            if lr > lc:
                if warn:
                    print 'Long row!'
                lr = lc
            for i in range(lr):
                data[i].append(SRSLoader._parse_value(r[i]))

            if lr < lc:
                if warn:
                    print 'Short row!'
                for i in range(lr, lc):
                    data[i].append(0)

#         from pycore import array as parray
        from numpy import array
        return [(c, array(d)) for c, d in zip(cols, data)]

    @staticmethod
    def _parse_value(text):
        '''
        Convert to integer, float or string (strips outer quotes)
        '''
        try:
            v = int(text)
        except ValueError:
            try:
                v = long(text)
            except ValueError:
                try:
                    v = float(text)
                except ValueError:
                    if text.startswith('\''):
                        if text.endswith('\''):
                            v = text[1:-1]
                        else:
                            raise io_exception, "No matching single quotes in string: " + text
                    elif text.startswith('"'):
                        if text.endswith('"'):
                            v = text[1:-1]
                        else:
                            raise io_exception, "No matching double quotes in string: " + text
                    else:
                        v = text
        return v

class DLSLoader(SRSLoader):
    '''
    Loads a DLS dat file and returns a dataholder object
    '''
    def load(self, warn=True):
        '''
        warn        -- if True (default), print warnings about key names

        Returns a DataHolder object
        '''

        f = open(self.name)
    
        try:
            hdrtext = []
            while True:
                l = f.readline()
                if not l:
                    raise io_exception, "End of file reached unexpectedly"
                ls = l.strip()
                if ls:
                    if _begin_number.match(ls):
                        break
                    if ls.startswith("#"):
                        if self.load_metadata:
                            ls = ls[1:].strip()
                            if ls:
                                hdrtext.append(ls)
            else:
                raise io_exception, "No end tag found"

            colstext = hdrtext.pop()[1:].strip() if hdrtext else None
            datatext = [ls]
            while True:
                l = f.readline()
                if l:
                    ls = l.strip()
                    if ls.startswith("#"):
                        if self.load_metadata:
                            ls = ls[1:].strip()
                            if ls:
                                hdrtext.append(ls)
                    elif _begin_number.match(ls):
                        datatext.append(ls)
                else:
                    break
    
            data = self._parse_data(colstext, datatext, warn)
            metadata = self._parse_head(hdrtext, warn)
    
            return DataHolder(data, metadata, warn)

        finally:
            f.close()

    @staticmethod
    def _parse_head(text, warn):
        '''
        Scan header lines and extract key/value pairs. A pair contains a colon
        but value can be more key/value pairs containing an equals sign, separated by semi-colons
        '''
        dlsmeta = []
        othermeta = []
        for l in text:
            r = l.split(':')
            if len(r) == 1:
                othermeta.append(r)
            else:
                if len(r) > 2 and warn:
                    print 'Line has more than one colon:', l
                dlsmeta.append((r[0], l[len(r[0])+1:].strip()))
        return dlsmeta

import os as _os
_path = _os.path
_join = _path.join

def find_scan_files(scan, data_dir, visit=None, year=None, ending=".dat"):
    '''Find scan files in given data directory

    Looks for file in data_dir/year/visit/
    Arguments:
    scan      - scan number
    data_dir - beamline data directory, such as '/dls/i01/data'
    visit    - visit-ID, such as cm1234-1 (defaults to data_dir and its sub-directories)
    year     - calendar year (defaults to visit directory and any year in range 2000-99)
    ending   - suffix or list of suffices (defaults to '.dat')

    Returns list of files
    '''
    from glob import glob, iglob

    scan = str(scan)
    if data_dir is None:
        raise ValueError, 'Beamline data directory must be defined'

    if type(ending) is str:
        ending = (ending,)
    es = [ '*' + e for e in ending ]


    if year is None:
        years = (None, '20[0-9][0-9]')
    else:
        years = (str(year),)

    if visit is None:
        visits = (None, '*')
    else:
        visits = (visit,)

    files = []

    for y in years:
        if y is None:
            ds = (data_dir,)
        else:
            ds = glob(_join(data_dir, y))
        for d in ds:
            for v in visits:
                if v is None:
                    vs = (d,)
                else:
                    vs = glob(_join(d, v))
                for lv in vs:
                    for e in es:
                        files.extend(iglob(_join(lv, scan + e)))
                    if len(files) > 0:
                        break
                if len(files) > 0:
                    break

    if len(files) == 0:
        raise IOError, 'Scan files not found'
    return files

def load(name, warn=True):
    ldr = SRSLoader(name)
    ldr.setloadmetadata(True)
    lfh = ldr.load(warn=warn)
    return lfh

