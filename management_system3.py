import tkinter as tk  # Import tkinter for creating the GUI
from tkinter import ttk, messagebox  # Import additional Tkinter modules for styling and displaying message boxes
import datetime  # Import datetime module for handling date inputs

# Task Class
class Task:
    def __init__(self, task_id, description, deadline, priority):
        self.task_id = task_id  # Unique identifier for the task
        self.description = description  # Description of the task
        self.deadline = deadline  # Deadline for the task (date)
        self.priority = priority  # Priority of the task (e.g., Low, Medium, High)
        self.status = "Pending"  # Default status of a task is "Pending"

# TaskGraph Class to represent the task dependencies as a graph
class TaskGraph:
    def __init__(self):
        self.tasks = {}  # Dictionary to store tasks by task_id
        self.edges = []  # List to store edges representing task dependencies

    def add_task(self, task):
        if task.task_id in self.tasks:  # Check if the task ID already exists
            raise ValueError("Task ID already exists.")  # Raise an error if task ID is duplicate
        self.tasks[task.task_id] = task  # Add the task to the dictionary

    def add_edge(self, from_task, to_task):
        if from_task not in self.tasks or to_task not in self.tasks:
            raise ValueError("Both tasks must exist to create an edge.")  # Ensure both tasks exist before adding an edge
        self.edges.append((from_task, to_task))  # Add the edge (dependency) to the list

# BudgetTree Class to represent the budget as a hierarchical tree structure
class BudgetTree:
    def __init__(self):
        self.root = self.Node("Company Budget", limit=0, expense=0)  # Create the root node (Company Budget)

    # Node class to represent each category in the budget tree
    class Node:
        def __init__(self, category, limit=0, expense=0):
            self.category = category  # Name of the budget category
            self.limit = limit  # Limit for this category
            self.expense = expense  # Expense for this category
            self.children = []  # Children categories (subcategories)

    # Method to add a new category (node) to the tree
    def add_node(self, parent_category, category, limit=0, expense=0):
        def find_node(node, category):
            if node.category == category:  # Search for the node by category name
                return node
            for child in node.children:  # Recursively check child nodes
                found = find_node(child, category)
                if found:
                    return found
            return None

        parent_node = find_node(self.root, parent_category) if parent_category else self.root  # Find parent node
        if not parent_node:
            raise ValueError("Parent category does not exist.")  # Raise error if parent category is not found

        new_node = self.Node(category, limit, expense)  # Create new node (subcategory)
        parent_node.children.append(new_node)  # Add the new node as a child of the parent node

    # Method to calculate the total expense recursively for a node and its children
    def calculate_total(self, node):
        total_expense = node.expense  # Start with the node's own expense
        for child in node.children:  # Add expense of all child nodes recursively
            total_expense += self.calculate_total(child)
        return total_expense

# FileManager Class to manage file structure as a tree
class FileManager:
    def __init__(self):
        self.files = {}  # Dictionary to store files and directories by name

    # Node class to represent each file or directory in the file structure
    class Node:
        def __init__(self, name):
            self.name = name  # Name of the file or directory
            self.children = []  # List of child files or directories

    # Method to add a new file or directory (node) under a parent
    def add_node(self, parent_name, child_name):
        if parent_name not in self.files:  # Create parent node if it doesn't exist
            self.files[parent_name] = self.Node(parent_name)
        parent_node = self.files[parent_name]  # Get the parent node

        if child_name not in self.files:  # Create child node if it doesn't exist
            child_node = self.Node(child_name)
            self.files[child_name] = child_node
            parent_node.children.append(child_node)  # Add the child node to the parent's children

# ManagementApp Class for the main application interface
class ManagementApp:
    def __init__(self, root):
        self.root = root  # Root window for the Tkinter app
        self.root.title("Integrated Management System")  # Set the title of the window
        self.notebook = ttk.Notebook(root)  # Create a notebook widget to hold the tabs
        self.notebook.pack(expand=True, fill="both")  # Add the notebook to the window

        # Budget Management Tab
        self.budget_tab = ttk.Frame(self.notebook)  # Create a frame for the budget tab
        self.notebook.add(self.budget_tab, text="Budget Management")  # Add the frame as a tab in the notebook
        self.budget_tree = BudgetTree()  # Create a BudgetTree object
        self.setup_budget_tab()  # Setup the UI for the budget tab

        # File Management Tab
        self.file_tab = ttk.Frame(self.notebook)  # Create a frame for the file tab
        self.notebook.add(self.file_tab, text="File Management")  # Add the frame as a tab in the notebook
        self.file_manager = FileManager()  # Create a FileManager object
        self.setup_file_tab()  # Setup the UI for the file tab

        # Task Management Tab
        self.task_tab = ttk.Frame(self.notebook)  # Create a frame for the task tab
        self.notebook.add(self.task_tab, text="Task Management")  # Add the frame as a tab in the notebook
        self.task_graph = TaskGraph()  # Create a TaskGraph object
        self.setup_task_tab()  # Setup the UI for the task tab

    # Method to setup the Budget Management Tab UI
    def setup_budget_tab(self):
        ttk.Label(self.budget_tab, text="Budget Management", font=("Arial", 16)).pack(pady=10)  # Tab title

        frame = ttk.Frame(self.budget_tab)  # Create a frame for the budget input fields
        frame.pack(pady=5)

        # Label and entry field for the parent category
        ttk.Label(frame, text="Parent Category:").grid(row=0, column=0, padx=5, pady=5)
        self.budget_parent_entry = ttk.Entry(frame)  # Entry widget to input parent category
        self.budget_parent_entry.grid(row=0, column=1, padx=5, pady=5)

        # Label and entry field for the new category
        ttk.Label(frame, text="Category:").grid(row=1, column=0, padx=5, pady=5)
        self.budget_category_entry = ttk.Entry(frame)  # Entry widget to input new category name
        self.budget_category_entry.grid(row=1, column=1, padx=5, pady=5)

        # Label and entry field for the limit of the category
        ttk.Label(frame, text="Limit:").grid(row=2, column=0, padx=5, pady=5)
        self.budget_limit_entry = ttk.Entry(frame)  # Entry widget to input limit value
        self.budget_limit_entry.grid(row=2, column=1, padx=5, pady=5)

        # Label and entry field for the expense of the category
        ttk.Label(frame, text="Expense:").grid(row=3, column=0, padx=5, pady=5)
        self.budget_expense_entry = ttk.Entry(frame)  # Entry widget to input expense value
        self.budget_expense_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Button(frame, text="Add Entry", command=self.add_budget_entry).grid(row=4, columnspan=2, pady=5)  # Add Entry button

        self.budget_tree_view = ttk.Treeview(self.budget_tab)  # Treeview widget to display the budget hierarchy
        self.budget_tree_view.pack(pady=10, fill="both", expand=True)

        self.budget_total_label = ttk.Label(self.budget_tab, text="Total Expense: $0", font=("Arial", 12))  # Label for total expense
        self.budget_total_label.pack(pady=5)

    # Method to add a budget entry
    def add_budget_entry(self):
        parent_category = self.budget_parent_entry.get().strip()  # Get parent category from entry field
        category = self.budget_category_entry.get().strip()  # Get new category from entry field
        limit_str = self.budget_limit_entry.get().strip()  # Get limit from entry field
        expense_str = self.budget_expense_entry.get().strip()  # Get expense from entry field

        if not category:  # Check if category is specified
            messagebox.showerror("Error", "Category must be specified.")  # Show error message if not
            return

        try:
            limit = float(limit_str) if limit_str else 1000  # Set default limit if not specified
            expense = float(expense_str) if expense_str else 0  # Set default expense if not specified
        except ValueError:
            messagebox.showerror("Error", "Limit and Expense must be numbers.")  # Show error if values are not valid numbers
            return

        try:
            self.budget_tree.add_node(parent_category, category, limit, expense)  # Add the budget entry to the tree
        except ValueError as e:
            messagebox.showerror("Error", str(e))  # Show error if parent category is not found
            return

        self.refresh_budget_tree()  # Refresh the treeview to display the updated budget tree

    # Method to refresh the budget tree view
    def refresh_budget_tree(self):
        self.budget_tree_view.delete(*self.budget_tree_view.get_children())  # Clear the current tree view

        def populate_budget_tree(node, parent_id):
            total_expense = self.budget_tree.calculate_total(node)  # Calculate total expense for the node and children
            node_id = self.budget_tree_view.insert(parent_id, "end", text=f"{node.category} (Limit: $ {node.limit}, Expense: $ {total_expense})")  # Add node to treeview
            for child in node.children:  # Recursively populate child nodes
                populate_budget_tree(child, node_id)

        if self.budget_tree.root:
            root_id = self.budget_tree_view.insert("", "end", text=f"{self.budget_tree.root.category} (Limit: $ {self.budget_tree.root.limit}, Expense: $ {self.budget_tree.calculate_total(self.budget_tree.root)})")
            for child in self.budget_tree.root.children:
                populate_budget_tree(child, root_id)

        # Update total expense label
        total = self.budget_tree.calculate_total(self.budget_tree.root) if self.budget_tree.root else 0
        self.budget_total_label.config(text=f"Total Expense: $ {total}")

# The rest of the code continues similarly...
    # Method to setup the File Management Tab UI

    # Label and entry field for the parent directory
    def setup_file_tab(self):
        ttk.Label(self.file_tab, text="File Management", font=("Arial", 16)).pack(pady=10)

        frame = ttk.Frame(self.file_tab)
        frame.pack(pady=5)

        ttk.Label(frame, text="Parent Node:").grid(row=0, column=0, padx=5, pady=5)
        self.parent_entry = ttk.Entry(frame)
        self.parent_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Child Node:").grid(row=1, column=0, padx=5, pady=5)
        self.child_entry = ttk.Entry(frame)
        self.child_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(frame, text="Add Node", command=self.add_file_node).grid(row=2, columnspan=2, pady=5)

        self.tree_view = ttk.Treeview(self.file_tab)
        self.tree_view.pack(pady=10, fill="both", expand=True)

    def add_file_node(self):
        parent_name = self.parent_entry.get().strip()
        child_name = self.child_entry.get().strip()

        if not parent_name or not child_name:
            messagebox.showerror("Error", "Both parent and child nodes must be specified.")
            return

        self.file_manager.add_node(parent_name, child_name)
        self.refresh_file_tree()

    def refresh_file_tree(self):
        # Clear the current tree
        self.tree_view.delete(*self.tree_view.get_children())

        def populate_tree(parent_node, parent_id):
            for child in parent_node.children:
                child_id = self.tree_view.insert(parent_id, "end", text=child.name)
                populate_tree(child, child_id)

        for root_name, root_node in self.file_manager.files.items():
            if not any(root_name in child.name for node in self.file_manager.files.values() for child in node.children):
                root_id = self.tree_view.insert("", "end", text=root_name)
                populate_tree(root_node, root_id)

    def setup_task_tab(self):
        ttk.Label(self.task_tab, text="Task Management", font=("Arial", 16)).pack(pady=10)

        frame = ttk.Frame(self.task_tab)
        frame.pack(pady=5)

        ttk.Label(frame, text="Task ID:").grid(row=0, column=0, padx=5, pady=5)
        self.task_id_entry = ttk.Entry(frame)
        self.task_id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Description:").grid(row=1, column=0, padx=5, pady=5)
        self.task_description_entry = ttk.Entry(frame)
        self.task_description_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Deadline (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5)
        self.task_deadline_entry = ttk.Entry(frame)
        self.task_deadline_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Priority:").grid(row=3, column=0, padx=5, pady=5)
        self.task_priority_combobox = ttk.Combobox(frame, state="readonly", values=["Low", "Medium", "High"])
        self.task_priority_combobox.grid(row=3, column=1, padx=5, pady=5)

        ttk.Button(frame, text="Add Task", command=self.add_task).grid(row=4, columnspan=3, pady=5)

        ttk.Label(frame, text="From Task ID:").grid(row=5, column=0, padx=5, pady=5)
        self.from_task_entry = ttk.Entry(frame)
        self.from_task_entry.grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(frame, text="To Task ID:").grid(row=6, column=0, padx=5, pady=5)
        self.to_task_entry = ttk.Entry(frame)
        self.to_task_entry.grid(row=6, column=1, padx=5, pady=5)

        ttk.Button(frame, text="Add Edge", command=self.add_edge).grid(row=7, columnspan=3, pady=5)

        # Display area for the task graph
        self.task_graph_view = ttk.Treeview(self.task_tab)
        self.task_graph_view.pack(pady=10, fill="both", expand=True)

    # Method to add a task entry
    def add_task(self):
        task_id = self.task_id_entry.get().strip()
        description = self.task_description_entry.get().strip()
        deadline_str = self.task_deadline_entry.get().strip()
        priority = self.task_priority_combobox.get().strip()

        if not task_id or not description or not deadline_str or not priority:
            messagebox.showerror("Error", "All task fields must be filled.")
            return

        try:
            deadline = datetime.datetime.strptime(deadline_str, "%Y-%m-%d").date()
        except ValueError:
            messagebox.showerror("Error", "Deadline must be in YYYY-MM-DD format.")
            return

        try:
            task = Task(task_id, description, deadline, priority)
            self.task_graph.add_task(task)
            self.refresh_task_graph()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def add_edge(self):
        from_task = self.from_task_entry.get().strip()
        to_task = self.to_task_entry.get().strip()

        if not from_task or not to_task:
            messagebox.showerror("Error", "Both 'From Task ID' and 'To Task ID' must be specified.")
            return

        try:
            self.task_graph.add_edge(from_task, to_task)
            self.refresh_task_graph()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def refresh_task_graph(self):
        # Clear the current tree
        self.task_graph_view.delete(*self.task_graph_view.get_children())

        def add_task_to_view(task_id, parent_id=""):
            task = self.task_graph.tasks[task_id]
            node_id = self.task_graph_view.insert(parent_id, "end", text=f"{task.task_id}: {task.description} (Priority: {task.priority}, Deadline: {task.deadline})")
            return node_id

        # Add tasks and edges
        task_ids = {}
        for task_id in self.task_graph.tasks:
            task_ids[task_id] = add_task_to_view(task_id)

        for from_task, to_task in self.task_graph.edges:
            if from_task in task_ids and to_task in task_ids:
                self.task_graph_view.move(task_ids[to_task], task_ids[from_task], "end")

# Main program to start the Tkinter application
if __name__ == "__main__":
    root = tk.Tk()  # Create the root Tkinter window
    app = ManagementApp(root) # Create the ManagementApp object with the root window
    root.mainloop()    # Start the Tkinter main event loop

