# -------------------------#
# ---Program by MiVainer---#
import json
import requests
url = "https://api.zmtech.ru:7778/v1/"
param_dict = {"id": "104556",
              "password": "e5d0403f963677d729ac7daa8c40ad9e0eab16cd"
              }

response = requests.post(url, data=json.dumps(param_dict))
print(response.status_code)