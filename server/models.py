from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin
# from sqlalchemy.sql import func

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# Add models here

class Cakes(db.Model, SerializerMixin):
    __tablename__ = 'cakes_table'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    #Add relationship
    cakebakeries = db.relationship("CakeBakeries", backref="cakes")

    #Add Serialzation
    serialze_rules = ('-cakebakeries.cakes_table',)

class Bakeries(db.Model, SerializerMixin):
    __tablename__ = 'bakeries_table'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String)

    #Add relationship
    cakebakeries = db.relationship("CakeBakeries", backref="bakeries")

    #Add Serialzation
    serialze_rules = ('-cakebakeries.bakeries_table',)
    
class CakeBakeries(db.Model, SerializerMixin):
    __tablename__ = 'cake_bakeries_table'

    id = db.Column(db.Integer, primary_key=True)
    cake_id = db.Column(db.Integer, db.ForeignKey('cakes_table.id'))
    bakery_id = db.Column(db.Integer, db.ForeignKey('bakeries_table.id'))
    price = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    #Add Seralization
    serialize_rules = ('-cakes', '-bakeries')

    #Add Validation
    @validates('price')
    def validate_price(self, key, price):
        if not 0 < price <= 1000:
            raise ValueError("Ptice must be between 1 and 1000.")
        return price