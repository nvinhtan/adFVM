import numpy as np
import os
import sys
from setuptools import setup, Extension, Command
from Cython.Build import cythonize

class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""
    user_options = []
    def initialize_options(self):
        pass
    def finalize_options(self):
        pass
    def run(self):
        os.system('rm -vrf ./build ./dist ./*.pyc ./*.tgz ./*.egg-info')


os.environ['CC'] = 'ccache mpicc'
os.environ['CXX'] = 'mpicxx'

compatDir = 'adFVM/compat/'
compile_args = ['-fopenmp']
link_args = ['-lgomp']
modules = cythonize(
        [Extension(compatDir + 'cfuncs', [compatDir + 'cfuncs.pyx'], 
        language='c++', extra_compile_args=compile_args, extra_link_args=link_args)])

cppDir = 'adFVM/cpp/'
incdirs = [np.get_include()]
incdirs += [cppDir + 'include/']
libdirs = []
libs = []
sources = ['mesh.cpp', 'cmesh.cpp']
sources = [cppDir + f for f in sources]

#compile_args = ['-std=c++11', '-O3']#, '-march=native']
compile_args += ['-std=c++11', '-O3', '-g']#, '-march=native']

for module, c_args in [[cppDir + 'cmesh', []], [cppDir + 'cmesh_gpu', ['-DCPU_FLOAT32']]]:
    mod = Extension(module,
                    sources=sources,
                    extra_compile_args=compile_args + c_args,
                    extra_link_args=link_args,
                    library_dirs=libdirs,
                    libraries=libs,
                    include_dirs=incdirs,
                    undef_macros = [ "NDEBUG" ])
    modules.append(mod)

setup(name='adFVM',
      version='0.1.1',
      description='finite volume method flow solver',
      author='Chaitanya Talnikar',
      author_email='talnikar@mit.edu',
      packages=['adFVM', 'adFVM.compat'],
      package_data={
      'adFVM': ['gencode/*', 'cpp/*', 'cpp/include/*'],
      },
      include_package_data=True,
      ext_modules = modules,
      include_dirs=incdirs,
      install_requires=[ 
          'numpy >= 1.8.2',
          'scipy >= 0.13.3',
          'mpi4py >= 0.13.1',
          'cython >= 0.24',
          #'h5py >= 2.6.0',
          #'matplotlib >= 1.3.1'
      ],
      cmdclass={
        'clean': CleanCommand,
      }
    )
