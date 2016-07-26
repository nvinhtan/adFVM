import numpy as np
import time
import cPickle as pkl
import os
import copy

from . import config, parallel, timestep
from .config import ad, T
from .parallel import pprint
from .memory import printMemUsage

from .field import Field, CellField, IOField
from .mesh import Mesh
from .mesh import extractField

logger = config.Logger(__name__)

class Solver(object):
    defaultConfig = {
                        'timeIntegrator': 'euler',
                        'objective': lambda x: 0,
                        'adjoint': False,
                        'dynamicMesh': False,
                        'localTimeStep': False,
                        'stepFactor': 1.0,
                        'postpro': [],
                        'sourceTerms': []
                    }

    def __init__(self, case, **userConfig):
        logger.info('initializing solver for {0}'.format(case))
        fullConfig = self.__class__.defaultConfig
        fullConfig.update(userConfig)
        for key in fullConfig:
            setattr(self, key, fullConfig[key])

        self.mesh = Mesh.create(case)
        self.resultFile = self.mesh.case + 'objective.txt'
        self.statusFile = self.mesh.case + 'status.pkl'
        self.timeSeriesFile = self.mesh.case + 'timeSeries.txt'
        Field.setSolver(self)

        self.timeStepCoeff = getattr(timestep, self.timeIntegrator)()
        self.nStages = self.timeStepCoeff[0].shape[0]
        self.stage = 0
        self.init = None
        return

    def compile(self, adjoint=False):
        self.compileInit()

        pprint('Compiling solver', self.__class__.defaultConfig['timeIntegrator'])
        if self.localTimeStep:
            self.dt = ad.bcmatrix()
        else:
            self.dt = ad.scalar()
        self.t0 = ad.scalar()

        # default values
        self.t = self.t0*1.
        self.dtc = self.dt
        self.local, self.remote = self.mesh.nCells, self.mesh.nFaces

        stackedFields = ad.matrix()
        newStackedFields = timestep.timeStepper(self.equation, self.boundary, stackedFields, self)
        self.map = self.function([stackedFields, self.dt, self.t0], \
                       [newStackedFields, self.dtc, self.local, self.remote], 'forward')
        if adjoint:
            stackedAdjointFields = ad.matrix()
            scalarFields = ad.sum(newStackedFields*stackedAdjointFields)
            gradientInputs = [stackedFields] + list(zip(*self.sourceTerms)[0])
            gradients = ad.grad(scalarFields, gradientInputs)
            #meshGradient = ad.grad(scalarFields, mesh)
            self.adjoint = self.function([stackedFields, stackedAdjointFields, self.dt, self.t0], \
                            gradients, 'adjoint')
            #self.tangent = self.function([stackedFields, stackedAdjointFields, self.dt], \
            #                ad.Rop(newStackedFields, stackedFields, stackedAdjointFields), 'tangent')
        if config.compile:
            exit()
        pprint()

    def compileInit(self, functionName='init'):
        internalFields = []
        completeFields = []
        for phi in self.fields:
            phiI, phiN = phi.completeField()
            internalFields.append(phiI)
            #completeFields.append(phiN)
        for phi in self.fields:
            phiN = phi.phi.field
            completeFields.append(phiN)
        self.init = self.function(internalFields, completeFields, functionName, source=False)
        return

    def function(self, inputs, outputs, name, **kwargs):
        return SolverFunction(inputs, outputs, self, name, **kwargs)

    def stackFields(self, fields, mod): 
        return mod.concatenate([phi.field for phi in fields], axis=1)

    def unstackFields(self, stackedFields, mod, names=None, **kwargs):
        if names is None:
            names = self.names
        fields = []
        nDimensions = np.concatenate(([0], np.cumsum(np.array(self.dimensions))))
        nDimensions = zip(nDimensions[:-1], nDimensions[1:])
        for name, dim, dimRange in zip(names, self.dimensions, nDimensions):
            phi = stackedFields[:, range(*dimRange)]
            fields.append(mod(name, phi, dim, **kwargs))
        return fields

    def getSymbolicFields(self, field=True):
        names = self.names
        fields = []
        for index, dim in enumerate(self.dimensions):
            if dim == (1,):
                field = ad.bcmatrix()
            else:
                field = ad.matrix()
            fields.append(CellField(names[index], field, dim))
        return fields

    def initSource(self):
        self.sourceFields = self.getSymbolicFields()
        symbolics = [phi.field for phi in self.sourceFields]
        values = [np.zeros((self.mesh.origMesh.nInternalCells, nDims[0]), config.precision) for nDims in self.dimensions]
        self.sourceTerms = zip(symbolics, values)
        return

    def updateSource(self, source):
        for index, value in enumerate(source):
            #if index == 1:
            #    phi = IOField.internalField('rhoUS', value, (3,))
            #    with IOField.handle(startTime):
            #        phi.write()
            self.sourceTerms[index][1][:] = value
        return

    def readFields(self, t):
        fields = []
        with IOField.handle(t):
            for name in self.names:
                fields.append(IOField.read(name))
        if self.init is None:
            self.fields = fields
        else:
            self.updateFields(fields)
        return 

    def getBCFields(self):
        return [phi.phi for phi in self.fields]

    def setBCFields(self, fields):
        for phi, phiN in zip(self.getBCFields(), fields):
            phi.field = phiN.field

    def setFields(self, fields):
        for phi, phiN in zip(self.fields, fields):
            phi.field = phiN.field
        return

    def initFields(self, t, read=True):
        if read:
            self.readFields(t)
        fields = self.init(*[phi.field for phi in self.fields])
        for phi, phiN in zip(self.fields, fields):
            phi.field = phiN
        return self.fields

    def updateFields(self, fields):
        self.setFields(fields)
        for phi, phiB in zip(self.getBCFields(), [phi.boundary for phi in fields]):
            for patchID in self.mesh.sortedPatches:
                patch = phi.BC[patchID]
                for key, value in zip(patch.keys, patch.inputs):
                    if key == 'value':
                        nFaces = self.mesh.origMesh.boundary[patchID]['nFaces']
                        value[1][:] = extractField(phiB[patchID][key], nFaces, phi.dimensions)
        return

    def writeFields(self, fields, t):
        self.setFields(fields) 
        with IOField.handle(t):
            for phi in self.fields:
                phi.write()
        return

    def readStatusFile(self):
        data = None
        scatterData = None
        if parallel.rank == 0:
            with open(self.statusFile, 'rb') as status:
                readData = pkl.load(status)
            data = readData[:-1]
            scatterData = readData[-1]
        data = parallel.mpi.bcast(data, root=0)
        data.append(parallel.mpi.scatter(scatterData, root=0))
        return data

    def writeStatusFile(self, data):
        data[-1] = parallel.mpi.gather(data[-1], root=0)
        if parallel.rank == 0:
            with open(self.statusFile, 'wb') as status:
                pkl.dump(data, status)
        return

    def removeStatusFile(self):
        if parallel.rank == 0:
            try:
                os.remove(self.statusFile)
            except OSError:
                pass

    def equation(self, *fields):
        pass

    def boundary(self, *newFields):
        boundaryFields = self.getBCFields()
        for phiB, phiN in zip(boundaryFields, newFields):
            phiB.setInternalField(phiN.field)
        return boundaryFields

    def run(self, endTime=np.inf, writeInterval=config.LARGE, startTime=0.0, dt=1e-3, nSteps=config.LARGE, \
            startIndex=0, result=0., mode='simulation', source=lambda *args: []):

        logger.info('running solver for {0}'.format(nSteps))
        mesh = self.mesh
        #initialize
        fields = self.initFields(startTime)
        pprint()

        # time management
        t = startTime
        dts = dt
        timeIndex = startIndex
        lastIndex = 0
        if self.localTimeStep:
            dt = dts*np.ones_like(mesh.origMesh.volumes)
        elif isinstance(dts, np.ndarray):
            dt = dts[timeIndex]
        stackedFields = self.stackFields(fields, np)

        # objective is local
        instObjective = self.objective(stackedFields)
        result += instObjective
        timeSeries = [parallel.sum(instObjective)]
        timeSteps = []

        # writing and returning local solutions
        if mode == 'forward':
            if self.dynamicMesh:
                instMesh = Mesh()
                instMesh.boundary = copy.deepcopy(self.mesh.origMesh.boundary)
                solutions = [(instMesh, stackedFields)]
            else:
                solutions = [stackedFields]

        # source term update
        self.updateSource(source(fields, mesh.origMesh, t))

        pprint('Time marching for', ' '.join(self.names))

        def iterate(t, timeIndex):
            return t < endTime and timeIndex < nSteps
        while iterate(t, timeIndex):
            printMemUsage()
            start = time.time()

            for index in range(0, len(fields)):
                fields[index].info()

            pprint('Time step', timeIndex)
            #stackedFields, dtc = self.map(stackedFields)
            stackedFields, dtc, local, remote = self.map(stackedFields, dt, t)
            #print local.shape, local.dtype, (local).max(), (local).min(), np.isnan(local).any()
            #print remote.shape, remote.dtype, np.abs(remote).max(), np.abs(remote).min(), (remote).max(), (remote).min(), np.isnan(remote).any()

            fields = self.unstackFields(stackedFields, IOField)

            # TODO: fix unstacking F_CONTIGUOUS
            for phi in fields:
                phi.field = np.ascontiguousarray(phi.field)

            parallel.mpi.Barrier()
            end = time.time()
            pprint('Time for iteration:', end-start)
            pprint('Time since beginning:', end-config.runtime)
            pprint('Running average objective: ', parallel.sum(result)/(timeIndex + 1))

            # time management
            timeSteps.append([t, dt])
            timeIndex += 1
            if self.localTimeStep:
                pprint('Simulation Time:', t, 'Time step: min', parallel.min(dt), 'max', parallel.max(dt))
                t += 1
            else:
                pprint('Simulation Time:', t, 'Time step:', dt)
                t = round(t+dt, 9)
            if self.localTimeStep:
                dt = dtc
            elif isinstance(dts, np.ndarray):
                dt = dts[timeIndex]
            else:
                dt = min(parallel.min(dtc), dt*self.stepFactor, endTime-t)

            mesh.update(t, dt)
            self.updateSource(source(fields, mesh.origMesh, t))

            # objective management
            instObjective = self.objective(stackedFields)
            result += instObjective
            timeSeries.append(parallel.sum(instObjective))

            # write management
            if mode == 'forward':
                if self.dynamicMesh:
                    instMesh = Mesh()
                    instMesh.boundary = copy.deepcopy(self.mesh.origMesh.boundary)
                    solutions.append((instMesh, stackedFields))
                else:
                    solutions.append(stackedFields)
            elif (timeIndex % writeInterval == 0) or not iterate(t, timeIndex):
                # write mesh, fields, status
                dtc = IOField.internalField('dtc', dtc, (1,))
                self.writeFields(fields + [dtc], t)
                if mode != 'simulation':
                    self.writeStatusFile([timeIndex, t, dt, result])

                # write timeSeries if in orig mode (problem.py)
                if mode == 'orig' and parallel.rank == 0:
                    with open(self.timeStepFile, 'a') as f:
                        np.savetxt(f, timeSteps[lastIndex:])
                    with open(self.timeSeriesFile, 'a') as f:
                        np.savetxt(f, timeSeries[lastIndex:])
                    lastIndex = len(timeSteps)
            pprint()

        if mode == 'forward':
            return solutions
        return result


class SolverFunction(object):
    counter = 0
    def __init__(self, inputs, outputs, solver, name, BCs=True, postpro=False, source=True):
        logger.info('compiling function')
        self.symbolic = []
        self.values = []
        mesh = solver.mesh
        # values require inplace substitution
        self.populate_mesh(self.symbolic, mesh, mesh)
        self.populate_mesh(self.values, mesh.origMesh, mesh)
        if BCs:
            self.populate_BCs(self.symbolic, solver, 0)
            self.populate_BCs(self.values, solver, 1)
        # source terms
        if source and len(solver.sourceTerms) > 0:
            symbolic, values = zip(*solver.sourceTerms)
            self.symbolic.extend(symbolic)
            self.values.extend(values)
        # postpro variables
        if postpro and len(solver.postpro) > 0:
            symbolic, values = zip(*solver.postpro)
            self.symbolic.extend(symbolic)
            self.values.extend(values)

        self.generate(inputs, outputs, solver.mesh.case, name)

    def populate_mesh(self, inputs, mesh, solverMesh):
        attrs = Mesh.fields + Mesh.constants
        for attr in attrs:
            inputs.append(getattr(mesh, attr))
        for patchID in solverMesh.sortedPatches:
            for attr in solverMesh.getBoundaryTensor(patchID):
                inputs.append(mesh.boundary[patchID][attr[0]])

    def populate_BCs(self, inputs, solver, index):
        fields = solver.getBCFields()
        for phi in fields:
            if hasattr(phi, 'BC'):
                for patchID in solver.mesh.sortedPatches:
                    inputs.extend([value[index] for value in phi.BC[patchID].inputs])

    def generate(self, inputs, outputs, caseDir, name):
        SolverFunction.counter += 1
        pklFile = caseDir + '{0}_func_{1}.pkl'.format(config.device, name)
        inputs.extend(self.symbolic)

        fn = None
        pklData = None
        if parallel.rank == 0:
            start = time.time()
            if os.path.exists(pklFile) and config.unpickleFunction:
                pprint('Loading pickled file', pklFile)
                pklData = open(pklFile).read()
            else:
                fn = T.function(inputs, outputs, on_unused_input='ignore', mode=config.compile_mode)#, allow_input_downcast=True)
                #T.printing.pydotprint(fn, outfile='graph.png')
                if config.pickleFunction or (parallel.nProcessors > 1):
                    pklData = pkl.dumps(fn)
                    pprint('Saving pickle file', pklFile)
                    open(pklFile, 'w').write(pklData)
                    pprint('Module size: {0:.2f}'.format(float(len(pklData))/(1024*1024)))
            end = time.time()
            pprint('Compilation time: {0:.2f}'.format(end-start))

        if not config.compile:
            start = time.time()
            pklData = parallel.mpi.bcast(pklData, root=0)
            #if parallel.mpi.bcast(fn is not None, root=0) and parallel.nProcessors > 1:
            #    T.gof.cc.get_module_cache().refresh(cleanup=False)
            end = time.time()
            pprint('Transfer time: {0:.2f}'.format(end-start))

            start = time.time()
            unloadingStages = config.user.unloadingStages
            coresPerNode = config.user.coresPerNode
            coresPerStage = coresPerNode/unloadingStages
            nodeStage = (parallel.rank % coresPerNode)/coresPerStage
            for stage in range(unloadingStages):
                printMemUsage()
                if (nodeStage == stage) and (fn is None):
                    fn = pkl.loads(pklData)
                parallel.mpi.Barrier()
            end = time.time()
            pprint('Loading time: {0:.2f}'.format(end-start))
            printMemUsage()

        self.fn = fn

    def __call__(self, *inputs):
        logger.info('running function')
        inputs = list(inputs)
        #print 'get', id(self.values[29].data)
        inputs.extend(self.values)
        return self.fn(*inputs)

