from pymongo import MongoClient
from datetime import datetime

nobel_winners = [
    {
        'category': 'Physics',
        'name': 'Albert Einstein',
        'nationality': 'Swiss',
        'sex': 'male',
        'year': 1921
    }, {
        'category': 'Physics',
        'name': 'Paul Dirac',
        'nationality': 'British',
        'sex': 'male',
        'year': 1933
    }, {
        'category': 'Chemistry',
        'name': 'Marie Curie',
        'nationality': 'Polish',
        'sex': 'female',
        'year': 1911
    },
]

DB_NOBEL_PRIZE = 'nobel_prize'
COLL_WINNERS = 'winners'


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


db = get_mongo_database(DB_NOBEL_PRIZE)
coll = db[COLL_WINNERS]

# coll.insert_many(nobel_winners)

# note that mongo ObjectIds have info about the object in addition to just an id

res = coll.find({'category': 'Chemistry'})
list(res)

# query by year > 1930
res = coll.find({'year': {'$gt': 1930}})
list(res)

# query using an or statement
res = coll.find({'$or': [
    {'year': {'$gt': 1930}},
    {'sex': 'female'}
]})

def mongo_coll_to_dicts(dbname='test',
                        collname='test',
                        query={},
                        del_id=True, **kw):
    """ Converts mongo collection to dict """

    db = get_mongo_database(dbname, **kw)
    res = list(db[collname].find(query))

    if del_id:
        for r in res:
            r.pop('_id')

    return res

# a note on time,
# yyyy-mm-dd                    Python format code '%Y-%m-%d'
# yyyy-mm-ddThh:mm:ssZ          UTC Z aftertime date and time 'T%H:%M:%S'
# yyyy-mm-ddThh:mm:ssZ+hh:mm    +2-hr offset from UTC

d = datetime.now()
d.isoformat() # this can be saved to json and used in both Python and JavaScript

