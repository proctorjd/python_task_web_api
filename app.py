from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import os, re, datetime
import db
from models import ToDo

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

if not os.path.isfile('todos.db'):
	db.connect()


@app.route('/')
@cross_origin()
def index():
	return render_template("index.html")


@app.route("/request", methods=['POST'])
def postRequest():
    req_data = request.get_json()
    task = req_data['task']

    tk = ToDo(db.getNewId(),task)
    print('new task: ', tk.serialize())
    db.insert(tk)
    new_tks = [b.serialize() for b in db.view()]
    print('task in lib: ', new_tks)
    
    return jsonify({
                # 'error': '',
                'res': tk.serialize(),
                'status': '200',
                'msg': 'Success creating a new task!👍😀'
            })


@app.route('/request', methods=['GET'])
def getRequest():
    content_type = request.headers.get('Content-Type')
    tks = [b.serialize() for b in db.view()]
    if (content_type == 'application/json'):
        json = request.json
        for b in tks:
            if b['id'] == int(json['id']):
                return jsonify({
                    # 'error': '',
                    'res': b,
                    'status': '200',
                    'msg': 'Success getting all tasks!👍😀'
                })
        return jsonify({
            'error': f"Error ⛔❌! task with id '{json['id']}' not found!",
            'res': '',
            'status': '404'
        })
    else:
        return jsonify({
                    # 'error': '',
                    'res': tks,
                    'status': '200',
                    'msg': 'Success getting all tasks!👍😀',
                    'no_of_tasks': len(tks)
                })


@app.route('/request/<id>', methods=['GET'])
def getRequestId(id):
    req_args = request.view_args
    # print('req_args: ', req_args)
    tks = [b.serialize() for b in db.view()]
    if req_args:
        for b in tks:
            if b['id'] == int(req_args['id']):
                return jsonify({
                    # 'error': '',
                    'res': b,
                    'status': '200',
                    'msg': 'Success getting task by ID!👍😀'
                })
        return jsonify({
            'error': f"Error ⛔❌! task with id '{req_args['id']}' was not found!",
            'res': '',
            'status': '404'
        })
    else:
        return jsonify({
                    # 'error': '',
                    'res': tks,
                    'status': '200',
                    'msg': 'Success getting task by ID!👍😀',
                    'no_of_books': len(tks)
                })

@app.route("/request", methods=['PUT'])
def putRequest():
    req_data = request.get_json()
    task = req_data['task']
    the_id = req_data['id']
    tks = [b.serialize() for b in db.view()]
    for b in tks:
        if b['id'] == the_id:
            tk = ToDo(
                the_id, 
                task 
            )
            print('new task: ', tk.serialize())
            db.update(tk)
            new_tks = [b.serialize() for b in db.view()]
            print('task : ', new_tks)
            return jsonify({
                # 'error': '',
                'res': tk.serialize(),
                'status': '200',
                'msg': f'Success updating the task!👍😀'
            })        
    return jsonify({
                # 'error': '',
                'res': f'Error ⛔❌! Failed to update task!',
                'status': '404'
            })
    
    


@app.route('/request/<id>', methods=['DELETE'])
def deleteRequest(id):
    req_args = request.view_args
    print('req_args: ', req_args)
    tks = [b.serialize() for b in db.view()]
    if req_args:
        for b in tks:
            if b['id'] == int(req_args['id']):
                db.delete(b['id'])
                updated_tks = [b.serialize() for b in db.view()]
                print('updated_tks: ', updated_tks)
                return jsonify({
                    'res': updated_tks,
                    'status': '200',
                    'msg': 'Success deleting task by ID!👍😀',
                    'no_of_tasks': len(updated_tks)
                })
    else:
        return jsonify({
            'error': f"Error ⛔❌! No task ID sent!",
            'res': '',
            'status': '404'
        })







if __name__ == '__main__':
	app.run()
