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


def slor2nifti(filename, merge_roi = False):
    """ open .slor files and convert them to Nifti """

    from numpy import array, zeros, dot, float32, reshape
    
    import array as arr_reader
    from os.path import join
    
    # open binary file and extract the data of all images
    f = open(filename, 'rb')
    data_arr = array(arr_reader.array('f', f.read()))
    nr_images = len(data_arr)/6239
    da = reshape(data_arr, (nr_images, 6239))
    #print 'Number of images in file %s: %s' % (filename, nr_images)

    # MNI-space: 181 x 217 x 181
    # create the 3d array
    # x = [-70,70] dim = 141
    # y = [-100,65] dim = 166
    # z = [-45, 70] dim = 116
    # order of the array is z,y,x
    # arr = zeros((116, 166, 141))
    arr = zeros((1, 181, 217,181), dtype=float32)
    # transformation matrix: XYZ1 in MNI (mm) to voxel indices
    # from the Colin_1mm brain
    trafo = array([[1,0,0, 89],
                      [0,1,0, 125],
                      [0,0,1, 71],
                      [0,0,0, 1]])
    
    # read the loreta mapping for the voxel
    from cviewer.action.common import RESOURCE_PATH
    lor_list = read_loretavoxelinf(join(RESOURCE_PATH, 'MNI-BAs-6239-voxels.csv'))
    
    if merge_roi:
        # loop over 1..n-1 images (which are e.g. ROIs), giving each an ID
        for image_idx in range(nr_images-1):
        #print 'ROI Nr: ', str(image_idx + 1)
            for i, vox in enumerate(lor_list):
                # i should go from 0 to 6238
        p = da[image_idx, i]
                if p != 0.0:
                    # write image_idx as a segementation label according to the ROI
                    # to the beautiful arr which will become the nifti volume
                    x,y,z = int(vox['X']), int(vox['Y']), int(vox['Z'])
            
            # transformation of mni RAS to voxel
            val = array([x, y, z, 1])
            # apply the transformation
            x,y,z, t =  dot(trafo, val)
            if 'ROI' in filename:
            
            vox_value = image_idx + 1
            else:
            vox_value = p
            arr[0, z-2:z+3, y-2:y+3, x-2:x+3] = vox_value

    # save arr as nifti
    #nim = nifti.NiftiImage(arr)
    from cviewer.io.nipy.imageformats.nifti1 import Nifti1Header, Nifti1Image
    #hdr = Nifti1Header()
    #hdr.set_sform(trafo)
    #hdr.set_data_dtype(float32)
    #hdr.set_sform(trafo)
    #hdr.set_data_shape(arr.shape)
    
    nim = Nifti1Image(arr, trafo)
    
    # hdr.set_sform(trafo, code='mni152')
    #nim.setPixDims([1.0, 1.0, 1.0])
    #nim.setVoxDims([1.0, 1.0, 1.0])
    #nim.setXYZUnit('mm')
    
    # close file and return nifti image
    f.close()
    return nim