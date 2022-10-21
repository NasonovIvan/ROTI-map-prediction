#curl -c cookies.txt -b cookies.txt -n -L "https://cddis.nasa.gov/archive/gnss/products/ionex/2010/001/roti0010.10f.Z" -O

#wget --auth-no-challenge "https://cddis.nasa.gov/archive/gnss/products/ionex/2010/001/roti0010.10f.Z"

curl -u gastello:12345Ivan -O --ftp-ssl ftp://cddis.gsfc.nasa.gov/gnss/products/ionex/{2010}/{002}/roti{002}0.{10}f.Z 

uncompress *.Z
