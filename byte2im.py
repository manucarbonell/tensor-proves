import os
import io
import numpy as np
import struct
import greyscale
from PIL import Image
from array import array
size=(32,32)

def save_image( npdata, outfilename ) :
    img = Image.fromarray( np.asarray( np.clip(npdata,0,255), dtype="uint8"), "RGB" )
    img.thumbnail(size,Image.ANTIALIAS)
    img.save(outfilename)

MAX_BYTES=100000
i=0
f = open("data_batch_1.bin", "rb")
im=np.zeros((32,32,3))
while i<MAX_BYTES:
    byte = f.read(1)
    value = struct.unpack('B', byte)[0]
    if(i%3073==0):
        name=str(value)
        print name
        byte = f.read(1)
        i=i+1
    value = struct.unpack('B', byte)[0]
    im[((i-1)%1024)/32,(i-1)%32,((i-1)%3072)/1024]=value
    i=i+1
    if(i%3073==0):
        save_image(im,"pictures/"+name+".jpg")
