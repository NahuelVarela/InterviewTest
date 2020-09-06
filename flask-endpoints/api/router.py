#########################
####  API Router ####
#########################

import os

from flask import (
	Blueprint,
	request,
	current_app as app
)

from flask_restx import (
	Api,
	Resource,
	reqparse
)

from werkzeug.datastructures import (
	FileStorage
)

from .broker import (
	sendMessage
)

from .schema_worker import (
	ReadCSV,
	UpdateDatabase
)

""" Parsers """

schema_parser = reqparse.RequestParser()
schema_parser.add_argument('name')
schema_parser.add_argument('file', location='files',
	type=FileStorage, required=True)

entry_parser = reqparse.RequestParser()
entry_parser.add_argument('id', required=True, help="ID must be included")
entry_parser.add_argument('name')
entry_parser.add_argument('city')
entry_parser.add_argument('iata')
entry_parser.add_argument('icao')
entry_parser.add_argument('latitude')
entry_parser.add_argument('longitude')
entry_parser.add_argument('altitude')
entry_parser.add_argument('timezone')
entry_parser.add_argument('dst')
entry_parser.add_argument('tz')
entry_parser.add_argument('type')
entry_parser.add_argument('source')

#We define the blueprint for this Module
rest_api = Blueprint('api', __name__)
api = Api(rest_api)

#Routes
""" Tribal test endpoint """
@api.route("test")
class HelloWorld(Resource):
	def get(self):
		return {'hello':'world'}

""" Endpoint that accepts the csv file and updates the table """
@api.route("schema/create")
class CreateSchema(Resource):

	@api.expect(schema_parser)	
	def post(self):
		#I should use secure file name as in Flask documentation
		#And also only allow csv
		#Also, care with the path as it will need to be a docker container.
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

""" Enpoint to create an entry"""
@api.route("entry/create")
class CreateEntry(Resource):
	@api.expect(entry_parser)
	def post(self):
		args = entry_parser.parse_args()
		args["action"] = "create"
		args["Domain"] = "entry"
		sendMessage("primary",args)
		args.pop("action")
		args.pop("Domain")
		response = {
		"Action": "Create",
		"Status": "Finished",
		"Success": True,
		"Object": args
		}
		return response
		

		

""" Enpoint to update an entry"""
@api.route("entry/update")
class UpdateEntry(Resource):
	@api.expect(entry_parser)
	def post(self):
		args = entry_parser.parse_args()
		args["action"] = "update"
		args["Domain"] = "entry"
		sendMessage("primary",args)
		args.pop("action")
		args.pop("Domain")
		confirmation_object = {}
		for field in args:
			if args[field] is  not None:
				confirmation_object[field] = args[field]
		response = {
		"Action": "Update",
		"Status": "Finished",
		"Success": True,
		"Object": confirmation_object
		}
		return response
		

""" Enpoint to delete an entry"""
@api.route("entry/delete")
class DeleteEntry(Resource):
	@api.expect(entry_parser)
	def post(self):
		args = entry_parser.parse_args()
		args["action"] = "delete"
		args["Domain"] = "entry"
		sendMessage("primary",args)
		args.pop("action")
		args.pop("Domain")
		response = {
		"Action": "Delete",
		"Status": "Finished",
		"Success": True,
		"Object": args["id"]
		}
		return response

@api.route("help/")
class Help(Resource):
	""" This endpoint is the Documentation endpoint """
	def get(self):
		import json
		path = os.path.join(app.config['UPLOAD_FOLDER'], 'docs.json')
		with open(path) as json_file:
		    data = json.load(json_file)
		return data
		
		