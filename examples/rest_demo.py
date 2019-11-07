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

print(cointiger.timestamp())
print(cointiger.currencys())

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

cointiger.set_key_and_secret(api_key, secret)

order_data = {
    'api_key': api_key,
    'symbol': 'btcusdt',
    'price': '0.01',
    'volume': '0.01',
    'side': const.SideType.BUY.value,
    'type': const.OrderType.LimitOrder.value,
    'time': int(time.time())
}
print(cointiger.get_sign(order_data))
print(cointiger.order(dict(order_data, **{'sign': cointiger.get_sign(order_data)})))

cancel_data = {
    'api_key': api_key,
    'orderIdList': '{"btcusdt":["1","2"],"ethusdt":["11","22"]}',
    'time': int(time.time()),
}
print(cointiger.batch_cancel(dict(cancel_data, **{'sign': cointiger.get_sign(cancel_data)})))
print(cointiger.orders('btcusdt', 'canceled', int(time.time()), types='buy-market'))
