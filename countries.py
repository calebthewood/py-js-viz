import requests
from pymongo import MongoClient


def print_collection(instance, field_a=None, field_b=None):
    """ Probs a better way to do this """

    collection = list(instance)

    if len(collection) == 0:
        return print("List is empty")

    if field_a and field_b:
        for doc in collection:
            print(doc[field_a][field_b])

    elif field_a and not field_b:
        for doc in collection:
            print(doc[field_a])

    else:
        for doc in collection:
            print(doc)


def get_mongo_database(db_name,
                       host="localhost",
                       port=27017,
                       username=None,
                       password=None):
    """ Get named db from MongoDB with/out auth """

    if username and password:
        mongo_uri = f"mongodb://{username}:{password}@{host}/{db_name}"
        conn = MongoClient(mongo_uri)
    else:
        conn = MongoClient(host, port)

    return conn[db_name]


def REST_country_request(field='all', name=None, params=None):
    REST_EU_URL = "https://restcountries.com/v3.1"
    headers = {'User-Agent': 'Mozilla/5.0'}

    if not params:
        params = {}

    if field == 'all':
        return requests.get(REST_EU_URL + "/all")

    url = f"{REST_EU_URL}/{field}/name"
    print('Requesting URL ' + url)
    response = requests.get(url=url, params=params, headers=headers)

    if not response.status_code == 200:
        raise Exception(
            'Request failed with status code ' + str(response.status_code))

    return response


db_nobel = get_mongo_database('nobel_prize')
collection = db_nobel['country_data']
# response = REST_country_request()
# collection.insert_many(response.json())

# neighbors = collection.find({'borders': {'$in': ['USA']}})

# usd = collection.find({'currencies.USD': {'$exists': True}})
# print_collection(usd, 'name', 'common')


def countLandLocked():
    landy = list()
    nolandy = list()

    for country in list(collection.find()):
        if country['landlocked']:
            landy.append(country)
        else:
            nolandy.append(country)

    return (str(len(landy)) + " Landlocked",
            str(len(nolandy)) + " Not-landlocked")
# results:
#   90 Landlocked countries
#   410 Not landlocked countries

def countUNMembers():
    is_un_is_ll = 0
    is_un_not_ll = 0
    not_un_is_ll = 0
    not_un_not_ll = 0

    for country in list(collection.find()):
        if country['unMember']:
            if country['landlocked']:
                is_un_is_ll += 1
            else:
                is_un_not_ll += 1
        else:
            if country['landlocked']:
                not_un_is_ll += 1
            else:
                not_un_not_ll += 1

    un_total = is_un_is_ll + is_un_not_ll
    non_un_total = not_un_is_ll + not_un_not_ll

    print(str((is_un_is_ll/un_total) * 100)+ "% \landlocked countries in UN")
    print(str((not_un_is_ll/non_un_total) * 100)+ "% not landlocked countries in UN")

    return {
        'is_un_is_ll': is_un_is_ll,
        'is_un_not_ll': is_un_not_ll,
        'not_un_is_ll': not_un_is_ll,
        'not_un_not_ll': not_un_not_ll
    }

un_stats = countUNMembers()

countries_keys = """
    _id
    name
    tld
    cca2
    ccn3
    cca3
    independent
    status
    unMember
    currencies
    idd
    capital
    altSpellings
    region
    subregion
    languages
    translations
    latlng
    landlocked
    area
    demonyms
    flag
    maps
    population
    car
    timezones
    continents
    flags
    coatOfArms
    startOfWeek
    capitalInfo
    """
