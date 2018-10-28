from pcraster import *
from pcraster.framework import *
import numpy as np

def calc_num(wj, i, j, g):
  sop = 0
  sop_d = 0
  for x in range(0,len(wj)):
    for y in range(0, len(wj)):
      if x != i or y != j:
        dist_xy_ij = ((x - i) ** 2 + (y - j) ** 2) ** 0.5
        d_exp = dist_xy_ij ** (-1 * g)
        sop = sop + d_exp * wj[x][y]
        sop_d = sop_d + d_exp
  sop_norm = float(sop/sop_d)
  #print sop
  #print sop_d
  #print sop_norm
  return sop_norm

class Fire(DynamicModel):
  def __init__(self):
    DynamicModel.__init__(self)
    setclone('model2.map')

  def initial(self):
      self.numpy_arr = np.full((10,10), 0)
      self.numpy_arr[4][4] = 1
      self.wj = numpy2pcr(Boolean, self.numpy_arr, -1)
      #aguila(self.wj)
      self.gamma = 2
      self.suit = uniform(1)
      self.it = 1

  def dynamic(self):
      C = 0.5
      cur_wj = pcr2numpy(self.wj, -1)

      res_qj = np.full((10,10), 0.0000)
      for i in range(0, len(cur_wj)):
        for j in range(0, len(cur_wj)):
          res_qj[i][j] = calc_num(cur_wj, i, j, self.gamma)
          #print res_qj[i][j]
          if(res_qj[i][j] > C):
            C = res_qj[i][j]
      pcr_qj = numpy2pcr(Scalar, res_qj, -1)
      #aguila(pcr_qj)
      pcr_qj = (1/C) * pcr_qj
      
      cur_wj = self.suit < pcr_qj
      #aguila(cur_wj)
      cur_wj = pcror(self.wj, cur_wj)

      #aguila(cur_wj)
      clu = clump(cur_wj)
      test = pcr2numpy(clu, 999)
      #test[test==1] = 0
      #print(test)
      #aguila(clu)
      size = areaarea(clu)
      #aguila(size)
      #test2 = pcr2numpy(size, 999)
      #test2[test2>50] = 0
      #print(test2)
      self.report(size, "clusters")
      tr = pcr2numpy(size, 999)
      #print(np.amax(tr))
      tr[tr>50] = 0
      #print(np.amax(tr))
        
      self.wj = cur_wj
      self.it += 1

      if self.it == 14:
        f = open("cluster.txt", 'w')
        for i in range(1,np.amax(test)-1):
          #print(np.unique(test2))
          print("Amount of cluster")
          flat = test.flatten()
          flat = flat.sort()
          
          if np.prod(flat) > 2: 
            secnMax = flat[-2]
            print(flat)
          
          si = size == i
          #aguila(si)
          #tm = pcr2numpy(si, 999)
          #print(tm)
          nc = clump(si)
          aguila(nc)
          grid = pcr2numpy(nc, 999)
          #grid[grid>50] = 0
          print(grid)
          #print("lll")
          print(np.amax(grid)-1)
          print("Cluster size: ",i)
          #print("lll")
          #print(np.amax(tm))
          
          f.write("{0},{1}\n".format(i,np.amax(grid)-1))
        f.close()




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

nrOfTimeSteps=15
myModel = Fire()
dynamicModel = DynamicFramework(myModel,nrOfTimeSteps)
dynamicModel.run()



