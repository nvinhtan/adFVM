from subprocess import check_call, STDOUT
from subprocess import check_output
import os
import pickle

def get_mesh(param, work_dir, work_dir_base, procs, fields=True):
    server = 'kolmogorov.mit.edu'
    base = '/home/talnikar/adFVM/cases/vane_optim/foam/laminar/'
    case = base + work_dir_base + '/'
    mesh_log = work_dir + 'mesh.log'
    with open(work_dir + 'params.pkl', 'w') as f:
        pickle.dump([param, base, case, procs, fields], f)
    #configure timeouts
    #copy profile to server
    try:
        check_output(['ssh', server, 'mkdir', '-p', case])
        check_output(['scp', work_dir + 'params.pkl', '{0}:{1}'.format(server, case)])
    except:
        raise Exception('Could not copy profile to server')

    #run mesh generator
    try:
        #ret = check_output('ssh {} \"python {}/vane_profile.py gen_mesh_param {}\"'.format(server, base, case + 'params.pkl'), shell=True, stderr=STDOUT)
        ret = check_call('ssh {} \"python {}/vane_profile.py gen_mesh_param {}\"'.format(server, base, case + 'params.pkl'), shell=True)
	#test=1
        #write_log(mesh_log, ret)
    except:
        raise Exception('Could not run mesh generator')
    
    #copy the mesh
    try:
        check_output(['rsync', '-aRv', '{0}:{1}/./par-*'.format(server, case), work_dir])
    except:
        raise Exception('Could not copy mesh from server')
    #delete mesh for future runs
    #try:
    #    check_call(['ssh', server, 'rm', mesh_dir + mesh_file])
    #except:
    #    raise Exception('Could not delete mesh from server')

def write_log(mesh_log, output):
    f = open(mesh_log, 'a')
    f.write(output)
    f.close()

if __name__ == "__main__":
    import numpy as np
    param = np.zeros(8)
    get_mesh(param, 'param_test/')
