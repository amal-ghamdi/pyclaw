#!/usr/bin/env python
# encoding: utf-8
import numpy as np
from numpy import sqrt, exp, cos


def setaux(x,rhoB=4,KB=4,rhoA=1,KA=1,alpha=0.5,xlower=0.,xupper=1.,bc=2):
    aux = np.empty([2,len(x)],order='F')
    xfrac = x-np.floor(x)
    # Density:
    rho_vec = rhoA*(xfrac<alpha)+rhoB*(xfrac>=alpha)

    # Bulk modulus:
    K_vec = KA  *(xfrac<alpha)+KB  *(xfrac>=alpha)

    # Impedance
    aux[0,:] = sqrt(rho_vec * K_vec)

    # Sound Speed
    aux[1,:] = sqrt(K_vec / rho_vec)

    return aux
    
def acoustics(use_petsc=False,kernel_language='Fortran',solver_type='classic',iplot=False,htmlplot=False,outdir='./_output',weno_order=5, disable_output=False):
    """
    This example solves the 1-dimensional acoustics equations in a spatially varying
    medium.
    """

    #=================================================================
    # Import the appropriate classes, depending on the options passed
    #=================================================================
    if use_petsc:
        import clawpack.petclaw as pyclaw
    else:
        from clawpack import pyclaw

    if solver_type=='classic':
        solver = pyclaw.ClawSolver1D()
    elif solver_type=='sharpclaw':
        solver = pyclaw.SharpClawSolver1D()
        solver.weno_order=weno_order
    else: raise Exception('Unrecognized value of solver_type.')

    #========================================================================
    # Instantiate the solver and define the system of equations to be solved
    #========================================================================
    solver.kernel_language=kernel_language
    from clawpack.riemann import rp_acoustics
    solver.num_waves=rp_acoustics.num_waves

    if kernel_language=='Python': 
        raise Exception('Python kernel not supported')
    else:
        from clawpack.riemann import rp1_acoustics_variable
        solver.rp = rp1_acoustics_variable

    solver.limiters = pyclaw.limiters.tvd.MC

    solver.bc_lower[0] = pyclaw.BC.periodic
    solver.bc_upper[0] = pyclaw.BC.periodic

    solver.aux_bc_lower[0] = pyclaw.BC.periodic
    solver.aux_bc_upper[0] = pyclaw.BC.periodic


    #========================================================================
    # Instantiate the domain and set the boundary conditions
    #========================================================================
    xlower = 0.0
    xupper = 300
    cells_per_layer = 20
    mx = cells_per_layer * (xupper - xlower)
    x = pyclaw.Dimension('x',xlower,xupper,mx)
    domain = pyclaw.Domain(x)
    num_eqn = 2
    state = pyclaw.State(domain,num_eqn)

    #========================================================================
    # Set problem-specific variables
    #========================================================================
    rhoB=1.0; KB=1.0; rhoA=3.0; KA=3.0; alpha=0.5
    bc = 2 ### this probably need to be modified (generalized)
    xc = x.centers
    aux = setaux(xc,rhoB=rhoB,KB=KB,rhoA=rhoA,KA=KA,alpha=alpha,
           xlower=xlower,xupper=xupper, bc=bc)
    state.aux = aux

    #========================================================================
    # Set the initial condition
    #========================================================================
    shift = (xupper - xlower)/2.0
    a = 0.2
    #f = lambda x: a*np.exp(-((x-shift))**2)
    
    f = lambda x: a*(np.abs(x-(shift+0.25)) <= .25) 
    print f(xc)[2970:3030] -aux[0][2970:3030]

    print aux[0][2970:3030]
    state.q[0,:] = f(xc)
    state.q[1,:] = state.q[0,:]# /state.aux[0,:]  

    #solver.dt_initial=domain.grid.delta[0]/np.max(state.aux[1])*0.1
    solver.cfl_desired = 1.0
    solver.dt_variable = True
    solver.max_steps = 100000

    #========================================================================
    # Set up the controller object
    #========================================================================
    claw = pyclaw.Controller()
    claw.solution = pyclaw.Solution(state,domain)
    claw.solver = solver
    claw.outdir = outdir
    claw.keep_copy = False
    claw.num_output_times = 5
    if disable_output:
        claw.output_format = None
    claw.tfinal = 100.0

    # Solve
    status = claw.run()

    # Plot results
    if htmlplot:  pyclaw.plot.html_plot(outdir=outdir)
    if iplot:     pyclaw.plot.interactive_plot(outdir=outdir)

    return claw

if __name__=="__main__":
    from clawpack.pyclaw.util import run_app_from_main
    output = run_app_from_main(acoustics)
