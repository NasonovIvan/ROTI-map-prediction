# ROTI-map-forecast
Neural network for daily prediction of the ROTI map

## Abstract

ROTI (index of Rate of Total Electron Content (TEC) change) maps are constructed with the grid of 2° × 2° resolution as a function of the magnetic local time and corrected magnetic latitude. The ROTI maps allow to estimate the overall fluctuation activity and auroral oval evolutions, in general, the ROTI values are corresponded to the probability of the GPS signals phase fluctuations.

The purpose of this study is to develop a neural network model, the learning result of which will predict the Rate of TEC Index (ROTI) map for the day ahead.

## Main part

Methodologically, the study of the problem is divided into two stages. At the first stage, a detailed analysis of the data is carried out, as well as their preparation for the neural network training process. At the second stage, the neural network architecture is being developed, hyperparameters are being selected and the model is being improved.

Solar and geomagnetic activity tend to be repeated with a 27-day period. This in turn affects the ROTI index itself, which is also subject to cyclical behavior. Based on these dependencies, we assumed that data for the current day and 27 days ago may correlate and help track periodic changes and anomalies.

As a result of the first stage, a data set was created in which we used the values of the 10.7 cm solar radio flux (F10.7), scalar B, BZ and the values of the ROTI map for the currentday. From the F10.7 index, its average value for each day was obtained, as well as 27-day median values for each day, because the average data has large changes from day to day. Themaximum values of the scalar B index and the minimum values of the BZ index for each day were also added to the dataset. Each ROTI map has 3600 index values - it is inefficient to addall the values to the training set, since the training time and the required power will increase. Therefore, the average index value for each ROTI map was calculated and this number wasadded to the dataset. 

<!-- ![ROTI data](/images/data_roti.jpeg "ROTI data for 2010-2020") -->

<!-- Now let's plot similar graphs for indexes: -->

<!-- ![ROTI data](/images/data_kp.jpeg "ROTI data for 2010-2020") -->
<!-- <img src="/images/data_kp.jpeg" alt="KP data for 2010-2020" width="400"/> <img src="/images/data_dst.jpeg" alt="DST data for 2010-2020" width="400"/>
<img src="/images/data_f107.jpeg" alt="F107 data for 2010-2020" width="400"/> <img src="/images/data_bz.jpeg" alt="IMF-BZ data for 2010-2020" width="400"/>
<img src="/images/data_plasma.jpeg" alt="Plasma Speed data for 2010-2020" width="400"/> <img src="/images/data_proton.jpeg" alt="Proton Density data for 2010-2020" width="400"/> -->

<!-- It is possible to observe a good correlation of the ROTI maps data with the indices F10-7 and IMF-BZ. There is also a weak correlation with the KP index, but for the initial analysis and testing of the success of the forecast, we will use data from the F10-7 and IMF-BZ indices.

Let's analyze the data using Principal Component Analysis (PCA). It can be seen that there is no need to reduce the dimension of the data.
![PCA](/images/pca.jpeg "PCA")

There is a problem of lack of data for neural network training, because the total amount of data is just below 4000. To solve this difficulty, we will use the generation of new data by adding noise to the index values obtained using the Ornstein–Uhlenbeck process:

$$dx_t = \theta(\mu - x_t)dt + \sigma dW_t$$

After that, we will get a little more than 11,000 data, which is already enough for training and testing a neural network.

The neural network will consist of two LSTM layers with L1 regularization coefficients, as well as an output layer of Dense. The learning process optimizer is Adam with a variable learning rate, and the loss function is MSE. -->

It should be noted that the average value of the F10.7 index, the maximum value of scalar B, the minimum value of the BZ index were added to the dataset not only for the current day, but also for the day that was 27 days ago, as well as the minimum value of the BZ index for the next day. The final contents of the dataset can be seen in the table:

| Index |                  Data                      |
| :-----: | :--------------------------------------- |
|   0   | average value of the F10.7                 |
|   1   | F10.7 27-days median                       |
|   2   | average value of the F10.7 27 days ago     |
|   3   | maximum value of the scalar B              |
|   4   | maximum value of the scalar B 27 days ago  |
|   5   | minimum value of the BZ                    |
|   6   | minimum value of the BZ 27 days ago        |
|   7   | minimum value of the BZ next day           |
|   8   | average value of the ROTI in the whole map |

Let's check the number of components selected for their use in neural network training. To do this, use Principal Component Analysis (PCA). To begin with, let's look at the ratio of variance and the number of components explaining it for all these indices, shown in the figures below. It can be seen that we do not have excessive information in the data, and although it is possible to describe the data with components 6 and 7 with an accuracy above 90%, we will not do this, since the impact on the training process will be insignificant.

![PCA](/images/pca.jpeg "PCA")
<img src="/images/pca_bar.pdf" alt="PCA" width="400"/>

Now it is necessary to check the cross-correlation of the data. In the figure below you can see the constructed matrix of cross-correlation of indices. It can be seen that the greatest correlation with the average value of the ROTI map is present between the values of F10.7 and the maximum value of scalar B. The negative correlation of the minimum value of the BZ index is explained by the fact that the lower this index, the more ionospheric irregularities occur, which means that the average value of the ROTI index is higher. From the correlation of the minimum BZ index of the current day and 27 days ago, it can be seen that our assumption about the 27-day correlation period is correct. It is also possible to observe an inverse correlation of the indices of maximum B and minimum BZ.

<!-- <object data="/images/cross-matrix-num.pdf" type="Cross-Cor-Matrix/pdf" width="50%"> 
</object> -->

<embed src="/images/cross-matrix-num.pdf" type="Cross-Cor-Matrix/pdf">

<!-- <img src="/images/cross-matrix-num.pdf" alt="Cross-Cor-Matrix" width="400"/> -->

The graph of the decreasing loss function can be seen in the figure below:

![Loss function](/images/train_loss.jpeg "Loss function train")

Neural network prediction results (right images):

![ROTI map](/images/result_1.jpeg "ROTI map prediction")
![ROTI map](/images/result_2.jpeg "ROTI map prediction")
![ROTI map](/images/result_3.jpeg "ROTI map prediction")

<!-- <img src="/images/ex_roti_map.jpeg" alt="ROTI map" width="400"/> <img src="/images/1_result.jpeg" alt="ROTI map prediction" width="400"/>
<img src="/images/2_target.jpeg" alt="ROTI map" width="400"/> <img src="/images/2_result.jpeg" alt="ROTI map prediction" width="400"/> -->

Work on this project continues - an article about this work will be published in the MDPI journal.

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

- [CS 230 Recurrent Neural Networks cheatsheet](https://stanford.edu/~shervine/teaching/cs-230/cheatsheet-recurrent-neural-networks)
- [RNN Keras guide](https://www.tensorflow.org/guide/keras/rnn)