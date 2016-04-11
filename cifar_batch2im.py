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

size=(32,32)
data_dir='Desktop/cifar-10-batches-bin'
image_dir='Desktop/extracted_images/'

if not(os.path.exists(image_dir)):
    os.mkdir(image_dir)

def save_image( npdata, outfilename ) :
    img = Image.fromarray( np.asarray( np.clip(npdata,0,255), dtype="uint8"), "RGB" )
    img.thumbnail(size,Image.ANTIALIAS)
    img.save(outfilename)

def extract_data(url,data_dir):


    '''
    filepath, _ = urllib.request.urlretrieve(DATA_URL, filepath)
    print "downloaded"

    tarfile.open(filepath, 'r:gz').extractall(data_dir)
    print "extracted"'''
    for subdir, dirs, files in os.walk(data_dir):
        for file in files:
            if os.path.join(subdir, file).endswith(".bin"):
                batch=os.path.join(subdir, file)

                '''batchdir=data_dir+"/pictures/"+batch.split('/')[-1].split('.')[0]+"/"
                if not os.path.exists(batchdir):
                    os.mkdir(batchdir)'''
                print "Introduce the maximum number of images to read from batch",batch.split('/')[-1]
                MAX_BYTES=3073*(int(raw_input()))
                i=0
                f = open(batch, "rb")
                im=np.zeros((32,32,3))
                while i<MAX_BYTES:
                    byte = f.read(1)
                    value = struct.unpack('B', byte)[0]

                    if(i%3073==0):
                        name=str(value)
                        byte = f.read(1)
                        i=i+1
                    value = struct.unpack('B', byte)[0]

                    im[((i-i/3073)%1024)/32,(i-i/3073)%32,((i-i/3073)%3072)/1024]=value
                    i=i+1
                    if(i%3073==0):
                        if not os.path.exists(image_dir+batch.split('/')[-1].split('.')[0]+'/'):
                            os.mkdir(image_dir+batch.split('/')[-1].split('.')[0]+'/')
                        save_image(im,image_dir+batch.split('/')[-1].split('.')[0]+'/'+name+'_'+str(i)+".jpg")

extract_data("",data_dir)
