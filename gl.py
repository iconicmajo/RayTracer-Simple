#Maria Jose Castro Lemus 
#181202
#Graficas por Computadora - 10
#RT1: Esferas
#snowman

import struct 
from obj import Obj
from Sphere import * 

def char(c):
    return struct.pack('=c', c.encode('ascii'))
def word(c):
    return struct.pack('=h', c)
def dword(c):
    return struct.pack('=l', c)
def color(r, g, b):
    return bytes([b, g, r]) 


class Render(object):
    def __init__(self):
        self.framebuffer =[]

    def glInit(self):
        pass

    def clear(self, r, g,b):
        self.framebuffer= [
        [color(r,g,b) for x in range(self.width)]
        for y in range(self.height)
        ]

    def  glClear(self):
        self.clear()

    def glClearcolor(self, r, g, b):
        r = round(r*255)
        g = round(g*255)
        b = round(b*255)
        self.clear(r, g, b)

    def glColor(self, r,g,b):
        r = round(r*255)
        g = round(g*255)
        b = round(b*255)
        return color(r, g, b)
        
    def glCreateWindow(self, width, height):
        self.width = width
        self.height = height
        #r = Render(width,height)

    def glViewport(self, x, y, width, height):
        self.viewPortWidth = width
        self.viewPortHeight = height
        self.xViewPort = x
        self.yViewPort = y

    def glVertex(self, x,y):
        calcX = round((x+1)*(self.viewPortWidth/2)+self.xViewPort)
        calcY = round((y+1)*(self.viewPortHeight/2)+self.yViewPort)
        self.point(calcX, calcY)


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

    #function dot
    def point(self, x, y):
        try:
            self.framebuffer[x][y] = self.glColor(0.01176470,0.583921569,0.9882352941)
        except:
            pass  

    def glLine(self,x0, y0, x1, y1):
        '''x0 = round((x0+1)*(self.viewPortWidth/2)+self.xViewPort)
        y0 = round((y0+1)*(self.viewPortHeight/2)+self.yViewPort)
        x1 = round((x1+1)*(self.viewPortWidth/2)+self.xViewPort)
        y1 = round((y1+1)*(self.viewPortHeight/2)+self.yViewPort)'''
        #print('coordenadas',x0, y0, x1, y1)
        dy = abs(y1 - y0)
        dx = abs(x1 - x0)
        steep = dy > dx

        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1

        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0

        dy = abs(y1 - y0)
        dx = abs(x1 - x0)

        offset = 0
        threshold = dx

        y = y0
        for x in range(x0, x1):
            if steep:
                self.point(y, x)
            else:
                self.point(x, y)
            
            offset += dy * 2
            if offset >= threshold:
                y += 1 if y0 < y1 else -1
                threshold += dx * 2

        #Referencia del repositorio ejemplo de dennis
    def glFinish(self, filename='out.bmp'):
        self.write(filename)

    def load(self, filename, translate, scale):
      model = Obj(filename)

      for face in model.faces:
        vcount = len(face)
        #print(vcount)

        for j in range(vcount):
            f1 = face[j][0]
            f2 = face[(j + 1) % vcount][0]

            v1 = model.vertices[f1 - 1]
            v2 = model.vertices[f2 - 1]
            
            x1 = round((v1[0] + translate[0]) * scale[0])
            y1 = round((v1[1] + translate[1]) * scale[1])
            x2 = round((v2[0] + translate[0]) * scale[0])
            y2 = round((v2[1] + translate[1]) * scale[1])
            #print(x1, y1, x2, y2)
            self.glLine(x1, y1, x2, y2)

    def scene_intersect(self, orig, direction):
        for obj in self.scene:
            if obj.ray_intersect(orig, direction):
                return obj.material
        return None

    def cast_ray(self, orig, dorection):
        #funcion de rayo que nos va a retorar un color
        impacted_material = self.scene_intersect(orig, direction)
        if impacted_material: #si si impacto retornamos el ojo
            return impacted_material.diffuse
            #return color (200, 0, 0)
        else:
            return color(0,0, 200)
        #reutrn color(0, 0, 200)


    def render(self):
        fov = int(pi/2) #la apertura o los grados del ojo
        for y in range(self.height):
            for x in range(self.width):
                i = (2* (x -0.5)/self.width-1)*self.width/self.height * tan(fov/2)
                i = (1- 2* (x -0.5)/self.width)* * tan(fov/2)
                r = (x/self.width)
                g = (y/self.height)
                b = 0 
                #self.pixels[y][x]= color(r, g,b) 
                direction = norm(V3(i, j, -1))
                self.pixels[y][x]= self.cast_ray(v3(0,0,0),direction)



r = Render()
r.glCreateWindow(1000, 1000)
r.scene = [
    Sphere(V3(0,-1.5,-10), 1.5, ivory),
    Sphere(V3(2,-1,-12), 1.5, snow)
]
#r.glClearcolor(0.75, 0.25, 0.39)

#r.load('lego-person.obj', [3, 0] ,[75,75])
r.glFinish()
