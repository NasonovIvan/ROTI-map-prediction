# import requests
# import sys

# # Reads the URL from the command line argument
# url = sys.argv[1]

# # Assigns the local file name to the last part of the URL
# filename = url.split('/')[-1]

# # Makes request of URL, stores response in variable r
# r = requests.get(url, stream=True)

# # Opens a local file of same name as remote file for writing to
# with open(filename, 'wb') as fd:
#     for chunk in r.iter_content(chunk_size=1000):
#         fd.write(chunk)

# # Closes local file
# fd.close()

# https://cddis.nasa.gov/Data_and_Derived_Products/CDDIS_Archive_Access.html
# https://cddis.nasa.gov/Data_and_Derived_Products/GNSS/atmospheric_products.html

import wget
url='https://cddis.nasa.gov/archive/gnss/products/ionex/2010/001/roti0010.10f.Z'
wget.download(url)
