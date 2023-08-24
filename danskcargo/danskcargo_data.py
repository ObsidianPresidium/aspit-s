from sqlalchemy.orm import declarative_base, Session  # install sqlalchemy with the command "pip install SQLAlchemy" in a terminal.
from sqlalchemy import Column, String, Integer  # the library sqlalchemy helps us to work with a database
from sqlalchemy import create_engine, select

db = "sqlite:///danskcargo_database.db"
Base = declarative_base()

class Object:
    attributes = []

    def convert_to_tuple(self):
        result = ()
        for i in self.attributes:
            result += i
        return result

#     def valid(self):
#         if

class Container(Base):
    __tablename__ = "containers"
    id = Column(Integer, primary_key=True)
    weight = Column(Integer)
    destination = Column(String)

    def convert_to_tuple(self):
        return self.id, self.weight, self.destination

class Aircraft(Base):
    __tablename__ = "aircraft"
    id = Column(Integer, primary_key=True)
    capacity = Column(Integer)
    registration = Column(String)
    def convert_to_tuple(self):
        return self.id, self.capacity, self.registration

class Transport(Base):
    __tablename__ = "transport"
    id = Column(Integer, primary_key=True)
    date = Column(String)
    container_id = Column(Integer)
    aircraft_id = Column(Integer)
    def convert_to_tuple(self):
        return self.id, self.date, self.container_id, self.aircraft_id

# In case I need this for later...
# to_data = [
#     Container(weight=3003, destination="Helsinki"),
#     Container(weight=, destination=""),
#     Container(weight=, destination=""),
#     Container(weight=, destination=""),
#     Container(weight=, destination=""),
#     Container(weight=, destination=""),
#     Container(weight=, destination=""),
#     Container(weight=, destination=""),
#     Container(weight=, destination=""),
#     Container(weight=, destination=""),
#
#     Aircraft(capacity=, registration=""),
#     Aircraft(capacity=, registration=""),
#     Aircraft(capacity=, registration=""),
#     Aircraft(capacity=, registration=""),
#     Aircraft(capacity=, registration=""),
#     Aircraft(capacity=, registration=""),
#     Aircraft(capacity=, registration=""),
#     Aircraft(capacity=, registration=""),
#     Aircraft(capacity=, registration=""),
#     Aircraft(capacity=, registration=""),
#
#     Transport(date="", container_id=, aircraft_id=),
#     Transport(date="", container_id=, aircraft_id=),
#     Transport(date="", container_id=, aircraft_id=),
#     Transport(date="", container_id=, aircraft_id=),
#     Transport(date="", container_id=, aircraft_id=),
# ]