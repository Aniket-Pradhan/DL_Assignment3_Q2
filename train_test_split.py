import os
import math
import shutil
import random
import argparse

def checkandcreatedir(pathdir):
    if not os.path.exists(pathdir):
        os.makedirs(pathdir)

def main():
    parser = argparse.ArgumentParser(description='Storing images in a well structured way')
    parser.add_argument('-d', '--datadir', type=str, required=True,
                        help='Path to the data files')
    parser.add_argument('-o', '--outdir', required=False, default="./",
                        help='Path to output pickle file')
    parser.add_argument('-s', '--split-size', required=False, default=0.2,
                        help='Split ratio as compared to total classes')
    args = parser.parse_args()

    datadir = args.datadir
    outdir = args.outdir
    split_size = float(args.split_size)

    traindir = os.path.join(outdir, "train")
    testdir = os.path.join(outdir, "test")
    valdir = os.path.join(outdir, "val")

    checkandcreatedir(traindir)
    checkandcreatedir(testdir)
    checkandcreatedir(valdir)

    classes = os.listdir(datadir)
    no_classes = len(classes)
    split_size = math.floor(no_classes * split_size)

    test_classes = random.sample(classes, k=split_size)
    classes = [x for x in classes if x not in test_classes]
    val_classes = random.sample(classes, k=split_size)
    train_classes = [x for x in classes if x not in val_classes]

    for x in train_classes:
        orig_path = os.path.join(datadir, x)
        new_path = os.path.join(traindir, x)
        shutil.move(orig_path, new_path)
    
    for x in test_classes:
        orig_path = os.path.join(datadir, x)
        new_path = os.path.join(testdir, x)
        shutil.move(orig_path, new_path)
    
    for x in val_classes:
        orig_path = os.path.join(datadir, x)
        new_path = os.path.join(valdir, x)
        shutil.move(orig_path, new_path)

if __name__ == "__main__":
    main()
