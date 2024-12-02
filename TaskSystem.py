from Node import Node

class TaskDatabase:
    def __init__(self):
        self.tasks = []

    def add_node(self, data):
        s = TaskNode(data)
        self.tasks.append(s)
        return s

    def __str__(self):
        return f"{self.tasks}"

class TaskNode(Node):
    def __init__(self, data):
        super().__init__(data)
        self.connections = []
    
    def add_connections(self, Node):
        self.connections.append(Node)

    def __repr__(self):
        return f"Task({self.data}), Dependent Upon {len(self.connections)} other tasks"
