import time
import logging
from cointiger_sdk import cointiger
from cointiger_sdk import const
from test_encrypt_config import get_exchange_config, get_by_strategy_name

log = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

""" 
Using version 2 of CoinTiger API to use Private Trading API
"""
#all_currencies = cointiger.currencys()
#print(all_currencies)  # fees, pairs and min withdrawls listed here.

sname = "ctiger-mirror"
config_file = "../safe/secrets_test2.ini"

with open(config_file, 'r') as enc_file:
    plain_text = enc_file.read()
    print(plain_text)
    parser = get_exchange_config(plain_text)
    strategy, api_key, secret, exchange_name =  get_by_strategy_name(parser, sname)
    log.info( f"strategy-name: {sname}, "
              f"exchange: {exchange_name}, "
              f"api_key: {api_key}, "
              f"secret: {secret}, "
              f"strategy: {strategy}")

timestamp = cointiger.timestamp()
print(timestamp)

ticker = cointiger.ticker('btseth')
print(ticker)

import time
from cointiger_sdk import cointiger
from cointiger_sdk import const

api_key = "f1361125-28a8-4f20-aa82-68ecc4f0c160"
secret = "MTNmMjA4ZThiOGJlZmEyMWI5N2VmZWJlODQ3Njk3ZWVkYzE4NWY5YTE3YmFhNTRmNTRlZDJlOGFhODQ5M2UwZQ=="

setkey = cointiger.set_key_and_secret(api_key, secret)
print(f'setting api key, secret : {setkey}')

order_data = {
    'api_key': api_key,
    'symbol': 'btseth',
    'price': '0.00016',
    'volume': '320',
    'side': const.SideType.SELL.value,
    'type': const.OrderType.LimitOrder.value,
    'time': int(time.time())
}

print(f'order data: {order_data}')

log.info("COINTIGER: get signature from order data")
print(cointiger.get_sign(order_data))

log.info("COINTIGER PLACE ORDER")
#order_id = cointiger.order(dict(order_data, **{'sign': cointiger.get_sign(order_data)}))
#print(order_id)

order_id = 127560418
print(cointiger.make_detail('btseth', order_id, int(time.time())))
print(cointiger.match_results('btseth', '2019-11-10', '2019-11-12', int(time.time())))

cancel_data = {
    'api_key': api_key,
    'orderIdList': '{"btseth":['+str(order_id)+']}',
    'time': int(time.time()),
}
print(cancel_data)

log.info("COINTIGER BATCH CANCEL")
cancel_resp = cointiger.batch_cancel(dict(cancel_data, **{'sign': cointiger.get_sign(cancel_data)})))
print(cancel_resp)

log.info("Show COINTIGER orders cancelled")
print(cointiger.orders('btseth', 'canceled', int(time.time()), types='buy-market'))


# success response string for order cancel
# {"code":"0","msg":"suc","data":{"success":[127560418],"failed":[]}}

#2019-11-11 00:05:38,817 INFO COINTIGER PLACE ORDER
#{"code":"0","msg":"suc","data":{"order_id":127560418}}

#2019-11-11 00:04:26,021 INFO COINTIGER PLACE ORDER
#{"code":"1","msg":"price precision exceed the limit","data":null}

#2019-11-11 00:15:21,765 INFO COINTIGER BATCH CANCEL
#{"code":"2","msg":"orderIdListNot EXIST","data":null}

#2019-11-11 00:17:21,128 INFO COINTIGER BATCH CANCEL
#{"code":"0","msg":"suc","data":{"success":[127560418],"failed":[]}}

