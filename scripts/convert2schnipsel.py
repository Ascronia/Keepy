import numpy as np

fname = 'subject1'
fnameending = '.dat'
# assumed sampling frequency
fs = 5000
# assumed duration of epoch in second
epdur = 0.5
# schnipsel file name
outfname = 'schnipsel%03i.asc'

print "loading file ", fname
#a=np.loadtxt(fname + fnameending)
n=a.shape[0]
print "number of datapoints", n
epoch_length = epdur * fs 
print "epoch length ", epoch_length
nr_of_epochs = n / epoch_length
print "number of epochs", nr_of_epochs
for i in xrange(nr_of_epochs):
    print "working on epoch ", i
    np.savetxt(fname + '-' +outfname % i, a[epoch_length*i:epoch_length*(i+1),:], fmt = '%.5f')