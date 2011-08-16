import nibabel
import numpy as np

# loreta voxel order matrix: 6239x3
def read_loretavoxelinf(filename = 'MNI-BAs-6239-voxels.csv'):
    """ Reads the voxel information of sLoreta """
    
    import csv
    fn = ['X', 'Y', 'Z', 'PrimAnat', 'SecAnat', 'BA']
    reader = csv.DictReader(open(filename, "r"), delimiter=',', fieldnames = fn)
    info = []
    for row in reader:
        info.append(row)
    return info

def slor2nifti2(filename):
    """ open .slor files and convert them to Nifti """

    from numpy import array, zeros, dot, float32, reshape
    
    import array as arr_reader
    from os.path import join
    
    # open binary file and extract the data of all images
    f = open(filename, 'rb')
    data_arr = array(arr_reader.array('f', f.read()))
    nr_images = len(data_arr)/6239
    da = reshape(data_arr, (nr_images, 6239))
    print 'Number of images in file %s: %s' % (filename, nr_images)

    n = 50

    arr = zeros((181,217,181,n), dtype=float32)
    trafo = array([[1,0,0, 89],
                      [0,1,0, 125],
                      [0,0,1, 71],
                      [0,0,0, 1]])
    lor_list = read_loretavoxelinf(join('MNI-BAs-6239-voxels.csv'))

    for image_idx in range(n):
        for i, vox in enumerate(lor_list):
            # i should go from 0 to 6238
            p = da[image_idx, i]
            if p != 0.0:
                # write image_idx as a segementation label according to the ROI
                # to the beautiful arr which will become the nifti volume
                x,y,z = int(vox['X']), int(vox['Y']), int(vox['Z'])
            else:
                print("voxel was zero")

            # transformation of mni RAS to voxel
            val = array([x, y, z, 1])
            # apply the transformation
            x,y,z, t =  dot(trafo, val)
            arr[z-2:z+3, y-2:y+3, x-2:x+3, image_idx] = p

    return arr, trafo


# your slor file
arr, trafo = slor2nifti2( 'P300_stim30_Norm00001.slor' )
hdr = nibabel.Nifti1Header()
hdr.set_sform(trafo)
hdr.set_data_dtype(np.float32)
hdr.set_data_shape(arr.shape)
nim = nibabel.Nifti1Image(arr, trafo)
nibabel.save( nim, 'test.nii.gz')

