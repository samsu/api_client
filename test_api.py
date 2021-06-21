import api_client.fortiauth_client as client


ApiClient=client.FortiAuthApiClient

api = [("10.100.101.127", 443, True)]
user = "admin"
password = "8H0aodSnvfSWRL0p9XuqhFyWslvcqgKVoItCwK3d"
cli = ApiClient(api, user, password)


res = cli.request("GET_SYSTEMINFO")
print(res)
res = cli.request("BACKUP_CONFIG")
print(res)
print(res.status)
print(res.msg)
f = open('tmp.conf', 'w')
f.write(res.body)
f.close()

f = open('tmp.conf', 'rb')
chunck = f.read()
message = {
    'file': chunck
}
res = cli.request("RESTORE_CONFIG", **message)
print(res.status)
print(res.body)



# res = cli.request