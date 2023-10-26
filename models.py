from sqlalchemy import create_engine, Column, Enum, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

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

# v1.4.39
engine = create_engine('sqlite:///data/nobel_prize.db', echo=True)

Base = declarative_base()


class Winner(Base):
    __tablename__ = 'winners'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    category = Column(String)
    year = Column(Integer)
    nationality = Column(String)
    sex = Column(Enum('male', 'female'))

    def __repr__(self):
        return f'<Winner name={self.name}, category={self.category}, year={self.year}>'


Session = sessionmaker(bind=engine)
session = Session()

# Adds Winner for each person
winner_rows = [Winner(**w) for w in nobel_winners]
session.add_all(winner_rows)
session.commit()

# Query by column name
print(session.query(Winner).count())
result = session.query(Winner).filter_by(nationality="Swiss")
print(list(result))

# Compound Query
result = session.query(Winner).filter(
    Winner.category == "Physics",
    Winner.nationality != "Swiss")
list(result)

# Query by id
session.query(Winner).get(3)

# Order by column name
result = session.query(Winner).order_by('year')
list(result)

def inst_to_dict(inst, delete_id=True):
    """ Converts an SQLA instance to a Dict. Deletes SQLA ID by default"""
    data = {}
    for column in inst.__table__.columns:
        data[column.name] = getattr(inst, column.name)
    if delete_id:
        data.pop('id')
    return data

# Convert instance to dict
winner_rows = session.query(Winner) # in a real db, it's usually bad to fetch an entire table.
nobel_winners = [inst_to_dict(w) for w in winner_rows]
for w in nobel_winners: print(w)

# Change an instance
marie = session.query(Winner).get(3)
marie.nationality = 'French'
session.dirty # displays pending changes

session.commit()

# drop a table
# Winner.__table__.drop(engine)



