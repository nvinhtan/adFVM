import matplotlib.pyplot as plt
import numpy as np
import sys
import os

import pickle as pkl
plt.rcParams.update({'legend.fontsize':'18'})
plt.rcParams.update({'axes.labelsize':'16'})
plt.rcParams.update({'xtick.labelsize':'16'})
plt.rcParams.update({'ytick.labelsize':'14'})
plt.rcParams.update({'figure.figsize':(7, 6)})

#fs = sys.argv[1:]
for beta in [0.0, 1.0, 2.0, 3.0, 10.0]:
    #f = 'beta_{}/optim_nd2_lorenz.pkl'.format(beta)
    f = 'beta_{}/optim_nd2_rosenbrock.pkl'.format(beta)
    try:
        a = pkl.load(open(f))
    except:
        continue
    y = []
    print len(a[0])
    for b in a[0]:
        #y.append([np.abs(x[1]) for x in b])
        #y.append([x[1]-0.5422 for x in b])
        y.append([np.sqrt(((x[0]-np.array([1.,1]))**2).sum()) for x in b])
        #y.append([(np.sqrt((x[0]-np.array([26.7035,2.59748]))**2).sum()) for x in b])
        #y.append([(np.sqrt((x[0]-np.array([26.7437,2.6065]))**2).sum()) for x in b])
        #y.append([(np.sqrt((x[0]-np.array([26.71,2.59]))**2).sum()) for x in b])
        print beta, b[-1]
    #    plt.plot(y[-1])
    #plt.show()
    y = np.array(y)
    #plt.hist(y[:,50], bins=np.arange(0.1, 0.2, 0.002))
    plt.semilogy(y.mean(axis=0), label='beta = {}'.format(beta))
    #plt.plot(y.mean(axis=0), label='beta = {}'.format(beta))
plt.xlabel('iteration number')
plt.ylabel('distance from minimum value')
plt.legend()
plt.show()