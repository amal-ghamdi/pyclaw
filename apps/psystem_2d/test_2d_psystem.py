def test_2d_psystem():
    """test_2d_psystem"""

    def verify_data():
        def verify(test_state):
            """ verifies gauge values generated by 2d psystem application 
            from a previously verified run """
            
            import os
            import numpy as np
            from clawpack.pyclaw.util import check_diff

            gauge_files = test_state.grid.gauge_files
            test_gauge_data= test_state.gauge_data
            expected_gauges=[]
            thisdir = os.path.dirname(__file__)
            
            expected_list=[]
            error_list=[]
            test_passed = True
            if test_gauge_data is not None:
                for i, gauge in enumerate(gauge_files):
                    verify_file = os.path.join(thisdir,'verify_' +
                                            gauge.name.split('/')[-1])
                    expected_gauges.append(np.loadtxt(verify_file))
                    return_value = check_diff(expected_gauges[i], 
                    test_gauge_data[i], reltol=1e-2)
                    
                    if return_value is not None:
                        expected_list.append(return_value[0])
                        error_list.append(return_value[1])
                        test_passed = False


                if test_passed:
                    return None
                else:
                    return(expected_list, error_list,return_value[2] )
            else:
                return
                
        return verify

    from clawpack.pyclaw.util import gen_variants
    from psystem import psystem2D

    classic_tests = gen_variants(psystem2D, verify_data(),
                                 kernel_languages=('Fortran',), 
                                 solver_type='classic')

    from itertools import chain
    for test in chain(classic_tests):
        yield test
