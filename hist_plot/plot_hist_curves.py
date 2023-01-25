import pylab as plt
from matplotlib.collections import LineCollection
import numpy as np

import datetime

import pickle
tdict=pickle.load(open("../dicts/tdict.pickle", "rb"))

ids=list(tdict.keys())
ids.remove("02953")


a=[tdict[id]["sumdatetimes"] for id in ids]
b=sum(a,[])
allyears=sorted(list(set(b)))


 
import os.path


if os.path.isfile("../dicts/valyears.pickle"):
    valyears=pickle.load(open("../dicts/valyears.pickle", "rb")) 
else:
    valyears=[]
    for year in allyears:
        print(year)
        valyear=[]
        for id in ids:
            meanb=tdict[id]["meanb"] 
            if year in np.array(tdict[id]["sumdatetimes"]):
                indx=np.where(year == np.array(tdict[id]["sumdatetimes"]))[0][0]
                valyear.append(tdict[id]["sumvals"][indx] - meanb)
        valyears.append(valyear)
    
    pickle.dump(valyears, open("../dicts/valyears.pickle", "wb"))


if os.path.isfile("../dicts/hists.pickle"):
    hists=pickle.load(open("../dicts/hists.pickle", "rb")) 
else:
    hists=[]
    
    for vals in valyears:
        #hist=plt.hist(vals, bins=50)
        vals=np.array(vals)
        hist=plt.hist(vals, np.linspace(vals.mean()-4, vals.mean()+4,101))
        
        #hist0=hist[0]/hist[0].max()
        hist0=hist[0]
        hist1=hist[1]
        hists.append([hist0,hist1])
    pickle.dump(hists, open("../dicts/hists.pickle", "wb"))
    

time_change = datetime.timedelta(days=365)



allhists=[]
fig = plt.figure(figsize=(7,9))
ax=fig.add_subplot(111)


verts=[]

xticks=[]
xticklabels=[]

maxis=[]
year_maxis=[]
fit_maxis=[]
fit_year_maxis=[]
fit_maxis_1=[]
fit_year_maxis_1=[]


cutyear1=1948
cutyear=1990

for i,year in enumerate(allyears):
    x1=year.timestamp()
    x2=(year+time_change).timestamp()
    x=[x1,x2]
    x12=(x1+x2)/2

    if year.year%10==0:
        xticks.append(x1)
        xticklabels.append(str(year.year))
    if year.year==cutyear1:
        xlim1=x1
    xlim2=x2



    allhists+=list(hists[i][0])
    yvals=(hists[i][1][1:]+hists[i][1][0:-1])*0.5


    year_maxis.append(x12)
    maxpos=np.where(hists[i][0]==hists[i][0].max())[0][0]
    maxis.append(yvals[maxpos])

    if year.year >=cutyear:
        fit_year_maxis.append(x12)
        fit_maxpos=np.where(hists[i][0]==hists[i][0].max())[0][0]
        fit_maxis.append(yvals[maxpos])
    if year.year <cutyear and year.year >=cutyear1:
        fit_year_maxis_1.append(x12)
        fit_maxpos_1=np.where(hists[i][0]==hists[i][0].max())[0][0]
        fit_maxis_1.append(yvals[maxpos])


    for j,y in enumerate(yvals):
        verts.append(np.column_stack([x, [y,y]]))



x=np.array(fit_year_maxis)
y=np.array(fit_maxis)
m,b = np.polyfit(x, y, 1)

x1=np.array(fit_year_maxis_1)
y1=np.array(fit_maxis_1)
m1,b1 = np.polyfit(x1, y1, 1)

    
line_segments = LineCollection(verts,linewidth=5.5, cmap="gist_heat_r", array=np.array(allhists))
#line_segments = LineCollection(verts,linewidth=10, cmap="inferno_r", array=np.array(allhists))
ax.add_collection(line_segments)

time_change = datetime.timedelta(days=(365*10))

cnt=0
for i in range(1):
    xticks.append((datetime.datetime(year=int(xticklabels[-1]), month=6, day=1)+time_change).timestamp())
    xticklabels.append(str(int(xticklabels[-1])+10))
    cnt+=1

ax.set_xticks(xticks)
ax.set_xticklabels(xticklabels)

p1=plt.plot(year_maxis, maxis, "bo", markersize=5, label="maximum count year > 1990")
p2=plt.plot(fit_year_maxis_1, fit_maxis_1, "go",label="maximum count year < 1990",   markersize=5)


time_change = datetime.timedelta(days=(365*10*cnt))

print(x)
x=np.append(x,(year+time_change).timestamp())
print(x)

xlim2=(year+time_change).timestamp()
l1=plt.plot(x,m*x+b, "b--", linewidth=3, label="linear fit 1990-2022")
l2=plt.plot(x1,m1*x1+b1, "g--", linewidth=3, label="linear fit 1948-1990" )
ax.legend(loc=2)
ax.set_xlim(xlim1,xlim2)
ylim1=-3
ax.set_ylim(ylim1,-ylim1+1)



today=datetime.datetime(year=2022, month=6, day=1).timestamp()


temp_today=m*today+b

plt.plot([today,today], [ylim1,temp_today], "k-")
plt.plot([xlim1,today], [temp_today,temp_today], "k-")

ax.set_xlabel("year")
ax.set_ylabel("yearly average temperatur - $T_{av}$ [°C]")
ax.set_title("Average temperature deviation per year\n at all available weather stations in Germany (DWD)")



from mpl_toolkits.axes_grid1 import make_axes_locatable
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="3%", pad=0.05)
   


axcb = fig.colorbar(line_segments, cax=cax)

axcb.set_label('No. of measurements')


plt.savefig("temperatur_all_wetterstations.png")



