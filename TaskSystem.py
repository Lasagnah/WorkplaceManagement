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
    
    def detect_cycle(self):
        # We want to be able to detect cycles because it can be problematic when one thing 
        # is dependent upon another thing being finished, which is dependent upon that first thing being finished
        def dfs(node, visited, recursion_stack):
                if node in recursion_stack:
                    # A cycle is detected
                    return True
                if node in visited:
                    # Node already fully processed
                    return False

                # Mark the node as visited and add it to the recursion stack
                visited.add(node)
                recursion_stack.add(node)

                # Recur for all connected nodes
                for neighbor in node.connections:
                    if dfs(neighbor, visited, recursion_stack):
                        return True

                # Remove the node from the recursion stack
                recursion_stack.remove(node)
                return False

        visited = set()
        recursion_stack = set()

        # Perform DFS for each unvisited node
        for task in self.tasks:
            if task not in visited:
                if dfs(task, visited, recursion_stack):
                    return True

        return False


class TaskNode(Node):
    def __init__(self, data):
        super().__init__(data)
        self.connections = []
    
    def add_connections(self, Node):
        self.connections.append(Node)

    def __repr__(self):
        return f"Task({self.data}), Dependent Upon {len(self.connections)} other tasks"
