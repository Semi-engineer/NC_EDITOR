import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import sqlite3

class MiniERPApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini ERP for SME")
        self.root.geometry("800x600")
        
        # เชื่อมต่อฐานข้อมูล SQLite
        self.conn = sqlite3.connect("mini_erp.db")
        self.create_tables()
        
        # สร้าง Notebook (Tabbed Interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=BOTH, expand=True)
        
        # เพิ่มแท็บต่างๆ
        self.create_order_tab()
        self.create_queue_tab()
        self.create_product_tab()
        self.create_report_tab()
    
    def create_tables(self):
        # สร้างตารางในฐานข้อมูล (ถ้ายังไม่มี)
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer TEXT NOT NULL,
                product TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                status TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS queues (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                status TEXT NOT NULL,
                FOREIGN KEY (order_id) REFERENCES orders (id)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                stock INTEGER NOT NULL
            )
        ''')
        self.conn.commit()
    
    def create_order_tab(self):
        # แท็บจัดการคำสั่งซื้อ
        order_tab = ttk.Frame(self.notebook)
        self.notebook.add(order_tab, text="จัดการคำสั่งซื้อ")
        
        # เพิ่ม Widgets สำหรับจัดการคำสั่งซื้อ
        lbl_order = ttk.Label(order_tab, text="จัดการคำสั่งซื้อ", font=('Helvetica', 16))
        lbl_order.pack(pady=10)
        
        self.order_tree = ttk.Treeview(order_tab, columns=("ID", "ลูกค้า", "สินค้า", "จำนวน", "สถานะ"), show="headings")
        self.order_tree.heading("ID", text="ID")
        self.order_tree.heading("ลูกค้า", text="ลูกค้า")
        self.order_tree.heading("สินค้า", text="สินค้า")
        self.order_tree.heading("จำนวน", text="จำนวน")
        self.order_tree.heading("สถานะ", text="สถานะ")
        self.order_tree.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Frame สำหรับปุ่มและฟิลด์เพิ่มคำสั่งซื้อ
        order_frame = ttk.Frame(order_tab)
        order_frame.pack(pady=10)
        
        lbl_customer = ttk.Label(order_frame, text="ลูกค้า:")
        lbl_customer.grid(row=0, column=0, padx=5)
        self.entry_customer = ttk.Entry(order_frame, width=20)
        self.entry_customer.grid(row=0, column=1, padx=5)
        
        lbl_product = ttk.Label(order_frame, text="สินค้า:")
        lbl_product.grid(row=0, column=2, padx=5)
        self.entry_product = ttk.Entry(order_frame, width=20)
        self.entry_product.grid(row=0, column=3, padx=5)
        
        lbl_quantity = ttk.Label(order_frame, text="จำนวน:")
        lbl_quantity.grid(row=0, column=4, padx=5)
        self.entry_quantity = ttk.Entry(order_frame, width=10)
        self.entry_quantity.grid(row=0, column=5, padx=5)
        
        btn_add_order = ttk.Button(order_frame, text="เพิ่มคำสั่งซื้อ", bootstyle=SUCCESS, command=self.add_order)
        btn_add_order.grid(row=0, column=6, padx=10)
        
        # โหลดข้อมูลคำสั่งซื้อ
        self.load_orders()
    
    def create_queue_tab(self):
        # แท็บจัดการคิวงาน
        queue_tab = ttk.Frame(self.notebook)
        self.notebook.add(queue_tab, text="จัดการคิวงาน")
        
        # เพิ่ม Widgets สำหรับจัดการคิวงาน
        lbl_queue = ttk.Label(queue_tab, text="จัดการคิวงาน", font=('Helvetica', 16))
        lbl_queue.pack(pady=10)
        
        self.queue_tree = ttk.Treeview(queue_tab, columns=("คิว", "คำสั่งซื้อ", "สถานะ"), show="headings")
        self.queue_tree.heading("คิว", text="คิว")
        self.queue_tree.heading("คำสั่งซื้อ", text="คำสั่งซื้อ")
        self.queue_tree.heading("สถานะ", text="สถานะ")
        self.queue_tree.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        btn_assign_queue = ttk.Button(queue_tab, text="จัดสรรคิวงาน", bootstyle=INFO, command=self.assign_queue)
        btn_assign_queue.pack(pady=5)
        
        # โหลดข้อมูลคิวงาน
        self.load_queues()
    
    def create_product_tab(self):
        # แท็บจัดการสินค้า
        product_tab = ttk.Frame(self.notebook)
        self.notebook.add(product_tab, text="จัดการสินค้า")
        
        # เพิ่ม Widgets สำหรับจัดการสินค้า
        lbl_product = ttk.Label(product_tab, text="จัดการสินค้า", font=('Helvetica', 16))
        lbl_product.pack(pady=10)
        
        self.product_tree = ttk.Treeview(product_tab, columns=("ID", "ชื่อสินค้า", "จำนวนคงเหลือ"), show="headings")
        self.product_tree.heading("ID", text="ID")
        self.product_tree.heading("ชื่อสินค้า", text="ชื่อสินค้า")
        self.product_tree.heading("จำนวนคงเหลือ", text="จำนวนคงเหลือ")
        self.product_tree.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # Frame สำหรับปุ่มและฟิลด์เพิ่มสินค้า
        product_frame = ttk.Frame(product_tab)
        product_frame.pack(pady=10)
        
        lbl_name = ttk.Label(product_frame, text="ชื่อสินค้า:")
        lbl_name.grid(row=0, column=0, padx=5)
        self.entry_product_name = ttk.Entry(product_frame, width=20)
        self.entry_product_name.grid(row=0, column=1, padx=5)
        
        lbl_stock = ttk.Label(product_frame, text="จำนวนคงเหลือ:")
        lbl_stock.grid(row=0, column=2, padx=5)
        self.entry_stock = ttk.Entry(product_frame, width=10)
        self.entry_stock.grid(row=0, column=3, padx=5)
        
        btn_add_product = ttk.Button(product_frame, text="เพิ่มสินค้า", bootstyle=SUCCESS, command=self.add_product)
        btn_add_product.grid(row=0, column=4, padx=10)
        
        # โหลดข้อมูลสินค้า
        self.load_products()
    
    def create_report_tab(self):
        # แท็บรายงาน
        report_tab = ttk.Frame(self.notebook)
        self.notebook.add(report_tab, text="รายงาน")
        
        # เพิ่ม Widgets สำหรับรายงาน
        lbl_report = ttk.Label(report_tab, text="รายงานการผลิตและคำสั่งซื้อ", font=('Helvetica', 16))
        lbl_report.pack(pady=10)
        
        self.report_text = tk.Text(report_tab, wrap=WORD)
        self.report_text.pack(fill=BOTH, expand=True, padx=10, pady=10)
        
        # โหลดรายงาน
        self.load_report()
    
    def add_order(self):
        # ฟังก์ชันเพิ่มคำสั่งซื้อ
        customer = self.entry_customer.get()
        product = self.entry_product.get()
        quantity = self.entry_quantity.get()
        
        if not customer or not product or not quantity:
            messagebox.showwarning("คำเตือน", "กรุณากรอกข้อมูลให้ครบถ้วน")
            return
        
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO orders (customer, product, quantity, status)
            VALUES (?, ?, ?, ?)
        ''', (customer, product, quantity, "รอดำเนินการ"))
        self.conn.commit()
        
        # ล้างฟิลด์
        self.entry_customer.delete(0, tk.END)
        self.entry_product.delete(0, tk.END)
        self.entry_quantity.delete(0, tk.END)
        
        # โหลดข้อมูลใหม่
        self.load_orders()
        messagebox.showinfo("สำเร็จ", "เพิ่มคำสั่งซื้อเรียบร้อยแล้ว")
    
    def assign_queue(self):
        # ฟังก์ชันจัดสรรคิวงาน
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM orders WHERE status = ?', ("รอดำเนินการ",))
        pending_orders = cursor.fetchall()
        
        if not pending_orders:
            messagebox.showwarning("คำเตือน", "ไม่มีคำสั่งซื้อที่ต้องจัดสรรคิวงาน")
            return
        
        for order in pending_orders:
            cursor.execute('''
                INSERT INTO queues (order_id, status)
                VALUES (?, ?)
            ''', (order[0], "กำลังดำเนินการ"))
            cursor.execute('UPDATE orders SET status = ? WHERE id = ?', ("กำลังดำเนินการ", order[0]))
        
        self.conn.commit()
        
        # โหลดข้อมูลใหม่
        self.load_queues()
        self.load_orders()
        messagebox.showinfo("สำเร็จ", "จัดสรรคิวงานเรียบร้อยแล้ว")
    
    def add_product(self):
        # ฟังก์ชันเพิ่มสินค้า
        name = self.entry_product_name.get()
        stock = self.entry_stock.get()
        
        if not name or not stock:
            messagebox.showwarning("คำเตือน", "กรุณากรอกข้อมูลให้ครบถ้วน")
            return
        
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO products (name, stock)
            VALUES (?, ?)
        ''', (name, stock))
        self.conn.commit()
        
        # ล้างฟิลด์
        self.entry_product_name.delete(0, tk.END)
        self.entry_stock.delete(0, tk.END)
        
        # โหลดข้อมูลใหม่
        self.load_products()
        messagebox.showinfo("สำเร็จ", "เพิ่มสินค้าเรียบร้อยแล้ว")
    
    def load_orders(self):
        # โหลดข้อมูลคำสั่งซื้อจากฐานข้อมูล
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM orders')
        orders = cursor.fetchall()
        
        self.order_tree.delete(*self.order_tree.get_children())
        for order in orders:
            self.order_tree.insert("", tk.END, values=order)
    
    def load_queues(self):
        # โหลดข้อมูลคิวงานจากฐานข้อมูล
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT queues.id, orders.id, queues.status
            FROM queues
            JOIN orders ON queues.order_id = orders.id
        ''')
        queues = cursor.fetchall()
        
        self.queue_tree.delete(*self.queue_tree.get_children())
        for queue in queues:
            self.queue_tree.insert("", tk.END, values=queue)
    
    def load_products(self):
        # โหลดข้อมูลสินค้าจากฐานข้อมูล
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM products')
        products = cursor.fetchall()
        
        self.product_tree.delete(*self.product_tree.get_children())
        for product in products:
            self.product_tree.insert("", tk.END, values=product)
    
    def load_report(self):
        # โหลดรายงานจากฐานข้อมูล
        cursor = self.conn.cursor()
        cursor.execute('SELECT COUNT(*) FROM orders')
        total_orders = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM queues')
        total_queues = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM products')
        total_products = cursor.fetchone()[0]
        
        report = "รายงานการผลิตและคำสั่งซื้อ:\n\n"
        report += f"จำนวนคำสั่งซื้อทั้งหมด: {total_orders}\n"
        report += f"จำนวนคิวงานทั้งหมด: {total_queues}\n"
        report += f"จำนวนสินค้าทั้งหมด: {total_products}\n"
        self.report_text.delete(1.0, tk.END)
        self.report_text.insert(tk.END, report)

if __name__ == "__main__":
    root = tb.Window(themename="cosmo")
    app = MiniERPApp(root)
    root.mainloop()