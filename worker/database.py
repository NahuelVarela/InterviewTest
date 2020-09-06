from sqlalchemy import create_engine,Column, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import json

#Worker credentials are worker and worker
engine = create_engine('mysql+pymysql://worker:worker@localhost/passenfly', echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Airports(Base):
	__tablename__ = 'airports'
	id = Column(Integer,primary_key=True, unique=True)
	name = Column(String(120), unique=False, nullable=False)
	country = Column(String(60), unique=False, nullable=False)
	iata = Column(String(60), unique=False, nullable=False)
	icao = Column(String(60), unique=False, nullable=False)
	latitude = Column(Float, unique=False, nullable=False)
	longitude = Column(Float, unique=False, nullable=False)
	altitude = Column(Float, unique=False, nullable=False)
	timezone = Column(Float, unique=False, nullable=False)
	DST = Column(String(5), unique=False, nullable=False)
	tz = Column(String(60), unique=False, nullable=False)
	type = Column(String(60), unique=False, nullable=False)
	source = Column(String(60), unique=False, nullable=False)
	flag = Column(Boolean, unique=False, nullable=False)

def CreateEntry(data):
	#We take excces data
	data.pop("action")
	data.pop("Domain")
	entry = Airports()
	#Now I will populate the entry
	for field in data:
		setattr(entry,field,data[field])
	session = Session()
	session.add(entry)
	try:
		session.commit()
		Succes = True 
	except:
		Succes = False
	finally:
		session.close()
		return Succes

def UpdateEntry(data):
	#We take excces data
	data.pop("action")
	data.pop("Domain")
	entry = Airports()
	#Now I will populate the entry only
	#with data that is not null
	for field in data:
		if data[field] is not None:
			setattr(entry,field,data[field])
	setattr(entry,"flag",False)
	session = Session()
	session.merge(entry)
	try:
		session.commit()
		Succes = True 
	except:
		Succes = False
	finally:
		session.close()
		return Succes

def DeleteEntry(data):
	#We take excces data
	data.pop("action")
	data.pop("Domain")
	#As this is a Delete, I don't care about anything
	#Except ID which is required
	entry = Airports(id=data["id"],flag=True)
	session = Session()
	session.merge(entry)
	try:
		session.commit()
		Succes = True 
	except:
		Succes = False
	finally:
		session.close()
		return Succes