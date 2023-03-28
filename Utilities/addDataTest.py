import http.client

conn = http.client.HTTPSConnection("stupefied-poitras.185-23-116-208.plesk.page")

payload = "{\n  \"node_ids\": [\n     \"test_node_2\"\n  ]\n}"

headers = { 'Content-Type': "application/json" }

conn.request("POST", "/api/sensordata-multiple", payload, headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))