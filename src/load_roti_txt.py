import numpy as np
from datetime import datetime, timedelta

def read_roti_txt(filename):
    with open(filename, 'rb') as f:
        maps = []
        map_date = []
        line = f.readline()
        while not line.strip().startswith(b"END OF FILE"):
            header_read = False
            date = None
            lats = []
            rows = []
            date_arr = []
            while not header_read or (line.strip() and not line.strip().startswith(b"END OF ROTIPOLARMAP")):
                if line.strip().startswith(b"START OF ROTIPOLARMAP"):
                    header_read = True
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
                    row = np.genfromtxt(block, dtype=float)
                    row = row.reshape(180,)
                    rows.append(row)
                line = f.readline()

            map_date.append(date_arr)
            maps.append(rows)
            line = f.readline()
        return date, np.array(lats), np.array(map_date), np.array(maps)