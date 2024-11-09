import requests
response = requests.get("https://nextride.brampton.ca:81/API/ServiceAlerts?format=json")
print (response)
