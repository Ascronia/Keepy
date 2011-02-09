import numpy as np

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

    