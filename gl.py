#Maria Jose Castro Lemus 
#181202
#Graficas por Computadora - 10
#RT1: Esferas
#snowman

import struct 
from materials import coal, snow, ivory, carrot,white
from sphere import Sphere
from mathfunc import norm, V3, color, char,dword, word
from collections import namedtuple
import random
from numpy import matrix, cos, sin, tan, pi
import math

BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255)

class Render(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.scene = []
        self.activeTexture = BLACK
        self.clear()

    def clear(self):
        self.framebuffer= [
        [self.activeTexture for x in range(self.width)]
        for y in range(self.height)
        ]

    def point(self, x, y, selectColor=None):
        try:
            self.framebuffer[y][x] = self.activeTexture
        except:
            pass
        
    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height
        #r = Render(width,height)

    def write(self, filename):
        f = open(filename, 'bw')
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(14 + 40))

        #image header 
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        #pixel data
        for x in range(self.width):
            for y in range(self.height):
                f.write(self.framebuffer[y][x])
        f.close()

        #Referencia del repositorio ejemplo de dennis
    def glFinish(self, filename='out.bmp'):
        self.write(filename)

    def scene_intersect(self, orig, direction):
        for obj in self.scene:
            if obj.ray_intersect(orig, direction):
                return obj.material
        return None

    def cast_ray(self, orig, direction):
        #funcion de rayo que nos va a retorar un color
        impacted_material = self.scene_intersect(orig, direction)
        if impacted_material: #si si impacto retornamos el ojo
            #print('impacted material', impacted_material.diffuse)
            return impacted_material.diffuse
            #return color (200, 0, 0)
        else:
            #print('color', color(0,0,200))
            return color(77, 158, 179)

    def render(self):
        fov = int(pi/2)
        for y in range(self.height):
            for x in range(self.width):
                i =  (2*(x + 0.5)/self.width - 1) * tan(fov/2) * self.width/self.height
                j =  (2*(y + 0.5)/self.height - 1) * tan(fov/2)
                direction = norm(V3(i, j, -1))
                self.framebuffer[y][x] = self.cast_ray(V3(0,0,0), direction)
                


r = Render(1000, 1000)
#r.glCreateWindow(1000, 1000)
#r.render(1000, 1000)
#r.glClearcolor(0.75, 0.25, 0.39)
r.scene = [
    
    #Carbones
    Sphere(V3(1,0,-10), 0.2, coal),
    Sphere(V3(-0.7,0,-10), 0.2, coal),
    Sphere(V3(-2.5,0,-10), 0.2, coal),
    
    #eyes
    Sphere(V3(4,0.5,-10), 0.18, coal),
    Sphere(V3(4,-0.5,-10), 0.18, coal),
    Sphere(V3(4,0.5,-10), 0.3, snow),
    Sphere(V3(4,-0.5,-10), 0.3, snow),

    #nose
    Sphere(V3(3,0,-10), 0.26, carrot),

    #smile
    Sphere(V3(2.25,0,-10), 0.1, coal),
    Sphere(V3(2.4,0.5,-10), 0.1, coal),
    Sphere(V3(2.4,-0.5,-10), 0.1, coal),
    Sphere(V3(2.7,0.8,-10), 0.1, coal),
    Sphere(V3(2.7,-0.8,-10), 0.1, coal),
    Sphere(V3(3.1,1,-10), 0.1, coal),
    Sphere(V3(3.1,-1,-10), 0.1, coal),

    #snowballs
    Sphere(V3(3.3,0,-10), 1.5, white),
    Sphere(V3(0.3,0,-10), 2, white),
    Sphere(V3(-3.1,0,-12), 3, white)

]
r.render()
r.glFinish()
