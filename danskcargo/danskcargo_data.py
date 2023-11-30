from sqlalchemy.orm import declarative_base, Session  # install sqlalchemy with the command "pip install SQLAlchemy" in a terminal.
from sqlalchemy import Column, String, Integer  # the library sqlalchemy helps us to work with a database
from sqlalchemy import create_engine, select
import os

db = "sqlite:///danskcargo_database.db"
Base = declarative_base()

class Object(Base):
    __abstract__ = True

    def __init__(self):
        super().__init__()

    # def __repr__(self):
    #     return self.__class__.__name__ + " type. I have the attributes " + repr(self.attributes)

    attributes = []

    def convert_to_tuple(self):
        return ("N/A")

    def valid(self, record):
        def do_test(test_record):
            if test_record.type == "INTEGER":
                try:
                    value = int(test_record)
                except ValueError:
                    return False
                return value >= 0
            elif test_record.type == "VARCHAR":
                try:
                    value = str(test_record)
                except ValueError:
                    return False
            else:
                return False

        if record == "ALL":
            valid_attributes = []
            for i in self.attributes:
                valid_attributes.append(do_test(i))
            return valid_attributes
        else:
            return do_test(record)

class Container(Object):
    __tablename__ = "containers"
    id = Column(Integer, primary_key=True)
    weight = Column(Integer)
    destination = Column(String)
    attributes = [id, weight, destination]

    def __init__(self, weight, destination):
        super().__init__()
        self.weight = weight
        self.destination = destination

    def convert_to_tuple(self):
        return self.id, self.weight, self.destination

class Aircraft(Object):
    __tablename__ = "aircraft"
    id = Column(Integer, primary_key=True)
    capacity = Column(Integer)
    registration = Column(String)
    attributes = [id, capacity, registration]

    def __init__(self, capacity, registration):
        super().__init__()
        self.capacity = capacity
        self.registration = registration

    def convert_to_tuple(self):
        return self.id, self.capacity, self.registration

class Transport(Object):
    __tablename__ = "transport"
    id = Column(Integer, primary_key=True)
    date = Column(String)
    container_id = Column(Integer)
    aircraft_id = Column(Integer)
    attributes = [id, date, container_id, aircraft_id]

    def __init__(self, date, container_id, aircraft_id):
        super().__init__()
        self.date = date
        self.container_id = container_id
        self.aircraft_id = aircraft_id

    def convert_to_tuple(self):
        return self.id, self.date, self.container_id, self.aircraft_id

def export_engine():
    engine = create_engine(db, echo=False, future=True)
    Base.metadata.create_all(engine)
    return engine

def create_data(records):
    engine = export_engine()
    with Session(engine) as session:
        session.add_all(records)
        session.commit()