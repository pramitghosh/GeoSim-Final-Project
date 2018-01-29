# GeoSim-Final-Project
Repository for the final project in Geosimulation Modelling (WS 2017/2018)


------
#GROUP MEMBERS:
Monica, Pramit, Raphael, Zhendong


------
#PAPER:
We are working with the paper "Distance-weighted city growth" by Rybski et al. (2013).


------
#TASK:
The task is to create a model that reproduces the results of the paper.

------
#This Branch:
This branch, coded and maintained by Pramit, tries to optimize the method for calculating the the probability q_j in each iteration. This branch, once working correctly, could be merged with the code for counting clusters of a given size and its probability density, which is being implemented currently within the group.

##General Methodology:
This branch contains a parallel alternative development to pre-calculate the distances (d). This avoids the use of nested loops in each run of the `dynamic` in the PCRaster Python framework, which saves considerable amount of time. The use of this branch is to first run `pre.py` and then `post.py` after that. `pre.py` pre-calculates the distances for each cell and saves them as a PCRaster timeseries(!). In `post.py`, these files are then renamed and read accordingly with the help of some low-level string manipulations on the file names based on the size of the region under study (here 100x100 cells). This size has been hardcoded for development purposes currently - it can be generalized for any N later on as needed.

##Current problems:
Currently, the new cells which are generated are limited till the cell with TRUE value in the initial configuration (here the center cell). While investigating this issue it was found that the q_j values obtained (from which the w_j values were calculated in each iteration) were skewed based on the initial configuration. Changing wj[i][j] to 1 in calc_num() results in a different pattern for q_j. This has to be investigated.