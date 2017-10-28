#!/bin/sh
#SBATCH --nodes=16
#SBATCH --ntasks-per-node=4
#SBATCH --ntasks-per-node=4
#SBATCH --mail-user=talnikar@mit.edu
#SBATCH --mail-type=ALL
source /etc/profile.d/master-bin.sh
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$HOME/sources/petsc/arch-linux2-c-opt/lib
export PYTHONPATH=$HOME/.local/lib/python2.7/site-packages/:\$PYTHONPATH
mpirun ~/adFVM/apps/adjoint.py ./vane_optim_adj.py