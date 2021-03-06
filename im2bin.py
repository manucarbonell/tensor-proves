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

wd='Desktop'
METADATA_DIR=wd+"/CompleteInstagramDataSet/InstaMetadata"
IMAGE_DIR=wd+"/CompleteInstagramDataSet/InstaImages/"
THUMB_DIR=wd+"/thumbnails/"
BIN_DIR=wd+"/data/"
BIN_TRAIN="data_batch_1.bin"
BIN_TEST="test_batch.bin"
N_FILES= len([name for name in os.listdir(METADATA_DIR) if os.path.isfile(os.path.join(METADATA_DIR, name))])
OUT_FILE="Desktop/insta_data.tar.gz"
j=0
tags=[]
f = open(BIN_DIR+BIN_TRAIN, "wb")
f2= open(BIN_DIR+BIN_TEST, "wb")

command='scp -P 2275'+OUT_FILE+'mcarbonell@asterix.gso.ac.upc.edu:/etc/cifar10_data/'+OUT_FILE


def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

for root, dirs, files in os.walk(METADATA_DIR):
    for name in files:
        if os.path.join(root, name).endswith('.json'):
            with open(os.path.join(root, name)) as metadata_file:
                try:
                    data = json.load(metadata_file,encoding="utf8")
                except ValueError:
                    print "bad encoding",metadata_file
                tag=', '.join(data['tags'])
                if len(tag.split(','))>1:
                    tag=tag.split(',')[0]
                if (tag not in tags):
                    if (len(tags)<10):
                        tags.append(tag)
                    else:
                        continue
                im = Image.open(IMAGE_DIR+name.split('.')[0]+'.jpg')
                im.thumbnail(size)

                #save thumbnails 2 out of 10 are used for test, rest are for train
                if j%10==0 or j%10==5:
                    im.save('Desktop/thumbnails/test/'+str(tags.index(tag))+'_'+str(j)+'.jpg')
                else:
                    im.save('Desktop/thumbnails/train/'+str(tags.index(tag))+'_'+str(j)+'.jpg')
                imarr=np.asarray(im,dtype='int32')
                byarr=bytearray(3073)
                byarr[0]=tags.index(tag)
                for i in range(0,len(byarr)-1):
                    byarr[i+1]=imarr[((i-i/3073)%1024)/32,(i-i/3073)%32,((i-i/3073)%3072)/1024]

                #write 20% of images to test bin, rest to train bin
                if j%10==0 or j%10==5:
                    f2.write(byarr)
                else:
                    f.write(byarr)

                j=j+1
f.close
with open(BIN_DIR+'batches.meta.txt','w') as f:
    for tag in tags:
        f.write(tag+'\n')

make_tarfile(OUT_FILE,BIN_DIR)

#SEND FILE TO ASTERIX
os.system(command)
