
import os
import io
import numpy as np
from PIL import Image
import gzip
import re
import sys
import tarfile
import tensorflow.python.platform
from six.moves import urllib
from six.moves import xrange  # pylint: disable=redefined-builtin

size=(32,32)
RECORDLENGTH=3073
IMAGE_DIR="Desktop/images/"
BIN_DIR="Desktop/cifar-10-batches-bin/"
OUT_FILE="Desktop/insta_data.tar.gz"
BATCH_SIZE=1000
tags=[]


def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

if not os.path.exists(BIN_DIR):
    os.makedirs(BIN_DIR)

data_batch=open(BIN_DIR+'data_batch.bin','wb')
test_batch=open(BIN_DIR+'test_batch.bin','wb')

j=0
for root, dirs, files in os.walk(IMAGE_DIR, topdown=False):
    for name in files:
        if name=='.DS_Store': continue
        filepath=os.path.join(root, name)
        index=filepath.split('/')[-2]
        im = Image.open(filepath)
        im.thumbnail(size)
        background = Image.new('RGB', size, (255, 255, 255))
        background.paste(im,((size[0] - im.size[0]) / 2, (size[1] - im.size[1]) / 2))
        im=background
        imarr=np.asarray(im,dtype='int32')
        byarr=bytearray(RECORDLENGTH)
        byarr[0]=int(index)

        for i in range(0,RECORDLENGTH-1):
            byarr[i+1]=imarr[(i%1024)/32,i%32,i/1024]
        if filepath.split('/')[2]=='train':
            data_batch.write(byarr)
        else:
            test_batch.write(byarr)
        sys.stdout.write('\rCompressing picture\t'+str(j))
        sys.stdout.flush()
        j=j+1

data_batch.close()
test_batch.close()

make_tarfile(OUT_FILE,BIN_DIR)
