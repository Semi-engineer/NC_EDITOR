import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, Menu
import pandas as pd
from queue import PriorityQueue

class Task:
    def __init__(self, name, description, priority):
        self.name = name
        self.description = description
        self.priority = priority
        self.status = "Pending"

    def __lt__(self, other):
        return self.priority < other.priority

class SmartQueue:
    def __init__(self):
        self.queue = PriorityQueue()

    def add_task(self, task):
        self.queue.put((task.priority, task))

    def get_next_task(self):
        if not self.queue.empty():
            return self.queue.get()[1]
        return None

    def is_empty(self):
        return self.queue.empty()

class MiniERP:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini ERP System")
        self.root.geometry("1000x800")

        # สร้างเมนูบาร์
        self.create_menu_bar()

        # สร้าง DataFrame เพื่อเก็บข้อมูล
        self.inventory_data = pd.DataFrame(columns=["Product ID", "Product Name", "Quantity", "Price"])
        self.customer_data = pd.DataFrame(columns=["Customer ID", "Customer Name", "Phone", "Email"])

        # สร้าง Smart Queue
        self.smart_queue = SmartQueue()

        # สร้าง Notebook (แท็บ)
        self.notebook = ttk.Notebook(root, bootstyle="info")
        self.notebook.pack(fill=BOTH, expand=True)

        # แท็บ Inventory Management
        self.inventory_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.inventory_frame, text="Inventory Management")

        # แท็บ Customer Management
        self.customer_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.customer_frame, text="Customer Management")

        # แท็บ Smart Queue Management
        self.queue_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.queue_frame, text="Smart Queue")

        # เรียกเมธอดสร้าง UI
        self.create_inventory_ui()
        self.create_customer_ui()
        self.create_queue_ui()

    def create_menu_bar(self):
        # สร้างเมนูบาร์
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        # เมนู File
        file_menu = Menu(menubar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        # เมนู Edit
        edit_menu = Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Cut")
        edit_menu.add_command(label="Copy")
        edit_menu.add_command(label="Paste")
        menubar.add_cascade(label="Edit", menu=edit_menu)

        # เมนู View
        view_menu = Menu(menubar, tearoff=0)
        view_menu.add_command(label="Refresh")
        menubar.add_cascade(label="View", menu=view_menu)

        # เมนู Option
        option_menu = Menu(menubar, tearoff=0)
        theme_menu = Menu(option_menu, tearoff=0)
        theme_menu.add_command(label="Cosmo", command=lambda: self.change_theme("cosmo"))
        theme_menu.add_command(label="Flatly", command=lambda: self.change_theme("flatly"))
        theme_menu.add_command(label="Darkly", command=lambda: self.change_theme("darkly"))
        theme_menu.add_command(label="Solar", command=lambda: self.change_theme("solar"))
        theme_menu.add_command(label="Superhero", command=lambda: self.change_theme("superhero"))
        option_menu.add_cascade(label="Theme", menu=theme_menu)
        menubar.add_cascade(label="Option", menu=option_menu)

        # เมนู Help
        help_menu = Menu(menubar, tearoff=0)
        help_menu.add_command(label="About")
        menubar.add_cascade(label="Help", menu=help_menu)

    def change_theme(self, theme_name):
        # เปลี่ยนธีมของ TTKBootstrap
        self.root.style.theme_use(theme_name)

    def create_inventory_ui(self):
        # สร้าง UI สำหรับ Inventory Management
        ttk.Label(self.inventory_frame, text="Product ID").grid(row=0, column=0, padx=10, pady=10)
        self.product_id_entry = ttk.Entry(self.inventory_frame)
        self.product_id_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self.inventory_frame, text="Product Name").grid(row=1, column=0, padx=10, pady=10)
        self.product_name_entry = ttk.Entry(self.inventory_frame)
        self.product_name_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(self.inventory_frame, text="Quantity").grid(row=2, column=0, padx=10, pady=10)
        self.quantity_entry = ttk.Entry(self.inventory_frame)
        self.quantity_entry.grid(row=2, column=1, padx=10, pady=10)

        ttk.Label(self.inventory_frame, text="Price").grid(row=3, column=0, padx=10, pady=10)
        self.price_entry = ttk.Entry(self.inventory_frame)
        self.price_entry.grid(row=3, column=1, padx=10, pady=10)

        ttk.Button(self.inventory_frame, text="Add Product", command=self.add_product, bootstyle="success").grid(row=4, column=0, columnspan=2, pady=10)

        # สร้าง Treeview เพื่อแสดงข้อมูลสินค้า
        self.inventory_tree = ttk.Treeview(self.inventory_frame, columns=("Product ID", "Product Name", "Quantity", "Price"), show="headings")
        self.inventory_tree.heading("Product ID", text="Product ID")
        self.inventory_tree.heading("Product Name", text="Product Name")
        self.inventory_tree.heading("Quantity", text="Quantity")
        self.inventory_tree.heading("Price", text="Price")
        self.inventory_tree.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def create_customer_ui(self):
        # สร้าง UI สำหรับ Customer Management
        ttk.Label(self.customer_frame, text="Customer ID").grid(row=0, column=0, padx=10, pady=10)
        self.customer_id_entry = ttk.Entry(self.customer_frame)
        self.customer_id_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self.customer_frame, text="Customer Name").grid(row=1, column=0, padx=10, pady=10)
        self.customer_name_entry = ttk.Entry(self.customer_frame)
        self.customer_name_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(self.customer_frame, text="Phone").grid(row=2, column=0, padx=10, pady=10)
        self.phone_entry = ttk.Entry(self.customer_frame)
        self.phone_entry.grid(row=2, column=1, padx=10, pady=10)

        ttk.Label(self.customer_frame, text="Email").grid(row=3, column=0, padx=10, pady=10)
        self.email_entry = ttk.Entry(self.customer_frame)
        self.email_entry.grid(row=3, column=1, padx=10, pady=10)

        ttk.Button(self.customer_frame, text="Add Customer", command=self.add_customer, bootstyle="success").grid(row=4, column=0, columnspan=2, pady=10)

        # สร้าง Treeview เพื่อแสดงข้อมูลลูกค้า
        self.customer_tree = ttk.Treeview(self.customer_frame, columns=("Customer ID", "Customer Name", "Phone", "Email"), show="headings")
        self.customer_tree.heading("Customer ID", text="Customer ID")
        self.customer_tree.heading("Customer Name", text="Customer Name")
        self.customer_tree.heading("Phone", text="Phone")
        self.customer_tree.heading("Email", text="Email")
        self.customer_tree.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def create_queue_ui(self):
        # สร้าง UI สำหรับ Smart Queue Management
        ttk.Label(self.queue_frame, text="Task Name").grid(row=0, column=0, padx=10, pady=10)
        self.task_name_entry = ttk.Entry(self.queue_frame)
        self.task_name_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self.queue_frame, text="Task Description").grid(row=1, column=0, padx=10, pady=10)
        self.task_description_entry = ttk.Entry(self.queue_frame)
        self.task_description_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(self.queue_frame, text="Priority").grid(row=2, column=0, padx=10, pady=10)
        self.task_priority_entry = ttk.Entry(self.queue_frame)
        self.task_priority_entry.grid(row=2, column=1, padx=10, pady=10)

        ttk.Button(self.queue_frame, text="Add Task", command=self.add_task, bootstyle="success").grid(row=3, column=0, columnspan=2, pady=10)
        ttk.Button(self.queue_frame, text="Process Next Task", command=self.process_next_task, bootstyle="warning").grid(row=4, column=0, columnspan=2, pady=10)

        # สร้าง Treeview เพื่อแสดงรายการงาน
        self.queue_tree = ttk.Treeview(self.queue_frame, columns=("Task Name", "Description", "Priority", "Status"), show="headings")
        self.queue_tree.heading("Task Name", text="Task Name")
        self.queue_tree.heading("Description", text="Description")
        self.queue_tree.heading("Priority", text="Priority")
        self.queue_tree.heading("Status", text="Status")
        self.queue_tree.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def add_task(self):
        # เพิ่มงานเข้าไปใน Smart Queue
        task_name = self.task_name_entry.get()
        task_description = self.task_description_entry.get()
        task_priority = self.task_priority_entry.get()

        if task_name and task_description and task_priority:
            try:
                task_priority = int(task_priority)
                new_task = Task(task_name, task_description, task_priority)
                self.smart_queue.add_task(new_task)
                self.queue_tree.insert("", "end", values=(task_name, task_description, task_priority, new_task.status))
                self.clear_queue_entries()
            except ValueError:
                messagebox.showwarning("Input Error", "Priority must be a number")
        else:
            messagebox.showwarning("Input Error", "Please fill all fields")

    def process_next_task(self):
        # ดึงงานถัดไปจากคิวและดำเนินการ
        next_task = self.smart_queue.get_next_task()
        if next_task:
            next_task.status = "Completed"
            messagebox.showinfo("Task Processed", f"Task '{next_task.name}' has been processed.")
            self.update_queue_tree()
        else:
            messagebox.showinfo("Queue Empty", "No tasks in the queue.")

    def update_queue_tree(self):
        # อัปเดต Treeview เพื่อแสดงสถานะงานล่าสุด
        self.queue_tree.delete(*self.queue_tree.get_children())
        for task in self.smart_queue.queue.queue:
            self.queue_tree.insert("", "end", values=(task[1].name, task[1].description, task[1].priority, task[1].status))

    def clear_queue_entries(self):
        # ล้างช่องกรอกข้อมูลงาน
        self.task_name_entry.delete(0, END)
        self.task_description_entry.delete(0, END)
        self.task_priority_entry.delete(0, END)

    def add_product(self):
        # เพิ่มสินค้าเข้าไปใน DataFrame และ Treeview
        product_id = self.product_id_entry.get()
        product_name = self.product_name_entry.get()
        quantity = self.quantity_entry.get()
        price = self.price_entry.get()

        if product_id and product_name and quantity and price:
            new_product = {"Product ID": product_id, "Product Name": product_name, "Quantity": quantity, "Price": price}
            self.inventory_data = self.inventory_data.append(new_product, ignore_index=True)
            self.inventory_tree.insert("", "end", values=(product_id, product_name, quantity, price))
            self.clear_inventory_entries()
        else:
            messagebox.showwarning("Input Error", "Please fill all fields")

    def add_customer(self):
        # เพิ่มลูกค้าเข้าไปใน DataFrame และ Treeview
        customer_id = self.customer_id_entry.get()
        customer_name = self.customer_name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()

        if customer_id and customer_name and phone and email:
            new_customer = {"Customer ID": customer_id, "Customer Name": customer_name, "Phone": phone, "Email": email}
            self.customer_data = self.customer_data.append(new_customer, ignore_index=True)
            self.customer_tree.insert("", "end", values=(customer_id, customer_name, phone, email))
            self.clear_customer_entries()
        else:
            messagebox.showwarning("Input Error", "Please fill all fields")

    def clear_inventory_entries(self):
        # ล้างช่องกรอกข้อมูลสินค้า
        self.product_id_entry.delete(0, END)
        self.product_name_entry.delete(0, END)
        self.quantity_entry.delete(0, END)
        self.price_entry.delete(0, END)

    def clear_customer_entries(self):
        # ล้างช่องกรอกข้อมูลลูกค้า
        self.customer_id_entry.delete(0, END)
        self.customer_name_entry.delete(0, END)
        self.phone_entry.delete(0, END)
        self.email_entry.delete(0, END)

if __name__ == "__main__":
    root = ttk.Window(themename="cosmo")
    app = MiniERP(root)
    root.mainloop()