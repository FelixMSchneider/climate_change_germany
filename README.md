## Plot Climate data for Germany

get data from 

    https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/subdaily/air_temperature/historical/



    mkdir data
    cd data

    wget  -r -nd --no-parent -A 'terminwert*.zip' https://opendata.dwd.de/climate_environment/CDC/observations_germany/climate/subdaily/air_temperature/historical/
    for zipfile in `ls termin*zip` 
    do 
    unzip $zipfile
    done


