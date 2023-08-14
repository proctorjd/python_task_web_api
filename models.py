
class ToDo:
	def __init__(self, id, task):
		self.id = id
		self.task = task

	def __repr__(self):
		return '<id {}>'.format(self.id)

	def serialize(self):
		return {
			'id': self.id,
			'task': self.task
		}
