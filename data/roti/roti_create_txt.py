def file_roti_txt(file_txt):
    with open(file_txt, 'wb') as ftxt:
        for year in range(10, 21, 1):
            for doy in range(1, 367, 1):
                if doy > 295 and year == 20:
                    break
            
                if len(str(doy)) == 1:
                    doy_str = "00" + str(doy)
                elif len(str(doy)) == 2:
                    doy_str = "0" + str(doy)
                else:
                    doy_str = str(doy)
                filename = './2010-2020/roti' + doy_str + '0.' + str(year) + 'f'
                try:
                    with open(filename, 'rb') as f:
                        line = f.readline()
                        while not line.strip().startswith(b"START OF ROTIPOLARMAP"):
                            line = f.readline()
                        while not line.strip().startswith(b"END OF ROTIPOLARMAP"):
                            ftxt.write(line)
                            line = f.readline()
                        ftxt.write(line)
                        ftxt.write(b"\n\n")
                except FileNotFoundError:
                    continue
        ftxt.write(b"END OF FILE")

file_txt = "rt_data_10-20.txt"
file_roti_txt(file_txt)