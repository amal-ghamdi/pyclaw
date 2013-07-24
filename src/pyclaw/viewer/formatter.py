#!/usr/bin/env python
# encoding: utf-8
r"""
Module containing the helper class :class:`~pyclaw.viewer.Formatter` and its subclasses.
"""

import os
import numpy as np
import logging
import sys

logger = logging.getLogger('io')

###import logging


# ==========================================================================
#  Formatter Class
# ==========================================================================
class Formatter(object):
    r"""
    Pyclaw Formatter superclass
    """

    # ========== Attributes ================================================
    
    # ========== Properties ================================================
          

    # ========== Initializer =============================================
    def __init__(self,**kargs): 
        r"""Formatter Initialization Routine
        
        """
        raise NotImplementedError
        


    
    # ========== Class Methods =============================================
    def view_int(value, name):
        raise NotImplementedError

    def view_float(value, name= None):
        raise NotImplementedError

    def view_bool(value, name):
        raise NotImplementedError

    def view_string(value, name):
        raise NotImplementedError

    def view_dict(value, name):
        raise NotImplementedError

    def view_ndarray(value, name=None):
        raise NotImplementedError
   
    def __del__():
        raise NotImplementedError




class AsciiFormatter(Formatter):
    r"""
    Pyclaw AsciiFormatter class
    """

    # ========== Attributes ================================================
    
    # ========== Properties ================================================
    @property
    def data_format(self):
        r"""(string) - """
        return 'ascii'


          

    # ========== Initializer =============================================
    ### modify output_file_prefix
    def __init__(self, frame, output_file_prefix,**kargs): # file_prefix='data',path='./_output'
        r"""AsciiFormatter Initialization Routine
        
        """
        self.frame = frame
        self.output_file_prefix = output_file_prefix+str(frame)+'.ascii'
 

    
    # ========== Class Methods =============================================
    def view_int(self,value, name=None):
        self.f.write("%5i                  %s\n" % (value, name))

    def view_double(self,value, name= None):
        self.f.write("%18.8e     %s\n" % (value,name))


#    def view_bool(value, name):

#    def view_string(value, name):

#    def view_dict(value, name):
    
    
    
    def view_array(self,value, name=None):
        ### this is temp, q should go in separate file
        q_file = self.f
        ### no need for this assignment, set value directly
        q = value
        dims = value.shape
        if len(dims) == 2:
            for k in xrange(dims[1]):
                for m in xrange(dims[0]):
                    q_file.write("%18.8e" % q[m,k])
                q_file.write('\n')
        elif len(dims) == 3:
            for j in xrange(dims[2]):
                for k in xrange(dims[1]):
                    for m in xrange(dims[0]):
                        q_file.write("%18.8e" % q[m,k,j])
                    q_file.write('\n')
                q_file.write('\n')
        elif len(dims) == 4:
            for l in xrange(dims[3]):
                for j in xrange(dims[2]):
                    for k in xrange(dims[1]):
                        for m in range(dims[0]):
                            q_file.write("%18.8e" % q[m,k,j,l])
                        q_file.write('\n')
                q_file.write('\n')
            q_file.write('\n')
        else:
            raise Exception("Dimension Exception in writing fort file.")

    def open(self):
        ### all this function needs modification::
        ### creating the dir should probably go somewhereelse
        # Determine if we need to create the path
        outdir = os.path.expandvars(os.path.expanduser('./outdir'))
        if not os.path.exists(outdir):
            try:
                os.makedirs(outdir)
            except OSError:
                print "directory already exists, ignoring"  



        try:
        # Create file 
            file_name = '%s_%s.%s' % (self.output_file_prefix,str(self.frame.get_counter()),'ascii')
            self.f = open(os.path.join(outdir,file_name),'w')
        except IOError, (errno, strerror):
            logger.error("Error opening file: %s" % os.path.join(self.outdir,
                         file_name))
            logger.error("I/O error(%s): %s" % (errno, strerror))
            raise 
        except:
            logger.error("Unexpected error:", sys.exc_info()[0])
            raise

    def close(self):
        self.f.close()

    def delete(self):
        pass

    
    def __del__(self):
        return



