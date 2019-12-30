import numpy as np

"""
  Write out the mesh in OFF format.
======
  Output:   verts will be in a Nx3 array.
            If there is color, it will be Nx6 array
"""


def write_off(filename, verts, faces=None):
    off = open(filename, 'w')
    if faces is None:
        face = False
    else:
        face = True

    verts = np.array(verts)
    nof_verts = 0
    if verts.shape[1] != 3 and verts.shape[0] != 3:
        raise ValueError('Invalid verts size. Please insert a Nx3 array input')
    # Get the number of verts
    if verts.shape[1] != 3:
        nof_verts = verts.shape[1]
    else:
        nof_verts = verts.shape[0]

    if face:
        nof_faces = 0
        if faces.shape[1] != 3:
            nof_faces = faces.shape[1]
        else:
            nof_faces = faces.shape[0]

    #print("nof verts: %d, nof faces: %d" % (nof_verts, nof_faces))
    off.write('OFF\n')
    if faces is not None:
        off.write('%d %d 0\n' % (nof_verts, nof_faces))
    else:
        off.write('%d 0 0\n' % (nof_verts))
    for vert in verts:
        off.write('%f %f %f\n' % (vert[0], vert[1], vert[2]))
    if faces is not None:
        for face in faces:
            off.write('3 %d %d %d\n' % (face[0], face[1], face[2]))
    off.close()


def read_off(filename):
    """
      returns:
      verts:
          The vertices points read
      faces:
          If faces exist, the faces ID in relation to the verts
    """
    #print("Reading OFF file")
    try:
        off = open(filename)
        first_line = off.readline()
        if "OFF" not in first_line:
            raise ValueError('The file does not start with the word OFF')
        color = True if "C" in first_line else False
        try:
            n_verts, n_faces, n_buffer = tuple(
                [int(s) for s in off.readline().strip().split(' ') if "#" not in s])
        except (ValueError) as e:
            print('No vertices!')
        verts = []
        faces = []
        colors = []

        for i_verts in range(n_verts):
            vals = ([s for s in off.readline().strip().split(' ')])
            if color:
                colors.append(np.array([int(vals[0]), int(vals[1]), int(vals[2])]))
            verts.append(np.array([float(vals[0]), float(vals[1]), float(vals[2])]))
        for i_faces in range(n_faces):
            f = np.array([int(s) for s in off.readline().strip().split(' ')][1:])
            faces.append(f)
        off.close()

        #print("number of verts: %d, number of faces: %d" % (n_verts, n_faces))
        if color:
            return np.array(verts), np.array(faces), np.array(colors)
        else:
            return np.array(verts), np.array(faces)

    except (OSError, IOError) as e:
        print('File cannot be opened.')


_off_loaders = {'OFF': read_off}
_off_writers = {'OFF': write_off}