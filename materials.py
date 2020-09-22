#MATERIALS

from mathfunc import color

class Material(object):
  def __init__(self,diffuse):
    self.diffuse = diffuse

ivory = Material(diffuse = color(100,100,80))
snow = Material(diffuse = color(209, 232, 237))
coal = Material(diffuse = color(0,0,0))
carrot = Material(diffuse = color(227, 110, 14))
white = Material(diffuse = color(255, 255, 255))
