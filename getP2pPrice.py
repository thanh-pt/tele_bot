import requests
import json

url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"

json_payload = {
  "page": 1,
  "rows": 20,
  "payTypes": [],
  "asset": "USDT",
  "tradeType": "BUY",
  "fiat": "VND",
  "publisherType": None
}

headers = {
  'Content-Type': 'application/json'
}

# BUY
response = requests.request("POST", url, headers=headers, data=json.dumps(json_payload))
json_response_data = json.loads(response.text)

buy_prices = []
count = 0
sum_buy_price = 0
for data in json_response_data["data"]:
    price = int(data["adv"]["price"])
    buy_prices.append(price)
    count = count + 1
    sum_buy_price = sum_buy_price + price
avg_buy_price = sum_buy_price/count

# SELL
json_payload["tradeType"] = "SELL"
response = requests.request("POST", url, headers=headers, data=json.dumps(json_payload))
json_response_data = json.loads(response.text)

sell_prices = []
count = 0
sum_sell_price = 0
for data in json_response_data["data"]:
    price = int(data["adv"]["price"])
    sell_prices.append(price)
    count = count + 1
    sum_sell_price = sum_sell_price + price
avg_sell_price = sum_sell_price/count

# Xử lý dữ liệu:
# Sent dữ liệu đến bot
print("+-----+-------+-------+")
print("| BUY |  SELL |  BUY  |")
print("+-----+-------+-------+")
print("| Min | %d | %d |" % (min(sell_prices), min(buy_prices)))
print("| Max | %d | %d |" % (max(sell_prices), max(buy_prices)))
print("| Avg | %d | %d |" % (avg_sell_price, avg_buy_price))
print("+-----+-------+-------+")
