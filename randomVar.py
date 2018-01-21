from pcraster import *
from pcraster.framework import *

class RandomModel(DynamicModel):
  def __init__(self):
    DynamicModel.__init__(self)
    setclone('clone.map')

  def initial(self):
    pass

  def dynamic(self):
    res_normal = normal(1)
    res_uniform = uniform(1)
##    self.report(res_normal, 'normal')
    self.report(res_uniform, 'uniform')
    res_mapuniform = mapuniform()
    self.report(res_mapuniform, 'muniform')
    q34 = 10 + res_normal*5
    self.report(q34, 'q34')
    ppt8 = res_uniform > 0.2
    self.report(ppt8, 'ppt8')

nrOfTimeSteps=10
myModel = RandomModel()
dynamicModel = DynamicFramework(myModel,nrOfTimeSteps)
dynamicModel.run()

