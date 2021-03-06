import numpy as np
import matplotlib.pyplot as plt
import sys
plt.rc('text', usetex=True)

fs = sys.argv[1:]
labels = [r'\lambda = 0.0', r'\lambda = 10^{-5}', r'\lambda = 10^{-4}']
for f, l in zip(fs, labels):
    x = np.sort(np.loadtxt(f))[::-1]
    xn = np.arange(0, len(x))
    y =  np.polyfit(xn, x, 1)
    n = round(-y[1]/y[0])
    print n
    l += ', n_u = {}'.format(n)
    plt.plot(1+xn, x, 'o', markersize=8, label=l)
    plt.plot(xn, np.zeros_like(x))
plt.legend(loc='lower left')
plt.xlabel('Exponent number')
plt.ylabel('Lyapunov exponent')
plt.show()
