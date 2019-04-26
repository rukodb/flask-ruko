from flask import Flask, request
from flask_restplus import Api, Resource
from uuid import uuid4

from flask_ruko import RukoDB

app = Flask(__name__)
api = Api(app)
db = RukoDB(app)

notes = db['notes']


@api.route('/todo')
class TodoRoute(Resource):
    def get(self):
        return notes.get()

    def post(self):
        data = request.get_json()
        todo = {
            'uuid': str(uuid4()),
            'title': data['title'],
            'description': data['description'],
            'done': False
        }
        notes.append(todo)
        return todo


@api.route('/todo/<uuid>')
class TodoItemRoute(Resource):
    def get(self, uuid):
        return notes.by('uuid')[uuid].get()

    def patch(self, uuid):
        data = request.get_json()
        note = notes.by('uuid')[uuid]
        note.update(data)
        return note()

    def delete(self, uuid):
        del notes.by('uuid')[uuid]


@api.route('/todo/<uuid>/done')
class TodoDoneRoute(Resource):
    def post(self, uuid):
        note = notes.by('uuid')[uuid]
        note['done'] = True
        return note()


if __name__ == '__main__':
    app.run()
