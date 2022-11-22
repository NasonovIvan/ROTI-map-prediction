import numpy as np
from datetime import datetime, timedelta

def read_roti(filename):
    with open(filename, 'rb') as f:
        header_read = False
        date = None
        lats = []
        rows = []
        date_arr = []
        line = f.readline()
        while not header_read or (line.strip() and not line.strip().startswith(b"END OF ROTIPOLARMAP")):
            if line.strip().startswith(b"START OF ROTIPOLARMAP"):
                header_read = True
            elif line.strip().startswith(b"END OF ROTIPOLARMAP") or line.strip().startswith(b"END OF FILE"):
                break
            elif not header_read:
                pass
            elif line[0:5].strip():
                date = datetime(int(line[0:7]), int(line[7:14]), int(line[14:21]))
                year = int(line[0:7])
                month = int(line[7:14])
                day = int(line[14:21])
                
                date_arr.append(day)
                date_arr.append(month)
                date_arr.append(year)
            else:
                lat, lon_start, lon_end = float(line[3:9]), float(line[9:15]), float(line[15:21])
                lats.append(lat)

                block = [f.readline() for _ in range(18)]
                row = np.genfromtxt(block)
                rows.append(row.ravel())
            line = f.readline()
        return date, np.array(lats), np.array(date_arr), np.array(rows)

def get_array_roti():
    maps = []
    map_date = []
    for year in range(10, 21, 1):
        for doy in range(1, 367, 1):
            if doy > 295 and year == 20:
                break
            daily_lats = []
            daily_date = []
            daily_map = []
            
            if len(str(doy)) == 1:
                doy_str = "00" + str(doy)
            elif len(str(doy)) == 2:
                doy_str = "0" + str(doy)
            else:
                doy_str = str(doy)
            filename = '../data/roti/2010-2020/roti' + doy_str + '0.' + str(year) + 'f'
            try:
                date, daily_lats, daily_date, daily_map = read_roti(filename)
            except FileNotFoundError:
                continue
            else:
                date, daily_lats, daily_date, daily_map = read_roti(filename)

            map_date.append(daily_date)
            maps.append(daily_map)

    return np.array(map_date), np.array(maps)

# roti data and date
roti_map_date = []
roti_maps = []
roti_map_date, roti_maps = get_array_roti()