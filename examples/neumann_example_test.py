import meshplex
import meshzoo
import pytest
from scipy.sparse import linalg

import pyfvm
from pyfvm.form_language import Subdomain, dGamma, dS, dV, integrate, n_dot_grad


@pytest.mark.skip("meshzoo doesn't have facepartitions anymore")
def test():
    class D1(Subdomain):
        def is_inside(self, x):
            return x[1] < 0.5

        is_boundary_only = True

    class Poisson:
        def apply(self, u):
            return (
                integrate(lambda x: -n_dot_grad(u(x)), dS)
                + integrate(lambda x: 3.0, dGamma)
                - integrate(lambda x: 1.0, dV)
            )

        def dirichlet(self, u):
            return [(u, D1())]

    vertices, cells = meshzoo.rectangle_tri((0.0, 0.0), (1.0, 1.0), 51)
    mesh = meshplex.Mesh(vertices, cells)

    matrix, rhs = pyfvm.discretize_linear(Poisson(), mesh)

    u = linalg.spsolve(matrix, rhs)

    mesh.write("out.vtk", point_data={"u": u})


if __name__ == "__main__":
    test()
