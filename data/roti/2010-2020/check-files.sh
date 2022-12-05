#!/bin/bash

#Check which files directory doesnt have and how many

sum=0
count=0
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
        FILE=roti"$day_string"0."$end_year"f
        if test -f "$FILE"; then
            count=$[ $count + 1 ]
        else
            echo "$FILE not exists."
            sum=$[ $sum + 1 ]
        fi
		day=$[ $day + 1 ]
	done
done

echo "All counts of files: $count"
echo "All counts of not existed files: $sum"
