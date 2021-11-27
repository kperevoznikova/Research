import re
import csv
from datetime import datetime
import json
import base64
import random
from string import ascii_lowercase
from websocket import create_connection

WSS_URL = 'wss://data.tradingview.com/socket.io/websocket'
DATA_URL = 'https://data.tradingview.com'


#
#   This is a raw refactoring of the https://github.com/rushic24/tradingview-scraper project
#

class Agent:
    SESSION_SIZE = 12

    def __init__(self):
        self.headers = json.dumps({'Origin': 'https://data.tradingview.com'})
        self.socket = create_connection('wss://data.tradingview.com/socket.io/websocket', headers=self.headers)
        self.session = self.gen_session()
        self.chart_session = self.gen_chart_session()

    def gen_session(self):
        return 'qs_' + ''.join(random.choice(ascii_lowercase) for i in range(self.SESSION_SIZE))

    def gen_chart_session(self):
        return 'cs_' + ''.join(random.choice(ascii_lowercase) for i in range(self.SESSION_SIZE))

    @staticmethod
    def make_json(api_func, param_list):
        return json.dumps({
            "m": api_func,
            "p": param_list
        }, separators=(',', ':')
        )

    @staticmethod
    def prepare_header(st):
        return "~m~" + str(len(st)) + "~m~" + st

    def send(self, api_func, param_list):
        self.socket.send(self.prepare_header(self.make_json(api_func, param_list)))

    def repo_transaction(self):
        self.send("set_auth_token", ["unauthorized_user_token"])
        self.send("chart_create_session", [self.chart_session, ""])
        self.send("quote_create_session", [self.session])
        self.send("quote_set_fields",
                  [self.session, "ch", "chp", "current_session", "description", "local_description", "language",
                   "exchange", "fractional", "is_tradable", "lp", "lp_time", "minmov", "minmove2", "original_name",
                   "pricescale", "pro_name", "short_name", "type", "update_mode", "volume", "currency_code", "rchp",
                   "rtc"])
        self.send("quote_add_symbols", [self.session, "NASDAQ:AAPL", {"flags": ['force_permission']}])
        self.send("quote_fast_symbols", [self.session, "NASDAQ:AAPL"])

        self.send("resolve_symbol", [self.chart_session, "symbol_1",
                                     "={\"symbol\":\"NASDAQ:AAPL\",\"adjustment\":\"splits\",\"session\":\"extended\"}"])
        self.send("create_series", [self.chart_session, "s1", "s1", "symbol_1", "1", 5000])


a = Agent()
a.repo_transaction()
resp = a.socket.recv()


def generate_csv(a):
    out = re.search('"s":\[(.+?)\}\]', a).group(1)
    x = out.split(',{\"')
    for xi in x:
        xi = re.split('\[|:|,|\]', xi)
        # print(xi)
        ind = int(xi[1])
        ts = datetime.fromtimestamp(float(xi[4])).strftime("%Y/%m/%d, %H:%M:%S")
        # ['index', 'date', 'open', 'high', 'low', 'close', 'volume']
        print(*[ind, ts, float(xi[5]), float(xi[6]), float(xi[7]), float(xi[8]), float(xi[9])])


generate_csv(resp)
# ['{"i"', '0', '"v"', '', '1627411680.0', '146.62', '146.69', '146.62', '146.67', '11910.0', '}']
# NameError: name 'employee_writer' is not defined
