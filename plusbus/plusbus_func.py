from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy import extract
from dateutil import parser
import datetime
import plusbus_data as pbd
import plusbus_sql as pbsql

# Før en booking bliver oprettet skal der tjekkes om der kan bookes flere
# passagerer på bussen uden at overskride dets maksimale transportkapacitet.
# Skriv en tilsvarende funktion i funktionslaget.

def booked_passengers(target_trip_id):
    # return the amount of booked passengers on a certain trip
    with Session(pbsql.engine) as session:
        records = session.scalars(select(pbd.Booking).where(pbd.Booking.trip_id == target_trip_id))
        num_booked_passengers = 0
        for record in records:
            num_booked_passengers += record.num_passengers
        return num_booked_passengers

def space_for_input_passengers(input_num_passengers, target_trip_id):
    # return true if there's space for passengers on a trip, if there's not, return false
    target_trip = pbsql.get_record(pbd.Trip, target_trip_id)
    return booked_passengers(target_trip_id) + input_num_passengers <= target_trip.capacity