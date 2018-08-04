from matplotlib import pyplot as plt
from numpy import *
import pylab as pl
from matplotlib import rc

rc('text', usetex=True)

# Creating Plot
#fig1 = plt.figure(figsize=(10, 8))
#ax1 = fig1.add_subplot(111)

#x = pl.frange(1,50)
#log_serie = [1/(e / 2)**(y / 4) for y in x]
#ax1.plot(x, log_serie, label = r"u($\mu$-topology$)", marker='o', linestyle='--', linewidth=1.0)
#ax1.set_ylabel('utility', fontsize=30)
#ax1.set_xlabel(r"$\mu$-topology", fontsize=30)
#ax1.tick_params(axis='x', labelsize=20)
#ax1.tick_params(axis='y', labelsize=20)
#ax1.set_ylim([0,1])

#trendline
#z = polyfit(x, log_serie, 1)
#p = poly1d(z)

#ax1.plot(x, p(x), "r--", label = 'utility trend')
#ax1.legend(loc='upper right', prop={'size':20})


##### Using Step Function
fig1 = plt.figure(figsize=(10, 8))
ax1 = fig1.add_subplot(111)

x_threshold = pl.frange(1,400)
constant_serie = [1 for i in x_threshold]

x = pl.frange(400,1000)
x_variable = pl.frange(0,600)
log_serie = [math.pow(0.995,i) for i in x_variable]

ax1.plot(x_threshold, constant_serie, label = r"u($\mu$-topology$)", linewidth=2.0, color='blue')
ax1.plot(x, log_serie, label = r"u($\mu$-topology$)", linewidth=2.0, color='blue')
ax1.set_ylabel('Utility', fontsize=30)
ax1.set_xlabel("Montly Cost (U\$)", fontsize=30)
ax1.tick_params(axis='x', labelsize=20)
ax1.tick_params(axis='y', labelsize=20)
ax1.set_ylim([0,1.1])

plt.axvspan(0, 400, color='grey', alpha=0.2)

ax1.annotate('Threshold', xy=(100, 0.5), xytext=(100, 0.5), fontsize=30)
#plt.show()


fig1.savefig("/Users/gomezsso/Documents/dissertation/Publications/Journal/2016_TOIT/gfx/utility_cost.pdf", format='pdf')