import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from datetime import datetime, timedelta
import statistics as sts

# define moving average function
def moving_avg(x, n):
    cumsum = np.cumsum(np.insert(x, 0, 0)) 
    return (cumsum[n:] - cumsum[:-n]) / float(n)

# check exist date in roti date array
def exist_date_roti(roti_date, date_check):
    for date_r in roti_date:
        if date_check[0] == date_r[0] and date_check[1] == date_r[1] and date_check[2] == date_r[2]:
            return True
    return False

# mean data
def mean_data(data, train_num=3935):
    mean = data[:train_num].mean(axis=0)
    data -= mean
    std = data[:train_num].std(axis=0)
    data /= std
    return data

# convert doy in normal date with day and month
def doy2day(doy, year):
    startDate = datetime(year=year, month=1, day=1)
    daysToShift = doy - 1
    endDate = startDate + timedelta(days=daysToShift)
    
    month = endDate.month
    day = endDate.day
    
    return day, month

# convert day date in day's number of the year
def day2doy(date):
    day = date[0]
    month = date[1]
    year = date[2]
    months = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]

    if 0 < month and month <= 12:
        sum = months[month - 1]
    else:
        print("month error")

    sum += day
    leap = 0

    if year % 400 == 0 or (year % 4 == 0 and year % 100 != 0):
        leap = 1

    if leap == 1 and month > 2:
        sum += 1
    
    return sum

# need to read ROTI file and returns polar data with date of file
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

# create arrays of roti maps --> returns arrays of dates and maps data
def get_array_roti(path_file):
    maps = []
    map_date = []
    for year in range(10, 23, 1):
        for doy in range(1, 367, 1):
            if doy >= 295 and year == 20:
                continue
            daily_lats = []
            daily_date = []
            daily_map = []
            
            if len(str(doy)) == 1:
                doy_str = "00" + str(doy)
            elif len(str(doy)) == 2:
                doy_str = "0" + str(doy)
            else:
                doy_str = str(doy)
            filename = path_file + doy_str + '0.' + str(year) + 'f'
            try:
                date, daily_lats, daily_date, daily_map = read_roti(filename)
            except FileNotFoundError:
                continue
            else:
                date, daily_lats, daily_date, daily_map = read_roti(filename)

            map_date.append(daily_date)
            maps.append(daily_map)

    return np.array(map_date), np.array(maps)

# here we create arrays of average values of F10-7, scalar B, min BZ from file
def read_all_data(filename, roti_date, day_end, month_end, year_end):
    with open(filename, 'rb') as f:
        all_data_arr = []
        date_arr = []
        
        day = 0
        month = 0
        year = 0
        
        while day != day_end or month != month_end or year != year_end:
            all_data_daily = []
            data_daily = []
            date = []
            
            line = f.readline()
            
            year = int(line[0:4])
            doy = int(line[5:8])
            day, month = doy2day(doy, year)
            
            date.append(day)
            date.append(month)
            date.append(year)

            if not exist_date_roti(roti_date, date) and year >= 2010:
                continue
            
            for _ in range(23):
                all_data_hour = []
                data_string = line[13:len(line)]
                data_values = data_string.split()
                for i in range(5):
                    all_data_hour.append(float(data_values[i].decode()))
                all_data_daily.append(all_data_hour)
                line = f.readline()

            all_data_daily = np.array(all_data_daily)
            data_min = all_data_daily.min(axis=0)
            data_max = all_data_daily.max(axis=0)
            data_means = np.mean(all_data_daily, axis=0)
            # add average values
            for i in range(len(data_means)):
                data_daily.append(data_means[i])
            # add max B scalar
            data_daily.append(data_max[0])
            # add min bz
            data_daily.append(data_min[1])
            all_data_arr.append(data_daily)
            date_arr.append(date)

    return np.array(all_data_arr), np.array(date_arr)

# this function need for median value of F10-7
def median_f107(all_data, start_indx):
    all_median = []

    for index in range(start_indx, len(all_data), 1):
        median = []
        for i in range(index - 26, index + 1, 1):
            median.append(all_data[i][2])
        median = sorted(median)
        all_median.append(median[14])
    return np.array(all_median)

# finally in this function we create the whole datasets of F10-7, scalar B and min BZ
def get_all_data(filename, train_roti_maps, roti_map_date, day_end, month_end, year_end):
    '''
    This is a description of get_all_data

    Parameters:
    filename (str): title of file
    train_roti_maps (array): array of avg ROTI in one-value
    roti_map_date (array) : dates of ROTI maps
    day_end (int)
    month_end (int)
    year_end (int)

    Returns:
    data_all_arr (array): array with shape (num_days, 9)
    all_date_arr (array): dates of data

    index | name
      0   | avg F10-7
      1   | F10-7 27-days median
      2   | avg F10-7 27 days ago
      3   | max scalar B
      4   | max scalar B 27 days ago
      5   | min BZ
      6   | min BZ 27 days ago
      7   | min BZ next day
      8   | avg ROTI in the whole map
    '''
    all_data, date_arr = read_all_data(filename, roti_map_date, day_end, month_end, year_end)
    data_all_arr = []
    all_date_arr = []

    start_indx = 0
    for i in range(len(date_arr)):
        if date_arr[i][0] == 1 and date_arr[i][1] == 1 and date_arr[i][2] == 2010:
            start_indx = i
            break
    f107_median = median_f107(all_data, start_indx)
    
    for i in range(start_indx, len(all_data) - 1, 1):
        data_daily = []
        # for j in range(6):
        #     data_daily.append(all_data[i][j])
        # data_daily.append(f107_median[i - 31])
        # for j in range(6):
        #     data_daily.append(all_data[i - 26][j])

        # avg F10-7
        data_daily.append(all_data[i][2])
        data_daily.append(f107_median[i - start_indx])
        data_daily.append(all_data[i - 27][2])
        # max scalar B
        data_daily.append(all_data[i][5])
        # max scalar B 27 days ago
        data_daily.append(all_data[i - 27][5])
        # min BZ
        data_daily.append(all_data[i][6])
        data_daily.append(all_data[i + 1][6])
        data_daily.append(all_data[i - 27][6])
        for j in range(len(train_roti_maps[i - start_indx])):
            data_daily.append(train_roti_maps[i - start_indx][j])
        all_date_arr.append(date_arr[i])
        data_all_arr.append(data_daily)

    return np.array(data_all_arr), np.array(all_date_arr)

# function for reducing dimension of maps --> returns a new shape data,
# where the last of couple shapes will be "compressed" like data.shape[-1]/less_num
# FE: (4500, 3600) and less_num = 5 --> new shape of data: (4500, 720)
def roti_encode(roti_maps, less_num):
    new_roti_maps = []
    for i in range(len(roti_maps)):
        j = 0
        new_roti_map = []
        while j < len(roti_maps[i]):
            numbers_roti = []
            for item in range(less_num):
                numbers_roti.append(roti_maps[i][j + item])
            j += less_num
            numbers_roti = np.array(numbers_roti)
            new_roti_map.append(np.mean(numbers_roti))
        new_roti_maps.append(new_roti_map)
    return np.array(new_roti_maps)

# this function does the opposed procedure of roti_encode function
# here is enlarging process 
def roti_decode(roti_maps, less_num):
    new_roti_maps = []
    for i in range(len(roti_maps)):
        j = 0
        new_roti_map = []
        while j < len(roti_maps[i]):
            for num in range(less_num):
                new_roti_map.append(roti_maps[i][j])
            j += 1
        new_roti_maps.append(new_roti_map)
    return np.array(new_roti_maps)

# for Huber function plot
def huber_func(x, delta=8.0):
    if abs(x) <= delta:
        answer = 0.5 * pow(x, 2)
    else:
        answer = delta * (abs(x) - 0.5 * delta)
    return answer

# plot roti nothern ROTI data in polar coordinates
def plot_data_roti(date, lons, lats, map):
    lons, lats = np.meshgrid(lons, lats)

    fig1 = plt.figure()
    ax = fig1.add_subplot(111, projection='polar')
    levels = np.arange(0, 0.6, 0.1)
    cc = ax.contourf(np.deg2rad(lons), 90. - lats, map, levels=levels, extend='both')

    plt.title("ROTI index date: " + str(date))

    plt.colorbar(cc, ax=ax, label="ROTI, TECU/min")

    mlt = np.linspace(0, 24, 49)

    plt.show()

# for plotting indeces
def plot_data_index(date, array_data, name_index):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    pdf = PdfPages("../images/ROTI-graph.pdf")

    data_month = []
    month_line = []

    data_half_year = []
    half_year_line = []

    data_year = []
    year_line = []

    day_line = np.arange(0, len(date), 1).reshape(len(array_data), 1)

    for i in range(len(array_data)):
        if i % 30 == 0:
            data_month.append(np.mean(array_data[i - 30: i]))
            month_line.append(i - 30 / 2)

    for i in range(len(array_data)):
        if i % 180 == 0:
            data_half_year.append(np.mean(array_data[i - 180: i]))
            half_year_line.append(i - 180 / 2)
    
    data_avg = moving_avg(array_data, 365)
    data_avg.reshape(len(data_avg), 1)
    step = len(array_data) / len(data_avg)
    day_avg = np.arange(0, len(date), step).reshape(len(data_avg), 1)

    ax.set_title('Data index ' + name_index)
    # ax.set_xlabel('Days', size=12)
    # ax.set_ylabel(name_index, size=12)
    ax.set_xlabel('Days')
    ax.set_ylabel(name_index)
    plt.show()

# for plotting roti data for the whole period of date
def plot_roti_graph(roti_maps_reshape, roti_map_date):
    average_roti = []
    for i in range(len(roti_maps_reshape)):
        avg = sts.mean(roti_maps_reshape[i])
        average_roti.append(avg)

    average_roti = np.array(average_roti)
    plot_data_index(roti_map_date, average_roti, 'Average ROTI')

# creating datasets with X and y labels for training part
# and here we REMOVE important dates and data, belonged them - theor dates are in forbidden_indx list
# then we can test our NN to predict these days
def multivariate_data(all_indexes, new_roti_maps, start_index, end_index, history_size, target_size):

    '''
    This is a description of multivariate_data

    Parameters:
    all_indexes (array): array data of indexes
    new_roti_maps (array): array data of roti maps
    start_index (int)
    end_index (int)
    history_size (int): the number of days on which we based our predction
    target_size (int): the number of days for prediction

    Returns:
    data (array): X array of samples.
    labels (array): Y array of labels (target).
    '''

    data = []
    labels = []

    forbidden_indx = [1897, 1898, 1899, 1900, 1901, 1994, 1995, 1996, 1997, 1998, 1999, 2000]

    start_index = start_index + history_size
    if end_index is None:
      end_index = len(all_indexes) - target_size

    for i in range(start_index, end_index):
      if i in forbidden_indx:
        continue
      indices = range(i - history_size, i, 1)
      data.append(all_indexes[indices])
      labels.append(new_roti_maps[i + target_size - 1])

    return np.array(data), np.array(labels)

# creating datasets with X and y labels for testing part
def multivariate_data_test(all_indexes, new_roti_maps, start_index, end_index, history_size, target_size):
    '''
    This is a description of multivariate_data

    Parameters:
    all_indexes (array): array data of indexes
    new_roti_maps (array): array data of roti maps
    start_index (int)
    end_index (int)
    history_size (int): the number of days on which we based our predction
    target_size (int): the number of days for prediction

    Returns:
    data (array): X array of samples.
    labels (array): Y array of labels (target).
    '''

    data = []
    labels = []

    start_index = start_index + history_size
    if end_index is None:
      end_index = len(all_indexes) - target_size

    for i in range(start_index, end_index):
      indices = range(i - history_size, i, 1)
      data.append(all_indexes[indices])
      labels.append(new_roti_maps[i + target_size - 1])

    return np.array(data), np.array(labels)

# plotting two charts of ROTI maps at the one plot: the origin and prediction of NN
def plot_roti_near(date, lons, lats, map, pred_map, pdf_file, WriteFile=False):
    lons, lats = np.meshgrid(lons, lats)

    if WriteFile:
        pdf = PdfPages(pdf_file)

    fig, axs = plt.subplots(nrows=1 , ncols=2, figsize=(15, 5))
    [axi.set_axis_off() for axi in axs.ravel()]

    for ax in axs:
        date_str = str(date)
        date_str = date_str[:-9]
        ax = fig.add_subplot(121, projection='polar')
        levels = np.arange(0, 0.6, 0.1)
        cc = ax.contourf(np.deg2rad(lons), 90. - lats, map, levels=levels, extend='both')
        ax.set_title("ROTI date: " + date_str, fontsize=18)
        fig.colorbar(cc, ax=ax, label="ROTI, TECU/min", location='left')
        mlt = np.linspace(0, 24, 49)

        ax = fig.add_subplot(122, projection='polar')
        levels = np.arange(0, 0.6, 0.1)
        cc = ax.contourf(np.deg2rad(lons), 90. - lats, pred_map, levels=levels, extend='both')
        ax.set_title("Prediction ROTI date: " + date_str, fontsize=18)
        fig.colorbar(cc, ax=ax, label="ROTI, TECU/min", location='right')
        mlt = np.linspace(0, 24, 49)
    
    if WriteFile:
        pdf.savefig(fig)
        pdf.close()
    plt.show()

# for plotting loss and accuracy history training
def PlotLossAcc(TrainData, ValData, Epochs, TrainLabel, ValLabel, yLabel, filename):
    pdf = PdfPages(filename)
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(Epochs, TrainData, 'b', label=TrainLabel)
    ax.plot(Epochs, ValData, 'g', label=ValLabel)
    ax.set_ylabel(yLabel)
    ax.set_xlabel("Epochs")
    plt.legend()
    pdf.savefig(fig)
    pdf.close()
    plt.show()

# plot series charts of ROTI predictions by using plot_roti_near func
def PlotRotiPredictions(start, end, y_pred, x_train_test, roti_map_date, pdf_file="", WriteFile=False):
    for i in range(start, end, 1):
        # doy = str(day2doy(roti_map_date[i]) + x_train.shape[-1] // 6)
        doy = str(day2doy(roti_map_date[i]) + x_train_test.shape[1])
        year = str(roti_map_date[i][2] - 2000)
        if len(doy) == 1:
            filename = '../data/roti/2010-2020/roti' + '00' + doy + '0.' + year + 'f'
        elif len(doy) == 2:
            filename = '../data/roti/2010-2020/roti' + '0' + doy + '0.' + year + 'f'
        else:
            filename = '../data/roti/2010-2020/roti' + doy + '0.' + year + 'f'

        all_maps = []
        pred_map = []

        for j in range(y_pred.shape[-1]):
            pred_map.append(y_pred[i - start][j])
        pred_map = np.array(pred_map)
        pred_map = pred_map.reshape(1, pred_map.shape[-1])

        # date, lats, date_map, map = read_roti(filename)
        try:
            date, lats, date_map, map = read_roti(filename)
        except FileNotFoundError:
            continue
        else:
            date, lats, date_map, map = read_roti(filename)

        all_maps.append(map)
        all_map = np.mean(all_maps, axis=0)
        lons = np.linspace(1, 361, all_map.shape[1])
        pred_map = roti_decode(pred_map, less_num=1)
        # pred_map = roti_decode(pred_map, less_num=5)
        pred_map = pred_map.reshape(20, 180)
        plot_roti_near(date, lons, lats, map, pred_map, pdf_file=pdf_file, WriteFile=WriteFile)
