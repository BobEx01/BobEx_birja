import requests

TOKEN = "7653469544:AAEuDWAsJTJ404V1AFIcx_lkJNUkLi_kgmU"
WEBHOOK_URL = "https://your-railway-app.up.railway.app/webhook"  # Bu yerga real webhook URL-ni yozing

url = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={WEBHOOK_URL}"

response = requests.get(url)
print(response.json())
