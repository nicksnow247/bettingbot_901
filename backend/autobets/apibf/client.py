import os
# BETFAIR_PASS = os.environ.get('BETFAIR_PASS')
# BETFAIR_USER = os.environ.get('BETFAIR_USER')
# BF_APP_KEY_DEV = os.environ.get('BF_APP_KEY_DEV')
# CERTS_DIR = 'backend/autobets/apibf/certs'

BF_APP_KEY_DEV='54zipkG6cgego8m9'
BETFAIR_USER='Dog2021'
BETFAIR_PASS='Leagoom13!!'

from betfairlightweight import APIClient

trading = APIClient(BETFAIR_USER, BETFAIR_PASS,BF_APP_KEY_DEV)


def get_betfair_client():
    if not trading.session_token:
        trading.login_interactive()
    return trading
get_betfair_client()
