import time
import requests

# اطلاعات کاربر
TELEGRAM_TOKEN = "7444087391:AAFC298G5cWJw9WFLb4J6lpLjKcH3DPpIy0"
TELEGRAM_CHAT_ID = "80898992"
WALLET_ADDRESS = "0x6cB9f119c81ECA65cF68b13Bb671b77F1beab131"

def get_withdrawable_weth():
    try:
        url = f"https://pac-finance-api.pages.dev/api/v1/account?address={WALLET_ADDRESS.lower()}"
        response = requests.get(url)
        data = response.json()

        for asset in data["data"]:
            if asset["symbol"] == "WETH":
                return float(asset["availableWithdraw"])
        return 0
    except Exception as e:
        print("Error checking WETH:", e)
        return 0

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    requests.post(url, data=payload)

while True:
    weth = get_withdrawable_weth()
    print(f"Current withdrawable WETH: {weth}")
    if weth >= 0.01:
        send_telegram_message(f"✅ موجودی قابل برداشت WETH شما در Pac Finance به {weth} رسید!")
        break
    time.sleep(600)  # هر 10 دقیقه
