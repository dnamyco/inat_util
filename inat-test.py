#!/usr/bin/env python

import requests
import json

response = requests.get("https://api.inaturalist.org/v1/observation_fields?q=Voucher%20Number(s)")
print(response.text)
