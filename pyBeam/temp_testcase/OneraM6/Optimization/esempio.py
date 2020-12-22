#!/usr/bin/env python3
#
# pyBeam, a Beam Solver
#
# Copyright (C) 2018 Ruben Sanchez, Rocco Bombardieri, Rauno Cavallaro
# 
# Developers: Ruben Sanchez (SciComp, TU Kaiserslautern)
#             Rocco Bombardieri, Rauno Cavallaro (Carlos III University Madrid)
#
# This file is part of pyBeam.
#
# pyBeam is free software: you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public License
# as published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# pyBeam is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See the GNU Affero General Public License for more details.
# You should have received a copy of the GNU Affero
# General Public License along with pyBeam.
# If not, see <http://www.gnu.org/licenses/>.
#

import numpy as np
import array
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys, os
from pyBeamLibAD import pyBeamSolverAD
from pyBeamOpenMDAO import pyBeamOpt
import re

# Load running directory
file_dir = os.path.dirname(os.path.realpath(__file__))
load = (19 ,100, 0, 5000)
beam = pyBeamOpt(file_dir ,'config_lin.cfg',load)

DV=(beam.SetInitialParameters()[0])
print(DV[0])
DesignVArs = np.array(DV).transpose()
DesignVArs = np.array(DesignVArs.tolist())
DesignVArs = np.reshape(DesignVArs, DesignVArs.size)
ad=beam.ComputeAdjointKSBuckling_opt_lin(DesignVArs)
print(ad)

#DV =np.array([272.63 ,53.52,1.00,1.00,100.00,8,25.00])
#ADw =beam.ComputeAdjointWeight_opt(DV)
#AdKS=beam.ComputeAdjointKS_opt_lin(DV)
#weight = beam.ComputeWeight_opt(DV)
#Ks=beam.ComputeResponseKSStress_opt_lin(DV)
#print(weight)
#print(Ks)




#beam.SetLoads(62 , 0, 0 ,-5) #
#beam.SetLoads(19 , 0, 0 , 7.8e-02)
#beam.SetLoads(19 , 0.78005, 0 , 0)

