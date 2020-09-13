from flask import Flask, jsonify, request

app = Flask(__name__)

completed_tasks = []

@app.route('/',methods=['GET'])
def printTasks():
	return jsonify(completed_tasks)

@app.route('/tasks',methods=['PUT'])
def addTask():
	content = request.json
	completed_tasks.append(content)
	return "Success"

if __name__ == '__main__':
	app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT', 5001)))