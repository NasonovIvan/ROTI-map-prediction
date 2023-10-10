# ROTI-map-forecast
Neural network for daily prediction of the ROTI map

## Abstract

ROTI (index of rate of total electron content (TEC) change) maps are constructed with the grid of 2° × 2° resolution as a function of the magnetic local time and corrected magnetic latitude. The ROTI maps allow to estimate the overall fluctuation activity and auroral oval evolutions, in general, the ROTI values are corresponded to the probability of the GPS signals phase fluctuations.

In this paper, the daily prediction of ROTI cards is implemented using machine learning methods.

## Main part

We will use the data of the ROTI maps for 2010-2020. Let's analyze these data, as well as index data for a similar time and try to find correlations.

In the figure below, we will plot the arithmetic mean of the ROTI maps for each day, for a month and a moving average for 400 days:

![ROTI data](/images/data_roti.jpeg "ROTI data for 2010-2020")

Solar and geomagnetic activity tend to be repeated with a 27-day period. This in turn affects the ROTI index itself, which is also subject to cyclical behavior. Based on these dependencies, we assumed that data for the current day and 27 days ago may correlate and help track periodic changes and anomalies.

As a result of the first stage, a data set was created in which we used the values of the 10.7 cm solar radio flux (F10.7), scalar B, BZ and the values of the ROTI map for the current day. From the F10.7 index, its average value for each day was obtained, as well as 27-day median values for each day, because the average data has large changes from day to day. The maximum values of the scalar B index and the minimum values of the BZ index for each day were also added to the dataset. Each ROTI map has 3600 index values - it is inefficient to add all the values to the training set, since the training time and the required power will increase. Therefore, the average index value for each ROTI map was calculated and this number was added to the dataset. 

It should be noted that the average value of the F10.7 index, the maximum value of scalar B, the minimum value of the BZ index were added to the dataset not only for the current day, but also for the day that was 27 days ago, as well as the minimum value of the BZ index for the next day.

For training and validation of the model, we used data from 1/1/2010 to 1/1/2020. But in this set there are important examples on which we would like to test the work of our neural network - these are the data intervals from 13/3/2015 to 17/3/2015 and from 18/6/2015 to 24/6/2015. To obtain reliable results, these data were excluded from the training set and placed in the test set, which also includes data from 2/1/2020 to 19/6/2022.

To predict the ROTI map, we decided to use data from the previous two days. Moreover, to create the final dataset, we used the shuffle method with a buffer size of 256 elements. This will randomly shuffle the elements of this dataset. Also we used mini-batches with a batch size of 24 elements.

Let's analyze the data using Principal Component Analysis (PCA). It can be seen that there is no need to reduce the dimension of the data.
![PCA](/images/pca-1.png "PCA")
<!-- <img src="/images/pca.pdf" alt="PCA" width="400"/> -->

The correlation matrix is here too. We can see a strong correlation between some of the indexes.
![corr](/images/cross-matrix-num-1.png "corr")

I used InceptionTime network in this work to analyse the series of data. The schema of the network is below.
![inception](/images/super-res-1-1.png)

We used ADAM as the optimizer for our neural network with default parameters. We chose the Huber function as the loss function because it is less sensitive to outliers in the data than the squared error loss.

The graph of the decreasing loss function can be seen in the figure below. The neural network was trained for 30 epochs.

![Loss function](/images/loss-1.png "Loss function train")
<!-- <img src="/images/loss.pdf" alt="Loss function" width="400"/> -->

Neural network prediction results:

<!-- <img src="/images/compare_result.svg.pdf" alt="ROTI map" width="400"/>
<img src="/images/compare_result_1.svg.pdf" alt="ROTI map" width="500"/>
<img src="/images/compare_result_2.svg.pdf" alt="ROTI map" width="600"/> -->

![ROTI map](/images/compare_result.svg-1.png "ROTI map prediction")
![ROTI map](/images/compare_result_1.svg-1.png "ROTI map prediction")
![ROTI map](/images/compare_result_2.svg-1.png "ROTI map prediction")

<!-- <img src="/images/ex_roti_map.jpeg" alt="ROTI map" width="400"/> <img src="/images/1_result.jpeg" alt="ROTI map prediction" width="400"/>
<img src="/images/2_target.jpeg" alt="ROTI map" width="400"/> <img src="/images/2_result.jpeg" alt="ROTI map prediction" width="400"/> -->

### Indexes

We want to take data period from 2010 to 2020 years for training our NN. In data from 2021 to 2022 we are going to test our network and analyze the result.

> Global data source:
> - https://lasp.colorado.edu/home/our-expertise/science/space-weather/
> - https://wdc.kugi.kyoto-u.ac.jp/wdc/Sec3.html

- The **Kp index**, or the planetary K index, is considered a proxy for the energy input from the solar wind to Earth. It is based on the geomagnetic effects of solar particles, the local K values, as measured by ground-based magnetometers around the world at geomagnetic latitudes between 44 degrees and 60 degrees (northern or southern). The higher the Kp value, the stronger the geomagnetic disturbance. **Ap Index** - the 3-hourly ap (equivalent range) index is derived from the Kp index.
> Source: ftp://ftp.gfz-potsdam.de/pub/home/obs/kp-ap/wdc/yearly/

- The **Dst index** provides a quantitative measure of geomagnetic disturbance. It is derived from a network of geomagnetic observatories near the Earth's geomagnetic equator that map to the globally symmetrical equatorial electrojet (the "ring current"). The lower the Dst value, the stronger the geomagnetic disturbance. Positive variations in Dst are mostly caused by the compression of the magnetosphere from solar wind pressure increases.
> Source:
> - https://wdc.kugi.kyoto-u.ac.jp/dst_provisional/index.html
> - https://wdc.kugi.kyoto-u.ac.jp/dst_final/index.html

- Penticton Solar Radio **Flux at 10.7 cm** - is an excellent indicator of solar activity. Often called the F10.7 index, it is one of the longest running records of solar activity. The F10.7 radio emissions originates high in the chromosphere and low in the corona of the solar atmosphere. The F10.7 correlates well with the sunspot number as well as a number of UltraViolet (UV) and visible solar irradiance records.
> Source: ftp://ftp.seismo.nrcan.gc.ca/spaceweather/solar_flux/daily_flux_values/fluxtable.txt

- ACE **Solar Wind** Electron, Proton, and Alpha Monitor - instrument sensors measure solar wind electrons at 1-900 eV energy and ions at 0.26-35 keV. SWEPAM data consists of ion and electron rates collected at each energy/charge (E/Q) step, polar lock direction, and azimuthal spin direction. A single spacecraft spin period of 12 seconds is sufficient for accumulation of count matricies to fully calculate the electron and ion distribution functions from which bulk moments (solar wind speed, density, temperature) can be calculated by ground data processing. Accumulated counts will actually be summed over one-minute intervals for increased statistical accuracy and for reduction of telemetry requirements.
> Source: https://sohoftp.nascom.nasa.gov/sdb/goes/ace/daily/

- **IMF-BZ** - The interplanetary magnetic field (IMF) plays a huge rule in how the solar wind interacts with Earth’s magnetosphere. The Bx and By components are not important for auroral activity and are therefor not featured on our website. The third component, the Bz value is perpendicular to the ecliptic and is created by waves and other disturbances in the solar wind. For a geomagnetic storm to develop it is vital that the direction of the interplanetary magnetic field (Bz) turns southward. Continues values of -10nT and lower are good indicators that a geomagnetic storm could develop but the lower this value goes the better it is for auroral activity.
> Source: https://omniweb.gsfc.nasa.gov/form/dx1.html

#### ROTI maps

> Source:
> - From where data should be downloaded: https://cddis.nasa.gov/Data_and_Derived_Products/GNSS/atmospheric_products.html
> - How data should be downloaded: https://cddis.nasa.gov/Data_and_Derived_Products/CDDIS_Archive_Access.html

#### Additional information

- [Inception Time Network](https://arxiv.org/abs/1909.04939)
