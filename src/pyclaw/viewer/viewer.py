#!/usr/bin/env python
# encoding: utf-8
r"""
Module containing pyclaw viewer classes
"""

import os
###import logging


# ============================================================================
#  Viewer Class
# ============================================================================
class Viewer(object):
    r"""
    Pyclaw viewer superclass
    """

    # ========== Attributes ==================================================
    
    # ========== Properties ==================================================
    @property
    def example(self):
        r"""(float) - Example att"""
        return 1
          

    # ========== Class Methods ===============================================
    def __init__(self,file_prefix='fort'):
        r"""Viewer Initialization Routine
        
        """

        ## anything
        ### open file?
        self._frame_no = 0
        try:
        # Create file name
            file_name = '%s.t%s' % (file_prefix,str(frame).zfill(4))
            self.f = open(os.path.join(path,file_name),'w')
        except IOError, (errno, strerror):
            logger.error("Error writing file: %s" % os.path.join(path,
                         file_name))
            logger.error("I/O error(%s): %s" % (errno, strerror))
            raise 
        except:
            logger.error("Unexpected error:", sys.exc_info()[0])
            raise


    
    # ========== Class Methods ===============================================
    def view_int(value, name):
        self.f.write("%5i                  %s\n" % (value, name))

    def view_bool(value, name):
        self.f.write("%5i                  %s\n" % (value, name))

    def viewer.view_string(value, name):
        return

    def viewer.view_dict(value, name):
        return

    def viewer.view_array(value, name=None):
        return
    
    def __del__():
        return
    
    def increment_frame()
        self._frame_no = self._frame_no + 1

