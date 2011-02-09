import keepy.converter as kc
import os
import numpy as np
from glob import glob
from StringIO import StringIO

folder = '/raw data/'
outputfolder = '/results/'

Meas = ['ROIlinLagConn', 'ROIlinTotConn', 'EEGlinLagConn', 'EEGlinTotConn']
Cond = ['B', 'R']
VP = [3,5,7,8,9,10,11,12,14,15,16,18,19,21,22,23,24,25,26,27,28,29,31]
VP = ['%02i' % v for v in VP]

bigarray = np.zeros( (len(Meas), len(Cond), len(VP), 19, 19, 8), dtype = np.float )

def retfn(ik, jc, stat):
    return '%s-%s-%s.csv' % (ik, jc, stat)

def generate_array():
    for i,ik in enumerate(Meas):
        for j,jc in enumerate(Cond):
            for k,kv in enumerate(VP):
                # filename
                fname = 'VP%s%s*-%s.txt' % (kv, jc, ik)
                newpath = os.path.join(folder, ik, jc)
                filename = glob(os.path.join(newpath, fname))[0]
                bigarray[i, j, k, :, :, :] = kc.extract_matrices(filename, enforce_nr_matrices = 8)
                
    return bigarray
            
def write_mean(bigarray):
    for i,ik in enumerate(Meas):
        for j,jc in enumerate(Cond):
            stri = StringIO()
            for fi in range(8):
                res = bigarray[i,j,:,:,:,fi].mean(axis=0)
                np.savetxt(stri, res, delimiter=',')
                stri.write(' \n')
                
            stri.seek(0)
            fnameout = os.path.join(outputfolder, retfn(ik, jc, 'mean'))
            with open(fnameout,'w') as f:
                f.write(stri.read())
                
def write_median(bigarray):
    for i,ik in enumerate(Meas):
        for j,jc in enumerate(Cond):
            stri = StringIO()
            for fi in range(8):
                res = np.median(bigarray[i,j,:,:,:,fi], axis=0)
                np.savetxt(stri, res, delimiter=',')
                stri.write(' \n')
                
            stri.seek(0)
            fnameout = os.path.join(outputfolder, retfn(ik, jc, 'median'))
            with open(fnameout,'w') as f:
                f.write(stri.read())
                
def write_std(bigarray):
    for i,ik in enumerate(Meas):
        for j,jc in enumerate(Cond):
            stri = StringIO()
            for fi in range(8):
                res = bigarray[i,j,:,:,:,fi].std(axis=0)
                np.savetxt(stri, res, delimiter=',')
                stri.write(' \n')
                
            stri.seek(0)
            fnameout = os.path.join(outputfolder, retfn(ik, jc, 'std'))
            with open(fnameout,'w') as f:
                f.write(stri.read())
                
def write_min(bigarray):
    for i,ik in enumerate(Meas):
        for j,jc in enumerate(Cond):
            stri = StringIO()
            for fi in range(8):
                res = bigarray[i,j,:,:,:,fi].min(axis=0)
                np.savetxt(stri, res, delimiter=',')
                stri.write(' \n')
                
            stri.seek(0)
            fnameout = os.path.join(outputfolder, retfn(ik, jc, 'min'))
            with open(fnameout,'w') as f:
                f.write(stri.read())
     
def write_max(bigarray):
    for i,ik in enumerate(Meas):
        for j,jc in enumerate(Cond):
            stri = StringIO()
            for fi in range(8):
                res = bigarray[i,j,:,:,:,fi].max(axis=0)
                np.savetxt(stri, res, delimiter=',')
                stri.write(' \n')
                
            stri.seek(0)
            fnameout = os.path.join(outputfolder, retfn(ik, jc, 'max'))
            with open(fnameout,'w') as f:
                f.write(stri.read())
                
     
def write_triumean(bigarray):
    for i,ik in enumerate(Meas):
        for j,jc in enumerate(Cond):
            stri = StringIO()
            for fi in range(8):
                res = np.triu(bigarray[i,j,:,:,:,fi].mean(axis=0), 1).mean()
                stri.write(res)
                stri.write(' \n')
                
            stri.seek(0)
            fnameout = os.path.join(outputfolder, retfn(ik, jc, 'triumean'))
            with open(fnameout,'w') as f:
                f.write(stri.read())
                
def write_triustd(bigarray):
    for i,ik in enumerate(Meas):
        for j,jc in enumerate(Cond):
            stri = StringIO()
            for fi in range(8):
                res = np.triu(bigarray[i,j,:,:,:,fi].mean(axis=0), 1).std()
                stri.write(res)
                stri.write(' \n')
                
            stri.seek(0)
            fnameout = os.path.join(outputfolder, retfn(ik, jc, 'triustd'))
            with open(fnameout,'w') as f:
                f.write(stri.read())      
                       
bigarray = generate_array()
write_mean(bigarray)
write_median(bigarray)
write_std(bigarray)
write_min(bigarray)
write_max(bigarray)
write_triumean(bigarray)
write_triustd(bigarray)
    
            
