'''
This program reads tags from instagram post json files, matches them with their respective tagged images into a .bin file with
cifar1o format.
'''
import os
import io
import numpy as np
import struct
from PIL import Image
from array import array
import gzip
import re
import sys
import tarfile
import tensorflow.python.platform
from six.moves import urllib
from six.moves import xrange  # pylint: disable=redefined-builtin
import tensorflow as tf
import json
from pprint import pprint
size=(32,32)
print os.getcwd()
IMAGE_DIR="Desktop/images/"
BIN_DIR="Desktop/cifar-10-batches-bin/"
if not os.path.exists(BIN_DIR):
    os.makedirs(BIN_DIR)
OUT_FILE="Desktop/insta_data.tar.gz"
j=0
tags=[]


def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

tags=[]

for d in os.listdir(IMAGE_DIR):
    if d != '.DS_Store':
        print "\nOpen directory",d,'\n'
        f=open(BIN_DIR+d+".bin",'wb')
        j=0
        for root, dirs, files in os.walk(IMAGE_DIR+d):
            for dir in dirs:
                for name in files:
                    print '\n',dir,name
                sys.stdout.write('\r>> Compressing %s %.1f%%' % (d,
                    float(j) / float(10000) * 100.0))
                sys.stdout.flush()

                '''if ',' in name:
                    tag=name.split(',')[0]
                else:
                    tag=name.split('_')[0]'''
                '''
                if tag not in tags:
                    tags.append(tag)
                index=tags.index(tag)
                im = Image.open(root+'/'+name)
                imarr=np.asarray(im,dtype='int32')
                byarr=bytearray(3073)
                byarr[0]=int(index)
                for i in range(0,len(byarr)-1):
                    byarr[i+1]=imarr[(i%1024)/32,i%32,i/1024]
                f.write(byarr)'''
                j=j+1

            f.close

make_tarfile(OUT_FILE,BIN_DIR)
