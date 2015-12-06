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
#import cifar_batch2im
size=(32,32)

target_dir="Desktop/CompleteInstagramDataSet/InstaMetadata"
image_dir="Desktop/CompleteInstagramDataSet/InstaImages/"
thumb_dir="Desktop/thumbnails/"
j=0
tags=[]
f = open('Desktop/data/file.bin', "wb")
for root, dirs, files in os.walk(target_dir):
    for name in files:
        if os.path.join(root, name).endswith('.json'):
            with open(os.path.join(root, name)) as data_file:
                try:
                    data = json.load(data_file,encoding="utf8")
                except ValueError:
                    print "bad encoding",data_file
                tag=', '.join(data['tags'])
                if len(tag.split(','))>1:
                    tag=tag.split(',')[0]
                if (tag not in tags):
                    tags.append(tag)
                print name
                im = Image.open(image_dir+name.split('.')[0]+'.jpg')
                im.thumbnail(size)
                im.save('Desktop/thumbnails/'+', '.join(data['tags'])+'_'+str(j)+'.jpg')
                imarr=np.asarray(im,dtype='int32')
                byarr=bytearray(3073)
                byarr[0]=tags.index(tag)
                for i in range(0,len(byarr)-1):
                    byarr[i+1]=imarr[((i-i/3073)%1024)/32,(i-i/3073)%32,((i-i/3073)%3072)/1024]
                f.write(byarr)

                j=j+1
f.close
with open('tags.txt','w') as f:
    for tag in tags:
        f.write(tag+'\n')
