#!/bin/bash

#Download all data from 2010 to 2020 years. Time about ~6 hours
for (( year=2010; year <= 2022; year++ ))
do
	day=1
	end_year=${year: -2}
	while [ $day -le 365 ]
	do
		num_day=${#day}
		if [ "$num_day" = "1" ]; then
			day_string="00"
			day_string+="${day}"
		elif [ "$num_day" = "2" ]; then
			day_string="0"
			day_string+="${day}"
		else
			day_string="$day"
		fi
		curl -u anonymous:your_email_address -O --ftp-ssl ftp://gdc.cddis.eosdis.nasa.gov/gnss/products/ionex/"$year"/"$day_string"/roti"$day_string"0."$end_year"f.Z
		if [ "$year" = "2012" ] || [ "$year" = "2016" ] || [ "$year" = "2020" ]; then
			curl -u anonymous:your_email_address -O --ftp-ssl ftp://gdc.cddis.eosdis.nasa.gov/gnss/products/ionex/"$year"/366/roti3660."$end_year"f.Z
		fi
		day=$[ $day + 1 ]
	done
done

