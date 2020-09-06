#importar las funciones matematias

class Sphere(object):
  def __init__(self, center,radius, material):
    self.center = center
    self.radius = radius
    self.material = material

  def ray_intersect(self, orig, direction):
    L = sub(self.center, orig)
    tca = dot(L, direction)
    l = lenght(L)
    d2 = 1**2 - tca**2

    if d2 >self.radius**2:
      return False

    thc = (self.radius **2 - d2 )**0.5
    t0  = tca -thc
    t1 = tca +thc

    if t0<0:
      t0=t1
    if t0 <0:
      return False
    return True 