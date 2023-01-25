python get_mean_tdiff_lat_lon.py > mean_lat_lon_tdiff_0.5.dat
python get_tdiff_lat_lon.py > lat_lon_tdiff
awk '{print $1,$2,$4}' lat_lon_tdiff > tdiff_stations
bash plot_Tdiff.sh

