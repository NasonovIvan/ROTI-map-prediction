# ROTI-map-forecast
Neural network for daily prediction of the ROTI map

## Abstract

ROTI (index of rate of total electron content (TEC) change) maps are constructed with the grid of 2° × 2° resolution as a function of the magnetic local time and corrected magnetic latitude. The ROTI maps allow to estimate the overall fluctuation activity and auroral oval evolutions, in general, the ROTI values are corresponded to the probability of the GPS signals phase fluctuations.

In this paper, the daily prediction of ROTI cards is implemented using machine learning methods.

## Main part

We will use the data of the ROTI maps for 2010-2020. Let's analyze these data, as well as index data for a similar time and try to find correlations.

In the figure below, we will plot the arithmetic mean of the ROTI maps for each day, for a month and a moving average for 400 days:

![ROTI data](/images/data_roti.jpeg "ROTI data for 2010-2020")

Now let's plot similar graphs for indexes:

<!-- ![ROTI data](/images/data_kp.jpeg "ROTI data for 2010-2020") -->
<img src="/images/data_kp.jpeg" alt="KP data for 2010-2020" width="400"/> <img src="/images/data_dst.jpeg" alt="DST data for 2010-2020" width="400"/>
<img src="/images/data_f107.jpeg" alt="F107 data for 2010-2020" width="400"/> <img src="/images/data_bz.jpeg" alt="IMF-BZ data for 2010-2020" width="400"/>
<img src="/images/data_plasma.jpeg" alt="Plasma Speed data for 2010-2020" width="400"/> <img src="/images/data_proton.jpeg" alt="Proton Density data for 2010-2020" width="400"/>

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