import sqlite3, random, datetime
from models import ToDo

def getNewId():
	return random.getrandbits(28)

todo = [
	{
		'task': 'test code'
	}
]

def connect():
    conn = sqlite3.connect('todos.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS todos (id INTEGER PRIMARY KEY, task TEXT)")
    conn.commit()
    conn.close()
    for i in todo:
        tl = ToDo(getNewId(), i['task'])
        insert(tl)

def insert(task):
    conn = sqlite3.connect('todos.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO todos VALUES (?,?)", (
        task.id,
        task.task,
    ))
    conn.commit()
    conn.close()

def view():
    conn = sqlite3.connect('todos.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM todos")
    rows = cur.fetchall()
    tasks = []
    for i in rows:
        task = ToDo(i[0], i[1])
        tasks.append(task)
    conn.close()
    return tasks

def update(task):
    conn = sqlite3.connect('todos.db')
    cur = conn.cursor()
    cur.execute("UPDATE todos SET task=? WHERE id=?", (task.task, task.id))
    conn.commit()
    conn.close()

def delete(theId):
    conn = sqlite3.connect('todos.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM todos WHERE id=?", (theId,))
    conn.commit()
    conn.close()

def deleteAll():
    conn = sqlite3.connect('todos.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM todos")
    conn.commit()
    conn.close()
