from flask_restful import Resource

# Sample data
todos = {
    1: {'task': 'Learn Python'},
    2: {'task': 'Build an API'},
    3: {'task': 'Deploy to production'},
}
class TodoResource(Resource):
    def get(self, todo_id):
        if todo_id in todos:
            return todos[todo_id]
        else:
            return {'error': 'Todo not found'}, 404

    def put(self, todo_id):
        todos[todo_id] = {'task': 'Updated task'}
        return todos[todo_id]

    def delete(self, todo_id):
        del todos[todo_id]
        return {'result': 'Todo deleted'}
