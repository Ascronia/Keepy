from glob import glob
import numpy as np
from keepy.connectivity.averager import *

mapbands = {
0:"delta",
1:"theta",
2:"alpha-1",
3:"alpha-2",
4:"beta-1",
5:"beta-2",
6:"beta-3",
7:"gamma",
}

a=glob("/home/stephan/Dropbox/Stephan&Patricia/Python/rawdata/ROIlinLagConn/C/*.txt")
bigarray=np.zeros( (19,19,8,len(a)) )

for i,fname in enumerate(a):
    bigarray[:,:,:,i]=extract_matrices(fname)

result=bigarray.mean(axis=3)

# result[(result>0.2) & (result<0.8)]=0.0

write_as_text(result, "/home/stephan/Dropbox/Stephan&Patricia/Python/results/result_C.txt")


# t-test value extraction
tvalues=extract_matrices("/home/stephan/Dropbox/Stephan&Patricia/Python/rawdata/ROIlinLagConn/C/ttest.txt")
tvalue_threshold = 0.4
nr_bands = 8

# write to textfiles
with open("/home/stephan/Dropbox/Stephan&Patricia/Python/significant.txt", "w") as f:
    for i in range(nr_bands):
        row_index, column_index = np.where(tvalues[:,:,i] > tvalue_threshold)
        f.write("For band: {0}\n".format(mapbands[i]) )
        row_index.tofile(f,sep=",")
        f.write("\n")
        column_index.tofile(f,sep=",")
        f.write("\n")
        result[row_index,column_index,i].tofile(f,sep=",")
        f.write("\n")
        f.write("\n")
    
