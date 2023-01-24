import pylab as plt
import numpy as np



from obspy import UTCDateTime
#useids=["00433", "03137"]  # for testing

import glob


def get_station_from_id(id):
    f=open("list_wetterstationen.txt", "r")
    while True:
        a=f.readline()
        if a.split()[0]==id: break

    wl=a[61:102].split()
    s=""
    for w in wl:
        s+=w+" "
    return s

#wfiles=sorted(glob.glob("../opendata.dwd.de/climate_environment/CDC/observations_germany/climate/subdaily/air_temperature/historical/produkt_tu_termin_1[8-9][0-6]*_202[0-9]*"))
wfiles=sorted(glob.glob("./data/produkt_tu_termin_1[8-9][0-6]*_202[0-9]*"))

fig=plt.figure()
ax=fig.add_subplot(111)
tdict={}

for wfile in wfiles:
     
    id=wfile.split("_")[-1].split(".")[0] 
    #if not id in useids: continue
    print(id, get_station_from_id(id))

    tdict[id]={}


#    if len(glob.glob("temperatur_id"+id+".png"))==1: continue

    f=open(wfile)
    f.readline()
    A=f.readlines()
    f.close()
    
    
    years=[int(a.split(";")[1][0:4]) for a in A]
    months=[int(a.split(";")[1][4:6]) for a in A]
    days=[int(a.split(";")[1][6:8]) for a in A]
    time=[int(a.split(";")[1][8:]) for a in A]
    times=[UTCDateTime(year=years[i], month=months[i], day=days[i], hour=time[i]) for i in range(len(years))]
    vals=[float(a.split(";")[3]) for a in A]
    datetimes=[t.datetime for t in times]
    
    
    
    t0=datetimes[0]
    sumvals=[]
    sumyears=[]
    sumval=0
    
    cnt=0
    for i,t in enumerate(datetimes):
        if t.year==t0.year: 
            if vals[i]<-500: continue
            cnt+=1
            sumval+=vals[i]
        else:
           if cnt>0: 
               sumvals.append(sumval/cnt)
               sumyears.append(t0.year)
           sumval=0
           t0=t
           sumval+=vals[i]
           cnt2=cnt
           cnt=0
    
   
    
    
    import datetime
    
    
    sumdatetimes=[]
    for year in sumyears:
        sumdatetimes.append(datetime.datetime(year,6,1))
    
    
    
    cutyear=1990
    
    cnt=0
    meanb=0
    for i,year in enumerate(sumyears):
        if year < cutyear:
            meanb+=sumvals[i]
            cnt+=1
    
    if cnt==0:
        print("no data available before "+str(cutyear))
        continue 
    meanb/=cnt
    
    
    cnt=0
    meana=0
    for i,year in enumerate(sumyears):
        if year >= cutyear:
            meana+=sumvals[i]
            cnt+=1
    meana/=cnt
    
    
    
    
    
    datetimes=np.array(datetimes)
    vals=np.array(vals)
    
    valid=np.where(vals>-500)[0]
    
    sumvals=np.array(sumvals)

#    sumvals-=meanb


    #ax.plot(datetimes[valid],vals[valid])
    ax.plot(sumdatetimes,np.array(sumvals))
    ax.plot(sumdatetimes,np.array(sumvals), "ko")
   

   
 
    #ax.plot([datetime.datetime(cutyear,6,1), sumdatetimes[-1]], [meana,meana], "r--")
    
    plt.gcf().autofmt_xdate()
    
    
    linfitvals=[]
    linfitdates=[]
    
    #cutyear=2000
    for i,year in enumerate(sumyears):
        if year >= cutyear: linfitvals.append(sumvals[i])
        if year >= cutyear: linfitdates.append(sumdatetimes[i])
    
    x=np.array([t.timestamp() for t in sumdatetimes if t.year >= cutyear])
    y=linfitvals
    
    #print(len(x),len(y))
    m,b = np.polyfit(x, y, 1)
    
    
    extradatetimes=[]
    
    endyear=2022
    
    for year in np.arange(cutyear, endyear,1):
        extradatetimes.append(datetime.datetime(int(year),6,1))
    
    x=np.array([t.timestamp() for t in extradatetimes])
    
    temp_ex=m*x+b
    
    tdiff=temp_ex[-1]-meanb
    
    ax.plot(extradatetimes, temp_ex ,"r--", linewidth=4)
   
    ylim1=meanb-1*tdiff
    ylim2=temp_ex[-1]+1*tdiff 
    ax.set_xlim(datetime.datetime(sumdatetimes[0].year-4,6,1), datetime.datetime(endyear+25,6,1))
    ax.plot([sumdatetimes[0], datetime.datetime(endyear+22,6,1)], [temp_ex[-1], temp_ex[-1]], "k--")
    ax.plot([sumdatetimes[0], datetime.datetime(endyear+22,6,1)], [0,0], "k--")
    #ax.plot([sumdatetimes[0], datetime.datetime(cutyear,6,1)], [meanb,meanb], "g--", linewidth=5)
    ax.plot([datetime.datetime(cutyear,6,1), datetime.datetime(cutyear,6,1)], [ylim1,ylim2], "k--")


    
    #ax.plot(datetimes[valid],vals[valid], zorder=-1, color="grey")
    #ax.plot(datetimes[valid],vals[valid]+temp_ex[-1], zorder=-2)
    #ax.set_ylim(0, 60)


    #ax.set_ylim(ylim1,ylim2)
   
    ax.set_ylabel("average temperatur [°C]")
    ax.set_xlabel("year")
    
    ax.set_title(get_station_from_id(id))

    lyear=2035
    ax.text(datetime.datetime(lyear,6,1), meanb+0.5*tdiff , "$\Delta$ t ="+str(round(tdiff,2))+"°", fontsize=12, ha="center",va="center", bbox=dict(facecolor='white', edgecolor='white', boxstyle='round'))
    ax.arrow(datetime.datetime(lyear,6,1), meanb,0,tdiff, head_width=2000, length_includes_head=True, head_length=0.1, width=5)
    ax.arrow(datetime.datetime(lyear,6,1), meanb+tdiff,0,-tdiff, head_width=2000, length_includes_head=True, head_length=0.1, width=5)
    tdict[id]["tdiff"]=tdiff
    tdict[id]["meanb"]=meanb
    tdict[id]["m"]=m
    tdict[id]["b"]=b
    tdict[id]["sumdatetimes"]=sumdatetimes
    tdict[id]["sumvals"]=sumvals

 
plt.savefig("temperatur_all.png")




import pickle

pickle.dump(tdict, open("tdict.pickle", "wb"))
