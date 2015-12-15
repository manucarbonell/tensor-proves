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

from tensorflow.models.image.cifar10 import cifar10_input
from tensorflow.python.platform import gfile
size=(32,32)
DATA_URL = 'http://www.cs.toronto.edu/~kriz/cifar-10-binary.tar.gz'
data_dir='Desktop/data'

if not(os.path.exists(data_dir)):
    os.mkdir(data_dir)
    os.mkdir(data_dir+'/pictures')

def save_image( npdata, outfilename ) :
    img = Image.fromarray( np.asarray( np.clip(npdata,0,255), dtype="uint8"), "RGB" )
    img.thumbnail(size,Image.ANTIALIAS)
    img.save(outfilename)

def extract_data(url,data_dir):
    filename = DATA_URL.split('/')[-1]
    filepath = os.path.join(data_dir, filename)

    '''
    filepath, _ = urllib.request.urlretrieve(DATA_URL, filepath)
    print "downloaded"

    tarfile.open(filepath, 'r:gz').extractall(data_dir)
    print "extracted"'''
    for subdir, dirs, files in os.walk(data_dir):
        for file in files:
            if os.path.join(subdir, file).endswith(".bin"):
                batch=os.path.join(subdir, file)
                print "Introduce the maximum number of images to read from batch",batch.split('/')[-1]
                MAX_BYTES=3073*(int(raw_input()))
                i=0
                f = open(batch, "rb")
                im=np.zeros((32,32,3))
                while i<MAX_BYTES:
                    byte = f.read(1)

                    print len(byte)
                    try:
                        value = struct.unpack('B', byte)[0]
                    except ValueError:
                        print "Bad introduced byte",byte


                    if(i%3073==0):
                        name=str(value)
                        byte = f.read(1)
                        i=i+1
                    value = struct.unpack('B', byte)[0]

                    im[((i-i/3073)%1024)/32,(i-i/3073)%32,((i-i/3073)%3072)/1024]=value
                    i=i+1
                    if(i%3073==0):
                        save_image(im,data_dir+"/pictures/"+name+'_'+str(i)+".jpg")

extract_data(DATA_URL,data_dir)
