import requests

TOKEN = "7653469544:AAEuDWAsJTJ404V1AFIcx_lkJNUkLi_kgmU"
url = f"https://api.telegram.org/bot{TOKEN}/deleteWebhook"

response = requests.post(url)
print(response.json())
