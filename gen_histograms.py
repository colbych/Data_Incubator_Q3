from loader import load_data
from loader import in_ipython
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#===========================================================

def start_up_fig():
    fig = plt.figure(1)
    fig.clf()
    ax = [fig.add_subplot(221+c) for c in range(4)]

    return fig,ax

#===========================================================

def make_hist(ax, H, x, wdat):
    lns = ax.plot((x[1:]+x[:-1])/2., H, 'k')
    ax.set_xlabel('April 2014 (Days)')
    if wdat == 'U':
        ax.set_ylabel('# of Ubers requested/5 minutes')
    elif wdat == 'C':
        ax.set_ylabel('# of Citi Bikes rented/5 minutes')

    return lns

#========================= Main ============================
    
if not in_ipython():
    loading_data = True
else:
    loading_data = (raw_input('Load Uber & Citi Bike data? ') == 'y')

if loading_data:
    dfU,dfC = load_data()

m = 'apr'
day_zoom = 27
print 'Plotting data'
fig,ax = start_up_fig()

HU,xU = histogram(dfU[m]['timesec']/24./60./60.,bins=12*24*30)
lns = make_hist(ax[0], HU, xU + 1.,'U')
lns = make_hist(ax[1], HU, xU + 1.,'U')

HC,xC = histogram(dfC[m]['timesec']/24./60./60.,bins=12*24*30)
lns = make_hist(ax[2], HC, xC + 1.,'C')
lns = make_hist(ax[3], HC, xC + 1.,'C')

#ax[0].plot(np.zeros(100)+ day_zoom, np.linspace(0,350.,100),'k--')
#ax[0].plot(np.zeros(100)+ day_zoom + 3.99, np.linspace(0,350.,100),'k--')
for a in [0,2]:
    ax[a].fill([day_zoom, day_zoom+4., day_zoom+4., day_zoom], 
             [0, 0, 350, 350], fill=False, hatch='/')

ax[1].set_xlim(day_zoom, day_zoom + 4)

ax[3].set_xlim(day_zoom, day_zoom + 4)

for a in ax:
    plt.sca(a)
    plt.minorticks_on()
    a.set_ylim(0,350.)

ax[0].set_xlim(1,31.)
ax[2].set_xlim(1,31.)

plt.tight_layout()
plt.draw()

fig.savefig('UberVCiti_histogram.pdf')
