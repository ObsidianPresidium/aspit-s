from sqlalchemy.orm import declarative_base, Session  # install sqlalchemy with the command "pip install SQLAlchemy" in a terminal.
from sqlalchemy import Column, String, Integer, Date, ForeignKey  # the library sqlalchemy helps us to work with a database
from sqlalchemy import create_engine
from dateutil import parser

db = "sqlite:///danskcargo_database.db"
engine = create_engine(db, echo=False, future=True)
Base = declarative_base()

class Object(Base):
    __abstract__ = True

    def __init__(self):
        super().__init__()

    # def __repr__(self):
    #     return self.__class__.__name__ + " type. I have the attributes " + repr(self.attributes)

    attributes_names = []
    valid_test_attribute = 1

    def convert_to_tuple(self):
        return ("N/A")

    def valid(self):
        try:
            value = int(self.convert_to_tuple()[self.valid_test_attribute])
        except ValueError:
            return False
        return value >= 0

class Container(Object):
    __tablename__ = "containers"
    id = Column(Integer, primary_key=True)
    weight = Column(Integer)
    destination = Column(String)
    attributes_names = ["id", "weight", "destination"]

    def __init__(self, weight, destination, id=-1):
        super().__init__()
        self.weight = weight
        self.destination = destination
        if id >= 0:
            self.id = id

    def convert_to_tuple(self):
        return self.id, self.weight, self.destination

class Aircraft(Object):
    __tablename__ = "aircraft"
    id = Column(Integer, primary_key=True)
    capacity = Column(Integer)
    registration = Column(String)
    attributes_names = ["id", "capacity", "registration"]

    def __init__(self, capacity, registration, id=-1):
        super().__init__()
        self.capacity = capacity
        self.registration = registration
        if id >= 0:
            self.id = id

    def convert_to_tuple(self):
        return self.id, self.capacity, self.registration

class Transport(Object):
    __tablename__ = "transport"
    id = Column(Integer, primary_key=True)
    date = Column(Date)
    container_id = Column(Integer, ForeignKey("containers.id"), nullable=False)
    aircraft_id = Column(Integer, ForeignKey("aircraft.id"), nullable=False)
    attributes_names = ["id", "date", "containerid", "aircraftid"]
    valid_test_attribute = 2

    def __init__(self, date, container_id, aircraft_id, id=-1):
        super().__init__()
        self.date = date
        self.container_id = container_id
        self.aircraft_id = aircraft_id
        if id >= 0:
            self.id = id

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

def convert_from_tuple(classparam, tuple_):
    if classparam == Container:
        return_object = Container(id=int(tuple_[0]), weight=int(tuple_[1]), destination=tuple_[2])
    elif classparam == Aircraft:
        return_object = Aircraft(id=int(tuple_[0]), capacity=int(tuple_[1]), registration=tuple_[2])
    elif classparam == Transport:
        return_object = Transport(id=int(tuple_[0]), date=parser.parse(tuple_[1]), container_id=int(tuple_[2]), aircraft_id=int(tuple_[3]))
    else:
        raise TypeError("Could not match classparam with a class that exists")

    return return_object