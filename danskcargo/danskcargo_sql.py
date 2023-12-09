from sqlalchemy.orm import Session  # install sqlalchemy with the command "pip install SQLAlchemy" in a terminal.
from sqlalchemy.engine import Engine
from sqlalchemy import create_engine, select, event, update, delete
from danskcargo_data import export_engine, Container, Aircraft, Transport

db = "sqlite:///danskcargo_database.db"
engine = create_engine(db, echo=False, future=True)

def match_attributes_and_entry_tuple(classparam, entry_tuple):
    args = {}
    for attribute in enumerate(classparam.attributes_names):
        args.update({attribute[1]: entry_tuple[attribute[0]]})

    return args

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

def select_all(classparam):  # return a list of all records in classparams table
    with Session(export_engine()) as session:
        records = session.scalars(select(classparam))
        result = []
        for record in records:
            result.append(record)
    return result


def get_record(classparam, record_id):  # return the record in classparams table with a certain id   https://docs.sqlalchemy.org/en/14/tutorial/data_select.html
    with Session(export_engine()) as session:
        # in the background this creates the sql query "select * from persons where id=record_id" when called with classparam=Person
        record = session.scalars(select(classparam).where(classparam.id == record_id)).first()
    return record

def create_record(record):
    with Session(engine) as session:
        record.id = None
        session.add(record)
        session.commit()

def update_record(classparam, entry_tuple):
    # update a record in a table specified by classparam
    args = match_attributes_and_entry_tuple(classparam, entry_tuple)
    with Session(engine) as session:
        session.execute(update(classparam).where(classparam.id == args["id"]).values(args))
        session.commit()

def delete_hard(classparam, entry_tuple):
    # delete a record in a table specified by classparam
    with Session(engine) as session:
        session.execute(delete(classparam).where(classparam.id == entry_tuple[0]))
        session.commit()

def delete_soft(classparam, entry_tuple):
    # soft delete a record in a table specified by classparam by making one of its values invalid
    matched_dict = match_attributes_and_entry_tuple(classparam, entry_tuple)
    if classparam == Transport:
        matched_dict["containerid"] = -1
    elif classparam == Aircraft:
        matched_dict["capacity"] = -1
    elif classparam == Container:
        matched_dict["weight"] = -1
    else:
        raise KeyError("Unknown record type passed to delete_soft function.")

    with Session(engine) as session:
        session.execute(update(classparam).where(classparam.id == matched_dict["id"]).values(matched_dict))
        session.commit()