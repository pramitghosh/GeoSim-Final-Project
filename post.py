from pcraster import *
from pcraster.framework import *
import numpy as np
##from os import *
import shutil

##class Helper(DynamicModel):
##    def __init__(self, x, y):
##        DynamicModel.__init__(self, x, y)
##        setclone('model3.map')
##
##    def initial(self, x, y):
##      pass
##
##    def dynamic(self, x, y):
##      
##      
##read through the timeseries maps outputted by pre.py
##use the right timeseries value
  


def calc_num(wj, i, j):#, ino):
##  divino = format(ino/float(1000), '.3f')
##  divino = divino.zfill(9)
##  fname = "20_" + divino
##  inostr = str(ino)
##  inostr = inostr.zfill(8)
##  fname = inostr + '.map'
##  fname = inostr

  fnum = i * 100 + j + 1
  fnum = str(fnum).zfill(8)
  fname = fnum
  
  wj[i][j] = 0
  pcr_wj = numpy2pcr(Scalar, wj, -1)
##  print cellvalue(pcr_wj, i * 100 + j + 1)
  d_map = readmap(fname)
  d_np = pcr2numpy(d_map, -1)
##  print d_np[49]
  n_map = pcr_wj * d_map
  sop_norm = float(maptotal(n_map))/float(maptotal(d_map))
  
  #Initializes an object of class Helper
  #Reads the value returned from the Helper
  #and uses that distance
  #
  #sop_d = value returned from Helper alone
  #sop = returned value if wk = TRUE; otherwise 0
  #sum up sop and sop_d using maptotal()
  #return the quotient of sop and sop_d
  
##  for x in range(0,len(wj)):
##    for y in range(0, len(wj)):
##      if x != i or y != j:
##        dist_xy_ij = ((x - i) ** 2 + (y - j) ** 2) ** 0.5
##        d_exp = dist_xy_ij ** (-1 * g)
##        sop = sop + d_exp * wj[x][y]
##        sop_d = sop_d + d_exp
##  sop_norm = float(sop/sop_d)
##  print sop
##  print sop_d
##  print sop_norm
  return sop_norm

class Fire(DynamicModel):
  def __init__(self):
    DynamicModel.__init__(self)
    setclone('model3.map')

  def initial(self):
      self.numpy_arr = np.full((100,100), 0)
      self.numpy_arr[49][49] = 1
      self.wj = numpy2pcr(Boolean, self.numpy_arr, -1)
##      aguila(self.wj)
      self.report(self.wj, 'wj')
      self.gamma = 2
      self.suit = uniform(1)
##      aguila(self.suit)
      self.it_no = 1

      for filename in os.listdir("."):
        if filename.startswith("20_") and not filename.endswith(".map"):
          print filename
          new_fname = filename[3:8] + filename[9:12] + '.map'
          rename(filename, new_fname)
##          shutil.move(str(filename), '/mapped/')

  def dynamic(self):
##      aguila(self.wj)
      cur_wj = pcr2numpy(self.wj, -1)
      C = 0.5
      res_qj = np.full((100,100), 0.0000)
      
      for i in range(100):
        for j in range(100):
          res_qj[i][j] = calc_num(cur_wj, i, j)#, self.it_no)
          if(res_qj[i][j] > C):
            C = res_qj[i][j]
##          print res_qj[i][j]


##      print res_qj[1][1]
##      print res_qj[99][99]
      pcr_qj = numpy2pcr(Scalar, res_qj, -1)
##      C = 1/C
##      aguila(pcr_qj)
##      C = 1/max(pcr_qj)
##      aguila(pcr_qj)
##      print 1/C
      pcr_qj = (1/C) * pcr_qj
##      aguila(pcr_qj)
      trsh_wj = pcr_qj > self.suit
      self.wj = pcror(self.wj, trsh_wj)
##      aguila(self.wj)
      
      self.it_no = self.it_no + 1
##      aguila(trsh_wj)
      aguila(self.wj)
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

nrOfTimeSteps=3
myModel = Fire()
dynamicModel = DynamicFramework(myModel,nrOfTimeSteps)
dynamicModel.run()

