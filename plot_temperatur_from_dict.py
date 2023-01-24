import pylab as plt
import numpy as np

import pickle
tdict=pickle.load( open("tdict.pickle", "rb"))


from obspy import UTCDateTime

useids=["00433",]
#useids=["03137"]

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

tdiffs=[]

fig=plt.figure()
ax=fig.add_subplot(111)


from matplotlib.collections import LineCollection


verts = []


a_first = np.linspace(0,1,50)
alpha_array =np.concatenate((np.flip(a_first),a_first))


for id in tdict.keys():

    if id == "02953": continue
     
    if not id in useids: continue
    print(id, get_station_from_id(id))

    import datetime
    
    cutyear=1990
    
    meanb=tdict[id]["meanb"] 
    sumvals=tdict[id]["sumvals"] 
    sumdatetimes=tdict[id]["sumdatetimes"]

    m=tdict[id]["m"] 
    b=tdict[id]["b"] 


    norm0=True
    norm0=False

    if norm0: sumvals-=meanb

    if m<0: continue

    tdiff=tdict[id]["tdiff"] 
    sumyears=[sdt.year for sdt in sumdatetimes] 
    
    plt.gcf().autofmt_xdate()
    
    
    extradatetimes=[]
    
    endyear=2022
    
    for year in np.arange(cutyear, endyear,1):
        extradatetimes.append(datetime.datetime(int(year),6,1))
    
    x=np.array([t.timestamp() for t in extradatetimes])
    
    temp_ex=m*x+b
    if norm0: 
        temp_ex-=meanb
        meanb=0
    
    tdiff=temp_ex[-1]-meanb
   

    ax.plot(extradatetimes, temp_ex ,"r--", linewidth=4)
   
    ax.plot(sumdatetimes,np.array(sumvals))
    ax.plot(sumdatetimes,np.array(sumvals), "ko")

    ylim1=meanb-1*tdiff
    ylim2=temp_ex[-1]+1*tdiff 
    ax.set_xlim(datetime.datetime(sumdatetimes[0].year-4,6,1), datetime.datetime(endyear+25,6,1))
    ax.plot([sumdatetimes[0], datetime.datetime(endyear+22,6,1)], [temp_ex[-1], temp_ex[-1]], "--", color="grey")
    ax.plot([sumdatetimes[0], datetime.datetime(endyear+22,6,1)], [meanb,meanb], "k--")
    ax.plot([sumdatetimes[0], datetime.datetime(cutyear,6,1)], [meanb,meanb], "g--", linewidth=5)
    ax.plot([datetime.datetime(cutyear,6,1), datetime.datetime(cutyear,6,1)], [ylim1,ylim2], "k--")

    x=[sumdatetimes[0].timestamp(), datetime.datetime(endyear+22,6,1).timestamp()]
    y=[temp_ex[-1], temp_ex[-1]]

    verts.append(np.column_stack([x, y]))


    ax.set_ylim(ylim1,ylim2)
   
    ax.set_ylabel("average temperatur [°C]")
    ax.set_xlabel("year")
    
    ax.set_title(get_station_from_id(id))
    tdiffs.append(tdiff)

line_segments = LineCollection(verts,linewidth=2, cmap="Blues_r", array=alpha_array)
ax.add_collection(line_segments)

tdiff=np.array(tdiffs).mean()


lyear=2035
ax.text(datetime.datetime(lyear,6,1), meanb+0.5*tdiff , "$\Delta$ t ="+str(round(tdiff,2))+"°", fontsize=12, ha="center",va="center", bbox=dict(facecolor='white', edgecolor='white', boxstyle='round'), zorder=12)
ax.arrow(datetime.datetime(lyear,6,1), meanb,0,tdiff, head_width=2000, length_includes_head=True, head_length=0.2, width=5, zorder=10)
ax.arrow(datetime.datetime(lyear,6,1), meanb+tdiff,0,-tdiff, head_width=2000, length_includes_head=True, head_length=0.2, width=5)

#ax.set_ylim(-4,9)

plt.savefig("temperatur_all.png")




