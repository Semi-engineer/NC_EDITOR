import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox, Menu
import sqlite3

class MiniERP:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini ERP System")
        self.root.geometry("1000x800")

        # เชื่อมต่อฐานข้อมูล SQLite
        self.conn = sqlite3.connect("mini_erp.db")
        self.cursor = self.conn.cursor()

        # สร้างตารางหากยังไม่มี
        self.create_tables()

        # สร้างเมนูบาร์
        self.create_menu_bar()

        # สร้าง Notebook (แท็บ)
        self.notebook = ttk.Notebook(root, bootstyle="info")
        self.notebook.pack(fill=BOTH, expand=True)

        # แท็บ Inventory Management
        self.inventory_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.inventory_frame, text="Inventory Management")

        # แท็บ Customer Management
        self.customer_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.customer_frame, text="Customer Management")

        # เรียกเมธอดสร้าง UI
        self.create_inventory_ui()
        self.create_customer_ui()

    def create_tables(self):
        # สร้างตารางสินค้า
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                product_id TEXT PRIMARY KEY,
                product_name TEXT,
                quantity INTEGER,
                price REAL
            )
        """)

        # สร้างตารางลูกค้า
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                customer_id TEXT PRIMARY KEY,
                customer_name TEXT,
                phone TEXT,
                email TEXT
            )
        """)
        self.conn.commit()

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

        # โหลดข้อมูลสินค้าจากฐานข้อมูล
        self.load_inventory_data()

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

        # โหลดข้อมูลลูกค้าจากฐานข้อมูล
        self.load_customer_data()

    def add_product(self):
        # เพิ่มสินค้าเข้าไปในฐานข้อมูล
        product_id = self.product_id_entry.get()
        product_name = self.product_name_entry.get()
        quantity = self.quantity_entry.get()
        price = self.price_entry.get()

        if product_id and product_name and quantity and price:
            try:
                self.cursor.execute("""
                    INSERT INTO inventory (product_id, product_name, quantity, price)
                    VALUES (?, ?, ?, ?)
                """, (product_id, product_name, int(quantity), float(price)))
                self.conn.commit()
                self.load_inventory_data()
                self.clear_inventory_entries()
            except sqlite3.IntegrityError:
                messagebox.showwarning("Input Error", "Product ID already exists")
            except ValueError:
                messagebox.showwarning("Input Error", "Quantity and Price must be numbers")
        else:
            messagebox.showwarning("Input Error", "Please fill all fields")

    def add_customer(self):
        # เพิ่มลูกค้าเข้าไปในฐานข้อมูล
        customer_id = self.customer_id_entry.get()
        customer_name = self.customer_name_entry.get()
        phone = self.phone_entry.get()
        email = self.email_entry.get()

        if customer_id and customer_name and phone and email:
            try:
                self.cursor.execute("""
                    INSERT INTO customers (customer_id, customer_name, phone, email)
                    VALUES (?, ?, ?, ?)
                """, (customer_id, customer_name, phone, email))
                self.conn.commit()
                self.load_customer_data()
                self.clear_customer_entries()
            except sqlite3.IntegrityError:
                messagebox.showwarning("Input Error", "Customer ID already exists")
        else:
            messagebox.showwarning("Input Error", "Please fill all fields")

    def load_inventory_data(self):
        # โหลดข้อมูลสินค้าจากฐานข้อมูลและแสดงใน Treeview
        self.inventory_tree.delete(*self.inventory_tree.get_children())
        self.cursor.execute("SELECT * FROM inventory")
        rows = self.cursor.fetchall()
        for row in rows:
            self.inventory_tree.insert("", "end", values=row)

    def load_customer_data(self):
        # โหลดข้อมูลลูกค้าจากฐานข้อมูลและแสดงใน Treeview
        self.customer_tree.delete(*self.customer_tree.get_children())
        self.cursor.execute("SELECT * FROM customers")
        rows = self.cursor.fetchall()
        for row in rows:
            self.customer_tree.insert("", "end", values=row)

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