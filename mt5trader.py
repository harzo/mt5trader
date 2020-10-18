import configparser
import pymt5adapter as mt5
import logging

config = configparser.ConfigParser()
config.read("config.ini")

mt5_connected = mt5.connected(
    server=config['auth']['server'],
    login=int(config['auth']['login']),
    password=config['auth']['password'],
    path=r'%s' % config['conn']['path'],
    portable=bool(config['conn']['portable']),
    timeout=int(config['conn']['timeout']),
    logger=mt5.get_logger(path_to_logfile=config['conn']['logfile'],
                          loglevel=logging.DEBUG, time_utc=False),
    ensure_trade_enabled=True,
    enable_real_trading=False,
    raise_on_errors=True,
    return_as_dict=False,
    return_as_native_python_objects=False,
)


def setup_logger():
    logger = logging.getLogger('mt5trader')
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(
        logging.Formatter('%(asctime)s [%(levelname)s] %(message)s'))
    logger.addHandler(handler)

    return logger


def run():
    logger = setup_logger()

    with mt5_connected as conn:
        logger.info('MT5 Terminal Connected')
        print(mt5.version())


if __name__ == '__main__':
    run()
