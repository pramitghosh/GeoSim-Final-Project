from pcraster import *
from pcraster.framework import *

class Fire(DynamicModel):
  def __init__(self):
    DynamicModel.__init__(self)
    setclone('clone.map')

  def initial(self):
    self.fire = readmap('start.map')

  def dynamic(self):
    cellsburning = window4total(scalar(self.fire))
    neighbourBurns = cellsburning > 0
    potentialNewFire = neighbourBurns & ~ self.fire
    self.report(potentialNewFire, 'pnf')

    realization = uniform(1) < 0.1
    self.report(realization, 'real')

    newFire = pcrand(potentialNewFire, realization)
    self.fire = pcror(self.fire, newFire)
    self.report(self.fire, 'fire')
    

nrOfTimeSteps=150
myModel = Fire()
dynamicModel = DynamicFramework(myModel,nrOfTimeSteps)
dynamicModel.run()

