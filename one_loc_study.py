# In april 2014 the most visited Citi Bike station was 
# id = 521 with the following coordianats
station_id = 521
org_lat = 40.75044999
org_lon = -73.994810509999994

# Note Earths radius is 6,371
# so 1km dS = 1./6371. dtheta
dS = 1./6371.

import pandas as pd
import numpy as np
months = ['apr', 'may', 'jun', 'jul', 'aug', 'sep']
nmd = [30, 31, 30, 31, 31, 30]

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

m = 'apr'
g = gen_time_windows()
ubs = None
cit = None
for m in months:
    print 'Processing Month ',m
    pickups_in_dS = ((np.deg2rad(dfU[m]['Lat']) - 
                      np.deg2rad(org_lat))**2 + 
                     (np.deg2rad(dfU[m]['Lon']) - 
                      np.deg2rad(org_lon))**2 < dS**2)

    rents_at_id = (dfC[m]['start station id'] == 521)


    for t in g[m]:
        u_in_times = comp(dfU[m], t)
        if ubs is None:
            ubs = dfU[m]['timesec'][(pickups_in_dS) & (u_in_times)] - t
        else:
            ubs = pd.concat((ubs,
                dfU[m]['timesec'][(pickups_in_dS) & (u_in_times)] - t))

        c_in_times = comp(dfC[m], t)
        if cit is None:
            cit = dfC[m]['timesec'][(rents_at_id) & (c_in_times)] - t
        else:
            cit = pd.concat((cit,
                dfC[m]['timesec'][(rents_at_id) & (c_in_times)] -t))

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



HU,xU = histogram(ubs/60./60., bins=3*60)

HC,xC = histogram(cit/60./60., bins=3*60)

fig,ax = start_up_fig()
lns = make_hist(ax[0], HU, xU,'U')
#lns = make_hist(ax[1], HU, xU,'U')

lns = make_hist(ax[2], HC, xC,'C')
#lns = make_hist(ax[3], HC, xC,'C')

#ax[1].set_xlim(day_zoom, day_zoom + 4)
#ax[3].set_xlim(day_zoom, day_zoom + 4)
