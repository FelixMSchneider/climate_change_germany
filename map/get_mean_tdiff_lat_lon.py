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
tdict=pickle.load(open("../dicts/tdict.pickle", "rb"))
ids=list(tdict.keys())


#for id in ids:
#    station, lat, lon=get_station_from_id(id)
#    print(lat,lon, station)

#import sys
#sys.exit()

dlat=0.5
dlon=0.5
dlat2=dlat/2
dlon2=dlon/2


glats=np.arange(47.4,55.1, dlat)
glons=np.arange(6.0,15, dlon)

#for glat in [51.75]:
for glat in glats:
    clat=glat+dlat2
    #for glon in [8.0]:
    for glon in glons:
        clon=glon+dlon2
        tds=[]

        for id in ids:
            station, lat, lon=get_station_from_id(id)
            if lat > (clat-dlat2) and lat < (clat + dlat2) and lon > (clon-dlon2) and lon < (clon + dlon2):
                if tdict[id]:
                    tds.append(tdict[id]["tdiff"])
        print(clat, clon, np.array(tds).mean())
    print("")

