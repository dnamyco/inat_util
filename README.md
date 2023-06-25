# iNaturalist Utility

This project is not affiliated with iNaturalist in any way. We are simply fans, and users. Our goal is to facilitate certain community actions like quickly adding the Foray Voucher IDs to a whole foray of Observations. The script has several safeguard built in to avoid abuse of the iNaturalist API, however misuse of the tool may result in rate limiting or worse. This software is distributed under the Apache License Version 2.

### An example use case:
The NAMA Foray generates several hundred specimens in a small region. 
- A list of the observations in the region are exported and matched to their voucher number during tissue extraction on a worksheet or tablet.
- The voucher sheet kept with the specimen mentions whether or not microscopy was done, so we'll also update that too.
- Our spreadsheet now looks like the one row example in the repo. There is a column who's name must be `iNaturalist ID` that contains the observation IDs, and columns for the two Observation Fields we're updating each with the observation row ID in the first row as a heaader.
    - The field IDs can be found on their detail pages here: [https://www.inaturalist.org/observation_fields]
- The coordinator gets their API toekn from [https://www.inaturalist.org/users/api_token] and exports it in their shell `export INAT_API_TOKEN="<long string>"`
- The script is executed like: `python inat_util.py update-vouchers --file /path/to/nama_vouchers.xlsx `

## Requirements
- Modern Python, the script is tested on Fedora 38 with Python 3.11.3
- pandas and pyinaturalist packages installed with pip
- An active iNaturalist user session (log in on the website)