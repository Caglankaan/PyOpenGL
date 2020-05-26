# CENG 487 Assignment# by
# Kaan Çağlan
# StudentId: 230201047
# Month Year: 18.05.2020

import numpy as np
from OpenGL.GL import *
import math

class ObjLoader:
    def __init__(self):
        self.chose_type = {3:GL_TRIANGLES, 4: GL_QUADS, 5:GL_POLYGON}
        self.vert_coords = []
        self.text_coords = []
        self.norm_coords = []

        self.vertex_index = []
        self.texture_index = []
        self.normal_index = []

        self.vertices = []
        self.data = []

    def load_model(self, file):
        indices = []
        text_i = []
        norm_i = []

        for line in open(file, 'r'):
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue

            if values[0] == 'v':
                self.vert_coords.append(values[1:4])
            if values[0] == 'vt':
                self.text_coords.append(values[1:3])
            if values[0] == 'vn':
                self.norm_coords.append(values[1:4])

            if values[0] == 'f':

                len_of_values = len(values[1:len(values)])

                if(len(self.data) > 0) and self.data[len(self.data)-1][0] == self.chose_type[len_of_values]:
                    self.data[len(self.data)-1][1] += len_of_values
                else:
                    if len_of_values not in self.chose_type:
                        print("There is no type: ", len_of_values)
                        exit(1)
                    self.data.append([self.chose_type[len_of_values], len_of_values])

                for v in values[1:len(values)]:
                    w = v.split('/')
                    indices.append(int(w[0])-1)
                    
                    if(w[1] != ''):
                        text_i.append(int(w[1])-1)
                    norm_i.append(int(w[2])-1)

        if(len(self.text_coords) == 0):

            self.text_coords.append(["0","0"])

        for i in range(len(indices)):
            self.vertices.extend(self.vert_coords[indices[i]])
            if(len(text_i) == len(indices)):
                self.vertices.extend(self.text_coords[text_i[i]])
            else:

                self.vertices.extend(self.text_coords[0])
            self.vertices.extend(self.norm_coords[norm_i[i]])

        self.vertices = np.array(self.vertices, dtype = 'float32')


    def load_modell_cornell(self, file):
        indices = []

        for line in open(file, 'r'):
            if line.startswith('#'): continue
            values = line.split()
            if not values: continue

            if values[0] == 'v':
                self.vert_coords.append([float(values[1]), float(values[2]), float(values[3])])
            elif values[0] == 'f':

                len_of_values = len(values[1:len(values)])

                if(len(self.data) > 0) and self.data[len(self.data)-1][0] == self.chose_type[len_of_values]:
                    self.data[len(self.data)-1][1] += len_of_values
                else:
                    if len_of_values not in self.chose_type:
                        print("There is no type: ", len_of_values)
                        exit(1)
                    self.data.append([self.chose_type[len_of_values], len_of_values])

                for v in values[1:len(values)]:
                    w = v.split('/')
                    indices.append(int(w[0]) - 1)

        self.text_coords.append(["0","0"])

        counter = 0
        
        for i in range(len(indices)): 
            if counter == 0:
                X = self.vert_coords[indices[i]]
                counter += 1
            elif counter == 1:
                Y = self.vert_coords[indices[i]]
                counter += 1
            elif counter == 2:
                Z = self.vert_coords[indices[i]]
                
                result = []
                for i in range(3):
                    result.append((Y[(i+1)%3] - X[(i+1)%3]) * (Z[(i+2)%3] - X[(i+2)%3]) - (Y[(i+2)%3] - X[(i+2)%3]) * (Z[(i+1)%3] - X[(i+1)%3]))

                sqrt_of_result = 0
                for i in range(3):
                    sqrt_of_result += math.pow(result[i],2)

                sqrt_of_result = math.sqrt(sqrt_of_result)


                for i in range(3):
                    result[i] /= sqrt_of_result

                self.vertices.extend(X)
                self.vertices.extend(self.text_coords[0])
                self.vertices.extend(result)
                self.vertices.extend(Y)
                self.vertices.extend(self.text_coords[0])
                self.vertices.extend(result)
                self.vertices.extend(Z)
                self.vertices.extend(self.text_coords[0])
                self.vertices.extend(result)
                counter = 0
            

        self.vertices = np.array(self.vertices, dtype = 'float32')