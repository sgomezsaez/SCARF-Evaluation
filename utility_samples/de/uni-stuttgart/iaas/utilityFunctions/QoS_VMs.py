from matplotlib import pyplot as plt
from numpy import *
import pylab as pl
from matplotlib import rc
rc('text', usetex=True)

x = pl.frange(1,50)
log_serie = [1/(e**(1 / y)) for y in x]
plt.plot(x, log_serie, label = r"u($\mu$-topology$)")
plt.ylabel('utility', fontsize=24)
plt.xlabel(r"$\mu$-topology", fontsize=24)
pl.ylim([0,1])

#trendline
z = polyfit(x, log_serie, 1)
p = poly1d(z)
plt.plot(x, p(x), "r--", label = 'utility trend')

plt.legend(loc='lower right', prop={'size':20})

plt.show()
