from sqlalchemy import *

# Scegliere il db da usare, ci sono cose che funzionano diversamente tra i db

# La password è quella che chiede quando si installa postgres, mettere "passwordsupersegreta" per facilitare lo sviluppo
# "platypos_airlines" è il nome del db da creare da shell o pgadmin4
# Da fare: pip install psycopg2
uri = 'postgres+psycopg2://postgres:passwordsupersegreta@localhost:5432/test'
engine = create_engine(uri, echo=True)

# Per TESTARE in memoria con SQLite, serve il parametro check_same_thread
# uri = 'sqlite:///:memory:'
# engine = create_engine(uri, echo=True, connect_args={"check_same_thread": False})

metadata = MetaData()

users = Table('users', metadata,
              Column('userId', Integer, primary_key=True),
              Column('email', String(254), unique=True, nullable=False),
              Column('password', String(128), nullable=False),
              Column('name', String(255), nullable=False),
              Column('surname', String(255), nullable=False),
              )

airports = Table('airports', metadata,
                 Column('airportId', Integer, primary_key=True),
                 Column('name', String(255), nullable=False),
                 Column('city', String(255), nullable=False),
                 Column('country', String(255), nullable=False),
                 )

airplanes = Table('airplanes', metadata,
                  Column('planeCode', Integer, primary_key=True),
                  Column('name', String(255), nullable=False),
                  Column('seats', Integer, nullable=False),
                  )

# Date -> Postgres Date
# DateTime -> Postgres Timestamp without timezone
# Da scoprire cosa si puo inserire veramente
flights = Table('flights', metadata,
                Column('flightCode', Integer, primary_key=True),
                Column('departureDate', Date, nullable=False),
                Column('departureTime', DateTime, nullable=False),
                Column('arrivalDate', Date, nullable=False),
                Column('arrivalTime', DateTime, nullable=False),
                Column('departureAirport', Integer, ForeignKey('airports.airportId')),
                Column('arrivalAirport', Integer, ForeignKey('airports.airportId')),
                Column('planeCode', Integer, ForeignKey('airplanes.planeCode')),
                )

bookings = Table('bookings', metadata,
                 Column('bookingId', Integer, primary_key=True),
                 Column('seatNumber', Integer, nullable=False),
                 Column('userId', Integer, ForeignKey('users.userId')),
                 Column('flightCode', Integer, ForeignKey('flights.flightCode')),
                 )

metadata.create_all(engine)
connection = engine.connect()
