# Python standard libraries
import os

from flask import Flask, Blueprint

UPLOAD_FOLDER = '/home/master/Documents/passenfly/Files'
ALLOWED_EXTENSIONS = {'csv'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://worker:worker@localhost/passenfly'

####################
#### Blueprints ####
####################

from api.router import rest_api as api
from api.schema_worker import db

db.init_app(app)

app.register_blueprint(api, url_prefix='/api/')


@app.route('/')
def hello_world():
	return 'Flask server is running'


if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 5000)))