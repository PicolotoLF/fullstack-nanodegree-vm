from session import session
from database_setup import Restaurant

for x in session.query(Restaurant).all():
    print(x.name, x.metadata, x.id)

