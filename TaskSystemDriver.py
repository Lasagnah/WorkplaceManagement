from TaskSystem import TaskDatabase, TaskNode

db = TaskDatabase()
t1 = db.add_node("task 1")
t2 = db.add_node("task 2")
t3 = db.add_node("task 3")
t4 = db.add_node("task 4")

t1.add_connections(t2)
t2.add_connections(t3)
# Circular connection (1-2-3-1)
t3.add_connections(t1)

print(db.detect_cycle())

print(db)