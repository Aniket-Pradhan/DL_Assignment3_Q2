import os
import sys
import h5py
import pickle
import argparse
import numpy as np
import matplotlib.pyplot as plt

from progressbar import progressbar


"""
with open('filename.pickle', 'wb') as handle:
    pickle.dump(a, handle, protocol=pickle.HIGHEST_PROTOCOL)

with open('filename.pickle', 'rb') as handle:
    b = pickle.load(handle)
"""

def checkandcreatedir(pathdir):
    if not os.path.exists(pathdir):
        os.makedirs(pathdir)

def main():
    parser = argparse.ArgumentParser(description='Storing images in a well structured way')
    parser.add_argument('-d', '--datadir', type=str, required=True,
                        help='Path to the data files')
    parser.add_argument('-o', '--outdir', required=False, default="./",
                        help='Path to output pickle file')
    args = parser.parse_args()

    datadir = args.datadir
    outdir = args.outdir

    outdir = os.path.join(outdir, "raw_data")
    checkandcreatedir(outdir)

    files = os.listdir(datadir)

    for file in progressbar(files):
        if ".mat" not in file:
            continue
        filepath = os.path.join(datadir, file)
        _outfilepath = os.path.join(outdir, file.split(".")[0])
        checkandcreatedir(_outfilepath)
        try:
            with h5py.File(filepath, 'r') as f:
                sprites = f.get('sprites')[()]
                for i, pose_i in enumerate(sprites):
                    pose_i = f[pose_i[0]][()]
                    for j, pose_j in enumerate(pose_i):
                        outfile = "{}_{}.png".format(i, j)
                        outfilepath = os.path.join(_outfilepath, outfile)
                        pose_j = pose_j.reshape((60, 60, 3), order='F')
                        plt.imsave(outfilepath, pose_j)
        except OSError:
            print("Corrupt file: {}".format(file))


if __name__ == "__main__":
    main()
