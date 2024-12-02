from TaskSystem import TaskDatabase, TaskNode

db = TaskDatabase()
t1 = db.add_node("task 1")
t2 = db.add_node("task 2")
t3 = db.add_node("task 3")

t3.add_connections(t2)
t2.add_connections(t3)

print(db)