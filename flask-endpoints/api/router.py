#########################
####  API Router ####
#########################

import os

from flask import (
	Blueprint,
	request,
	current_app as app,
	jsonify
)

from flask_restx import (
	Api,
	Resource,
	reqparse,
	fields
)

from werkzeug.datastructures import (
	FileStorage
)

from .broker import (
	sendMessage
)

from .schema_worker import (
	ReadCSV,
	GetSchema,
	UpdateDatabase
)

#We define the blueprint for this Module
rest_api = Blueprint('api', __name__)
api = Api(rest_api, 
	version = "1.1",
	title="Updated Exam")

# Parser - Only used for the csv file
schema_parser = reqparse.RequestParser()
schema_parser.add_argument('name')
schema_parser.add_argument('file', location='files',
	type=FileStorage, required=True)

#restx model
airport_model = api.model('Airports',{
	'id':fields.Integer(required=True, readonly=True, description='Entry unique id'),
	'name':fields.String(readonly=True, description='Name of the Airport'),
	'city':fields.String(readonly=True, description=''),
	'country':fields.String(readonly=True, description=''),
	'iata':fields.String(readonly=True, description=''),
	'icao':fields.String(readonly=True, description=''),
	'latitude':fields.Float(readonly=True, description=''),
	'longitude':fields.Float(readonly=True, description=''),
	'altitude':fields.Float(readonly=True, description=''),
	'timezone':fields.Float(readonly=True, description=''),
	'DST':fields.String(readonly=True, description=''),
	'tz':fields.String(readonly=True, description=''),
	'type':fields.String(readonly=True, description=''),
	'source':fields.String(readonly=True, description=''),
	})

class TaskTracker(object):
	def __init__(self):
		self.counter = 0

	def get(self):
		return self.counter

	def add(self):
		self.counter += 1

task = TaskTracker()


#Routes

""" Endpoint that accepts the csv file and updates the table """
@api.route('schema')
class UpdateTable(Resource):
	@api.doc('Update Table')
	@api.expect(schema_parser)
	@api.response(200,"Airports database has been succesfully updated")	
	def patch(self):
		""" Updates the database by reading a csv file """
		args = schema_parser.parse_args()
		uploaded_file = args['file']
		filename = args['name']
		path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
		uploaded_file.save(path)
		result = UpdateDatabase(path)
		if result.get("Success?"):
			message = "Airports database has been succesfully updated with {} rows".format(result.get("Number of Rows"))
			return message
		else:
			return "There was an error on the update process"
		return UpdateDatabase(path,table)

	@api.doc('Get Schema')
	@api.expect(schema_parser)
	def post(self):
		""" It reads the csv file header and returns the table schema """
		args = schema_parser.parse_args()
		uploaded_file = args['file']
		filename = args['name']
		path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
		uploaded_file.save(path)
		schema = GetSchema(path)

		return jsonify(str(vars(schema)))



@api.route("entry")
class CreateEntry(Resource):
	
	""" Endpoint to send the action of Create Entry """
	@api.expect(airport_model)
	@api.marshal_with(airport_model)
	@api.doc("create_entry")
	def put(self):
		""" Adds an entry to the Airports database """
		object_data = api.payload
		processing_info = {
		"task-id": task.get(),
		"action": "create",
		}
		message = [object_data,processing_info]
		sendMessage("primary",message)
		task.add()
		return "done"

	@api.expect(airport_model)
	@api.marshal_with(airport_model)
	@api.doc("update_entry")
	def patch(self):
		""" Updates an entry on the database """
		object_data = api.payload
		processing_info = {
		"task-id": task.get(),
		"action": "update",
		}
		message = [object_data,processing_info]
		sendMessage("primary",message)
		task.add()
		return "la concha de tu madre"

	@api.expect(airport_model)
	@api.marshal_with(airport_model)
	@api.doc("delete_entry")
	def delete(self):
		""" Deletes an entry on the database """
		object_data = api.payload
		processing_info = {
		"task-id": task.get(),
		"action": "delete",
		}
		message = [object_data,processing_info]
		sendMessage("primary",message)
		task.add()
		return "la concha de tu madre"

