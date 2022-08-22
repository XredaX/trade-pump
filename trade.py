from telethon import TelegramClient, events
import re
from ticker_rules import rules
from binance.client import Client
import time

Pkey = 'JQXJRxtaJXpzbpudJUWhIYodTz6RsOzJ8l6yjPN7GD4Bi1o37J5rtpwIGZNkRS0b'
Skey = 'NpZ73iF1dZjs1tg7eNSRXsEwF6JYItWy3JFeJAqzsWokuuJlE8si51udFPK9B3HH'
api_id = '3686067'
api_hash = '98d331dfb25569d1e362a95f63f40c44'
client1 = TelegramClient('reda', api_id, api_hash)

client = Client(api_key=Pkey, api_secret=Skey)

@client1.on(events.NewMessage)
async def handlmsg(event):
    # try:
        chat_id = event.chat_id
        msg = event.raw_text
        file1 = ""
        if chat_id == -1001165902042:
            coin = ""
            res = msg.split()
            for r in res:
                cleanString = re.sub('\W+','', r).upper()
                if re.search("USDT", cleanString):
                    for t in rules:
                        if cleanString == t:
                            coin = cleanString
                            break
                else:
                    cleanString = cleanString+"USDT"
                    for t in rules:
                        if cleanString == t:
                            coin = cleanString
                            break
            if coin != "":
                with open('database.txt') as f:
                    file1 = f.readlines()
                    f.close()
                    if file1[0] != coin:
                        balance = client.get_asset_balance(asset = "USDT")
                        balance = float(balance["free"])
                        usdt_amount = balance
                        if usdt_amount > rules[coin][4]:
                            float_format = "%."+str(rules[coin][0])+"f"
                            usdt_amount = float_format % usdt_amount
                            avg_price = client.get_avg_price(symbol = coin)
                            avg_price = float(avg_price["price"])
                            quantity = float(usdt_amount) / avg_price
                            quantity = str(quantity)
                            quantity = quantity.split(".")
                            quantity1 = ""
                            for q in range(int(rules[coin][3])):
                                quantity1 += quantity[1][q]
                            quantity = quantity[0]+"."+quantity1
                            quantity = float(quantity)
                            client.order_market_buy(symbol=coin, quantity=quantity)

                            time.sleep(10)

                            client.order_market_sell(symbol=coin, quantity=quantity)

                            with open('database.txt', 'w') as f1:
                                file1 = file1[0].replace(file1[0], coin)
                                f1.write(file1)
                                f1.close()
   # except:
    #    pass

client1.start()
client1.run_until_disconnected()
