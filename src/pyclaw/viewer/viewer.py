#!/usr/bin/env python
# encoding: utf-8
r"""
Module containing pyclaw viewer classes
"""

import os
###import logging


# ==========================================================================
#  Viewer Class
# ==========================================================================
class Viewer(object):
    r"""
    Pyclaw viewer superclass
    """

    # ========== Attributes ================================================
    
    # ========== Properties ================================================
          

    # ========== Initializer =============================================
    def __init__(self,**kargs): # file_prefix='data',path='./_output'    
        r"""Viewer Initialization Routine
        
        """

        ## anything
        ### open file?
        #self._frame_no = 0
        try:
        # Create file 
            file_name = '%s.%s' % (file_prefix,self.file_format)
            self.f = open(os.path.join(path,file_name),'w')
        except IOError, (errno, strerror):
            logger.error("Error opening file: %s" % os.path.join(path,
                         file_name))
            logger.error("I/O error(%s): %s" % (errno, strerror))
            raise 
        except:
            logger.error("Unexpected error:", sys.exc_info()[0])
            raise
        


    
    # ========== Class Methods =============================================



class AsciiViewer(Viewer):
    r"""
    Pyclaw AsciiViewer class
    """

    # ========== Attributes ================================================
    
    # ========== Properties ================================================
    @property
    def file_format(self):
        r"""(string) - """
        return 'ascii'
          

    # ========== Initializer =============================================
    def __init__(self,**kargs): # file_prefix='data',path='./_output'
        r"""AsciiViewer Initialization Routine
        
        """
        super(UniformRandomSimulation, self).__init__(**kargs)
         


    
    # ========== Class Methods =============================================
    def view_int(value, name):
        self.f.write("%5i                  %s\n" % (value, name))

    def view_float(value, name= None):
        self.f.write("%18.8e     d%s\n" % (value,name))


#    def view_bool(value, name):

#    def view_string(value, name):

#    def view_dict(value, name):

    def view_array(value, name=None):
        dims = value.shape
        if length(len(value.shape)) == 2:
            for k in xrange(dims[1]):
                for m in xrange(dims[0]):
                    q_file.write("%18.8e" % q[m,k])
                q_file.write('\n')
        elif patch.num_dim == 3:
            for j in xrange(dims[2]):
                for k in xrange(dims[1]):
                    for m in xrange(dims[0]):
                        q_file.write("%18.8e" % q[m,k,j])
                    q_file.write('\n')
                q_file.write('\n')
        elif patch.num_dim == 4:
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


    
    def __del__():
        return


