import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
from ttkbootstrap.constants import *

class MiniERPApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini ERP for SME")
        self.root.geometry("800x600")
        
        # สร้าง Notebook (Tabbed Interface)
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=BOTH, expand=True)
        
        # เพิ่มแท็บต่างๆ
        self.create_order_tab()
        self.create_queue_tab()
        self.create_product_tab()
        self.create_report_tab()
    
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
        
        btn_add_order = ttk.Button(order_tab, text="เพิ่มคำสั่งซื้อ", bootstyle=SUCCESS, command=self.add_order)
        btn_add_order.pack(pady=5)
    
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
        
        btn_add_product = ttk.Button(product_tab, text="เพิ่มสินค้า", bootstyle=SUCCESS, command=self.add_product)
        btn_add_product.pack(pady=5)
    
    def create_report_tab(self):
        # แท็บรายงาน
        report_tab = ttk.Frame(self.notebook)
        self.notebook.add(report_tab, text="รายงาน")
        
        # เพิ่ม Widgets สำหรับรายงาน
        lbl_report = ttk.Label(report_tab, text="รายงานการผลิตและคำสั่งซื้อ", font=('Helvetica', 16))
        lbl_report.pack(pady=10)
        
        self.report_text = tk.Text(report_tab, wrap=WORD)
        self.report_text.pack(fill=BOTH, expand=True, padx=10, pady=10)
    
    def add_order(self):
        # ฟังก์ชันเพิ่มคำสั่งซื้อ
        pass
    
    def assign_queue(self):
        # ฟังก์ชันจัดสรรคิวงาน
        pass
    
    def add_product(self):
        # ฟังก์ชันเพิ่มสินค้า
        pass

if __name__ == "__main__":
    root = tb.Window(themename="cosmo")
    app = MiniERPApp(root)
    root.mainloop()