import os
import errno
import argparse
from PIL import Image
import numpy as np
import json
import sys
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--imagespath', type=str, default="NONE")
parser.add_argument('--labelspath', type=str , default="NONE")

args = parser.parse_args()
def get_img_shape(path):
    image=Image.open(path)
    return np.array(image.size)

def convert_labels(path, x1, y1, x2, y2):

    def sorting(l1, l2):
        if l1 > l2:
            lmax, lmin = l1, l2
            return lmax, lmin
        else:
            lmax, lmin = l2, l1
            return lmax, lmin
    size = get_img_shape(path)
    xmax, xmin = sorting(x1, x2)
    ymax, ymin = sorting(y1, y2)
    dw = 1./size[0]
    dh = 1./size[1]
    x = (xmin + xmax)/2.0
    y = (ymin + ymax)/2.0
    w = xmax - xmin
    h = ymax - ymin
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

imageslist= os.listdir(args.imagespath)
labelslist= os.listdir(args.labelspath)

imageslist.sort()
labelslist.sort()
filename=os.path.join(os.getcwd(),"labels/yolo")
os.makedirs(filename,exist_ok=True)

j=0
i=0
while i<len(imageslist) and j<len(labelslist):
    
    image_confirmed=False
    while image_confirmed==False:
        
        if os.path.splitext(imageslist[i])[0] != os.path.splitext(labelslist[j])[0]:

            i=i+1
        else:
            image_confirmed=True


    outf= open(os.path.join("labels/yolo",labelslist[j].replace("json","txt")),'w')


    path=os.path.join(args.imagespath,imageslist[i])
    label=os.path.join(args.labelspath,labelslist[j])
    with open(label, 'rb') as f:
        obj=json.load(f)

    print(imageslist[i])
    print(labelslist[j])
    
    
    for k in obj:
        x,y,w,h=convert_labels(path,k['Left'],k['Top'],k['Right'],k['Bottom'])
        if abs(k['Left']-k['Right'])*abs(k['Top']-k['Bottom']) <= 2500:
            pass
        elif not (x>1 or y>1 or w>1 or h>1):
            if k['ObjectClassId']==2000:
                k['ObjectClassId']=0
            elif k['ObjectClassId']==1040:
                k['ObjectClassId']=1
            elif k['ObjectClassId']==1070:
                k['ObjectClassId']=2
            elif k['ObjectClassId']==1110:
                k['ObjectClassId']=3
            elif k['ObjectClassId']==4000:
                k['ObjectClassId']=4
            elif k['ObjectClassId']==5010:
                k['ObjectClassId']=5
            elif k['ObjectClassId']==2010:
                k['ObjectClassId']=6
            elif k['ObjectClassId']==1120:
                k['ObjectClassId']=7
            elif k['ObjectClassId']==1013:
                k['ObjectClassId']=8
            elif k['ObjectClassId']==1011:
                k['ObjectClassId']=9
            elif k['ObjectClassId']==1012:
                k['ObjectClassId']=10
            elif k['ObjectClassId']==1030:
                k['ObjectClassId']=11
            elif k['ObjectClassId']==1100:
                k['ObjectClassId']=12
            elif k['ObjectClassId']==1135:
                k['ObjectClassId']=13
            elif k['ObjectClassId']==1002:
                k['ObjectClassId']=14
            elif k['ObjectClassId']==1003:
                k['ObjectClassId']=15
            elif k['ObjectClassId']==2050:
                k['ObjectClassId']=16
            outf.write(str(k['ObjectClassId'])+" "+str(x)+" "+str(y)+" "+str(w)+" "+str(h)+"\n")

    j=j+1
    i=i+1
