import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from decimal import Decimal
import datetime


class SavingsBucketApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Savings Bucket Manager")
        self.root.state('zoomed')  # Open in full screen on macOS

        # Initialize data
        self.data_file = "savings_data.json"
        self.config_file = "savings_config.json"
        self.load_data()

        # Create main frames
        self.create_menu()
        self.setup_main_frame()
        self.show_dashboard()

    def create_menu(self):
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save", command=self.save_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)

        # Navigation menu
        nav_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="Navigation", menu=nav_menu)
        nav_menu.add_command(label="Dashboard", command=self.show_dashboard)
        nav_menu.add_command(label="Manage Categories",
                             command=self.show_category_manager)
        nav_menu.add_command(label="Make Deposit",
                             command=self.show_deposit_screen)
        nav_menu.add_command(label="Reallocate Funds",
                             command=self.show_reallocation_screen)

    def setup_main_frame(self):
        # Main content frame
        self.main_frame = ttk.Frame(self.root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

    def load_data(self):
        # Load saved data or create default structure
        try:
            with open(self.data_file, 'r') as f:
                self.savings_data = json.load(f)
        except FileNotFoundError:
            self.savings_data = {
                "total_balance": 0,
                "buckets": {},
                "transactions": []
            }

        try:
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            self.config = {
                "allocations": {}
            }

    def save_data(self):
        with open(self.data_file, 'w') as f:
            json.dump(self.savings_data, f, indent=2)

        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)

        messagebox.showinfo("Success", "Data saved successfully")

    def clear_main_frame(self):
        # Remove all widgets from main frame
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # Dashboard screen
    def show_dashboard(self):
        self.clear_main_frame()

        # Header
        header = ttk.Label(self.main_frame, text="Savings Dashboard",
                           font=("Arial", 24, "bold"))
        header.pack(pady=20)

        # Total balance
        total_frame = ttk.Frame(self.main_frame)
        total_frame.pack(fill=tk.X, pady=10)

        ttk.Label(total_frame, text="Total Balance:",
                  font=("Arial", 16)).pack(side=tk.LEFT, padx=10)
        ttk.Label(total_frame, text=f"${self.savings_data['total_balance']:,.2f}",
                  font=("Arial", 16, "bold")).pack(side=tk.LEFT)

        # Buckets display
        bucket_frame = ttk.Frame(self.main_frame)
        bucket_frame.pack(fill=tk.BOTH, expand=True, pady=20)

        # Column headers
        ttk.Label(bucket_frame, text="Category", font=("Arial", 14, "bold")).grid(
            row=0, column=0, padx=10, pady=5, sticky="w")
        ttk.Label(bucket_frame, text="Balance", font=("Arial", 14, "bold")).grid(
            row=0, column=1, padx=10, pady=5, sticky="w")
        ttk.Label(bucket_frame, text="Allocation %", font=("Arial", 14, "bold")).grid(
            row=0, column=2, padx=10, pady=5, sticky="w")

        # List buckets
        row = 1
        for bucket, amount in self.savings_data["buckets"].items():
            ttk.Label(bucket_frame, text=bucket, font=("Arial", 12)).grid(
                row=row, column=0, padx=10, pady=5, sticky="w")
            ttk.Label(bucket_frame, text=f"${float(amount):,.2f}",
                      font=("Arial", 12)).grid(
                row=row, column=1, padx=10, pady=5, sticky="w")

            allocation = self.config["allocations"].get(bucket, 0)
            ttk.Label(bucket_frame, text=f"{allocation}%",
                      font=("Arial", 12)).grid(
                row=row, column=2, padx=10, pady=5, sticky="w")

            row += 1

        # Action buttons
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=20)

        ttk.Button(button_frame, text="Make Deposit",
                   command=self.show_deposit_screen).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Manage Categories",
                   command=self.show_category_manager).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Reallocate Funds",
                   command=self.show_reallocation_screen).pack(side=tk.LEFT, padx=10)

    # Category management screen
    def show_category_manager(self):
        self.clear_main_frame()

        # Header
        header = ttk.Label(self.main_frame, text="Manage Categories",
                           font=("Arial", 24, "bold"))
        header.pack(pady=20)

        # Current categories
        categories_frame = ttk.LabelFrame(
            self.main_frame, text="Current Categories")
        categories_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Column headers
        ttk.Label(categories_frame, text="Category",
                  font=("Arial", 12, "bold")).grid(
            row=0, column=0, padx=10, pady=5, sticky="w")
        ttk.Label(categories_frame, text="Allocation %",
                  font=("Arial", 12, "bold")).grid(
            row=0, column=1, padx=10, pady=5, sticky="w")
        ttk.Label(categories_frame, text="Actions",
                  font=("Arial", 12, "bold")).grid(
            row=0, column=2, padx=10, pady=5, sticky="w")

        # List categories
        self.allocation_vars = {}
        row = 1
        for bucket in self.savings_data["buckets"]:
            ttk.Label(categories_frame, text=bucket).grid(
                row=row, column=0, padx=10, pady=5, sticky="w")

            allocation_var = tk.StringVar(
                value=str(self.config["allocations"].get(bucket, 0)))
            self.allocation_vars[bucket] = allocation_var
            allocation_entry = ttk.Entry(
                categories_frame, textvariable=allocation_var, width=10)
            allocation_entry.grid(
                row=row, column=1, padx=10, pady=5, sticky="w")

            ttk.Button(categories_frame, text="Delete",
                       command=lambda b=bucket: self.delete_category(b)).grid(
                row=row, column=2, padx=10, pady=5)

            row += 1

        # New category section
        new_category_frame = ttk.LabelFrame(
            self.main_frame, text="Add New Category")
        new_category_frame.pack(fill=tk.X, padx=20, pady=10)

        ttk.Label(new_category_frame, text="Name:").grid(
            row=0, column=0, padx=10, pady=10, sticky="w")
        self.new_category_var = tk.StringVar()
        ttk.Entry(new_category_frame, textvariable=self.new_category_var, width=20).grid(
            row=0, column=1, padx=10, pady=10, sticky="w")

        ttk.Label(new_category_frame, text="Allocation %:").grid(
            row=0, column=2, padx=10, pady=10, sticky="w")
        self.new_allocation_var = tk.StringVar(value="0")
        ttk.Entry(new_category_frame, textvariable=self.new_allocation_var, width=10).grid(
            row=0, column=3, padx=10, pady=10, sticky="w")

        ttk.Button(new_category_frame, text="Add Category",
                   command=self.add_category).grid(
            row=0, column=4, padx=10, pady=10)

        # Action buttons
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=20)

        ttk.Button(button_frame, text="Save Allocations",
                   command=self.save_allocations).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Back to Dashboard",
                   command=self.show_dashboard).pack(side=tk.LEFT, padx=10)

    def add_category(self):
        name = self.new_category_var.get().strip()
        try:
            allocation = float(self.new_allocation_var.get())
            if name and allocation >= 0:
                if name in self.savings_data["buckets"]:
                    messagebox.showerror("Error", f"Category '{
                                         name}' already exists")
                    return

                self.savings_data["buckets"][name] = 0
                self.config["allocations"][name] = allocation
                self.save_data()
                self.show_category_manager()  # Refresh the screen
            else:
                messagebox.showerror(
                    "Error", "Please enter a valid name and allocation")
        except ValueError:
            messagebox.showerror("Error", "Allocation must be a number")

    def delete_category(self, bucket):
        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete '{
                bucket}'? Any funds will be unallocated."
        )
        if confirm:
            if bucket in self.savings_data["buckets"]:
                # Add the funds back to total (they'll be reallocated on next deposit)
                self.savings_data["buckets"].pop(bucket)
                if bucket in self.config["allocations"]:
                    self.config["allocations"].pop(bucket)

                self.save_data()
                self.show_category_manager()  # Refresh the screen

    def save_allocations(self):
        # Validate that allocations sum to 100%
        total_allocation = 0
        for bucket, var in self.allocation_vars.items():
            try:
                allocation = float(var.get())
                if allocation < 0:
                    messagebox.showerror("Error", f"Allocation for {
                                         bucket} cannot be negative")
                    return
                total_allocation += allocation
                self.config["allocations"][bucket] = allocation
            except ValueError:
                messagebox.showerror(
                    "Error", f"Invalid allocation for {bucket}")
                return

        if abs(total_allocation - 100) > 0.01:  # Allow small rounding errors
            messagebox.showerror(
                "Error", f"Allocations must sum to 100% (current: {total_allocation}%)")
            return

        self.save_data()
        messagebox.showinfo("Success", "Allocations saved successfully")

    # Deposit screen
    def show_deposit_screen(self):
        self.clear_main_frame()

        # Header
        header = ttk.Label(self.main_frame, text="Make a Deposit",
                           font=("Arial", 24, "bold"))
        header.pack(pady=20)

        # Deposit amount
        deposit_frame = ttk.Frame(self.main_frame)
        deposit_frame.pack(fill=tk.X, pady=10, padx=20)

        ttk.Label(deposit_frame, text="Deposit Amount: $",
                  font=("Arial", 14)).pack(side=tk.LEFT)
        self.deposit_amount_var = tk.StringVar()
        ttk.Entry(deposit_frame, textvariable=self.deposit_amount_var,
                  width=15, font=("Arial", 14)).pack(side=tk.LEFT, padx=5)

        # Allocation preview
        preview_frame = ttk.LabelFrame(
            self.main_frame, text="Allocation Preview")
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Column headers
        ttk.Label(preview_frame, text="Category",
                  font=("Arial", 12, "bold")).grid(
            row=0, column=0, padx=10, pady=5, sticky="w")
        ttk.Label(preview_frame, text="Current Balance",
                  font=("Arial", 12, "bold")).grid(
            row=0, column=1, padx=10, pady=5, sticky="w")
        ttk.Label(preview_frame, text="Allocation %",
                  font=("Arial", 12, "bold")).grid(
            row=0, column=2, padx=10, pady=5, sticky="w")
        ttk.Label(preview_frame, text="Amount to Add",
                  font=("Arial", 12, "bold")).grid(
            row=0, column=3, padx=10, pady=5, sticky="w")
        ttk.Label(preview_frame, text="New Balance",
                  font=("Arial", 12, "bold")).grid(
            row=0, column=4, padx=10, pady=5, sticky="w")

        # Preview allocation (initially empty)
        self.preview_labels = {}
        row = 1
        for bucket in self.savings_data["buckets"]:
            ttk.Label(preview_frame, text=bucket).grid(
                row=row, column=0, padx=10, pady=5, sticky="w")

            current = self.savings_data["buckets"][bucket]
            ttk.Label(preview_frame, text=f"${float(current):,.2f}").grid(
                row=row, column=1, padx=10, pady=5, sticky="w")

            allocation = self.config["allocations"].get(bucket, 0)
            ttk.Label(preview_frame, text=f"{allocation}%").grid(
                row=row, column=2, padx=10, pady=5, sticky="w")

            # Placeholders for dynamic values
            amount_label = ttk.Label(preview_frame, text="$0.00")
            amount_label.grid(row=row, column=3, padx=10, pady=5, sticky="w")

            new_balance_label = ttk.Label(
                preview_frame, text=f"${float(current):,.2f}")
            new_balance_label.grid(
                row=row, column=4, padx=10, pady=5, sticky="w")

            self.preview_labels[bucket] = (amount_label, new_balance_label)

            row += 1

        # Calculate button
        ttk.Button(self.main_frame, text="Calculate Allocation",
                   command=self.calculate_allocation).pack(pady=10)

        # Action buttons
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=20)

        self.complete_deposit_button = ttk.Button(
            button_frame, text="Complete Deposit", command=self.complete_deposit, state=tk.DISABLED)
        self.complete_deposit_button.pack(side=tk.LEFT, padx=10)

        ttk.Button(button_frame, text="Back to Dashboard",
                   command=self.show_dashboard).pack(side=tk.LEFT, padx=10)

    def calculate_allocation(self):
        try:
            deposit_amount = float(self.deposit_amount_var.get())
            if deposit_amount <= 0:
                messagebox.showerror(
                    "Error", "Please enter a positive deposit amount")
                return

            # Calculate allocations
            self.pending_allocations = {}
            total_allocated_percent = sum(self.config["allocations"].values())

            if total_allocated_percent == 0:
                messagebox.showerror(
                    "Error", "No allocation percentages defined. Please set up categories first.")
                return

            for bucket, allocation_percent in self.config["allocations"].items():
                # Scale allocation if total is not exactly 100%
                scaled_percent = allocation_percent / total_allocated_percent * 100
                allocation_amount = deposit_amount * (scaled_percent / 100)
                self.pending_allocations[bucket] = allocation_amount

                current = self.savings_data["buckets"].get(bucket, 0)
                new_balance = current + allocation_amount

                # Update preview
                if bucket in self.preview_labels:
                    amount_label, balance_label = self.preview_labels[bucket]
                    amount_label.config(text=f"${allocation_amount:.2f}")
                    balance_label.config(text=f"${new_balance:.2f}")

            # Enable the deposit button
            self.complete_deposit_button.config(state=tk.NORMAL)

        except ValueError:
            messagebox.showerror(
                "Error", "Please enter a valid deposit amount")

    def complete_deposit(self):
        try:
            deposit_amount = float(self.deposit_amount_var.get())

            # Apply the allocations
            for bucket, amount in self.pending_allocations.items():
                if bucket in self.savings_data["buckets"]:
                    self.savings_data["buckets"][bucket] += amount
                else:
                    self.savings_data["buckets"][bucket] = amount

            # Update total balance
            self.savings_data["total_balance"] += deposit_amount

            # Record transaction
            transaction = {
                "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "type": "deposit",
                "amount": deposit_amount,
                "allocations": self.pending_allocations
            }
            self.savings_data["transactions"].append(transaction)

            # Save data
            self.save_data()

            messagebox.showinfo("Success", f"Deposit of ${
                                deposit_amount:.2f} completed successfully")
            self.show_dashboard()

        except ValueError:
            messagebox.showerror(
                "Error", "Please enter a valid deposit amount")

    # Reallocation screen
    def show_reallocation_screen(self):
        self.clear_main_frame()

        # Header
        header = ttk.Label(self.main_frame, text="Reallocate Funds",
                           font=("Arial", 24, "bold"))
        header.pack(pady=20)

        # Source bucket selection
        source_frame = ttk.LabelFrame(self.main_frame, text="Source")
        source_frame.pack(fill=tk.X, pady=10, padx=20)

        ttk.Label(source_frame, text="From Category:").grid(
            row=0, column=0, padx=10, pady=10, sticky="w")

        self.source_bucket_var = tk.StringVar()
        source_combo = ttk.Combobox(source_frame, textvariable=self.source_bucket_var,
                                    state="readonly", width=20)
        source_combo["values"] = list(self.savings_data["buckets"].keys())
        if source_combo["values"]:
            source_combo.current(0)
        source_combo.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        source_combo.bind("<<ComboboxSelected>>", self.update_source_info)

        ttk.Label(source_frame, text="Current Balance:").grid(
            row=0, column=2, padx=10, pady=10, sticky="w")
        self.source_balance_var = tk.StringVar(value="$0.00")
        ttk.Label(source_frame, textvariable=self.source_balance_var).grid(
            row=0, column=3, padx=10, pady=10, sticky="w")

        ttk.Label(source_frame, text="Amount to Move: $").grid(
            row=1, column=0, padx=10, pady=10, sticky="w")
        self.reallocation_amount_var = tk.StringVar()
        ttk.Entry(source_frame, textvariable=self.reallocation_amount_var, width=15).grid(
            row=1, column=1, padx=10, pady=10, sticky="w")

        # Initialize source info if we have buckets
        if self.savings_data["buckets"]:
            self.update_source_info()

        # Destination bucket selection
        dest_frame = ttk.LabelFrame(self.main_frame, text="Destination")
        dest_frame.pack(fill=tk.X, pady=10, padx=20)

        ttk.Label(dest_frame, text="To Category:").grid(
            row=0, column=0, padx=10, pady=10, sticky="w")

        self.dest_bucket_var = tk.StringVar()
        dest_combo = ttk.Combobox(dest_frame, textvariable=self.dest_bucket_var,
                                  state="readonly", width=20)
        dest_combo["values"] = list(self.savings_data["buckets"].keys())
        if len(dest_combo["values"]) > 1:
            dest_combo.current(1)
        elif dest_combo["values"]:
            dest_combo.current(0)
        dest_combo.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        dest_combo.bind("<<ComboboxSelected>>", self.update_dest_info)

        ttk.Label(dest_frame, text="Current Balance:").grid(
            row=0, column=2, padx=10, pady=10, sticky="w")
        self.dest_balance_var = tk.StringVar(value="$0.00")
        ttk.Label(dest_frame, textvariable=self.dest_balance_var).grid(
            row=0, column=3, padx=10, pady=10, sticky="w")

        # Initialize destination info if we have buckets
        if self.savings_data["buckets"]:
            self.update_dest_info()

        # Preview section
        preview_frame = ttk.LabelFrame(self.main_frame, text="Preview")
        preview_frame.pack(fill=tk.X, pady=10, padx=20)

        ttk.Label(preview_frame, text="Source New Balance:").grid(
            row=0, column=0, padx=10, pady=10, sticky="w")
        self.source_new_balance_var = tk.StringVar(value="$0.00")
        ttk.Label(preview_frame, textvariable=self.source_new_balance_var).grid(
            row=0, column=1, padx=10, pady=10, sticky="w")

        ttk.Label(preview_frame, text="Destination New Balance:").grid(
            row=0, column=2, padx=10, pady=10, sticky="w")
        self.dest_new_balance_var = tk.StringVar(value="$0.00")
        ttk.Label(preview_frame, textvariable=self.dest_new_balance_var).grid(
            row=0, column=3, padx=10, pady=10, sticky="w")

        # Calculate button
        ttk.Button(self.main_frame, text="Calculate Reallocation",
                   command=self.calculate_reallocation).pack(pady=10)

        # Action buttons
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=20)

        self.complete_reallocation_button = ttk.Button(
            button_frame, text="Complete Reallocation",
            command=self.complete_reallocation, state=tk.DISABLED)
        self.complete_reallocation_button.pack(side=tk.LEFT, padx=10)

        ttk.Button(button_frame, text="Back to Dashboard",
                   command=self.show_dashboard).pack(side=tk.LEFT, padx=10)

    def update_source_info(self, event=None):
        source_bucket = self.source_bucket_var.get()
        if source_bucket in self.savings_data["buckets"]:
            current_balance = self.savings_data["buckets"][source_bucket]
            self.source_balance_var.set(f"${float(current_balance):,.2f}")

    def update_dest_info(self, event=None):
        dest_bucket = self.dest_bucket_var.get()
        if dest_bucket in self.savings_data["buckets"]:
            current_balance = self.savings_data["buckets"][dest_bucket]
            self.dest_balance_var.set(f"${float(current_balance):,.2f}")

    def calculate_reallocation(self):
        source_bucket = self.source_bucket_var.get()
        dest_bucket = self.dest_bucket_var.get()

        if source_bucket == dest_bucket:
            messagebox.showerror(
                "Error", "Source and destination categories must be different")
            return

        try:
            amount = float(self.reallocation_amount_var.get())
            if amount <= 0:
                messagebox.showerror("Error", "Please enter a positive amount")
                return

            source_balance = self.savings_data["buckets"].get(source_bucket, 0)
            if amount > source_balance:
                messagebox.showerror(
                    "Error", "Insufficient funds in source category")
                return

            dest_balance = self.savings_data["buckets"].get(dest_bucket, 0)

            # Calculate new balances
            source_new_balance = source_balance - amount
            dest_new_balance = dest_balance + amount

            # Update preview
            self.source_new_balance_var.set(f"${source_new_balance:,.2f}")
            self.dest_new_balance_var.set(f"${dest_new_balance:,.2f}")

            # Enable reallocation button
            self.complete_reallocation_button.config(state=tk.NORMAL)

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")

    def complete_reallocation(self):
        source_bucket = self.source_bucket_var.get()
        dest_bucket = self.dest_bucket_var.get()

        try:
            amount = float(self.reallocation_amount_var.get())

            # Update balances
            self.savings_data["buckets"][source_bucket] -= amount
            self.savings_data["buckets"][dest_bucket] += amount

            # Record transaction
            transaction = {
                "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "type": "reallocation",
                "amount": amount,
                "from_bucket": source_bucket,
                "to_bucket": dest_bucket
            }
            self.savings_data["transactions"].append(transaction)

            # Save data
            self.save_data()

            messagebox.showinfo("Success",
                                f"Successfully moved ${amount:.2f} from {source_bucket} to {dest_bucket}")
            self.show_dashboard()

        except ValueError:
            messagebox.showerror("Error", "Please enter a valid amount")


# Main application
if __name__ == "__main__":
    root = tk.Tk()
    app = SavingsBucketApp(root)
    root.mainloop()
