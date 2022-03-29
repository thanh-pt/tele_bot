import requests
import json

def readFileConfig():
    f = open ('./config.json', "r")
    data = json.loads(f.read())
    f.close()
    return data

def telegram_bot_sendtext(token_bot, id_chat, bot_message):
   bot_token = token_bot
   bot_chatID = id_chat
   send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

   response = requests.get(send_text)
   return response.json()

def send_message(message):

    send = telegram_bot_sendtext(data['id_bot'], data['id_user'], message)
    print(send)

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
avg_buy_price = int(sum_buy_price/count)

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
avg_sell_price = int(sum_sell_price/count)

# Xu ly du lieu:
# Sent du lieu đen bot
# print("+-----+-------+-------+")
# print("| BUY |  SELL |  BUY  |")
# print("+-----+-------+-------+")
# print("| Min | %d | %d |" % (min(sell_prices), min(buy_prices)))
# print("| Max | %d | %d |" % (max(sell_prices), max(buy_prices)))
# print("| Avg | %d | %d |" % (avg_sell_price, avg_buy_price))
# print("+-----+-------+-------+")

buy_text  = "Buy : " + str(min(buy_prices)/1000) + " | " +  str(max(buy_prices)/1000) + " | " +  str(avg_buy_price/1000)
sell_text = "Sell: " + str(min(sell_prices)/1000) + " | " +  str(max(sell_prices)/1000) + " | " +  str(avg_sell_price/1000)

data = readFileConfig()
message = "Price is " + data['type'] + " " + str(int(data['price'])/1000) + "\n" \
          + buy_text + '\n' \
          + sell_text
# print(message)
if (data['type'] == 'upper'):
  if (int(data['price']) < max(sell_prices)):
    send_message(message)

elif (data['type'] == 'lower'):
  if (int(data['price']) > min(buy_prices)):
    send_message(message)
