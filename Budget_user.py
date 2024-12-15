import tkinter as tk
from tkinter import messagebox

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

    def add_child(self, child_node):
        self.children.append(child_node)

    def display_categories(self, level=0):
        # Display the category with its expenses and limit
        print("  " * level + f"{self.category}: Spent {self.expenses}, Limit {self.limit}")
        for child in self.children:
            child.display_categories(level + 1)  # Recursively display children

class BudgetTree:
    def __init__(self):
        self.root = BudgetNode("Company Budget")
        self.limits = {
            "Food": 500,
            "Groceries": 300,
            "Restaurants": 200,
            "Travel": 1000,
            "Entertainment": 400
        }

    def add_category(self, parent_category, category, limit=None):
        parent_node = self.search(self.root, parent_category)
        if parent_node:
            if category in self.limits:
                limit = self.limits[category]  # Predefined limit
            new_category = BudgetNode(category, limit)
            parent_node.add_child(new_category)
            print(f"Category '{category}' added under '{parent_category}' with limit {limit}.")
        else:
            print(f"Parent category '{parent_category}' not found.")

    def search(self, node, category):
        if node.category == category:
            return node
        for child in node.children:
            found = self.search(child, category)
            if found:
                return found
        return None

class BudgetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Budget Management System")

        self.budget = BudgetTree()

        self.frame = tk.Frame(root)
        self.frame.pack(pady=10)

        # Category input
        self.category_label = tk.Label(self.frame, text="Category Name:")
        self.category_label.grid(row=0, column=0, padx=5)

        self.category_entry = tk.Entry(self.frame)
        self.category_entry.grid(row=0, column=1, padx=5)

        # Subcategory input (new feature)
        self.parent_category_label = tk.Label(self.frame, text="Parent Category:")
        self.parent_category_label.grid(row=1, column=0, padx=5)

        self.parent_category_entry = tk.Entry(self.frame)
        self.parent_category_entry.grid(row=1, column=1, padx=5)

        # Limit input
        self.limit_label = tk.Label(self.frame, text="Limit (Leave blank for predefined):")
        self.limit_label.grid(row=2, column=0, padx=5)

        self.limit_entry = tk.Entry(self.frame)
        self.limit_entry.grid(row=2, column=1, padx=5)

        # Add category button
        self.add_category_button = tk.Button(self.frame, text="Add Category", command=self.add_category)
        self.add_category_button.grid(row=3, columnspan=2, pady=10)

        # Expense inputs
        self.expense_category_label = tk.Label(self.frame, text="Category for Expense:")
        self.expense_category_label.grid(row=4, column=0, padx=5)

        self.expense_category_entry = tk.Entry(self.frame)
        self.expense_category_entry.grid(row=4, column=1, padx=5)

        self.expense_amount_label = tk.Label(self.frame, text="Expense Amount:")
        self.expense_amount_label.grid(row=5, column=0, padx=5)

        self.expense_amount_entry = tk.Entry(self.frame)
        self.expense_amount_entry.grid(row=5, column=1, padx=5)

        # Add expense button
        self.add_expense_button = tk.Button(self.frame, text="Add Expense", command=self.add_expense)
        self.add_expense_button.grid(row=6, columnspan=2, pady=10)

        # Display button
        self.display_button = tk.Button(self.frame, text="Display Budget", command=self.display_budget)
        self.display_button.grid(row=7, columnspan=2, pady=10)

    def add_category(self):
        category_name = self.category_entry.get().strip()
        parent_category = self.parent_category_entry.get().strip()
        limit = self.limit_entry.get().strip()

        if not category_name:
            messagebox.showerror("Input Error", "Category name cannot be empty.")
            return

        if not parent_category:
            messagebox.showerror("Input Error", "Parent category is required.")
            return

        if category_name in self.budget.limits:
            self.budget.add_category(parent_category, category_name)  # Use predefined limit
            messagebox.showinfo("Success", f"Category '{category_name}' added under '{parent_category}' with predefined limit.")
        else:
            if not limit:
                messagebox.showerror("Input Error", f"Please enter a limit for '{category_name}'.")
                return

            try:
                limit = float(limit)
                self.budget.add_category(parent_category, category_name, limit)
                messagebox.showinfo("Success", f"Category '{category_name}' added under '{parent_category}' with limit {limit}.")
            except ValueError:
                messagebox.showerror("Input Error", "Please enter a valid number for the limit.")

        self.category_entry.delete(0, tk.END)
        self.parent_category_entry.delete(0, tk.END)
        self.limit_entry.delete(0, tk.END)

    def add_expense(self):
        category_name = self.expense_category_entry.get().strip()
        amount = self.expense_amount_entry.get().strip()

        if category_name and amount:
            try:
                amount = float(amount)
                node = self.budget.search(self.budget.root, category_name)
                if node:
                    node.add_expense(amount)
                    messagebox.showinfo("Success", f"Expense of {amount} added to '{category_name}'.")
                    self.expense_category_entry.delete(0, tk.END)
                    self.expense_amount_entry.delete(0, tk.END)
                else:
                    messagebox.showerror("Category Not Found", f"Category '{category_name}' not found.")
            except ValueError:
                messagebox.showerror("Input Error", "Please enter a valid amount.")
        else:
            messagebox.showerror("Input Error", "Both category and amount are required.")

    def display_budget(self):
        budget_overview = self.get_budget_overview(self.budget.root)
        messagebox.showinfo("Budget Overview", budget_overview)

    def get_budget_overview(self, node, level=0):
        overview = "  " * level + f"{node.category}: Spent {node.expenses}, Limit {node.limit}\n"
        for child in node.children:
            overview += self.get_budget_overview(child, level + 1)
        return overview

# Main Program
root = tk.Tk()
app = BudgetApp(root)
root.mainloop()
