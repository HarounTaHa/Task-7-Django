import json
import requests
from itertools import islice

data_mac = open('data/mac_candidates.txt').read()
data_json = json.loads(data_mac)


# method each iter split dic 500 item
def chunks(dic_data, SIZE=500):
    it = iter(dic_data)
    for i in range(0, len(dic_data), SIZE):
        yield {k: dic_data[k] for k in islice(it, SIZE)}


for data in chunks(data_json):
    data_requests = []
    keys_values = data.items()
    for key, value in keys_values:
        data_send = {}
        data_send.update({'mac': str(key), 'vendor': str(value)})
        data_requests.append(data_send)

    r = requests.post('http://127.0.0.1:8000/vendor/', json=data_requests)
    print(f"Status Code: {r.status_code}, Response: {r.json()}")
