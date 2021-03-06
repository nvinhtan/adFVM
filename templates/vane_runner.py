import numpy as np
import os

from adFVM import config
from adFVM.compat import intersectPlane
from adFVM.density import RCF 
from adpy import tensor
from adFVM.mesh import Mesh

# import the design objective and some helper functions
from adFVM.objectives.vane import objective, getPlane, getWeights

# base folder for flow problem
case = './'
config.hdf5 = True

# create and initialize the folder (read mesh and setup boundary conditions)
primal = RCF(case, objective=objective, fixedTimeStep=True)
getPlane(primal)
getWeights(primal)

# define perturbations for computing sensitivities of the design objective
def makePerturb(mid):
    def perturb(fields, mesh, t):
        G = 1e0*np.exp(-1e2*np.linalg.norm(mid-mesh.cellCentres[:mesh.nInternalCells], axis=1, keepdims=1)**2)
        #rho
        rho = G
        rhoU = np.zeros((mesh.nInternalCells, 3), config.precision)
        rhoU[:, 0] = G.flatten()*100
        rhoE = G*2e5
        return rho, rhoU, rhoE
    return perturb
perturb = [makePerturb(np.array([-0.02, 0.01, 0.005], config.precision)),
           makePerturb(np.array([-0.08, -0.01, 0.005], config.precision))]
# perturbation type: source terms for the compressible Navier-Stokes equations
parameters = 'source'

# define perturbation to mesh points
#def makePerturb(param, eps=1e-6):
#    def perturbMesh(fields, mesh, t):
#        if not hasattr(perturbMesh, 'perturbation'):
#            ## do the perturbation based on param and eps
#            #perturbMesh.perturbation = mesh.getPerturbation()
#            points = np.zeros_like(mesh.points)
#            #points[param] = eps
#            points[:] = eps*mesh.points
#            #points[:] = eps
#            perturbMesh.perturbation = mesh.getPointsPerturbation(points)
#        return perturbMesh.perturbation
#    return perturbMesh
#perturb = [makePerturb(1)]
##perturb = []
#
#parameters = 'mesh'

# number of time steps for which to run the simulation
nSteps = NSTEPS
# checkpointing interval for the simulation
# has to be a factor of nSteps
writeInterval = NSTEPS
# sampling interval for the long-time averaged statistics
# has to be a factor of nSteps and writeInterval
sampleInterval = 1
# interval for reporting information about the flow fields
# has to be a factor of nSteps and writeInterval
reportInterval = 1
# starting time for the simulation
startTime = STARTTIME
# initial time step for the simulation
dt = 1e-8

#nSteps = 10
#writeInterval = 5
#sampleInterval = 1
#reportInterval = 1

# interval for how frequently viscosity should be added
viscousInterval = 1
# number of checkpoints to run in a single simulation
# has to be less than nSteps/writeInterval
runCheckpoints = 3
# viscosity stabilized adjoint parameters
# first argument: viscosity scaling factor
# second argument: type of viscosity 
# third argument: not used
#adjParams = [1e-3, 'entropy_barth', None]
