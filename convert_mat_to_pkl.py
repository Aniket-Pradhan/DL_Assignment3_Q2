import os
import sys
import h5py
import pickle
import argparse
import numpy as np

from progressbar import progressbar


"""
with open('filename.pickle', 'wb') as handle:
    pickle.dump(a, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('filename.pickle', 'rb') as handle:
    b = pickle.load(handle)
"""
def save_file(obj, path):
    with open(path, 'wb') as handle:
        pickle.dump(obj, handle, protocol=pickle.HIGHEST_PROTOCOL)

def checkandcreatedir(pathdir):
    if not os.path.exists(pathdir):
        os.makedirs(pathdir)

def main():
    parser = argparse.ArgumentParser(description='Storing images in a well structured way')
    parser.add_argument('-d', '--datadir', type=str, required=True,
                        help='Path to the data files')
    parser.add_argument('-o', '--outdir', required=False, default="./"
                        help='Path to output pickle file')
    parser.add_argument('-n', '--outname', required=False, default="sprites.pkl"
                        help='Name for the output pickle file')

    args = parser.parse_args()

    datadir = args.datadir
    outdir = args.outdir
    outfile = args.outname

    checkandcreatedir(outdir)

    rawdata = {}

    files = os.listdir(datadir)

    for file in progressbar(files):
        rawdata[file] = []
        filepath = os.path.join(datadir, file)

        with h5py.File(filepath, 'r') as f:
            sprites = f.get('sprites')[()]
            for s in sprites:
                s = f[s[0]][()]
                for ss in s:
                    ss = ss.reshape((60, 60, 3), order='F')
                    rawdata[file].append(ss)

    outfile = os.path.join(outdir, outfile)
    save_file(rawdata, outfile)

if __name__ == "__main__":
    main()
