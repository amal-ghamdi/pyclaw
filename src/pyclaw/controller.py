#!/usr/bin/env python
# encoding: utf-8
r"""
Controller for basic computation and plotting setup.

This module defines the Pyclaw controller class.  It can be used to perform
simulations in a convenient manner similar to that available in previous
versions of Clawpack, i.e. with output_style and
output time specification.  It also can be used to set up easy plotting and 
running of compiled fortran binaries.
"""

import logging
import sys
import os
import copy

from .solver import Solver
from .util import FrameCounter

class Controller(object):
    r"""Controller for pyclaw simulation runs and plotting
            
    :Initialization:
    
        Input: None
    
    :Examples:

        >>> import clawpack.pyclaw as pyclaw
        >>> x = pyclaw.Dimension('x',0.,1.,100)
        >>> domain = pyclaw.Domain((x))
        >>> state = pyclaw.State(domain,3,2)
        >>> claw = pyclaw.Controller()
        >>> claw.solution = pyclaw.Solution(state,domain)
        >>> claw.solver = pyclaw.ClawSolver1D()
    """

    #  ======================================================================
    #   Property Definitions
    #  ======================================================================

    #  ======================================================================
    #   Initialization routines
    #  ======================================================================
    def __init__(self):
        r"""
        Initialization routine for a Controller object.
        
        See :class:`Controller` for full documentation.
        """
        
        import numpy as np

        self.viewable_attributes = ['xdir','rundir','outdir','overwrite',
                        'xclawcmd','xclawout','xclawerr','runmake','savecode',
                        'solver','keep_copy','write_aux_init',
                        'write_aux_always','output_format',
                        'output_file_prefix','output_options','num_output_times',
                        'output_style','verbosity']
        r"""(list) - Viewable attributes of the `:class:`~pyclaw.controller.Controller`"""

        # Global information for running and/or plotting
        self.xdir = os.getcwd()
        r"""(string) - Executable path, executes xclawcmd in xdir"""
        self.rundir = os.getcwd()
        r"""(string) - Directory to run from (containing \*.data files), uses 
        \*.data from rundir"""
        self.outdir = os.getcwd()+'/_output'
        r"""(string) - Output directory, directs output files to outdir"""

        self.xclawcmd = 'xclaw'
        r"""(string) - Command to execute (if using fortran), defaults to xclaw or
        xclaw.exe if cygwin is being used (which it checks vis sys.platform)"""
        if sys.platform == 'cygwin':
            self.xclawcmd = 'xclaw.exe'


        self.xclawout = None
        r"""(string) - Where to write timestep messages"""
        self.xclawerr = None
        r"""(string) - Where to write error messages"""
        self.runmake = False
        r"""(bool) - Run make in xdir before xclawcmd"""
        self.savecode = False
        r"""(bool) - Save a copy of \*.f files in outdir"""
        
        # Solver information
        self.solution = None
        self.solver = None
        r"""(:class:`~pyclaw.solver.Solver`) - Solver object"""
        
        # Classic output parameters, used in run convenience method
        self.tfinal = 1.0
        r"""(float) - Final time output, ``default = 1.0``"""
        self.verbosity = 0 
        r"""(int) - Level of output, ``default = 0``"""
        
        ### could go in the plot viewer
        # Data objects
        self.plotdata = None
        r"""(:class:`~visclaw.data.ClawPlotData`) - An instance of a 
        :class:`~visclaw.data.ClawPlotData` object defining the 
        objects plot parameters."""
        


        self.start_frame = 0


    # ========== Access methods ===============================================
    def __str__(self):        
        output = "Controller attributes:\n"
        for attr in self.viewable_attributes:
            value = getattr(self,attr)
            output = output + "  %s = %s \n" % (attr,value)
        output = output + '\n'
        if self.plotdata is not None:
            output = output + "  Data "+str(self.plotdata)+"\n"
        if self.solver is not None:
            output = output + "  Solver "+str(self.solver)+"\n"
        if len(self.frames) > 0:
            output = output + "  Frames \n"
            for frame in self.frames:
                output = output + "    " + str(frame) + "\n"
        return output
        
    # ========== Properties ==================================================
    
    def check_validity(self):
        r"""Check that the controller has been properly set up and is ready to run.

            Checks validity of the solver
        """
        # Check to make sure we have a valid solver to use
        if self.solver is None:
            raise Exception("No solver set in controller.")
        if not isinstance(self.solver,Solver):
            raise Exception("Solver is not of correct type.")
        if not self.solver.is_valid():
            raise Exception("The solver failed to initialize properly.") 
            
        # Check to make sure the initial solution is valid
        if not self.solution.is_valid():
            raise Exception("Initial solution is not valid.")
        if not all([state.is_valid() for state in self.solution.states]):
            raise Exception("Initial states are not valid.")
        
 
    # ========== Plotting methods ============================================        
    # ========== Solver convenience methods ==================================
    def run(self):
        r"""
        Convenience routine that will evolve solution based on the 
        traditional clawpack output and run parameters.
        
        This function uses the run parameters and solver parameters to evolve
        the solution to the end time specified in run_data, outputting at the
        appropriate times.
        
        :Input:
            None
            
        :Ouput:
            (dict) - Return a dictionary of the status of the solver.
        """
        import numpy as np

        if self.solver is None or self.solution is None:
            raise Exception('To run, a Controller must have a Solver and a Solution.')

        ### create viewer
        ### hand it in
        ### destroy viewer
        ### controller should provide tfinal for each viewer

        ### setting the start frame for each viewer
        
        ### Create default viewer in the case of no viewers were
        ### setting tinitial?

        ### set up
        if len(self.viewers) == 0:
            ### you should import the correct pyclaw lib
            default_viewer = pyclaw.viewer.AsciiViewer()
            self.viewers.append(default_viewer)
            default_viewer.num_output_times = 10
        else:
            self.viewers[0].tfinal = self.tfinal
            self.viewers[0].start_frame = self.start_frame


        ### elsewhere self.start_frame = self.solution.start_frame
        if len(self.solution.patch.grid.gauges)>0:
            self.solution.patch.grid.setup_gauge_files(self.outdir)
        frame = FrameCounter()

        frame.set_counter(self.start_frame)
        if self.keep_copy:
            self.frames = []
                    
        self.solver.setup(self.solution)
        self.solver.dt = self.solver.dt_initial
            
        self.check_validity()

        # Write initial gauge values
        self.solver.write_gauge_values(self.solution)
        

        ### define viewers to be viewer if you only have one viewer,
        ### or to be the first one? what is the convention? 

        # Output styles
        ###if self.output_style == 1:
        ###    output_times = np.linspace(self.solution.t,
        ###            self.tfinal,self.num_output_times+1
        ###            -self.start_frame)
        ###elif self.output_style == 2:
        ###    output_times = self.out_times
        ###elif self.output_style == 3:
        ###    output_times = np.ones((self.num_output_times+1
        ###                            -self.start_frame))
        ###else:
        ###    raise Exception("Invalid output style %s" % self.output_style)  
        
        ### this leave space for customized viewer (if viewer == 'checkpoint')
        self.solution.view_function = self.solution.view


        ### this propaply be a list of tuples containing the viewer index and the time
        ### modify the way it is set
        output_times = self.viewers[0].out_times
        
        ### modify the palce of the import and the way the library is defined
        from clawpack.pyclaw.viewer import formatter 

        # Output and save initial frame
        if self.keep_copy:
            self.frames.append(copy.deepcopy(self.solution))
        ### modify
        if self.viewers[0].file_format is not None:
            if os.path.exists(self.outdir) and self.viewers[0].overwrite==False:
                raise Exception("Refusing to overwrite existing output data. \
                 \nEither delete/move the directory or set controller.overwrite=True.")
            if self.viewers[0].compute_p is not None:
                self.viewers[0].compute_p(self.solution.state)
                formattor = formatter.AsciiFormatter(frame,'./testp') ### frame, file

                ### modify parameters
                self.solution.view_function(formattor,write_p=True)

###                self.solution.view_function(frame,self.p_outdir,
###                                        self.output_format,
###                                        self.p_file_prefix ,
###                                        write_aux = False,
###                                        options = self.output_options,
###                                        write_p = True) 
            formattor = formatter.AsciiFormatter(frame,'./test')
            self.solution.view_function( formattor)
###            self.solution.write(frame,self.outdir,
###                                        self.output_format,
###                                        self.output_file_prefix,
###                                        self.write_aux_init,
###                                        self.output_options)

### later:
###        self.write_F('w')

        self.log_info("Solution %s computed for time t=%f" % 
                        (frame,self.solution.t) )

        for t in output_times[1:]:                
            if self.output_style < 3:
                status = self.solver.evolve_to_time(self.solution,t)
            else:
                # Take nstepout steps and output
                for n in xrange(self.nstepout):
                    status = self.solver.evolve_to_time(self.solution)
            frame.increment()
            if self.keep_copy:
                # Save current solution to dictionary with frame as key
                self.frames.append(copy.deepcopy(self.solution))
            if self.output_format is not None:
                if self.compute_p is not None:
                    self.compute_p(self.solution.state)
                    self.solution.write(frame,self.p_outdir,
                                            self.output_format,
                                            self.p_file_prefix ,
                                            write_aux = False, 
                                            options = self.output_options,
                                            write_p = True) 
                
                self.solution.write(frame,self.outdir,
                                            self.output_format,
                                            self.output_file_prefix,
                                            self.write_aux_always,
                                            self.output_options)
            self.write_F()

            self.log_info("Solution %s computed for time t=%f"
                % (frame,self.solution.t))
            for gfile in self.solution.state.grid.gauge_files: 
                gfile.flush()
            
        self.solver.teardown()
        for gfile in self.solution.state.grid.gauge_files: gfile.close()

        # Return the current status of the solver
        return status
    
    # ========== Advanced output methods ==================================

    def write_F(self,mode='a'):
        if self.compute_F is not None:
            self.compute_F(self.solution.state)
            F = [0]*self.solution.state.mF
            for i in xrange(self.solution.state.mF):
                F[i] = self.solution.state.sum_F(i)
            if self.is_proc_0():
                t=self.solution.t
                F_file = open(self.F_outdir,mode)
                F_file.write(str(t)+' '+' '.join(str(j) for j in F) + '\n')
                F_file.close()
    
    def is_proc_0(self):
        return True

    def log_info(self, str):
        import logging
        logging.info(str)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
