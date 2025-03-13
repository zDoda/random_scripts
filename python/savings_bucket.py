#!/usr/bin/env python3

import tkinter as tk
from tkinter import PhotoImage, ttk, messagebox
import json
import os
import datetime


class SavingsBucketApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Savings Bucket Manager")
        self.root.state('zoomed')  # Open in full screen on macOS

        # Set up custom styles
        self.setup_styles()

        # Initialize data
        self.data_file = os.path.dirname(
            os.path.abspath(__file__)) + "/savings_data.json"
        self.config_file = os.path.dirname(
            os.path.abspath(__file__)) + "/savings_config.json"
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
        nav_menu.add_command(label="Withdraw Funds",
                             command=self.show_withdrawal_screen)
        nav_menu.add_command(label="Reallocate Funds",
                             command=self.show_reallocation_screen)
        nav_menu.add_command(label="Transaction History",
                             command=self.show_transaction_history)

    def setup_main_frame(self):
        # Main content frame
        self.main_frame = ttk.Frame(self.root, padding="20", style="TFrame")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Status bar at the bottom
        self.status_frame = ttk.Frame(self.root, style="TFrame")
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)

        self.status_var = tk.StringVar()
        self.status_label = ttk.Label(self.status_frame, textvariable=self.status_var,
                                      anchor=tk.W, padding=5)
        self.status_label.pack(fill=tk.X)

        # Initially hide the status
        self.status_frame.pack_forget()

    def show_status(self, message, status_type="info"):
        self.status_var.set(message)

        # Configure appearance based on status type
        if status_type == "error":
            self.status_label.configure(style="Error.TLabel")
        elif status_type == "success":
            self.status_label.configure(style="Success.TLabel")
        else:  # info
            self.status_label.configure(style="Info.TLabel")

        # Show the status frame
        self.status_frame.pack(fill=tk.X, side=tk.BOTTOM)

        # Schedule it to disappear after a few seconds
        self.root.after(5000, self.hide_status)

    def hide_status(self):
        self.status_frame.pack_forget()

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
        # In the show_dashboard method, update the bucket display section:
        for bucket, amount in self.savings_data["buckets"].items():
            ttk.Label(bucket_frame, text=bucket, font=("Arial", 12)).grid(
                row=row, column=0, padx=10, pady=5, sticky="w")
            ttk.Label(bucket_frame, text=f"${float(amount):,.2f}",
                      font=("Arial", 12)).grid(
                row=row, column=1, padx=10, pady=5, sticky="w")

            allocation = self.config["allocations"].get(bucket, 0)
            if bucket == "Other":
                allocation_text = f"{allocation}% (automatic)"
            else:
                allocation_text = f"{allocation}%"

            ttk.Label(bucket_frame, text=allocation_text,
                      font=("Arial", 12)).grid(
                row=row, column=2, padx=10, pady=5, sticky="w")

            row += 1

        # Update in show_dashboard method, in the button_frame section:
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=20)

        ttk.Button(button_frame, text="Make Deposit", style="Primary.TButton",
                   command=self.show_deposit_screen).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Withdraw Funds", style="Danger.TButton",
                   command=self.show_withdrawal_screen).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Manage Categories",
                   command=self.show_category_manager).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Reallocate Funds",
                   command=self.show_reallocation_screen).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Transaction History",
                   command=self.show_transaction_history).pack(side=tk.LEFT, padx=10)

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
        if bucket == "Other":
            messagebox.showerror("Error", "'Other' bucket cannot be deleted")
            return

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

        if total_allocation > 100:
            messagebox.showerror(
                "Error", f"Allocations exceed 100% (current: {total_allocation}%)")
            return
        elif total_allocation < 100:
            # Create "Other" bucket if it doesn't exist
            if "Other" not in self.savings_data["buckets"]:
                self.savings_data["buckets"]["Other"] = 0
                self.config["allocations"]["Other"] = 0

            remaining = 100 - total_allocation
            self.config["allocations"]["Other"] = remaining
            messagebox.showinfo("Notice", f"Remaining {
                                remaining}% has been allocated to 'Other' bucket")
        else:
            # If "Other" bucket exists but has 0% allocation, remove it
            if "Other" in self.config["allocations"] and self.config["allocations"]["Other"] == 0:
                del self.config["allocations"]["Other"]
                if "Other" in self.savings_data["buckets"]:
                    del self.savings_data["buckets"]["Other"]

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

    def setup_styles(self):
        # Create a dark theme
        style = ttk.Style()

        # Dark theme colors
        bg_color = "#000000"           # Black background
        secondary_bg = "#1e1e1e"       # Slightly lighter black for cards/elements
        text_color = "#ffffff"         # White text
        accent_color = "#2a9df4"       # Blue accent color
        danger_color = "#ff453a"       # Red for dangerous actions
        success_color = "#30d158"      # Green for success states

        # Configure the main application background
        self.root.configure(background=bg_color)

        # Configure styles for various widgets
        style.configure("TFrame", background=bg_color)
        style.configure("Card.TFrame", background=secondary_bg,
                        relief="flat", borderwidth=0)

        # Button styles
        style.configure("TButton", font=("Arial", 12), background=accent_color,
                        foreground=text_color, borderwidth=0, focusthickness=0)
        style.map("TButton", background=[
                  ("active", "#007aff"), ("disabled", "#555555")])

        # Primary action button
        style.configure("Primary.TButton", font=("Arial", 12, "bold"),
                        background=accent_color, foreground=text_color)

        # Danger button (for withdrawals, deletions)
        style.configure("Danger.TButton",
                        background=danger_color, foreground=text_color)
        style.map("Danger.TButton", background=[("active", "#d63125")])

        # Label styles
        style.configure("TLabel", background=bg_color,
                        foreground=text_color, font=("Arial", 12))
        style.configure("Header.TLabel", font=("Arial", 24, "bold"),
                        background=bg_color, foreground=text_color)
        style.configure("Subheader.TLabel", font=("Arial", 18),
                        background=bg_color, foreground=text_color)
        style.configure("Balance.TLabel", font=(
            "Arial", 16, "bold"), foreground=accent_color)

        # Entry and combobox styles
        style.configure("TEntry", font=("Arial", 12),
                        fieldbackground=secondary_bg, foreground=text_color)
        style.configure("TCombobox", font=("Arial", 12),
                        fieldbackground=secondary_bg, foreground=text_color)
        style.map("TCombobox", fieldbackground=[("readonly", secondary_bg)])
        style.map("TCombobox", selectbackground=[("readonly", accent_color)])
        style.map("TCombobox", selectforeground=[("readonly", text_color)])

        # Frame with card-like appearance for sections
        style.configure("Card.TFrame", background=secondary_bg,
                        relief="raised", borderwidth=1)

        # LabelFrame styling
        style.configure("TLabelframe", background=bg_color)
        style.configure("TLabelframe.Label", background=bg_color,
                        foreground=text_color, font=("Arial", 12, "bold"))

        # Treeview for transaction history
        style.configure("Treeview",
                        background=secondary_bg,
                        fieldbackground=secondary_bg,
                        foreground=text_color,
                        font=("Arial", 11))
        style.configure("Treeview.Heading",
                        font=("Arial", 12, "bold"),
                        background=secondary_bg,
                        foreground=text_color)

        # Radio buttons
        style.map("TRadiobutton",
                  background=[("", bg_color)],
                  foreground=[("", text_color)])

        # Status bar styles
        style.configure("Error.TLabel", background="#3a0000",
                        foreground="#ff6b6b")
        style.configure("Success.TLabel", background="#003a00",
                        foreground="#6bff6b")
        style.configure("Info.TLabel", background="#00003a",
                        foreground="#6b6bff")

    def show_withdrawal_screen(self):
        self.clear_main_frame()

        # Header
        header = ttk.Label(
            self.main_frame, text="Withdraw Funds", style="Header.TLabel")
        header.pack(pady=20)

        # Main content in a card-like frame
        content_frame = ttk.Frame(
            self.main_frame, style="Card.TFrame", padding=20)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Withdrawal type selection
        type_frame = ttk.Frame(content_frame)
        type_frame.pack(fill=tk.X, pady=10)

        ttk.Label(type_frame, text="Withdrawal Type:").pack(
            side=tk.LEFT, padx=(0, 10))

        self.withdrawal_type = tk.StringVar(value="general")
        general_radio = ttk.Radiobutton(type_frame, text="General Withdrawal",
                                        variable=self.withdrawal_type, value="general",
                                        command=self.update_withdrawal_ui)
        general_radio.pack(side=tk.LEFT, padx=10)

        specific_radio = ttk.Radiobutton(type_frame, text="Withdraw from Specific Bucket",
                                         variable=self.withdrawal_type, value="specific",
                                         command=self.update_withdrawal_ui)
        specific_radio.pack(side=tk.LEFT, padx=10)

        # Container for withdrawal details (changes based on type)
        self.withdrawal_details_frame = ttk.Frame(content_frame)
        self.withdrawal_details_frame.pack(fill=tk.X, pady=10)

        # Initialize with general withdrawal UI
        self.update_withdrawal_ui()

        # Action buttons
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=20)

        self.process_withdrawal_button = ttk.Button(button_frame, text="Process Withdrawal",
                                                    command=self.process_withdrawal,
                                                    style="Primary.TButton")
        self.process_withdrawal_button.pack(side=tk.LEFT, padx=10)

        ttk.Button(button_frame, text="Back to Dashboard",
                   command=self.show_dashboard).pack(side=tk.LEFT, padx=10)

    def update_withdrawal_ui(self):
        # Clear the details frame
        for widget in self.withdrawal_details_frame.winfo_children():
            widget.destroy()

        withdrawal_type = self.withdrawal_type.get()

        if withdrawal_type == "general":
            # General withdrawal UI
            ttk.Label(self.withdrawal_details_frame,
                      text="Withdrawal Amount: $").grid(row=0, column=0, padx=5, pady=10, sticky="w")

            self.withdrawal_amount_var = tk.StringVar()
            ttk.Entry(self.withdrawal_details_frame, textvariable=self.withdrawal_amount_var,
                      width=15).grid(row=0, column=1, padx=5, pady=10, sticky="w")

            ttk.Label(self.withdrawal_details_frame,
                      text=f"Total Available: ${self.savings_data['total_balance']:,.2f}").grid(
                row=0, column=2, padx=10, pady=10, sticky="w")

            # Preview section
            preview_frame = ttk.LabelFrame(
                self.withdrawal_details_frame, text="Impact Preview")
            preview_frame.grid(row=1, column=0, columnspan=3,
                               padx=5, pady=15, sticky="ew")

            ttk.Button(preview_frame, text="Calculate Impact",
                       command=self.calculate_withdrawal_impact).grid(
                row=0, column=0, padx=10, pady=10)

            self.impact_container = ttk.Frame(preview_frame)
            self.impact_container.grid(
                row=1, column=0, padx=10, pady=10, sticky="ew")

        else:  # specific bucket withdrawal
            # Bucket selection
            ttk.Label(self.withdrawal_details_frame,
                      text="Select Bucket:").grid(row=0, column=0, padx=5, pady=10, sticky="w")

            self.specific_bucket_var = tk.StringVar()
            bucket_combo = ttk.Combobox(self.withdrawal_details_frame,
                                        textvariable=self.specific_bucket_var,
                                        state="readonly", width=20)
            bucket_combo["values"] = list(self.savings_data["buckets"].keys())
            if bucket_combo["values"]:
                bucket_combo.current(0)
            bucket_combo.grid(row=0, column=1, padx=5, pady=10, sticky="w")
            bucket_combo.bind("<<ComboboxSelected>>",
                              self.update_bucket_balance)

            # Bucket balance
            ttk.Label(self.withdrawal_details_frame,
                      text="Bucket Balance:").grid(row=0, column=2, padx=5, pady=10, sticky="w")

            self.bucket_balance_var = tk.StringVar(value="$0.00")
            ttk.Label(self.withdrawal_details_frame,
                      textvariable=self.bucket_balance_var).grid(
                row=0, column=3, padx=5, pady=10, sticky="w")

            # Withdrawal amount
            ttk.Label(self.withdrawal_details_frame,
                      text="Withdrawal Amount: $").grid(row=1, column=0, padx=5, pady=10, sticky="w")

            self.specific_withdrawal_amount_var = tk.StringVar()
            ttk.Entry(self.withdrawal_details_frame,
                      textvariable=self.specific_withdrawal_amount_var,
                      width=15).grid(row=1, column=1, padx=5, pady=10, sticky="w")

            # New balance preview
            ttk.Label(self.withdrawal_details_frame,
                      text="New Bucket Balance:").grid(row=1, column=2, padx=5, pady=10, sticky="w")

            self.new_bucket_balance_var = tk.StringVar(value="$0.00")
            ttk.Label(self.withdrawal_details_frame,
                      textvariable=self.new_bucket_balance_var).grid(
                row=1, column=3, padx=5, pady=10, sticky="w")

            ttk.Button(self.withdrawal_details_frame, text="Calculate",
                       command=self.calculate_specific_withdrawal).grid(
                row=2, column=0, columnspan=4, pady=10)

            # Initialize the bucket balance if we have buckets
            if self.savings_data["buckets"]:
                self.update_bucket_balance()

    def update_bucket_balance(self, event=None):
        bucket = self.specific_bucket_var.get()
        if bucket in self.savings_data["buckets"]:
            balance = self.savings_data["buckets"][bucket]
            self.bucket_balance_var.set(f"${float(balance):,.2f}")

    def calculate_specific_withdrawal(self):
        bucket = self.specific_bucket_var.get()

        try:
            amount = float(self.specific_withdrawal_amount_var.get())
            if amount <= 0:
                self.show_status("Please enter a positive amount", "error")
                return

            current_balance = self.savings_data["buckets"].get(bucket, 0)
            if amount > current_balance:
                self.show_status(
                    "Insufficient funds in selected bucket", "error")
                return

            new_balance = current_balance - amount
            self.new_bucket_balance_var.set(f"${new_balance:,.2f}")

            # Enable withdrawal button
            self.process_withdrawal_button.config(state=tk.NORMAL)

        except ValueError:
            self.show_status("Please enter a valid amount", "error")

    def calculate_withdrawal_impact(self):
        try:
            amount = float(self.withdrawal_amount_var.get())
            if amount <= 0:
                self.show_status("Please enter a positive amount", "error")
                return

            if amount > self.savings_data["total_balance"]:
                self.show_status(
                    "Withdrawal amount exceeds total balance", "error")
                return

            # Clear previous impact display
            for widget in self.impact_container.winfo_children():
                widget.destroy()

            # Calculate impact on each bucket (proportional withdrawal)
            total_balance = self.savings_data["total_balance"]
            impact_data = {}

            for bucket, bucket_balance in self.savings_data["buckets"].items():
                proportion = bucket_balance / total_balance if total_balance > 0 else 0
                bucket_withdrawal = amount * proportion
                new_balance = bucket_balance - bucket_withdrawal
                impact_data[bucket] = (bucket_withdrawal, new_balance)

            # Display impact
            ttk.Label(self.impact_container, text="Bucket", font=("Arial", 11, "bold")).grid(
                row=0, column=0, padx=5, pady=2, sticky="w")
            ttk.Label(self.impact_container, text="Amount Withdrawn", font=("Arial", 11, "bold")).grid(
                row=0, column=1, padx=5, pady=2, sticky="w")
            ttk.Label(self.impact_container, text="New Balance", font=("Arial", 11, "bold")).grid(
                row=0, column=2, padx=5, pady=2, sticky="w")

            row = 1
            for bucket, (withdrawal, new_balance) in impact_data.items():
                ttk.Label(self.impact_container, text=bucket).grid(
                    row=row, column=0, padx=5, pady=2, sticky="w")
                ttk.Label(self.impact_container, text=f"${withdrawal:.2f}").grid(
                    row=row, column=1, padx=5, pady=2, sticky="w")
                ttk.Label(self.impact_container, text=f"${new_balance:.2f}").grid(
                    row=row, column=2, padx=5, pady=2, sticky="w")
                row += 1

            # Enable withdrawal button
            self.process_withdrawal_button.config(state=tk.NORMAL)

        except ValueError:
            self.show_status("Please enter a valid amount", "error")

    def process_withdrawal(self):
        withdrawal_type = self.withdrawal_type.get()

        try:
            if withdrawal_type == "general":
                amount = float(self.withdrawal_amount_var.get())

                if amount > self.savings_data["total_balance"]:
                    self.show_status(
                        "Withdrawal amount exceeds total balance", "error")
                    return

                # Calculate proportional withdrawals from each bucket
                total_balance = self.savings_data["total_balance"]
                impact_data = {}

                for bucket, bucket_balance in self.savings_data["buckets"].items():
                    proportion = bucket_balance / total_balance if total_balance > 0 else 0
                    bucket_withdrawal = amount * proportion
                    self.savings_data["buckets"][bucket] -= bucket_withdrawal
                    impact_data[bucket] = bucket_withdrawal

                # Update total balance
                self.savings_data["total_balance"] -= amount

                # Record transaction
                transaction = {
                    "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "type": "withdrawal",
                    "amount": amount,
                    "impact": impact_data
                }

            else:  # specific bucket withdrawal
                bucket = self.specific_bucket_var.get()
                amount = float(self.specific_withdrawal_amount_var.get())

                # Update bucket balance
                self.savings_data["buckets"][bucket] -= amount

                # Update total balance
                self.savings_data["total_balance"] -= amount

                # Record transaction
                transaction = {
                    "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "type": "bucket_withdrawal",
                    "amount": amount,
                    "bucket": bucket
                }

            # Add transaction to history
            self.savings_data["transactions"].append(transaction)

            # Save data
            self.save_data()

            self.show_status(f"Successfully withdrew ${amount:.2f}", "success")
            self.show_dashboard()

        except ValueError:
            self.show_status("Please enter a valid amount", "error")

    def show_transaction_history(self):
        self.clear_main_frame()

        # Header
        header = ttk.Label(self.main_frame, text="Transaction History",
                           style="Header.TLabel")
        header.pack(pady=20)

        # Transactions table
        frame = ttk.Frame(self.main_frame, style="Card.TFrame", padding=10)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Create treeview for transactions
        columns = ("date", "type", "amount", "details")
        tree = ttk.Treeview(frame, columns=columns,
                            show="headings", style="Treeview")

        # Configure columns
        tree.heading("date", text="Date")
        tree.heading("type", text="Type")
        tree.heading("amount", text="Amount")
        tree.heading("details", text="Details")

        tree.column("date", width=150)
        tree.column("type", width=100)
        tree.column("amount", width=100)
        tree.column("details", width=350)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(
            frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        tree.pack(fill=tk.BOTH, expand=True)

        # Populate with transactions
        for i, transaction in enumerate(reversed(self.savings_data["transactions"])):
            date = transaction["date"]
            txn_type = transaction["type"].capitalize()
            amount = f"${transaction['amount']:.2f}"

            # Create details string based on transaction type
            if txn_type == "Deposit":
                details = "Deposited to various buckets"
            elif txn_type == "Withdrawal":
                details = "Withdrawn proportionally from all buckets"
            elif txn_type == "Bucket_withdrawal":
                details = f"Withdrawn from {transaction['bucket']}"
            elif txn_type == "Reallocation":
                details = f"Moved from {transaction['from_bucket']} to {
                    transaction['to_bucket']}"
            else:
                details = ""

            tree.insert("", tk.END, values=(date, txn_type, amount, details))

        # Back button
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(pady=20)

        ttk.Button(button_frame, text="Back to Dashboard",
                   command=self.show_dashboard).pack()


# Main application
if __name__ == "__main__":
    root = tk.Tk(className="Muh Savings Buckets")
    root.wm_title("Muh Savings Buckets")
    photo = PhotoImage(
        file="/Users/camdynzook/Github/random_scripts/python/coolfrog.png")
    root.iconphoto(False, photo)
    app = SavingsBucketApp(root)
    root.mainloop()
