from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Planet(db.Model, SerializerMixin):
    __tablename__ = 'planets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    distance_from_earth = db.Column(db.Integer)
    nearest_star = db.Column(db.String)

    # Add relationship
    missions = db.relationship("Mission", backref="planet", cascade="all, delete-orphan")

    # Add serialization rules
    serialize_rules = ("-missions.planet", "-scientists.planets")


class Scientist(db.Model, SerializerMixin):
    __tablename__ = 'scientists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    field_of_study = db.Column(db.String)

    # Add relationship
    missions = db.relationship("Mission", backref="scientist", cascade="all, delete-orphan")

    # Add serialization rules
    serialize_rules = ("-missions.scientist", "-planets.scientists")

    # Add validation
    @validates("name")
    def validate_name(self, key, name):
        if not name or len(name) < 1:
            raise ValueError("Scientist must have name longer than 0 characters.")
        return name


    @validates("field_of_study")
    def validate_field_of_study(self, key, field_of_study):
        if not field_of_study or len(field_of_study) < 1:
            raise ValueError("Scientist must have a field of study longer than 0 characters.")
        return field_of_study


class Mission(db.Model, SerializerMixin):
    __tablename__ = 'missions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # Add relationships
    scientist_id = db.Column(db.Integer, db.ForeignKey('scientists.id'))
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))

    # Add serialization rules
    serialize_rules = ("-scientist.missions", "-planet.missions")

    # Add validation
    @validates("name")
    def validate_name(self, key, name):
        if not name or len(name) < 1:
            raise ValueError("Mission must have name longer than 0 characters.")
        return name
    
    @validates("scientist_id")
    def validate_scientist_id(self, key, scientist_id):
        if not scientist_id or scientist_id < 1:
            raise ValueError("Mission must have scientist_id longer than 0 characters.")
        return scientist_id
    
    @validates("planet_id")
    def validate_planet_id(self, key, planet_id):
        if not planet_id or planet_id < 1:
            raise ValueError("Scientist must have planet_id longer than 0 characters.")
        return planet_id


# add any models you may need.
