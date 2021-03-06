#!/usr/bin/env python
#
# pyBeam, an open-source Beam Solver
#
# Copyright (C) 2019 by the authors
# 
# File Developers: Ruben Sanchez (SciComp, TU Kaiserslautern)
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

import shutil
import numpy as np
import sys, os, csv

from pyBeamLib import pyBeamSolver
from pyBeamLibAD import pyBeamSolverAD
import pyMLSInterface as interpolate

import pickle

# Load running directory
file_dir = os.path.dirname(os.path.realpath(__file__))

############################
# Import data stored
############################
input_file = file_dir + '/data.pkl'
f = open(input_file, 'rb')
StructNodes, AeroNodes, AeroLoads, AeroAdjoints = pickle.load(f)

# Copy the solution file to the running directory
solution_file = file_dir + '/solution.pyBeam'
shutil.move(solution_file, "solution.pyBeam")

config_file = file_dir + '/config.pyMLS'
MLS = interpolate.pyMLSInterface(config_file, AeroNodes, StructNodes)

loadsX = MLS.interpolation_matrix.transpose().dot(AeroLoads[:,0])
loadsY = MLS.interpolation_matrix.transpose().dot(AeroLoads[:,1])
loadsZ = MLS.interpolation_matrix.transpose().dot(AeroLoads[:,2])

adjX = MLS.interpolation_matrix.transpose().dot(AeroAdjoints[:,0])
adjY = MLS.interpolation_matrix.transpose().dot(AeroAdjoints[:,1])
adjZ = MLS.interpolation_matrix.transpose().dot(AeroAdjoints[:,2])

########################################
# Initialize and set loads/crossed terms
########################################

adjoint = pyBeamSolverAD(file_dir, 'configAD.pyBeam')

for iNode in range(0,len(loadsX)):
  adjoint.SetLoads(iNode, loadsX[iNode], loadsY[iNode], loadsZ[iNode])
  adjoint.SetDisplacementAdjoint(iNode, adjX[iNode], adjY[iNode], adjZ[iNode])
  
############################
# Solve adjoint
############################
  
adjoint.ReadRestart() 
adjoint.StartRecording()
adjoint.SetDependencies()
adjoint.Restart()
adjoint.StopRecording()
adjoint.ComputeAdjoint()

sensE = adjoint.PrintSensitivityE()

############################
# Tests
############################

print("\n############################\n TEST \n############################\n")
test = adjoint.TestSensitivityE(sensE, 1.0546216892681002e-13)

exit(test)
