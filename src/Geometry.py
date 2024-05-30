import numpy as np
import warnings

from OpenGL.GL import *

class Geometry:
    def __init__(self, filename):
        # Vertices stores all of the model data per face in the following format:
        # vertex_x, vertex_y, vertex_z, texture_s, texture_t, normal_x, normal_y, normal_z
        # Each value is a 32bit float
        # This means that if you wanted to get all of the vertex data:
        # Your start index would be 0, size would be 3 (x, y , x) and your stride would be 32

        self.vertices = self.LoadFile(filename)
        self.vertexCount = len(self.vertices) // 8
        self.vertices = np.array(self.vertices, dtype=np.float32)

        self.vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        # Create Vertex Attributes Pointers Here
        # Note that you will need to use ctypes.c_void_p(i) to specify the starting index
        # when using glVertexAttribPointer

        # position
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
        # texture
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))
        # normal
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(20))

    def LoadFile(self, filename):

        # raw, unassembled data
        v = []
        vt = []
        vn = []
        faces = []

        # final, assembled and packed result
        vertices = []

        # open the obj file and read the data
        with open(filename, 'r') as f:
            line = f.readline()
            while line:
                firstSpace = line.find(" ")
                flag = line[0:firstSpace]
                if flag == "v":
                    # vertex
                    line = line.replace("v ", "")
                    line = line.split()  # This accounts for '  ' spacing instead of ' ' spacing
                    l = [float(x) for x in line]
                    v.append(l)
                elif flag == "vt":
                    # texture coordinate
                    line = line.replace("vt ", "")
                    line = line.split()
                    l = [float(x) for x in line]
                    vt.append(l)
                elif flag == "vn":
                    # normal
                    line = line.replace("vn ", "")
                    line = line.split()
                    l = [float(x) for x in line]
                    vn.append(l)
                elif flag == "f":
                    # face, three or more vertices in v/vt/vn form
                    line = line.replace("f ", "")
                    line = line.replace("\n", "")
                    faces.append(line)
                line = f.readline()

        # Now we use the face data to setup the vertex ordering

        hasNormals = len(vn) > 0
        hasTextureCoords = len(vt) > 0

        if not hasNormals:
            warnings.warn("WARNING: Model has no normals. Will attempt to calculate them manually.")

        if not hasTextureCoords:
            warnings.warn("WARNING: Model has no texture coordinates.")

        for face in faces:
            # get the individual vertices for each line
            line = face.split()
            faceVertices = []
            faceTextures = []
            faceNormals = []

            if not hasNormals:
                cNorms = self.calcNormals(line, v, hasTextureCoords)

            for i in range(len(line)):
                # break out into [v,vt,vn],
                # correct for 0 based indexing.
                l = line[i].split("/")
                position = int(l[0]) - 1
                faceVertices.append(v[position])
                if hasTextureCoords:
                    texture = int(l[1]) - 1
                    faceTextures.append(vt[texture])
                else:
                    faceTextures.append([0.0, 0.0])  # UV Coordinate of (0,0)

                if hasNormals:
                    normal = int(l[2]) - 1
                    faceNormals.append(vn[normal])
                else:
                    faceNormals.append(cNorms)

            # obj file uses triangle fan format for each face individually.
            # unpack each face
            triangles_in_face = len(line) - 2

            vertex_order = []
            """
                eg. 0,1,2,3 unpacks to vertices: [0,1,2,0,2,3]
            """
            for i in range(triangles_in_face):
                vertex_order.append(0)
                vertex_order.append(i + 1)
                vertex_order.append(i + 2)
            for i in vertex_order:
                for x in faceVertices[i]:
                    vertices.append(x)
                for x in faceTextures[i]:
                    vertices.append(x)
                for x in faceNormals[i]:
                    vertices.append(x)

        return vertices

    def calcNormals(self, face, vertices, hasTexCoords):

        # Convert vertex positions into numpy matrix
        if hasTexCoords:
            vertex_positions = np.array([
                vertices[int(vi.split('/')[0]) - 1] for vi in face
            ])
        else:
            vertex_positions = np.array([
                vertices[int(vi) - 1] for vi in face
            ])

        # We now calculate a face normal by taken the normalized cross product of (v[1]-v[0] x v[2] - [v0])
        # which the cross product of the tangent and the bi-tangent (which gives us the normal vector)
        # Note this assumes clockwise defined vertex positions

        BA = vertex_positions[1] - vertex_positions[0]
        CA = vertex_positions[2] - vertex_positions[0]

        N = np.cross(BA, CA)
        normalized_N = N / np.linalg.norm(N)

        return normalized_N.tolist()

    def cleanup(self):
        glDeleteBuffers(1, (self.vbo,))