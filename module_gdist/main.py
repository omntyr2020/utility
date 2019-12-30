import gdist
import numpy as np
from utility_off import read_off, write_off

if __name__ == "__main__":

    verts, faces = read_off('model.off')
    
    # 3079 chest center index
    # 646  chest most left vertex index
    v1 = verts[3079,:].reshape((1,3))
    v2 = verts[646, :].reshape((1,3))

    print("v1",v1)
    print("v2",v2)

    print("v1,v2 norm",np.linalg.norm(v1-v2))

    path_v1 = 'vert_center.off'
    path_v2 = 'vert_left_chest.off'
    write_off(path_v1, v1) 
    write_off(path_v2, v2)

    # print("type of verts",verts.dtype)
    # print("type of faces",faces.dtype)

    faces = faces.astype(np.int32)

    src = np.array([3079]).astype(np.int32)
    trg = np.array([646]).astype(np.int32)

    # print("type of src",src.dtype)
    # print("type of trg",trg.dtype)

    # dist = gdist.compute_gdist(verts, faces, source_indices = src, target_indices = trg)
    dist = gdist.compute_gdist(verts, faces, source_indices = src, max_distance = 10) # target_indices = trg)

    print("shape of dist",dist.shape)
    indices = np.where(dist!=np.infty)[0]

    path_chest_10 = 'chest_10.off'
    write_off(path_chest_10,verts[indices,:])

    print("indices",indices)

    print("dist",dist)

    for a in dir(gdist):
        print(getattr(gdist, a))

    # compute_gdist accepts five arguments, max_distance