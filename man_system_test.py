import tkinter as tk
from tkinter import ttk, messagebox
import datetime

# ================= Budget Management Code =================
class BudgetNode:
    def __init__(self, category, limit=None):
        self.category = category
        self.limit = limit
        self.expenses = 0
        self.children = []

    def add_expense(self, amount):
        if self.limit and self.expenses + amount > self.limit:
            print(f"Warning: Budget exceeded for {self.category}")
        self.expenses += amount
        self.update_parent_expenses()

    def add_child(self, child_node):
        self.children.append(child_node)

    def get_categories(self, level=0):
        result = [("  " * level + f"{self.category}: Spent {self.expenses}, Limit {self.limit}")]
        for child in self.children:
            result.extend(child.get_categories(level + 1))
        return result

    def update_parent_expenses(self):
        if self.parent:  # Update parent's expense when a child is updated
            self.parent.update_expenses()

    def update_expenses(self):
        total_expenses = sum(child.expenses for child in self.children)
        self.expenses = total_expenses

class BudgetTree:
    def __init__(self):
        self.root = BudgetNode("Company Budget")
        self.root.parent = None  # Root has no parent
        self.limits = {
            "Food": 500,
            "Groceries": 300,
            "Restaurants": 200,
            "Travel": 1000,
            "Entertainment": 400
        }

    def add_category(self, parent_category, category, limit=None):
        # Default to root if parent_category is not specified
        parent_node = self.root if not parent_category else self.search(self.root, parent_category)
        if parent_node:
            if category in self.limits:
                limit = self.limits[category]
            new_category = BudgetNode(category, limit)
            new_category.parent = parent_node  # Set parent
            parent_node.add_child(new_category)
            print(f"Category '{category}' added under '{parent_category or 'Company Budget'}' with limit {limit}.")
        else:
            print(f"Parent category '{parent_category}' not found.")

    def add_expense(self, category, amount):
        category_node = self.search(self.root, category)
        if category_node and category_node != self.root:  # Prevent expense on root
            category_node.add_expense(amount)
        else:
            print(f"Cannot add expense to the root node or non-existent category: {category}")

    def search(self, node, category):
        if node.category == category:
            return node
        for child in node.children:
            found = self.search(child, category)
            if found:
                return found
        return None

# ================= File Management Code =================
class FileNode:
    def __init__(self, name, size=0):
        self.name = name
        self.size = size
        self.creation_date = datetime.datetime.now()
        self.parent = None

class FolderNode:
    def __init__(self, name):
        self.name = name
        self.subfolders = []
        self.files = []
        self.parent = None

    def add_folder(self, folder):
        folder.parent = self
        self.subfolders.append(folder)

    def add_file(self, file):
        file.parent = self
        self.files.append(file)

    def list_contents(self):
        folder_names = [folder.name for folder in self.subfolders]
        file_names = [file.name for file in self.files]
        return folder_names, file_names

class FileManager:
    def __init__(self):
        self.root = FolderNode("root")

    def create_folder(self, folder_name, parent_folder=None):
        parent = self.root if parent_folder is None else parent_folder
        new_folder = FolderNode(folder_name)
        parent.add_folder(new_folder)
        return new_folder

# ================= Task Management Code =================
class Task:
    def __init__(self, task_id, description, deadline, priority):
        self.task_id = task_id
        self.description = description
        self.deadline = deadline
        self.priority = priority
        self.status = "Pending"

class TaskGraph:
    def __init__(self):
        self.tasks = {}

    def add_task(self, task):
        self.tasks[task.task_id] = task

# ================= Unified Application UI =================
class ManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Integrated Management System")
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill="both")

        # Budget Management
        self.budget_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.budget_tab, text="Budget Management")
        self.budget_tree = BudgetTree()
        self.setup_budget_tab()

        # File Management
        self.file_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.file_tab, text="File Management")
        self.file_manager = FileManager()
        self.setup_file_tab()

        # Task Management
        self.task_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.task_tab, text="Task Management")
        self.task_graph = TaskGraph()
        self.setup_task_tab()

    def setup_budget_tab(self):
        ttk.Label(self.budget_tab, text="Budget Management", font=("Arial", 16)).pack(pady=10)

        frame = ttk.Frame(self.budget_tab)
        frame.pack(pady=5)

        ttk.Label(frame, text="Parent Category:").grid(row=0, column=0, padx=5, pady=5)
        self.budget_parent_category_entry = ttk.Entry(frame)
        self.budget_parent_category_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Category Name:").grid(row=1, column=0, padx=5, pady=5)
        self.budget_category_entry = ttk.Entry(frame)
        self.budget_category_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Limit:").grid(row=2, column=0, padx=5, pady=5)
        self.budget_limit_entry = ttk.Entry(frame)
        self.budget_limit_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(frame, text="Add Category", command=self.add_budget_category).grid(row=3, columnspan=3, pady=5)

        # Expense input fields
        ttk.Label(self.budget_tab, text="Enter Expense", font=("Arial", 12)).pack(pady=10)

        expense_frame = ttk.Frame(self.budget_tab)
        expense_frame.pack(pady=5)

        ttk.Label(expense_frame, text="Category:").grid(row=0, column=0, padx=5, pady=5)
        self.budget_expense_category_combobox = ttk.Combobox(expense_frame, state="readonly")
        self.budget_expense_category_combobox.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(expense_frame, text="Amount:").grid(row=1, column=0, padx=5, pady=5)
        self.budget_expense_amount_entry = ttk.Entry(expense_frame)
        self.budget_expense_amount_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(expense_frame, text="Add Expense", command=self.add_expense).grid(row=2, columnspan=3, pady=5)

        # Treeview for hierarchical structure
        self.budget_tree_view = ttk.Treeview(self.budget_tab)
        self.budget_tree_view.pack(pady=10, expand=True, fill="both")
        self.refresh_budget_display()

    def add_budget_category(self):
        parent_category = self.budget_parent_category_entry.get().strip()
        category_name = self.budget_category_entry.get().strip()
        limit = self.budget_limit_entry.get().strip()

        # Validate limit
        try:
            limit = float(limit) if limit else None
            if limit and limit <= 0:
                raise ValueError("Limit must be greater than zero.")
        except ValueError:
            messagebox.showerror("Error", "Invalid limit value.")
            return

        if category_name:
            # If parent category is not specified, default to "Company Budget"
            parent_category = parent_category or "Company Budget"
            self.budget_tree.add_category(parent_category, category_name, limit)
            self.refresh_budget_display()
            messagebox.showinfo("Success", f"Category '{category_name}' added under '{parent_category}' with limit {limit}.")
        else:
            messagebox.showerror("Error", "Category name is required.")

    def add_expense(self):
        category = self.budget_expense_category_combobox.get().strip()
        amount = self.budget_expense_amount_entry.get().strip()

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Expense amount must be greater than zero.")
        except ValueError:
            messagebox.showerror("Error", "Invalid expense amount.")
            return

        if category and category != "Company Budget":
            self.budget_tree.add_expense(category, amount)
            self.refresh_budget_display()
            messagebox.showinfo("Success", f"Expense of {amount} added to '{category}'.")
        else:
            messagebox.showerror("Error", "Cannot add expense to the root node.")

    def refresh_budget_display(self):
        # Clear previous content in the Treeview
        for item in self.budget_tree_view.get_children():
            self.budget_tree_view.delete(item)

        # Add updated budget categories into the Treeview
        self.add_budget_to_tree(self.budget_tree.root)

        # Update the category combobox for expense entry
        categories = [node.category for node in self.get_all_categories(self.budget_tree.root)]
        # Exclude the root category from the dropdown
        categories = [cat for cat in categories if cat != "Company Budget"]
        self.budget_expense_category_combobox['values'] = categories

    def add_budget_to_tree(self, node, parent=""):
        # Insert the current category node into the Treeview
        limit_text = f"Limit {node.limit}" if node.limit is not None else "No limit"
        node_id = self.budget_tree_view.insert(parent, "end", text=f"{node.category}: Spent {node.expenses}, {limit_text}", open=True)

        # Recursively insert child categories
        for child in node.children:
            self.add_budget_to_tree(child, node_id)

    def get_all_categories(self, node):
        categories = [node]
        for child in node.children:
            categories.extend(self.get_all_categories(child))
        return categories

    def setup_file_tab(self):
        ttk.Label(self.file_tab, text="File Management", font=("Arial", 16)).pack(pady=10)

        frame = ttk.Frame(self.file_tab)
        frame.pack(pady=5)

        ttk.Label(frame, text="Folder Name:").grid(row=0, column=0, padx=5, pady=5)
        self.file_folder_entry = ttk.Entry(frame)
        self.file_folder_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Button(frame, text="Create Folder", command=self.create_folder).grid(row=0, column=2, padx=5, pady=5)

        # Treeview for folder structure
        self.file_tree_view = ttk.Treeview(self.file_tab)
        self.file_tree_view.pack(pady=10, expand=True, fill="both")
        self.refresh_file_display()

    def create_folder(self):
        folder_name = self.file_folder_entry.get().strip()
        if folder_name:
            self.file_manager.create_folder(folder_name)
            self.refresh_file_display()
            messagebox.showinfo("Success", f"Folder '{folder_name}' created.")
        else:
            messagebox.showerror("Error", "Folder name cannot be empty.")

    def refresh_file_display(self):
        # Clear previous content in the Treeview
        for item in self.file_tree_view.get_children():
            self.file_tree_view.delete(item)

        # Add folders into the Treeview
        self.add_folders_to_tree(self.file_manager.root)

    def add_folders_to_tree(self, folder, parent=""):
        # Insert the current folder node into the Treeview
        folder_id = self.file_tree_view.insert(parent, "end", text=folder.name, open=True)

        # Recursively insert subfolders
        for subfolder in folder.subfolders:
            self.add_folders_to_tree(subfolder, folder_id)

        # Insert files into the folder
        for file in folder.files:
            self.file_tree_view.insert(folder_id, "end", text=f"{file.name} - {file.size} bytes")

    def setup_task_tab(self):
        ttk.Label(self.task_tab, text="Task Management", font=("Arial", 16)).pack(pady=10)

        frame = ttk.Frame(self.task_tab)
        frame.pack(pady=5)

        ttk.Label(frame, text="Task Description:").grid(row=0, column=0, padx=5, pady=5)
        self.task_description_entry = ttk.Entry(frame)
        self.task_description_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Priority (High/Medium/Low):").grid(row=1, column=0, padx=5, pady=5)
        self.task_priority_combobox = ttk.Combobox(frame, state="readonly", values=["High", "Medium", "Low"])
        self.task_priority_combobox.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Deadline (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=5)
        self.task_deadline_entry = ttk.Entry(frame)
        self.task_deadline_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(frame, text="Add Task", command=self.add_task).grid(row=3, columnspan=3, pady=5)

        # Treeview for tasks
        self.task_tree_view = ttk.Treeview(self.task_tab)
        self.task_tree_view.pack(pady=10, expand=True, fill="both")
        self.refresh_task_display()

    def add_task(self):
        task_description = self.task_description_entry.get().strip()
        task_priority = self.task_priority_combobox.get()
        task_deadline = self.task_deadline_entry.get().strip()

        if not task_description or not task_priority or not task_deadline:
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            task_deadline = datetime.datetime.strptime(task_deadline, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD.")
            return

        task_id = len(self.task_graph.tasks) + 1
        task = Task(task_id, task_description, task_deadline, task_priority)
        self.task_graph.add_task(task)
        self.refresh_task_display()
        messagebox.showinfo("Success", f"Task '{task_description}' added.")

    def refresh_task_display(self):
        # Clear previous content in the Treeview
        for item in self.task_tree_view.get_children():
            self.task_tree_view.delete(item)

        # Add tasks into the Treeview
        for task in self.task_graph.tasks.values():
            self.task_tree_view.insert("", "end", text=f"Task {task.task_id}: {task.description} - Status: {task.status}")

# ================= Main Program =================
def run_application():
    root = tk.Tk()
    app = ManagementApp(root)
    root.mainloop()

# Run the app
run_application()
