# CENG 487 Assignment# by
# Kaan Çağlan
# StudentId: 230201047
# Month Year: 10.05.2020

from OpenGL.GL import *       
import os

class Shader:
    def __init__(self, vertex_source, fragment_source, geometry_source = None):
        
        self.glid = None
        vert = self.loadShader(GL_VERTEX_SHADER, vertex_source )
        frag = self.loadShader(GL_FRAGMENT_SHADER, fragment_source )
        geom = False
        if geometry_source != None:
            geom = self.loadShader(GL_GEOMETRY_SHADER, geometry_source)

        if vert and frag and geom:
            print("buraya girdi hleal olsun")
            self.glid = glCreateProgram()  # pylint: disable=E1111
            glAttachShader(self.glid, vert)
            glAttachShader(self.glid, frag)
            glAttachShader(self.glid, geom)
            glLinkProgram(self.glid)
            glDeleteShader(vert)
            glDeleteShader(frag)
            glDeleteShader(geom)
            status = glGetProgramiv(self.glid, GL_LINK_STATUS)
            if not status:
                print(glGetProgramInfoLog(self.glid).decode('ascii'))
                glDeleteProgram(self.glid)
                self.glid = None

        if vert and frag:
            self.glid = glCreateProgram()  # pylint: disable=E1111
            glAttachShader(self.glid, vert)
            glAttachShader(self.glid, frag)
            glLinkProgram(self.glid)
            glDeleteShader(vert)
            glDeleteShader(frag)
            status = glGetProgramiv(self.glid, GL_LINK_STATUS)
            if not status:
                print(glGetProgramInfoLog(self.glid).decode('ascii'))
                glDeleteProgram(self.glid)
                self.glid = None
        

    def __del__(self):
        glUseProgram(0)
        if self.glid:
            glDeleteProgram(self.glid)

    def findFileOrThrow(self, strBasename):
        
        LOCAL_FILE_DIR = "shaders" + os.sep
        GLOBAL_FILE_DIR = ".." + os.sep + "shaders" + os.sep

        strFilename = LOCAL_FILE_DIR + strBasename
        if os.path.isfile(strFilename):
            return strFilename

        strFilename = GLOBAL_FILE_DIR + strBasename
        if os.path.isfile(strFilename):
            return strFilename

        raise IOError('Could not find target file ' + strBasename)


    def loadShader(self, shaderType, shaderFile):
        strFilename = self.findFileOrThrow(shaderFile)
        shaderData = None
        with open(strFilename, 'r') as f:
            shaderData = f.read()

        shader = glCreateShader(shaderType)
        glShaderSource(shader, shaderData)

        glCompileShader(shader)

        status = glGetShaderiv(shader, GL_COMPILE_STATUS)
        if status == GL_FALSE:
            strInfoLog = glGetShaderInfoLog(shader)
            print(strInfoLog)
            strShaderType = ""
            if shaderType is GL_VERTEX_SHADER:
                strShaderType = "vertex"
            elif shaderType is GL_GEOMETRY_SHADER:
                strShaderType = "geometry"
            elif shaderType is GL_FRAGMENT_SHADER:
                strShaderType = "fragment"

            #print ("Compilation failure for " + strShaderType + " shader:\n" + strInfoLog)

        return shader