from field import Field, CellField

from config import ad, Logger
logger = Logger(__name__)
import config

def TVD_dual(phi):
    from op import grad
    assert len(phi.dimensions) == 1
    logger.info('TVD {0}'.format(phi.name))
    mesh = phi.mesh
    # van leer
    psi = lambda r, rabs: (r + rabs)/(1 + rabs)

    faceField = ad.zeros((mesh.nFaces, phi.dimensions[0]))
    faceFields = [faceField, faceField.copy()]
    gradField = grad(interpolate(phi), ghost=True, transpose=True)

    def update(start, end):
        owner = mesh.owner[start:end]
        neighbour = mesh.neighbour[start:end]
        index = 0
        for C, D in [[owner, neighbour], [neighbour, owner]]:
            phiC = phi.field[C]
            phiD = phi.field[D]
            phiDC = phiD-phiC
            R = Field('R', ad.array(mesh.cellCentres[D] - mesh.cellCentres[C]), (3,))
            gradC = Field('gradC({0})'.format(phi.name), gradField.field[C], gradField.dimensions)
            gradF = Field('gradF({0})'.format(phi.name), phiDC, phi.dimensions)
            if phi.dimensions[0] == 1:
                r = 2*gradC.dot(R)/(gradF + config.SMALL) - 1
            else:
                r = 2*gradC.dot(R).dot(gradF)/(gradF.magSqr() + config.SMALL) - 1
            ad.set_subtensor(faceFields[index][start:end], phiC + 0.5*psi(r, r.abs()).field*phiDC)
            index += 1

    update(0, mesh.nInternalFaces)
    for patchID in phi.boundary:
        startFace = mesh.boundary[patchID]['startFace']
        endFace = startFace + mesh.boundary[patchID]['nFaces']
        if phi.boundary[patchID]['type'] in config.coupledPatches:
            update(startFace, endFace)
        else:
            for faceField in faceFields:
                ad.set_subtensor(faceField[startFace:endFace], phi.field[mesh.neighbour[startFace:endFace]])

    return [Field('{0}F'.format(phi.name), faceField, phi.dimensions) for faceField in faceFields]


def upwind(phi, U): 
    assert len(phi.dimensions) == 1
    logger.info('upwinding {0} using {1}'.format(phi.name, U.name)) 
    mesh = phi.mesh
    faceField = ad.zeros((mesh.nFaces, phi.dimensions[0]))
    def update(start, end):
        positiveFlux = ad.value(ad.sum(U.field[start:end] * mesh.normals[start:end], axis=1)) > 0
        negativeFlux = 1 - positiveFlux
        faceField[positiveFlux] = phi.field[mesh.owner[positiveFlux]]
        faceField[negativeFlux] = phi.field[mesh.neighbour[negativeFlux]]

    update(0, mesh.nInternalFaces)
    for patchID in phi.boundary:
        startFace = mesh.boundary[patchID]['startFace']
        endFace = startFace + mesh.boundary[patchID]['nFaces']
        if phi.boundary[patchID]['type'] in config.coupledPatches:
            update(startFace, endFace)
        else:
            faceField[startFace:endFace] = phi.field[mesh.neighbour[startFace:endFace]]

    return Field('{0}F'.format(phi.name), faceField, phi.dimensions)

def central(phi):
    logger.info('interpolating {0}'.format(phi.name))
    mesh = phi.mesh
    factor = mesh.weights
    # for tensor
    if len(factor.shape)-1 < len(phi.dimensions):
        factor = factor.reshape((factor.shape[0], 1, 1))
    faceField = Field('{0}F'.format(phi.name), phi.field[mesh.owner]*factor + phi.field[mesh.neighbour]*(1-factor), phi.dimensions)
    return faceField

interpolate = central


