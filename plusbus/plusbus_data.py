from sqlalchemy.orm import declarative_base, Session
from sqlalchemy import Column, String, Integer, Date, ForeignKey, create_engine
from dateutil import parser

db = "sqlite:///plusbus_database.db"
engine = create_engine(db, echo=False, future=True)
Base = declarative_base()
class Object(Base):
    __abstract__ = True
    attributes_names = []

    def __repr__(self):
        return f"Record type: {self.__class__.__name__}"

    def convert_to_tuple(self):
        return ("N/A")

    def valid(self):
        try:
            value = int(self.convert_to_tuple()[3]) # 3 is the valid test attribute in all except one class
        except ValueError:
            return False
        return value >= 0


class Customer(Object):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    phone = Column(String)

    attributes_names = ["id", "name", "phone"]

    def __init__(self, name, phone, id=-1):
        super().__init__()
        self.name = name
        self.phone = phone
        if id >= 0:
            self.id = id

    def valid(self):
        try:
            value = str(self.convert_to_tuple()[1])
        except ValueError:
            return False
        return value != "INVALID_RECORD"

    def convert_to_tuple(self):
        return self.id, self.name, self.phone

class Trip(Object):
    __tablename__ = "trips"
    id = Column(Integer, primary_key=True)
    route = Column(String)
    departure = Column(Date)
    capacity = Column(Integer)
    attributes_names = ["id", "route", "departure", "capacity"]

    def __init__(self, route, departure, capacity, id=-1):
        super().__init__()
        self.route = route
        self.departure = departure
        self.capacity = capacity
        if id >= 0:
            self.id = id

    def convert_to_tuple(self):
        return self.id, self.route, self.departure, self.capacity

class Booking(Object):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)
    num_passengers = Column(Integer)
    attributes_names = ["id", "customer_id", "trip_id", "num_passengers"]

    def __init__(self, customer_id, trip_id, num_passengers, id=-1):
        super().__init__()
        self.customer_id = customer_id
        self.trip_id = trip_id
        self.num_passengers = num_passengers
        if id >= 0:
            self.id = id

    def convert_to_tuple(self):
        return self.id, self.customer_id, self.trip_id, self.num_passengers

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
    if classparam == Customer:
        return_object = Customer(id=int(tuple_[0]), name=tuple_[1], phone=tuple_[2])
    elif classparam == Trip:
        return_object = Trip(id=int(tuple_[0]), route=tuple_[1], departure=parser.parse(tuple_[2]), capacity=int(tuple_[3]))
    elif classparam == Booking:
        return_object = Booking(id=int(tuple_[0]), customer_id=int(tuple_[1]), trip_id=int(tuple_[2]), num_passengers=int(tuple_[3]))
    else:
        raise TypeError("Could not match classparam with a class that exists")

    return return_object