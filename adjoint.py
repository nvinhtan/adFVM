#!/usr/bin/python2
from __future__ import print_function

import numpy as np
import time
import sys

from field import CellField
from ops import derivative, forget, strip
from utils import ad

firstCheckpoint = 0
if len(sys.argv) > 1:
    timeSteps = np.loadtxt(sys.argv[1])
    if len(sys.argv) > 2:
        firstCheckpoint = int(sys.argv[2])
else:
    print('Primal run time step file not specified')
    exit()

from problem import primal, nSteps, writeInterval, objective
assert ad.__name__ == 'numpad'
mesh = primal.mesh

if firstCheckpoint == 0:
    adjointFields = [CellField('{0}a'.format(name), mesh, ad.zeros((mesh.nInternalCells, dimensions[0])), mesh.calculatedBoundary) for name, dimensions in zip(primal.names, primal.dimensions)]
else:
    adjointFields = [CellField.read('{0}a'.format(name), mesh, timeSteps[nSteps - firstCheckpoint*writeInterval][0]) for name in primal.names]
stackedAdjointFields = np.hstack([ad.value(phi.field) for phi in adjointFields])
nDimensions = np.concatenate(([0], np.cumsum(np.array([phi.dimensions[0] for phi in adjointFields]))))
nDimensions = zip(nDimensions[:-1], nDimensions[1:])

print('STARTING ADJOINT\n')

def writeAdjointFields(writeTime):
    for index in range(0, len(nDimensions)):
        phi = adjointFields[index]
        # range creates a copy
        phi.field = stackedAdjointFields[:, range(*nDimensions[index])]
        phi.info()
        phi.write(writeTime)
    print()

for checkpoint in range(firstCheckpoint, nSteps/writeInterval):
    print('PRIMAL FORWARD RUN {0}: {1} Steps\n'.format(checkpoint, writeInterval))
    primalIndex = nSteps - (checkpoint + 1)*writeInterval
    solutions = primal.run(timeSteps[primalIndex], nSteps=writeInterval, adjoint=True)

    print('ADJOINT BACKWARD RUN {0}: {1} Steps\n'.format(checkpoint, writeInterval))
    if checkpoint == 0:
        lastSolution = solutions[-1][-1]
        stackedAdjointFields = derivative(objective(lastSolution), lastSolution)
        writeAdjointFields(timeSteps[-1][0])

    for step in range(0, writeInterval):
        start = time.time()

        adjointIndex = writeInterval-1 - step
        currentSolution = solutions[adjointIndex + 1][0]
        previousSolution = solutions[adjointIndex][-1]
        stackedFields = ad.hstack([phi.field for phi in currentSolution])
        jacobians = derivative(ad.sum(stackedFields*stackedAdjointFields), previousSolution)
        sensitivities = derivative(objective(previousSolution), previousSolution)
        print(jacobians.min(), jacobians.max())
        print(sensitivities.min(), sensitivities.max())
        stackedAdjointFields = jacobians + sensitivities
        forget(currentSolution)

        end = time.time()
        print('Time for iteration: {0}'.format(end-start))
        print('Simulation Time and step: {0}, {1}\n'.format(*timeSteps[primalIndex + adjointIndex + 1]))

    writeAdjointFields(timeSteps[primalIndex][0])