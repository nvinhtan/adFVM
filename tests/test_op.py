from __future__ import print_function
from test import *

from field import Field, CellField
from mesh import Mesh

from op import grad, div, laplacian, snGrad

class TestOp(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.case = '../cases/convection/'
        self.mesh = Mesh.create(self.case)
        Field.setSolver(self)
        self.meshO = self.mesh.origMesh
        
        self.X = self.meshO.cellCentres[:, 0]
        self.Y = self.meshO.cellCentres[:, 1]
        self.XF = self.meshO.faceCentres[:, 0]
        self.YF = self.meshO.faceCentres[:, 1]

        self.U = ad.matrix()
        self.FU = CellField('F', self.U, (3,))
        self.V = ad.bcmatrix()
        self.FV = CellField('F', self.V, (1,))

    def test_grad_scalar(self):
        R = grad(self.FV)
        self.assertTrue(isinstance(R, Field))
        self.assertEqual(R.dimensions, (3,))

        T = np.zeros((self.meshO.nFaces, 1))
        T[:,0] = self.XF*self.YF + self.XF**2 + self.YF**2 + self.XF
        res = evaluate(R.field, self.V, T)
        ref = np.zeros((self.meshO.nInternalCells, 3))
        X = self.X[:self.meshO.nInternalCells]
        Y = self.Y[:self.meshO.nInternalCells]
        ref[:, 0] = Y + 2*X + 1
        ref[:, 1] = X + 2*Y
        checkVolSum(self, res, ref)
        
    def test_grad_vector(self):
        R = grad(self.FU)
        self.assertTrue(isinstance(R, Field))
        self.assertEqual(R.dimensions, (3,3))

        T = np.zeros((self.meshO.nFaces, 3))
        T[:, 0] = self.XF*self.YF + self.XF**2
        T[:, 1] = self.YF + self.YF**2 
        T[:, 2] = 1.
        res = evaluate(R.field, self.U, T)
        ref = np.zeros((self.meshO.nInternalCells, 3, 3))
        X = self.X[:self.meshO.nInternalCells]
        Y = self.Y[:self.meshO.nInternalCells]
        ref[:, 0, 0] = Y + 2*X
        ref[:, 1, 0] = X
        ref[:, 1, 1] = 1 + 2*Y
        checkVolSum(self, res, ref)

    def test_div(self):
        R = div(self.FU.dotN())
        self.assertTrue(isinstance(R, Field))
        self.assertEqual(R.dimensions, (1,))

        T = np.zeros((self.meshO.nFaces, 3))
        T[:, 0] = self.XF + np.sin(2*np.pi*self.XF)*np.cos(2*np.pi*self.YF)
        T[:, 1] = self.YF**2 - np.cos(2*np.pi*self.XF)*np.sin(2*np.pi*self.YF)
        T[:, 2] = self.XF
        res = evaluate(R.field, self.U, T)
        Y = self.Y[:self.meshO.nInternalCells]
        ref = (1 + 2*Y).reshape(-1,1)
        checkVolSum(self, res, ref)

    def test_laplacian(self):
        R = laplacian(self.FV, 1.)
        self.assertTrue(isinstance(R, Field))
        self.assertEqual(R.dimensions, (1,))

        T = np.zeros((self.meshO.nCells, 1))
        T[:, 0] = self.X**2 + self.Y**2 + self.X*self.Y
        res = evaluate(R.field, self.V, T)
        ref = 4.*np.ones((self.meshO.nInternalCells, 1))
        checkVolSum(self, res, ref, relThres=1e-2)

if __name__ == "__main__":
        unittest.main(verbosity=2, buffer=True)