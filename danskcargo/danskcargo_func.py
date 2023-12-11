from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy import extract
from dateutil import parser
import datetime
import danskcargo_data as dcd
import danskcargo_sql as dcsql


def ensure_date(date_):
    if not isinstance(date_, datetime.datetime):
        return parser.parse(date_)
    return date_

def booked_cargo(aircraft, date_):
    # returns the already booked cargo on an aircraft at a certain date
    date_ = ensure_date(date_)
    with Session(dcsql.engine) as session:
        records = session.scalars(select(dcd.Transport).where(dcd.Transport.aircraft_id == aircraft.id).where(extract("day", dcd.Transport.date) == date_.day).where(extract("month", dcd.Transport.date) == date_.month).where(extract("year", dcd.Transport.date) == date_.year))
        weight = 0
        for record in records:
            weight += dcsql.get_record(dcd.Container, record.container_id)
        return weight

def get_transport_conflict(classparam, id):
    with Session(dcsql.engine) as session:
        if classparam == dcd.Container:
            return session.scalars(select(dcd.Transport).where(dcd.Transport.container_id == id).where(dcd.Transport.aircraft_id != -1)).first()
        elif classparam == dcd.Aircraft:
            return session.scalars(select(dcd.Transport).where(dcd.Transport.aircraft_id == id).where(dcd.Transport.aircraft_id != -1)).first()
        else:
            return False

def capacity_available(aircraft, date_, new_container):
    # does the already booked cargo plus the new container weigh less than the aircraft's maximum cargo weight?
    date_ = ensure_date(date_)
    booked = booked_cargo(aircraft, date_)
    return aircraft.capacity >= booked + new_container.weight

def find_destination(aircraft, date_):
    date_ = ensure_date(date_)
    with Session(dcsql.engine) as session:
        records = session.scalars(select(dcd.Transport).where(dcd.Transport.aircraft_id == aircraft.id).where(extract('day', dcd.Transport.date) == date_.day).where(extract('month', dcd.Transport.date) == date_.month).where(extract('year', dcd.Transport.date) == date_.year))
        for record in records:
            return dcsql.get_record(dcd.Container, record.container_id).destination
        return None

def max_one_destination(aircraft, date_, new_container):
    # is the aircraft's destination at a certain date identical to the new container's destination?
    destination = find_destination(aircraft, date_)
    return destination is None or destination == new_container.destination # Returns also true if aircraft had no destination yet