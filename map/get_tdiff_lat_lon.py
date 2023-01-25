import numpy as np
def get_station_from_id(id):
    f=open("../list_wetterstationen.txt", "r")
    while True:
        a=f.readline()
        if a.split()[0]==id: break

    wl=a[61:102].split()

    lat=float(a.split()[4])
    lon=float(a.split()[5])

    s=""
    for w in wl:
        s+=w+" "
    return s, lat, lon


import pickle
tdiffdict=pickle.load(open("../dicts/tdict.pickle", "rb"))
ids=list(tdiffdict.keys())


for id in ids:
    if tdiffdict[id]:
        station, lat, lon=get_station_from_id(id)
        print(lat,lon, tdiffdict[id]["tdiff"], station, id)

import sys
sys.exit()

dlat=0.5
dlon=0.5
dlat2=dlat/2
dlon2=dlon/2


glats=np.arange(47.4,55.1, dlat)
glons=np.arange(6.0,15, dlon)

#for glat in glats:
for glat in [51.75]:
    clat=glat+dlat2
    #for glon in glons:
    for glon in [8.0]:
        clon=glon+dlon2
        tds=[]

        for id in ids:
            station, lat, lon=get_station_from_id(id)
            if lat > (clat-dlat2) and lat < (clat + dlat2) and lon > (clon-dlon2) and lon < (clon + dlon2):
                tds.append(tdiffdict[id]["tdiff"])
        print(tds)
        print(clat, clon, np.array(tds).mean())
    print("")

