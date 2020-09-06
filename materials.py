#MATERIALS
class Material(object):
  def __init__(self,diffuse):
    self.diffuse = diffuse

ivory = Material(diffuse=color(100,100,80))
snow = Material(diffuse=color(80,10,0))

