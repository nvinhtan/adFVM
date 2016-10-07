import numpy as np

from adFVM import config
from adFVM.config import ad
from adFVM.compat import norm, intersectPlane
from adFVM.density import RCF 

primal = RCF('/home/talnikar/adFVM/cases/naca0012/adjoint_weno/', 
             timeIntegrator='SSPRK', 
             CFL=1.2, 
             mu=lambda T: T/T*3.4e-5,
             #faceReconstructor='SecondOrder',
             faceReconstructor='WENO',
             boundaryRiemannSolver='eulerLaxFriedrichs'
)

def dot(a, b):
    return ad.sum(a*b, axis=1, keepdims=True)

# drag over cylinder surface
def objectiveDrag(fields, mesh):
    rho, rhoU, rhoE = fields
    patchID = 'airfoil'
    patch = mesh.boundary[patchID]
    start, end, nF = mesh.getPatchFaceRange(patchID)
    areas = mesh.areas[start:end]
    nx = mesh.normals[start:end, 0].reshape((-1, 1))
    internalIndices = mesh.owner[start:end]
    start = mesh.nInternalCells + start - mesh.nInternalFaces 
    end = mesh.nInternalCells + end - mesh.nInternalFaces
    p = rhoE.field[start:end]*(primal.gamma-1)
    #deltas = (mesh.cellCentres[start:end]-mesh.cellCentres[internalIndices]).norm(2, axis=1, keepdims=True)
    deltas = (mesh.cellCentres[start:end]-mesh.cellCentres[internalIndices]).norm(2, axis=1).reshape((nF,1))
    T = rhoE/(rho*primal.Cv)
    #mungUx = (rhoU.field[start:end, [0]]/rho.field[start:end]-rhoU.field[internalIndices, [0]]/rho.field[internalIndices])*primal.mu(T).field[start:end]/deltas
    mungUx = (rhoU.field[start:end, 0].reshape((nF,1))/rho.field[start:end]-rhoU.field[internalIndices, 0].reshape((nF,1))/rho.field[internalIndices])*primal.mu(T).field[start:end]/deltas
    return ad.sum((p*nx-mungUx)*areas)

def getPlane(solver):
    #point = np.array([0.0032,0.0,0.0], config.precision)
    point = np.array([0.032,0.0,0.0], config.precision)
    normal = np.array([1.,0.,0.], config.precision)
    interCells, interArea = intersectPlane(solver.mesh, point, normal)
    #print interCells.shape, interArea.sum()
    solver.postpro.extend([(ad.ivector(), interCells), (ad.bcmatrix(), interArea)])
    return solver.postpro[-2][0], solver.postpro[-1][0], normal
    
def objectivePressureLoss(fields, mesh):
    #if not hasattr(objectivePressureLoss, interArea):
    #    objectivePressureLoss.cells, objectivePressureLoss.area = getPlane(primal)
    #cells, area = objectivePressureLoss.cells, objectivePressureLoss.area
    ptin = 104190.
    cells, area, normal = getPlane(primal)
    rho, rhoU, rhoE = fields
    solver = rhoE.solver
    g = solver.gamma
    U, T, p = solver.primitive(rho, rhoU, rhoE)
    pi, rhoi, Ui = p.field[cells], rho.field[cells], U.field[cells]
    rhoUi, ci = rhoi*Ui, ad.sqrt(g*pi/rhoi)
    rhoUni, Umagi = dot(rhoUi, normal), ad.sqrt(dot(Ui, Ui))
    Mi = Umagi/ci
    pti = pi*(1 + 0.5*(g-1)*Mi*Mi)**(g/(g-1))
    #res = ad.sum((ptin-pti)*rhoUni*area)/(ad.sum(rhoUni*area) + config.VSMALL)
    res = ad.sum((ptin-pti)*rhoUni*area)#/(ad.sum(rhoUni*area) + config.VSMALL)
    return res 

objective = objectiveDrag
#objective = objectivePressureLoss

def perturb(fields, mesh, t):
    #mid = np.array([-0.012, 0.0, 0.])
    #G = 100*np.exp(-3e4*norm(mid-mesh.cellCentres[:mesh.nInternalCells], axis=1)**2)
    mid = np.array([-0.01, 0.0, 0.])
    G = 1e1*np.exp(-1e6*norm(mid-mesh.cellCentres[:mesh.nInternalCells], axis=1)**2)
    rho = G
    rhoU = np.zeros((mesh.nInternalCells, 3))
    rhoU[:, 0] += G.flatten()*100
    rhoE = G*2e5
    return rho, rhoU, rhoE

nSteps = 100000
writeInterval = 200
startTime = 3.0
dt = 6e-9