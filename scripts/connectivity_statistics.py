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


def extract_metadata(filename):
    """ Extract metadata, namely number of electrodes and nr of matrices
    and band type """
        
    f = open(filename, 'r')
    for line in f:
        lsp = line.split(' = ')
        if len(lsp) == 1:
            continue
        elif lsp == '':
            break

        if 'Number Electrodes' in lsp[1] or 'Number of regions of interest' in lsp[1]:
            nr_elect = int(lsp[0])
        elif 'Number of matrices' in lsp[1]:
            nr_mat = int(lsp[0])
        
    f.close()
    return nr_elect, nr_mat

def extract_matrices(filename, enforce_nr_matrices = None):
    """ Extracts a matrix (N,N,M) from a sLORETA connectivity file where
    N is the number of ROIs or electrodes, and M is the number of frequency bands
    """
    
    nr_elect, nr_mat = extract_metadata(filename)
    
    if not enforce_nr_matrices is None:
        nr_mat = enforce_nr_matrices

    result_matrix = np.zeros( (nr_elect,nr_elect, nr_mat), dtype = np.float )
                
    f = open(filename, 'r')
    
    # skip header
    a = f.readline()
    while ' = ' in a  or 'File name' in a or a == '':
        a = f.readline()
        
    for mat_i in range(nr_mat):
       # print 'Matrix: ', str(mat_i)
        
        for elect_i in range(nr_elect):
           # print 'ROI:', str(elect_i)
            line = f.readline()
           # print "line", line

            lsp = line.split('  ')
            try:
                lsp.remove('') # remove first empty character
            except ValueError:
                break

            assert len(lsp) == nr_elect
            
            result_matrix[elect_i, :, mat_i] = np.array(lsp)
            
        line = f.readline()     
                        
    f.close()
    
    return result_matrix


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
                bigarray[i, j, k, :, :, :] = extract_matrices(filename, enforce_nr_matrices = 8)
                
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
    
            
