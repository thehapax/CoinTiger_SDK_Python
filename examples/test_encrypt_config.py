import logging
from getpass import getpass
from configparser import ConfigParser, NoOptionError

log = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

# only accept API keys for these ccxt exchanges, cross check here.
EXCHANGES = ['cointiger', 'binance', 'bitfinex']
STRATEGIES =['simple', 'ccxt-mirror', 'triangular']

def test_encrypt(input_passwd, config_filename):
    with open(config_filename, 'rb') as config_file:
        file_content = config_file.read()
        cipher_text = encrypt_file(input_passwd, file_content)
        log.info("Cipher: %s", binascii.hexlify(bytearray(cipher_text)))

    enc_filename = "enc_"+config_filename
    with open(enc_filename, 'wb') as enc_file:
        enc_file.write(cipher_text)

    return cipher_text


def test_decrypt(input_passwd, config_filename):
    with open(config_filename, 'rb') as enc_file:
        content = enc_file.read()
        plain_text = decrypt_file(input_passwd, content)
        if plain_text is None:
            log.info("Plain text unable to decrypt, error")
    return plain_text


def get_exchange_config(content):
    try:
        parser = ConfigParser()
        parser.read_string(content)
        return parser
    except Exception as e:
        log.error(e)
        pass


def get_by_strategy_name(parser, name):
    section_name = None

    has_section = parser.has_section(name)
    if has_section:
        log.info(f'section_name: {name}')
        section_name = name

    try:
        strategy= parser.get(section_name, 'strategy')
        api_key = parser.get(section_name, 'api_key')
        secret = parser.get(section_name, 'secret')
        exchange_name = parser.get(section_name, 'exchange-name')

        return strategy, api_key, secret, exchange_name
    except NoOptionError as e:
        log.error(e)


if __name__ == "__main__":
    sname = "ctiger-mirror"
    config_file = "secrets_test2.ini"

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


    input_passwd = getpass("password: ")
    test_encrypt(input_passwd, config_file)
    plain_decrypt = test_decrypt(input_passwd, "enc_"+config_file)




