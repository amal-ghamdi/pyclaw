#!/usr/bin/env python
# encoding: utf-8
r"""
Module containing pyclaw viewer classes
"""

import os
import numpy as np
import logging
import sys

logger = logging.getLogger('io')

# ==========================================================================
#  Viewer Class
# ==========================================================================
class Viewer(object):
    r"""
    Pyclaw viewer superclass
    """

    # ========== Attributes ================================================
    
    # ========== Properties ================================================
    @property
    def out_times(self):
        r"""(int) - Output time list, only used with ``output_style = 2``,
        ``default = numpy.linspace(self.tinitial,self.tfinal,
                                    self.num_output_times
                                    -self.start_frame)``"""
        if self.output_style == 2 and \
           self._out_times_custom is not None:
            return self._out_times_custom
        elif self.tfinal is None:
            raise Exception('the class variable `tfinal` was not set.')
        else:
            self._out_times = np.linspace(self.tinitial,self.tfinal,
                                    self.num_output_times
                                    -self.start_frame)
            return self._out_times
  
    _out_times = None
    _out_times_custom = None
    @out_times.setter
    def out_times(self,value):
        if self.output_style == 2:
            self._out_times_custom = value # Outstyle 2
        else:
            raise Exception("`out_times` cannot be set for `output_style`"+
            str(self.output_style))

    @property
    def p_outdir(self):
        r"""(string) - Directory to use for writing derived quantity files"""
        return os.path.join(self.outdir,'_p')
    @property
    def F_outdir(self):
        r"""(string) - Full path to output file for functionals"""
        return os.path.join(self.outdir,self.F_file_prefix+'.txt')


    # ========== Initializer =============================================
    def __init__(self,**kargs): # file_prefix='data',path='./_output'    
        r"""Viewer Initialization Routine
        
        """

        self.keep_copy = False 
        r"""(bool) - Keep a copy in memory of every output time, 
        ``default = False``"""
        self.frames = []
        r"""(list) - List of saved frames if ``keep_copy`` is set to ``True``"""
        self.nstepout = 1               # Outstyle 3 defaults
        r"""(int) - Number of steps between output, only used with 
        ``output_style = 3``, ``default = 1``"""

        self.output_style = 1
        r"""(int) - Time output style, ``default = 1``"""

        self.num_output_times = 10                  # Outstyle 1 defaults
        r"""(int) - Number of output times, only used with ``output_style = 1``,
        ``default = 10``"""

        self.start_frame = None

        self.tfinal = None
        r"""(float) - Final time output """

        self.tinitial = 0.0
        r"""(float) - Initial time """

        self.xdir = os.getcwd()
        r"""(string) - Executable path, executes xclawcmd in xdir"""

        self.rundir = os.getcwd()
        r"""(string) - Directory to run from (containing \*.data files), uses 
        \*.data from rundir"""

        self.overwrite = True
        r"""(bool) - Ok to overwrite old result in outdir, ``default = True``"""

        self.outdir = os.getcwd()+'/_output'
        r"""(string) - Output directory, directs output files to outdir"""

        # Derived quantity p
        self.p_file_prefix = 'claw_p'
        r"""(string) - File prefix to be prepended to derived quantity output files"""
        self.compute_p = None
        r"""(function) - function that computes derived quantities"""
        
        # functionals
        self.compute_F = None
        r"""(function) - Function that computes density of functional F"""
        self.F_file_prefix = 'F'
        r"""(string) - Name of text file containing functionals"""







        
        


    
    # ========== Class Methods =============================================
    



class RawDataViewer(Viewer):
    r"""
    Pyclaw RawDataViewer class
    """

    # ========== Attributes ================================================
    
    # ========== Properties ================================================

    # ========== Initializer =============================================
    def __init__(self,**kargs): # file_prefix='data',path='./_output'    
        r"""Viewer Initialization Routine
        """
        
        super(RawDataViewer, self).__init__(**kargs)

        self.viewer_type= None
        r"""(string) - could take either ``checkpoint`` or ``customized``
        """

        self.subdir = os.path.join(self.outdir,'checkpoint')
        r"""(string) - Output directory, directs output files to outdir"""

        self.write_aux_init = False
        r"""(bool) - Write out initial auxiliary array, ``default = False``"""
        
        self.write_aux_always = False
        r"""(bool) - Write out auxiliary array at every time step, 
        ``default = False``"""

        # Output parameters for run convenience method
        self.file_format = 'ascii'
        r"""(list of strings) - Format or list of formats to output the data, 
        if this is None, no output is performed.  See _pyclaw_io for more info
        on available formats.  ``default = 'ascii'``"""
        self.output_file_prefix = 'claw'
        r"""(string) - File prefix to be appended to output files, 
        ``default = None``"""
        self.output_options = {}
        r"""(dict) - Output options passed to function writing and reading 
        data in output_format's format.  ``default = {}``"""


        ## anything
        ### open file?
        #self._frame_no = 0


    
    # ========== Class Methods =============================================
    def create_file():
        ### creating the dir should probably go somewhereelse
        # Determine if we need to create the path
        path = os.path.expandvars(os.path.expanduser(self.outdir))
        if not os.path.exists(self.outdir):
            try:
                os.makedirs(self.outdir)
            except OSError:
                print "directory already exists, ignoring"  



        try:
        # Create file 
            file_name = '%s.%s' % (self.output_file_prefix,self.file_format)
            self.f = open(os.path.join(self.outdir,file_name),'w')
        except IOError, (errno, strerror):
            logger.error("Error opening file: %s" % os.path.join(self.outdir,
                         file_name))
            logger.error("I/O error(%s): %s" % (errno, strerror))
            raise 
        except:
            logger.error("Unexpected error:", sys.exc_info()[0])
            raise

    

