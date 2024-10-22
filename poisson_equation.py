import matplotlib.pyplot as plt
import numpy as np

from fenics import *

# Create mesh and define function space
mesh = UnitSquareMesh(8, 10)
V = FunctionSpace(mesh, 'P', 3)

# Define boundary condition
u_D = Expression('1 + x[0]*x[0] + 2*x[1]*x[1]', degree=2)


def boundary(x, on_boundary):
    return on_boundary


bc = DirichletBC(V, u_D, boundary)

# Define Varational problem
u = TrialFunction(V)
v = TestFunction(V)
f = Constant(-6.0)
a = dot(grad(u), grad(v))*dx
L = f*v*dx

# Compute solution
u = Function(V)
solve(a == L, u, bc)


# Save solution to file in VTK format
vtkfile = File('poisson/solution.pvd')
vtkfile << u

# Compute error in L2 norm
error_L2 = errornorm(u_D, u, 'L2')

# Compute maximum error at vertices
vertex_value_u_D = u_D.compute_vertex_values(mesh)
vertex_value_u = u.compute_vertex_values(mesh)
error_max = np.max(np.abs(vertex_value_u_D - vertex_value_u))

# Print errors
print('u:', u)
print('Error L2:', error_L2)
print('Error max:', error_max)

# Plot solution and mesh
plot(u)
plt.show()
plt.savefig('poissonEq.png')
