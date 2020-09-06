from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Airports(db.Model):
    id = db.Column(db.Integer,primary_key=True, unique=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    country = db.Column(db.String(60), unique=False, nullable=False)
    iata = db.Column(db.String(60), unique=False, nullable=False)
    icao = db.Column(db.String(60), unique=False, nullable=False)
    latitude = db.Column(db.Float, unique=False, nullable=False)
    longitude = db.Column(db.Float, unique=False, nullable=False)
    altitude = db.Column(db.Float, unique=False, nullable=False)
    timezone = db.Column(db.Float, unique=False, nullable=False)
    DST = db.Column(db.String(5), unique=False, nullable=False)
    tz = db.Column(db.String(60), unique=False, nullable=False)
    type = db.Column(db.String(60), unique=False, nullable=False)
    source = db.Column(db.String(60), unique=False, nullable=False)
    flag = db.Column(db.Boolean, unique=False, nullable=False)

def ReadCSV(path):
	import csv
	with open(path, newline='') as csvfile:
		data_object = csv.DictReader(csvfile,delimiter=',')
		data_object = list(data_object)
		return data_object


def UpdateDatabase(path):
	""" Insted of using add, I will use merge.
	If data is in csv but not in table --> Insert
	If data is in csv and in table--> Update
	Merge takes care of this.
	 """
	full_data = ReadCSV(path)
	for row in full_data:
		#If Float values are missing,  replace with Null
		if len(row["latitude"].strip()) == 0:
			row["latitude"] = None
		if len(row["longitude"].strip()) == 0:
			row["longitude"] = None
		if len(row["altitude"].strip()) == 0:
			row["altitude"] = None
		if len(row["timezone"].strip()) == 0:
			row["timezone"] = None

		airport = Airports(
			id=row["id"],
			name=row["name"],
			country=row["country"],
			iata=row["iata"],
			icao=row["icao"],
			latitude=row["latitude"],
			longitude=row["longitude"],
			altitude=row["altitude"],
			timezone=row["timezone"],
			DST=row["DST"],
			tz=row["tz"],
			type=row["type"],
			source=row["source"],
			flag=False)
		db.session.merge(airport)
	try:
		db.session.commit()
		result = {
		"Success?": True,
		"Number of Rows": len(full_data)
		}

	except:
		db.session.rollback()
		result = {
		"Success?": False
		}
	finally:
		db.session.close()
		return result
    