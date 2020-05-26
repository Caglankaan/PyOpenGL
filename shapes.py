# CENG 487 Assignment# by
# Kaan Çağlan
# StudentId: 230201047
# Month Year: 18.05.2020

from math import *
from OpenGL.GLUT import *
from texture_loader import *
import numpy as np 
from OpenGL.GLU import *
from OpenGL.GL import *    
from matrix import Matrix
from vector import Vector3f
from PIL import Image
import math

class Cylinder:
    def __init__(self, shader, object_position, radius, height, image):
        self.shader = shader
        self.object_position = object_position
        self.height = height
        self.baseRadius = radius
        self.topRadius = radius

        self.sectorCount = 36
        self.stackCount = 8
        self.indices = []
        self.data = []

        self.buildVerticesSmooth()

        self.data = np.array(self.data, dtype=np.float32)
        self.indices = np.array(self.indices, dtype=np.uint32)
        
        VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, self.data.itemsize * len(self.data), self.data, GL_STATIC_DRAW)
 
        EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.itemsize * len(self.indices), self.indices, GL_STATIC_DRAW)

        self.image = image
        self.image_data = numpy.array(list(image.getdata()), numpy.uint8)

        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)

        # Set the texture wrapping parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        # Set texture filtering parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)


    def draw(self, projection, view, model):

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.image.width, self.image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, self.image_data)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, self.data.itemsize * 5, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, self.data.itemsize * 5, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)
        
        glUseProgram(self.shader.glid)
        glClearColor(0.2, 0.3, 0.2, 1.0)
        glEnable(GL_DEPTH_TEST)
    
        model_loc = glGetUniformLocation(self.shader.glid, "model")
        view_loc = glGetUniformLocation(self.shader.glid, "view")
        proj_loc = glGetUniformLocation(self.shader.glid, "proj")

        glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
        glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)

        model = Matrix.create_from_translation(self.object_position)


        glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)

        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)

    def getUnitCircleVertices(self):
        sectorStep = 2*pi / self.sectorCount
        
        unitCircleVertices = []

        for i in range(0, self.sectorCount+1):
            sectorAngle = i * sectorStep
            unitCircleVertices.append(cos(sectorAngle))
            unitCircleVertices.append(sin(sectorAngle))
            unitCircleVertices.append(0)
        
        return unitCircleVertices

    def buildVerticesSmooth(self):
        unitVertices = self.getUnitCircleVertices()
        vertices = []
        normals = []
        texCoords = []
        data = []

        for i in range (0, 2):
            h = -self.height / 2.0 + i * self.height
            t = 1.0 -i

            k = 0
            for j in range(0, self.sectorCount + 1):
                ux = unitVertices[k]
                uy = unitVertices[k+1]
                uz = unitVertices[k+2]

                data.append(ux * self.baseRadius)
                data.append(uy * self.baseRadius)
                data.append(h)
                data.append(j/self.sectorCount)
                data.append(t)

                vertices.append(ux * self.baseRadius) #?
                vertices.append(uy * self.baseRadius)
                vertices.append(h)

                normals.append(ux)
                normals.append(uy)
                normals.append(uz)

                texCoords.append(j/self.sectorCount)
                texCoords.append(t)

                k += 3

        baseCenterIndex = len(vertices) / 3
        topCenterIndex = baseCenterIndex + self.sectorCount + 1

        for i in range(0,2):
            h = -self.height / 2.0 + i * self.height
            nz = i*2 -1

            vertices.append(0)
            vertices.append(0)
            vertices.append(h)

            data.append(0)
            data.append(0)
            data.append(h)
            data.append(0.5)
            data.append(0.5)

            normals.append(0)
            normals.append(0)
            normals.append(nz)

            texCoords.append(0.5)
            texCoords.append(0.5)
            
            k = 0
            for j in range(0, self.sectorCount):
                ux = unitVertices[k]
                uy = unitVertices[k+1]

                vertices.append(ux * self.baseRadius) #?
                vertices.append(uy * self.baseRadius)
                vertices.append(h)

                data.append(ux * self.baseRadius) #?
                data.append(uy * self.baseRadius)
                data.append(h)
                data.append(-ux * 0.5 + 0.5)
                data.append(-uy * 0.5 + 0.5)

                normals.append(0)
                normals.append(0)
                normals.append(nz)

                texCoords.append(-ux * 0.5 + 0.5)
                texCoords.append(-uy * 0.5 + 0.5)

                k += 3

        indices = []
        k1 = 0
        k2 = self.sectorCount +1
        for i in range(self.sectorCount):
            indices.append(k1)
            indices.append(k1+1)
            indices.append(k2)

            indices.append(k2)
            indices.append(k1+1)
            indices.append(k2+1)
            k1 += 1
            k2 += 1
        
        k = baseCenterIndex + 1
        for i in range(self.sectorCount):
            if(i < self.sectorCount -1):
                indices.append(baseCenterIndex)
                indices.append(k+1)
                indices.append(k)
            else:
                indices.append(baseCenterIndex)
                indices.append(baseCenterIndex+1)
                indices.append(k)
            k+=1
        
        k = topCenterIndex+1
        for i in range(self.sectorCount):
            if(i < self.sectorCount -1):
                indices.append(topCenterIndex)
                indices.append(k)
                indices.append(k+1)
            else:
                indices.append(topCenterIndex)
                indices.append(k)
                indices.append(topCenterIndex+1)
            k+=1

        self.data = data
        self.indices = indices

class Cube:
    def __init__(self, shader, object_position, image):
        self.shader = shader
        self.object_position = object_position
        
        self.image = image
        self.image_data = numpy.array(list(image.getdata()), numpy.uint8)

        cube = [-0.5, -0.5, 0.5, 0.0, 0.0,
            0.5, -0.5, 0.5, 1.0, 0.0,
            0.5, 0.5, 0.5, 1.0, 1.0,
            -0.5, 0.5, 0.5, 0.0, 1.0,

            -0.5, -0.5, -0.5, 0.0, 0.0,
            0.5, -0.5, -0.5, 1.0, 0.0,
            0.5, 0.5, -0.5, 1.0, 1.0,
            -0.5, 0.5, -0.5, 0.0, 1.0,

            0.5, -0.5, -0.5, 0.0, 0.0,
            0.5, 0.5, -0.5, 1.0, 0.0,
            0.5, 0.5, 0.5, 1.0, 1.0,
            0.5, -0.5, 0.5, 0.0, 1.0,

            -0.5, 0.5, -0.5, 0.0, 0.0,
            -0.5, -0.5, -0.5, 1.0, 0.0,
            -0.5, -0.5, 0.5, 1.0, 1.0,
            -0.5, 0.5, 0.5, 0.0, 1.0,

            -0.5, -0.5, -0.5, 0.0, 0.0,
            0.5, -0.5, -0.5, 1.0, 0.0,
            0.5, -0.5, 0.5, 1.0, 1.0,
            -0.5, -0.5, 0.5, 0.0, 1.0,

            0.5, 0.5, -0.5, 0.0, 0.0,
            -0.5, 0.5, -0.5, 1.0, 0.0,
            -0.5, 0.5, 0.5, 1.0, 1.0,
            0.5, 0.5, 0.5, 0.0, 1.0]

        indices = [0, 1, 2, 2, 3, 0,
                4, 5, 6, 6, 7, 4,
                8, 9, 10, 10, 11, 8,
                12, 13, 14, 14, 15, 12,
                16, 17, 18, 18, 19, 16,
                20, 21, 22, 22, 23, 20]

        cube = np.array(cube, dtype = np.float32)
        indices = np.array(indices, dtype=np.uint32)

        self.data = cube
        self.indices = indices

        VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, self.data.itemsize * len(self.data), self.data, GL_STATIC_DRAW)
 
        EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.itemsize * len(self.indices), self.indices, GL_STATIC_DRAW)

        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)

        # Set the texture wrapping parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        # Set texture filtering parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    def draw(self, projection, view, model):

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.image.width, self.image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, self.image_data)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, self.data.itemsize * 5, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, self.data.itemsize * 5, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)


        glUseProgram(self.shader.glid)
        glClearColor(0.2, 0.3, 0.2, 1.0)
        glEnable(GL_DEPTH_TEST)
    
        model_loc = glGetUniformLocation(self.shader.glid, "model")
        view_loc = glGetUniformLocation(self.shader.glid, "view")
        proj_loc = glGetUniformLocation(self.shader.glid, "proj")

        glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
        glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)
        
        model = Matrix.create_from_translation(self.object_position)
        
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)

        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)

class Sphere:
    def __init__(self, shader, object_position, image):
        self.shader = shader
        self.count = 0
        self.image = image
        self.image_data = numpy.array(list(image.getdata()), numpy.uint8)

        indices = []
        data = []

        X_SEGMENTS = 100
        Y_SEGMENTS = 100
        
        for y in range(Y_SEGMENTS+1):
            for x in range(X_SEGMENTS+1):
                xSegment = x / X_SEGMENTS
                ySegment = y / Y_SEGMENTS
                xPos = cos(xSegment * 2.0 * pi) * sin(ySegment * pi)
                yPos = cos(ySegment * pi)
                zPos = sin(xSegment * 2.0 * pi) * sin(ySegment * pi)

                data.append(xPos)
                data.append(yPos)
                data.append(zPos)
                data.append(xSegment)
                data.append(ySegment)


        oddRow = False
        for y in range(Y_SEGMENTS):
            if not oddRow:
                for x in range(X_SEGMENTS+1):
                    indices.append(y * (X_SEGMENTS+1) +x)
                    indices.append((y+1) * (X_SEGMENTS+1) +x)
            else:
                for x in range(X_SEGMENTS, -1, -1):
                    indices.append((y+1) * (X_SEGMENTS+1) +x)
                    indices.append(y * (X_SEGMENTS+1) +x)
            
            oddRow = not oddRow
    

        data = np.array(data, dtype=np.float32)
        indices = np.array(indices, dtype=np.uint32)

        
        self.data = data
        
        self.indices = indices
        
        self.object_position = object_position
        
        VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, self.data.itemsize * len(self.data), self.data, GL_STATIC_DRAW)
 
        EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.itemsize * len(self.indices), self.indices, GL_STATIC_DRAW)

        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)

        # Set the texture wrapping parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        # Set texture filtering parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    def draw(self, projection, view, model):

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, self.image.width, self.image.height, 0, GL_RGB, GL_UNSIGNED_BYTE, self.image_data)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, self.data.itemsize * 5, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, self.data.itemsize * 5, ctypes.c_void_p(12))
        glEnableVertexAttribArray(1)

        glUseProgram(self.shader.glid)
        glClearColor(0.2, 0.3, 0.2, 1.0)
        glEnable(GL_DEPTH_TEST)
    
        model_loc = glGetUniformLocation(self.shader.glid, "model")
        view_loc = glGetUniformLocation(self.shader.glid, "view")
        proj_loc = glGetUniformLocation(self.shader.glid, "proj")

        glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
        glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)

        model = Matrix.create_from_translation(self.object_position)
        
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)

        glDrawElements(GL_TRIANGLE_STRIP, len(self.indices), GL_UNSIGNED_INT, None)
        
class ShapeFromObjectFile:
    def __init__(self, camera, shader, object_position, obj, image, second_image, lighter_object1, lighter_object2):
        self.image = image
        self.camera = camera
        self.lighter_object = lighter_object1
        self.lighter_object2 = lighter_object2
        self.second_image = second_image
        
        self.shader = shader
        self.obj = obj
        self.animation = False
        self.object_position = object_position
        self.color = [1.0, 1.0, 1.0]

        VAO = glGenVertexArrays(1)
        glBindVertexArray(VAO)

        VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, VBO)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, self.obj.vertices.itemsize * 8, ctypes.c_void_p(0))

        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, self.obj.vertices.itemsize * 8, ctypes.c_void_p(3*4))
        
        if(self.lighter_object is not None or self.lighter_object2 is not None):
            glEnableVertexAttribArray(2)
            glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, self.obj.vertices.itemsize * 8, ctypes.c_void_p(5*4))

       
    
    def draw(self, projection, view, model, show_animation, tex_alpha, blinn_switch, lighter_object_1, lighter_object_2):
        self.lighter_object = lighter_object_1
        self.lighter_object2 = lighter_object_2

        model = Matrix.create_from_translation(self.object_position)

        self.animation = show_animation

        glBufferData(GL_ARRAY_BUFFER, self.obj.vertices, GL_STATIC_DRAW)
        glUseProgram(self.shader.glid)
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glEnable(GL_DEPTH_TEST)
    
        model_loc = glGetUniformLocation(self.shader.glid, "model")
        view_loc = glGetUniformLocation(self.shader.glid, "view")
        proj_loc = glGetUniformLocation(self.shader.glid, "proj")
        obj_color = glGetUniformLocation(self.shader.glid, "obj_color")
        view_pos = glGetUniformLocation(self.shader.glid, "view_pos")
        
        light_pos = glGetUniformLocation(self.shader.glid, "light_source[0].light_pos")
        light_pos2 = glGetUniformLocation(self.shader.glid, "light_source[1].light_pos")

        """
        text_alpha = glGetUniformLocation(self.shader.glid, "tex_alpha")
        text1 = glGetUniformLocation(self.shader.glid, "tex_sampler")
        text2 = glGetUniformLocation(self.shader.glid, "tex_sampler2")
        """
        blinn = glGetUniformLocation(self.shader.glid, "blinn")

        light_on_1 = glGetUniformLocation(self.shader.glid, "light_source[0].light_on")
        light_on_2 = glGetUniformLocation(self.shader.glid, "light_source[1].light_on")

        """
        glUniform1i(text1, 0)
        glUniform1i(text2, 1)
        """ 
        glUniform1i(blinn, blinn_switch)
        glUniform3f(view_pos, self.camera.eye.x, self.camera.eye.y, self.camera.eye.z)
        glUniform3f(obj_color, self.color[0], self.color[1], self.color[2])
        """
        glUniform1f(text_alpha, tex_alpha)
        """
        
        if(self.lighter_object is not None):
            glUniform1i(light_on_1, 1)
            glUniform3f(light_pos, self.lighter_object.object_position[0], self.lighter_object.object_position[1], self.lighter_object.object_position[2])
        else:
            glUniform1i(light_on_1, 0)
            
        if(self.lighter_object2 is not None):
            glUniform1i(light_on_2, 1)
            glUniform3f(light_pos2, self.lighter_object2.object_position[0], self.lighter_object2.object_position[1], self.lighter_object2.object_position[2])
        else:
            glUniform1i(light_on_2, 0)

        glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
        glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
        
        """
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.image)
        glActiveTexture(GL_TEXTURE0 + 1)
        glBindTexture(GL_TEXTURE_2D, self.second_image)
        """
        starting_offset = 0
        for i in self.obj.data:
            glDrawArrays(i[0], starting_offset, i[1])
            starting_offset += i[1]


class LightObject:
    def __init__(self, shader, object_position, obj, color, animation):
        self.color = color
        self.shader = shader
        self.counter = 0
        self.frame_counter = 0
        self.animation = animation
        self.obj = obj
        self.object_position = object_position

        VAO = glGenVertexArrays(1)
        glBindVertexArray(VAO)

        VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, VBO)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, self.obj.vertices.itemsize * 8, ctypes.c_void_p(0))

        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, self.obj.vertices.itemsize * 8, ctypes.c_void_p(3*4))
        
    def draw(self, projection, view, model, show_animation, tex_alpha, blinn_status, lighter_object_1, lighter_object_2):
        glBufferData(GL_ARRAY_BUFFER, self.obj.vertices, GL_STATIC_DRAW)


        glUseProgram(self.shader.glid)

        glClearColor(0.0, 0.0, 0.0, 0.0)
        glEnable(GL_DEPTH_TEST)

        model_loc = glGetUniformLocation(self.shader.glid, "model")
        view_loc = glGetUniformLocation(self.shader.glid, "view")
        proj_loc = glGetUniformLocation(self.shader.glid, "proj")

        color = glGetUniformLocation(self.shader.glid, "color")

        glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
        glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)
        glUniform3f(color, self.color[0], self.color[1], self.color[2])

        model = Matrix.create_from_translation(self.object_position)


        if show_animation and self.animation:
            self.object_position[0] = -math.sin(self.frame_counter) * 10 +8
            self.object_position[2] = math.cos(self.frame_counter) * 10 
            self.frame_counter += 360/50/50
            
            glutPostRedisplay()

        glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)

        starting_offset = 0
        for i in self.obj.data:
            glDrawArrays(i[0], starting_offset, i[1])
            starting_offset += i[1]