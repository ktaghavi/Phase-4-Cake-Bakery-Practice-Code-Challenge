from random import choice as rc, randint
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import app
from models import db, Cakes, CakeBakeries, Bakeries
with app.app_context():
    pass
fake = Faker()
def createcakes():
    cakes = []
    for _ in range(10):
        c = Cakes(
            name = fake.name(),
            description = fake.sentence(),
         )
        cakes.append(c)
    return cakes

def createbakeries():
    bakery= []
    for _ in range(10):
        b = Bakeries(
            name = fake.name(),
            address = fake.address(),
         )
        bakery.append(b)
    return bakery 

def createcakebakeries():
    cakebakeries= []
    for _ in range(10):
       cakebakeries.append(CakeBakeries(
            price = randint(1,100),
            cake_id = randint(1,10),
            bakery_id = randint(1,10),
        ))
    return cakebakeries

if __name__ == '__main__':
    with app.app_context():
        Cakes.query.delete()
        Bakeries.query.delete()
        CakeBakeries.query.delete()
        cakes = createcakes()
        bakeries = createbakeries()
        cakebakeries = createcakebakeries()

        db.session.add_all(cakes)
        db.session.add_all(cakebakeries)
        db.session.add_all(bakeries)
        db.session.commit()