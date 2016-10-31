# In april 2014 the most visited Citi Bike station was 
# id = 521 with the following coordianats
station_id = 521
org_lat = 40.75044999
org_lon = -73.994810509999994

# Note Earths radius is 6,371
# so 1km dS = 1./6371. dtheta
dS = 1./6371.

from loader import load_data
from loader import in_ipython
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
months = ['apr', 'may', 'jun', 'jul', 'aug']
nmd = [30, 31, 30, 31, 31]

def gen_time_windows():
    """ We want to look at every Tuesday between
        3-9 PM
    """
    # The first window will be (3 + 12)*60*60
    wds = {}
    str = 15*60*60
    sec_in_week = 7*24*60*60
    for m,n in zip(months, nmd):
        wds[m] = range(str, n*24*60*60, sec_in_week)
        str = sec_in_week + wds[m][-1] - n*24*60*60

    return wds
def comp(df, time):
    window = 6*60*60
    return ((time < df['timesec']) & (df['timesec'] < time + window))

#========================= Main ============================
    
if not in_ipython():
    loading_data = True
else:
    loading_data = (raw_input('Load Uber & Citi Bike data? ') == 'y')

if loading_data:
    dfU,dfC = load_data()
    

m = 'apr'
g = gen_time_windows()
ubs = None
cit = None
ubs = []
cit = []
for m in months:
    print 'Processing Month ',m
    pickups_in_dS = ((np.deg2rad(dfU[m]['Lat']) - 
                      np.deg2rad(org_lat))**2 + 
                     (np.deg2rad(dfU[m]['Lon']) - 
                      np.deg2rad(org_lon))**2 < dS**2)

    rents_at_id = (dfC[m]['start station id'] == 521)


    for t in g[m]:
        u_in_times = comp(dfU[m], t)
        ubs.append(dfU[m]['timesec'][(pickups_in_dS) & (u_in_times)] - t)
        #if ubs is None:
        #    ubs = dfU[m]['timesec'][(pickups_in_dS) & (u_in_times)] - t
        #else:
        #    ubs = pd.concat((ubs,
        #        dfU[m]['timesec'][(pickups_in_dS) & (u_in_times)] - t))

        c_in_times = comp(dfC[m], t)
        cit.append(dfC[m]['timesec'][(rents_at_id) & (c_in_times)] - t)
        #if cit is None:
        #    cit = dfC[m]['timesec'][(rents_at_id) & (c_in_times)] - t
        #else:
        #    cit = pd.concat((cit,
        #        dfC[m]['timesec'][(rents_at_id) & (c_in_times)] -t))

    #u_in_times = comp(dfU[m], g[m][0])
    #c_in_times = comp(dfC[m], g[m][0])

    #for t in g[m][1:]:
    #    u_in_times = ((u_in_times) | (comp(dfU[m], t)))
    #    c_in_times = ((c_in_times) | (comp(dfC[m], t)))


    #if ubs is None:
    #    ubs = dfU[m]['timesec'][(pickups_in_dS) & (u_in_times)]
    #else:
    #    ubs = pd.concat((ubs,
    #        dfU[m]['timesec'][(pickups_in_dS) & (u_in_times)]))

    #if cit is None:
    #    cit = dfC[m]['timesec'][(rents_at_id) & (c_in_times)]
    #else:
    #    cit = pd.concat((cit,
    #        dfC[m]['timesec'][(rents_at_id) & (c_in_times)]))

n_of_cars = []
n_of_bike= []
for u,c in zip(ubs, cit):
    n_of_cars.append(len(u))
    n_of_bike.append(len(c))

n_of_cars = np.array(n_of_cars)
n_of_bike = np.array(n_of_bike)


fig = plt.figure(1)
fig.clf()
ax = fig.add_subplot(111)
ax.plot((n_of_cars - np.mean(n_of_cars))/np.std(n_of_cars), label='Uber')
ax.plot((n_of_bike - np.mean(n_of_bike))/np.std(n_of_bike), label='Citi Bike')

ax.set_xlim(0,21)
ax.legend(loc='upper left')
ax.plot(np.arange(30), np.zeros(30), 'k--')
plt.xticks(np.arange(0,22, 2.0))
dates = ['4/1', '4/8', '4/15', '4/22', '4/29', 
         '5/6', '5/13', '5/20', '5/27',
         '6/3', '6/10', '6/17', '6/24',
         '7/1', '7/8', '7/15', '7/22', '7/29', 
         '8/5', '8/12', '8/19', '8/26']

ax.set_xticklabels(dates[::2])
ax.set_xlabel('Tuesdays in 2014')
ylb  = r'$\frac{X - \left < X\right >}{\sqrt{\left <(X - \left<X\right >)^2\right >}}$; $X$ = 6 hour average'
ax.set_ylabel(ylb)

plt.draw()

fig.savefig('comp_diviation.pdf')
