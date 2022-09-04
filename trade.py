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

def get_change(current, previous):
    if current == previous:
        return 100.0
    try:
        return (abs(current - previous) / previous) * 100.0
    except ZeroDivisionError:
        return 0

@client1.on(events.NewMessage)
async def handlmsg(event):
    try:
        chat_id = event.chat_id
        msg = event.raw_text
        file1 = ""
        if chat_id == -1001377022329:
            coin = ""
            res = msg.split()
            for r in res:
                cleanString = re.sub('\W+','', r).upper()
                cleanString = cleanString + "BTC"
                for t in rules:
                    if cleanString == t:
                        coin = cleanString
                        break
            if coin != "":
                with open('database.txt') as f:
                    file1 = f.readlines()
                    f.close()
                    if file1[0] != coin:
                        balance = client.get_asset_balance(asset = "BTC")
                        balance = float(balance["free"])
                        balance = 0.97 * float(balance)
                        usdt_amount = balance
                        if usdt_amount > rules[coin][4]:
                            float_format = "%."+str(rules[coin][0])+"f"
                            usdt_amount = float_format % usdt_amount
                            avg_price = client.get_avg_price(symbol = coin)
                            avg_price = float(avg_price["price"])
                            quantity = float(usdt_amount) / avg_price
                            quantity = round(quantity, rules[coin][3])
                            quantity = float(quantity)
                            buyor = client.order_market_buy(symbol=coin, quantity=quantity)
                            time.sleep(10)
                            sellor = client.order_market_sell(symbol=coin, quantity=quantity)
                            per = get_change(float(sellor['fills'][0]['price']), float(buyor['fills'][0]['price']))
                            per = round(per, 3)
                            if float(sellor['fills'][0]['price']) > float(buyor['fills'][0]['price']):
                                per = '+ '+ str(per) + '%'
                            else:
                                per = '- '+ str(per) + '%'
                            msg = '#'+str(coin)+'\n\nbuy at price '+str(buyor['fills'][0]['price'])+'\n\nsell at price '+str(sellor['fills'][0]['price'])+'\n\n'+str(per)
                            await client1.send_message(-1001302391646, msg)
                            with open('database.txt', 'w') as f1:
                                file1 = file1[0].replace(file1[0], coin)
                                f1.write(file1)
                                f1.close()
    except:
        pass

client1.start()
client1.run_until_disconnected()
