#!/bin/bash

gmtset PLOT_DEGREE_FORMAT ddd:mm:ssF
gmtset PAGE_ORIENTATION portrait
gmtset PAPER_MEDIA a2
gmtset TICK_LENGTH 0.3c

R=-R5E/16E/47N/55N
B=-BSWnea1.0f0.5
J=-JM30
C=-CTdiff.cpt 

datafile=Tdiff.grd
psname=Tdiff_map.ps


makecpt -Chot -I  -D -T1.4/3.0/0.2  > Tdiff.cpt

grep -v nan mean_lat_lon_tdiff_0.5.dat|grep ^[0-9] > Tdiff.xyz

 awk '{print $2, $1, $3}' Tdiff.xyz| surface  $R  -I1m -G$datafile -T0.25  -C0.1 
# awk '{print $2, $1, $3}' lat_lon_tdiff| surface  $R  -I1m -G$datafile -T0.25  -C0.1 

psbasemap $R $J $B -Y5 -G200 -K > $psname

awk '{print $2, $1}' tdiff_stations| psmask  $R $J -I0.1m -S1.2  -K -O >> $psname
grdimage $datafile $R $J $C  -K -O >>  $psname
psmask -C -K -O >> $psname


pscoast $J $R -Df $L -N1/5.0p/197/82/33 -K -O >>$psname        # plotet Grenzen
pscoast -J -R -Df $L -S0/100/255 -K -O >> $psname          # plotet Meer
pscoast -J -R -Df $L -Ir/1.0p/79/147/198 -K -O >> $psname  # plotet Flüsse
pscoast -J -R -Df $L -C115/181/230 -K -O >> $psname        # plotet Seen



# plot station names and symbols
#awk '{print $2" "$1" "$3}' lat_lon_tdiff |psxy $R $J -Sc0.3 -G255 -W4,0 -O -K $C >> $psname
awk '{print $2" "$1" "$3}' lat_lon_tdiff |psxy $R $J -St0.6 -G255 -W4,0 -O -K $C >> $psname
#awk '{print $2" "$1" "$3}' Tdiff.xyz |psxy $R $J -Sc0.5 -G255 -W4,0 -O -K $C >> $psname
#awk '{print $6" "$5" "}'  list_wetterstationen.txt|psxy $R $J -Sc0.1 -W1,0 -O -K  >> $psname
awk '{print $2" "$1" "1.35" "2.1}'  Tdiff.xyz|psxy $R $J -Sr -W1,0 -O -K  >> $psname


psscale $C -D15/-1.4/10/0.5h -B0.2/:"Tdiff":  -O   >> $psname
ps2raster -Tg -A $psname
rm $psname .gmt*4
