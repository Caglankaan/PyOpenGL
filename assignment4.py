# CENG 487 Assignment# by
# Kaan Çağlan
# StudentId: 230201047
# Month Year: 18.05.2020

from shapes import *
from shader import Shader
from OpenGL.GLUT import *
from camera import *
import random
from viewer import Viewer
from object_loader import *
from texture_loader import *

def main():
    cam = Camera("hw2")
    cam.createView(Point3f(0.0, 0.0, 30.0),
                  Vector3f(0.0, 1.0, 0.0))
    
    cam.setNear(1)
    cam.setFar(1000)

    viewer = Viewer(cam)
    color_shader = Shader("vert.vs", "frag.fs")
    geom_shader = Shader("point_shadows_depth.vs","point_shadows_depth.fs","point_shadows_depth.gs")

    lighter_shader = Shader("light_vert.vs", "light_frag.fs")

    """
    image = load_texture("textures/cube2.png")
    second_image = load_texture("textures/cube.png")
    """

    sphere_obj = ObjLoader()
    sphere_obj.load_model("object_files/sphere.obj")
    
    cornell_obj = ObjLoader()
    cornell_obj.load_modell_cornell("object_files/cornell.obj")

    LighterObject = LightObject(lighter_shader, [18,3,0], sphere_obj, [1.0, 1.0, 3.0], True)
    LighterObject2 = LightObject(lighter_shader, [0,40,0], sphere_obj, [1.0, 1.0, 3.0], False)
    ShadowsObject = RenderShadows(cam, color_shader, geom_shader, [0,0,-5], cornell_obj, None, None, LighterObject,LighterObject2)
    CornellObject = ShapeFromObjectFile(cam, color_shader, [0,0,-5], cornell_obj, None, None, LighterObject,LighterObject2)
    
    viewer.add(["Shadow", True, ShadowsObject, False, LighterObject, LighterObject2])
    viewer.add(["Cornell", True, CornellObject, False, LighterObject, LighterObject2])
    viewer.add(["Lighter1", True, LighterObject, False, LighterObject, LighterObject2])
    viewer.add(["Lighter2", True, LighterObject2, False, LighterObject, LighterObject2])
    print("Press a to enable/disable lighter1 animation.")
    print("Press 1 and 2 to enable/disable lighters.")
    print("Press b to enable/disable blinn specular formula for lighters.")
    print("Press x and Shift +x to move in x direction.")
    print("Press y and Shift +y to move in y direction.")
    print("Press z and Shift +z to move in z direction.")
    glutMainLoop()


if __name__ == '__main__':
    main()
