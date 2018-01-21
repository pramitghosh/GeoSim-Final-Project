from pcraster import *
from pcraster.framework import *

class Fire(DynamicModel):
  def __init__(self):
    DynamicModel.__init__(self)
    setclone('clone.map')

  def initial(self):
    self.fire = self.readmap("start")
##    aguila(self.fire)
    self.dem = self.readmap("dem")
    self.dem_ldd = ldd(self.dem)
    self.report(self.dem_ldd, 'ldd')

  def dynamic(self):
    win_sum = window4total(scalar(self.fire))
    atleast1 = win_sum >= 1
    prev_burn = pcrnot(self.fire)
##    neighbourBurns = pcrand(atleast1, prev_burn)
    neighbourBurns = atleast1
    self.report(neighbourBurns, 'nburn')
    potentialNewFire = pcrand(prev_burn, neighbourBurns)
    self.report(potentialNewFire, 'pnewfire')

    downhillBurning = downstream(self.dem_ldd, self.fire)
    self.report(downhillBurning, 'downhill')
    p = ifthenelse(downhillBurning == True, scalar(0.8), scalar(0.1))
    self.report(p, 'prob')
    realization = uniform(1) < p
    newFire = pcrand(realization, potentialNewFire)
    self.report(newFire, 'newFire')

    self.fire = pcror(self.fire, newFire)
    self.report(self.fire, 'fire')

nrOfTimeSteps=200
myModel = Fire()
dynamicModel = DynamicFramework(myModel,nrOfTimeSteps)
dynamicModel.run()

