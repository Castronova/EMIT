from ctypes import*

swmmLib = CDLL("libSWMMQOpenMI.dylib")
print swmmLib
swmmLib.swmm_run("Logan.inp","Logan.rpt","Logan.out")
print 'model run was successful'


# lib = '/Users/tonycastronova/Downloads/swmm_build/DerivedData/swmm_build/Build/Products/Debug/libswmm_build.dylib'
# clib = CDLL(lib)
# print clib.test()
# clib.swmm_run("Logan.inp","Logan.rpt","Logan.out")
# print 'done'