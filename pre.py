from pcraster import *
from pcraster.framework import *
import numpy as np
  

##
##def calc_num(dist_template, mgamma):
##  d_map = spread(dist_template, 0, 1)
##  d_exp = d_map ** mgamma
##  return d_exp
##  
##  for x in range(0, len(self.dist_ij)):
##    for y in range(0, len(self.dist_ij)):
##        dist_xy_ij = ((x - i) ** 2 + (y - j) ** 2) ** 0.5
##        d_exp = dist_xy_ij ** (-1 * g)
##        sop = sop + d_exp * wj[x][y]
##        sop_d = sop_d + d_exp
##  sop_norm = float(sop/sop_d)
##  print sop
##  print sop_d
##  print sop_norm
##  return sop_norm

class Fire(DynamicModel):
  def __init__(self):
    DynamicModel.__init__(self)
    setclone('model3.map')

  def initial(self):
      self.dist_ij = np.full((100,100), 0)
##      self.numpy_arr[49][49] = 1
##      self.wj = numpy2pcr(Boolean, self.numpy_arr, -1)
##      aguila(self.wj)
##      self.report(self.wj, 'wj')
      gamma = 2
      self.mg = -1 * gamma
##      self.suit = uniform(1)
      self.it_no = 0

  def dynamic(self):
##    print self.it_no
    i = self.it_no % 100
    j = self.it_no / 100
    self.dist_ij = np.full((100,100), 0)
    self.dist_ij[i][j] = 1
    pcr_dist = numpy2pcr(Nominal,self.dist_ij,-1)
##    aguila(pcr_dist)
    d_map = spread(pcr_dist, 0, 1)
    d_exp = d_map ** self.mg

    self.report(d_exp, '20_')
    self.it_no = self.it_no + 1
    
      # dist_map = spread(self.wj,0,1)
      # aguila(dist_map)
      # dist_exp = dist_map ** (-1 * self.gamma)
      # aguila(dist_exp)
      # dist_sum = maptotal(dist_exp)
      # aguila(dist_sum)

# #     win_sum = window4total(scalar(self.fire))
# #     atleast1 = win_sum >= 1
# #     prev_burn = pcrnot(self.fire)
# # ##    neighbourBurns = pcrand(atleast1, prev_burn)
# #     neighbourBurns = atleast1
# #     self.report(neighbourBurns, 'nburn')
# #     potentialNewFire = pcrand(prev_burn, neighbourBurns)
# #     self.report(potentialNewFire, 'pnewfire')
# #
# #     realization = uniform(1) < 0.1
# #     newFire = pcrand(realization, potentialNewFire)
# #     self.report(newFire, 'newFire')
# #
# #     self.fire = pcror(self.fire, newFire)
# #     self.report(self.fire, 'fire')

nrOfTimeSteps=100*100
myModel = Fire()
dynamicModel = DynamicFramework(myModel,nrOfTimeSteps)
dynamicModel.run()
