import pandas as pd
import numpy as np
months = ['apr', 'may', 'jun', 'jul', 'aug', 'sep']

#===========================================================

def in_ipython():
    try:
        __IPYTHON__
        return True
    except NameError:
        return False

#===========================================================

def make_time_sec(df, wdat):
    """ take a data frame with a date and time field
        and converit time in to time in seconds
        
        df (DataFrame): for a given month
        wdat (str 'U' || 'C'): which type of data are we looking at
            uber or citi bike

    """

    if wdat == 'U': #M/d/Y
        ddp = 1
        spr = '/'
    elif wdat == 'C': #Y-M-d
        ddp = 2
        spr = '-'

    print 'Splitting time'
    tmp = df['time'].str.split(':').str
    print 'Splitting date'
    day = df['date'].str.split(spr).str[ddp].astype(float)

    print 'Calculating time in seconds'
    df['timesec'] = tmp[2].astype(float)\
                  + 60*tmp[1].astype(float)\
                  + 60*60*tmp[0].astype(float)\
                  + 24*60*60*(day - 1)

    return None

#===========================================================

def load_data(): #~ 10 seconds
    """ Load a whole mess of data from Uber and Citi Bike
        April 2014 - September 2014
        
        Returns:
            two dictionarys with months as keys and DataFrames as values

    """

    fnameU = '../data/uber-raw-data-{}14.csv'
    fnameC = '../data/2014-{:02d} - Citi Bike trip data.csv'
    months = ['apr', 'may', 'jun', 'jul', 'aug', 'sep']
    monthn = [4, 5, 6, 7, 8, 9]
    dfU = {}
    dfC = {}
    msg1 = 'Loading {} in {}'
    msg2 = 'Cleaning up {} in {}'
    for m,n in zip(months, monthn):
        print msg1.format('Uber',m)
        dfU[m] = pd.read_csv(fnameU.format(m))

        print msg2.format('Uber', m)
        tmp = dfU[m]['Date/Time'].str.split()
        #dfU[m]['day'] = tmp.str[0].str.split('/').str[1]
        dfU[m]['date'] = tmp.str[0]#.str.split('/').str[1]
        dfU[m]['time'] = tmp.str[1]
        make_time_sec(dfU[m], 'U')

        print msg1.format('Citi',m)
        dfC[m] = pd.read_csv(fnameC.format(n))

        print msg2.format('Citi', m)
        tmp = dfC[m]['starttime'].str.split()
        #dfC[m]['day'] = tmp.str[0].str.split('/').str[2]
        dfC[m]['date'] = tmp.str[0]#.str#.split('/').str[2]
        dfC[m]['time'] = tmp.str[1]
        make_time_sec(dfC[m], 'C')

    return dfU,dfC

#===========================================================




