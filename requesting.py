import requests
import urllib3
import ssl

# response = requests.get("https://en.wikipedia.org/wiki/Nobel_Prize")

# response = requests.get(
#     "https://cdph.data.ca.gov/api/views/6tej-5zx7/rows.json")

# data = response.json()
# data.keys()


# ************ Hacky Fix Alert ************

# see S.O. link for details. Some websites, have a compatibility error
# with Python cryptography package. Below is one solution,
# https://stackoverflow.com/questions/71603314/ssl-error-unsafe-legacy-renegotiation-disabled
# another is to change conda's ssl version.
# conda install -n conda-env-name openssl=1

class CustomHttpAdapter(requests.adapters.HTTPAdapter):
    def __init__(self, ssl_context=None, **kwargs):
        self.ssl_context = ssl_context
        super().__init__(**kwargs)

    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = urllib3.poolmanager.PoolManager(
            num_pools=connections, maxsize=maxsize,
            block=block, ssl_context=self.ssl_context)


def get_legacy_session():
    ctx = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    ctx.options |= 0x4  # OP_LEGACY_SERVER_CONNECT
    session = requests.session()
    session.mount('https://', CustomHttpAdapter(ctx))
    return session

# ************ End Hacky Fix ************


OECD_ROOT_URL = 'http://stats.oecd.org/sdmx-json/data'


def make_OECD_request(dsname, dimensions, params=None, root_dir=OECD_ROOT_URL):
    """ Makes a GET request for the OECD API """

    if not params:
        params = {}

    dim_args = ['+'.join(d) for d in dimensions]
    dim_str = '.'.join(dim_args)

    url = root_dir + '/' + dsname + '/' + dim_str + '/all'

    headers = {'User-Agent': 'Mozilla/5.0'} # didn't solve ssl issue, leaving anyway

    print("Requesting URL: " + url)
    return get_legacy_session().get(url, params=params, headers=headers)


response = make_OECD_request('QNA',
                             (('USA', 'AUS'), ('GDP', 'B1_GE'),
                              ('CUR', 'VOBARSA'), ('Q')),
                             {'startTime': '2013-Q1', 'endTime': '2014-Q1'})

if response.status_code == 200:
    json = response.json()
    print(json.keys())


