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


        #VAO = glGenVertexArrays(1)
        #glBindVertexArray(VAO)

        VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, VBO)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, self.obj.vertices.itemsize * 8, ctypes.c_void_p(0))

        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, self.obj.vertices.itemsize * 8, ctypes.c_void_p(3*4))
        
        if(self.lighter_object is not None or self.lighter_object2 is not None):
            glEnableVertexAttribArray(2)
            glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, self.obj.vertices.itemsize * 8, ctypes.c_void_p(5*4))

       
    
    def draw(self, projection, view, model, show_animation, tex_alpha, blinn_switch, lighter_object_1, lighter_object_2, show_shadows):
        #glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.lighter_object = lighter_object_1
        self.lighter_object2 = lighter_object_2

        model = Matrix.create_from_translation(self.object_position)

        self.animation = show_animation

        glBufferData(GL_ARRAY_BUFFER, self.obj.vertices, GL_STATIC_DRAW)

        glUseProgram(self.shader.glid)
        glEnable(GL_DEPTH_TEST)

        far_plane = glGetUniformLocation(self.shader.glid, "far_plane")
        model_loc = glGetUniformLocation(self.shader.glid, "model")
        view_loc = glGetUniformLocation(self.shader.glid, "view")
        proj_loc = glGetUniformLocation(self.shader.glid, "proj")
        open_shadows = glGetUniformLocation(self.shader.glid, "open_shadows")

        obj_color = glGetUniformLocation(self.shader.glid, "obj_color")
        view_pos = glGetUniformLocation(self.shader.glid, "view_pos")
        
        light_pos = glGetUniformLocation(self.shader.glid, "light_source[0].light_pos")
        light_pos2 = glGetUniformLocation(self.shader.glid, "light_source[1].light_pos")

        blinn = glGetUniformLocation(self.shader.glid, "blinn")

        light_on_1 = glGetUniformLocation(self.shader.glid, "light_source[0].light_on")
        light_on_2 = glGetUniformLocation(self.shader.glid, "light_source[1].light_on")
 
        glUniform1i(blinn, blinn_switch)

        glUniform1f(far_plane, 25.0)
        glUniform3f(view_pos, self.camera.eye.x, self.camera.eye.y, self.camera.eye.z)
        glUniform3f(obj_color, self.color[0], self.color[1], self.color[2])
        
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
        
        if(show_shadows):
            glUniform1i(open_shadows, True)
        else:
            glUniform1i(open_shadows, False)


        glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)
        glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)

        starting_offset = 0
        for i in self.obj.data:
            glDrawArrays(i[0], starting_offset, i[1])
            starting_offset += i[1]

class RenderShadows:
    def __init__(self, camera, shader, geom_shader, object_position, obj, image, second_image, lighter_object1, lighter_object2):
        self.image = image
        self.camera = camera
        self.lighter_object = lighter_object1
        self.lighter_object2 = lighter_object2
        self.second_image = second_image
        
        self.shader = shader
        self.geom_shader = geom_shader
        self.obj = obj
        self.animation = False
        self.object_position = object_position
        self.color = [1.0, 1.0, 1.0]

        self.depthMapFBO = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, self.depthMapFBO)

        glDrawBuffer(GL_NONE)
        glReadBuffer(GL_NONE)
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
    
    def draw(self, projection, view, model, show_animation, tex_alpha, blinn_switch, lighter_object_1, lighter_object_2, show_shadows):


        #glBindFramebuffer(GL_FRAMEBUFFER, self.depthMapFBO)
        #glClear(GL_DEPTH_BUFFER_BIT)
        self.lighter_object = lighter_object_1
        self.lighter_object2 = lighter_object_2
        

        self.animation = show_animation

        glBufferData(GL_ARRAY_BUFFER, self.obj.vertices, GL_STATIC_DRAW)

        glUseProgram(self.geom_shader.glid)
        glEnable(GL_DEPTH_TEST)


        shadowTransforms = []
        shadowProj = Matrix.create_perspective_projection(90.0*0.01745329251994329576923690768489, 1.0, 1.0, 25.0)

        model = Matrix.create_from_translation(self.object_position)

        shadowTransforms.append(np.dot(shadowProj,self.look_at_shadow(self.lighter_object.object_position, [-12.0, 0.0, 0.0], (0.0,-1.0, 0.0))))
        shadowTransforms.append(np.dot(shadowProj, self.look_at_shadow(self.lighter_object.object_position, [-1.0, 0.0, 0.0], (0.0,-1.0, 0.0))))
        shadowTransforms.append(np.dot(shadowProj, self.look_at_shadow(self.lighter_object.object_position, [0.0, 1.0, 0.0], (0.0,0.0, -1.0))))
        shadowTransforms.append(np.dot(shadowProj, self.look_at_shadow(self.lighter_object.object_position, [0.0, -1.0, 0.0], (0.0,0.0, -1.0))))
        shadowTransforms.append(np.dot(shadowProj, self.look_at_shadow(self.lighter_object.object_position, [0.0, 0.0, 1.0], (0.0,-1.0, 0.0))))
        shadowTransforms.append(np.dot(shadowProj, self.look_at_shadow(self.lighter_object.object_position, [0.0, 0.0, -1.0], (0.0,-1.0, 0.0))))

        light_pos = glGetUniformLocation(self.geom_shader.glid, "lightPos")
        model_loc = glGetUniformLocation(self.geom_shader.glid, "model")
        
        far_plane = glGetUniformLocation(self.geom_shader.glid, "far_plane")

        for i in range(6):
            shadow_matrices_i = glGetUniformLocation(self.geom_shader.glid, "shadowMatrices[" + str(i) + "]")
            glUniformMatrix4fv(shadow_matrices_i, 1, GL_FALSE, shadowTransforms[i])
        glUniform1f(far_plane, 25.0)
        glUniform3f(light_pos, self.lighter_object.object_position[0], self.lighter_object.object_position[1], self.lighter_object.object_position[2])

        glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)


        starting_offset = 0
        for i in self.obj.data:
            glDrawArrays(i[0], starting_offset, i[1])
            starting_offset += i[1]

        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        

    def look_at_shadow(self, eye, center, up):
        center = [eye[0]+center[0], eye[1]+center[1], eye[2]+center[2]]
        f = (center[0] - eye[0], center[1] - eye[1], center[2] - eye[2])
        f_norm = np.linalg.norm(f)
        
        f = f/f_norm

        s = np.cross(f, up)
        s_norm = np.linalg.norm(s)
        s = s/s_norm

        u = np.cross(s,f)

        
        mat = numpy.identity(4)
        mat[0][0] = s[0]
        mat[1][0] = s[1]
        mat[2][0] = s[2]
        mat[0][1] = u[0]
        mat[1][1] = u[1]
        mat[2][1] = u[2]
        mat[0][2] = -f[0]
        mat[1][2] = -f[1]
        mat[2][2] = -f[2]
        mat[3][0] = np.dot(s, eye)
        mat[3][1] = np.dot(u, eye)
        mat[3][2] = np.dot(f, eye)
        
        return mat


class LightObject:
    def __init__(self, shader, object_position, obj, color, animation):
        self.color = color
        self.shader = shader
        self.counter = 0
        self.frame_counter = 0
        self.animation = animation
        self.obj = obj
        self.object_position = object_position

        #VAO = glGenVertexArrays(1)
        #glBindVertexArray(VAO)

        #VBO = glGenBuffers(1)
        #glBindBuffer(GL_ARRAY_BUFFER, VBO)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, self.obj.vertices.itemsize * 8, ctypes.c_void_p(0))

        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, self.obj.vertices.itemsize * 8, ctypes.c_void_p(3*4))
        
    def draw(self, projection, view, model, show_animation, tex_alpha, blinn_status, lighter_object_1, lighter_object_2, show_shadows):
        glBufferData(GL_ARRAY_BUFFER, self.obj.vertices, GL_STATIC_DRAW)


        glUseProgram(self.shader.glid)

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