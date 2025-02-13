import ezdxf
import tkinter as tk
import ttkbootstrap as ttk
import re
from ttkbootstrap import Style
from ttkbootstrap.widgets import Frame, Label, Entry, Button, Radiobutton, Combobox
from tkinter import filedialog, messagebox, simpledialog
from ttkbootstrap.constants import *


class MachinistNotepad:
    def __init__(self, root):
        self.root = root
        self.root.title("Machinist Notepad")
        self.root.geometry("800x600")
        root.iconbitmap('icon.ico')

        # Initialize ttkbootstrap style with a default theme
        self.style = ttk.Style("vapor")

        # สถานะว่ามีการแก้ไขไฟล์หรือไม่
        self.file_path = None
        self.is_modified = False

        # สร้างเมนู
        self.create_menu()

        # สร้าง Text editor
        self.create_text_area()

        # อัพเดทการแก้ไขทุกครั้งที่พิมพ์
        self.text_area.bind("<KeyPress>", self.on_modify)
        self.text_area.bind("<KeyRelease>", self.update_line_numbers)
        self.text_area.bind("<KeyRelease>", self.highlight_code)
        

    def create_menu(self):
        # สร้างเมนู
        self.menubar = ttk.Menu(self.root)
        self.root.config(menu=self.menubar)

        # เมนู File
        self.file_menu = ttk.Menu(self.menubar, tearoff=False)
        self.menubar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.new_file)
        self.file_menu.add_command(label="Open", command=self.open_file)
        self.file_menu.add_command(label="Save", command=self.save_file)
        self.file_menu.add_command(label="Save As", command=self.save_as_file)
        self.file_menu.add_command(label="Exit", command=self.exit_window)

        # เมนู Edit
        self.edit_menu = ttk.Menu(self.menubar, tearoff=False)
        self.menubar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo")
        self.edit_menu.add_command(label="Redo")

        # Create Tools menu
        self.tools_menu = tk.Menu(self.menubar, tearoff=0, bg="#282C34", fg="white")
        self.menubar.add_cascade(label="Tools", menu=self.tools_menu)
        self.tools_menu.add_command(label="Insert Number")
        self.tools_menu.add_command(label="Remove Numbers")
        self.tools_menu.add_command(label="Insert Whitespace")
        self.tools_menu.add_command(label="Remove Whitespace")
        self.tools_menu.add_separator()
        self.tools_menu.add_command(label="Calculate Feed and Speed", command=self.speed_cal)

        # Create application menu
        self.application_menu = tk.Menu(self.menubar, tearoff=0, bg="#282C34", fg="white")
        self.menubar.add_cascade(label="Application", menu=self.application_menu)
        self.application_menu.add_command(label="DRILL HOLE", command=self.nc_gen1)
        self.application_menu.add_command(label="POCKET HOLE", command=self.nc_gen2)
        self.application_menu.add_separator()
        self.application_menu.add_command(label="External Turning")
        self.application_menu.add_command(label="Thread Turning")
        self.application_menu.add_command(label="Taper Turning")

        # Options Menu
        options_menu = tk.Menu(self.menubar, tearoff=0)
        themes_menu = tk.Menu(options_menu, tearoff=0)
        self.create_theme_menu(themes_menu)
        options_menu.add_cascade(label="Select Theme", menu=themes_menu)
        # Corrected this line to properly add the options menu to the menubar
        self.menubar.add_cascade(label="Options", menu=options_menu)

    def create_theme_menu(self, menu):
        # List of available themes in ttkbootstrap
        themes = ttk.Style().theme_names()
        for theme in themes:
            menu.add_command(label=theme, command=lambda t=theme: self.change_theme(t))

    def change_theme(self, theme):
        # Change the theme using ttkbootstrap style
        self.style.theme_use(theme)
        self.highlight_code()

    def create_text_area(self):
        # Frame สำหรับบรรจุ Line Numbers และ Text widget
        self.text_frame = ttk.Frame(self.root)
        self.text_frame.pack(fill="both", expand=True)

        # สร้าง Scrollbar
        self.scrollbar = ttk.Scrollbar(self.text_frame)
        self.scrollbar.pack(side="right", fill="y")

        # สร้าง Text widget สำหรับบรรทัดเลข
        self.line_numbers = tk.Text(self.text_frame, width=6, padx=5, takefocus=0, border=0, font=("Tahoma", 10),
                                    background='#2b2b2b', foreground='#8f908a', state='disabled')
        self.line_numbers.pack(side="left", fill="y")

        # สร้าง Text widget สำหรับพิมพ์ข้อความ
        self.text_area = tk.Text(self.text_frame, wrap="word", font=("Tahoma", 10), undo=True, 
                                 yscrollcommand=self.on_text_scroll)
        self.text_area.pack(fill="both", expand=True, side="right")

        # ผูก Scrollbar กับ Text widget
        self.scrollbar.config(command=self.on_scrollbar_scroll)

        self.update_line_numbers()  # เรียกอัพเดท Line Numbers ทันที

    def update_line_numbers(self, event=None):
        # อัพเดทเลขบรรทัดเมื่อมีการเปลี่ยนแปลง
        self.line_numbers.config(state='normal')
        self.line_numbers.delete(1.0, tk.END)

        # นับจำนวนบรรทัด
        line_count = int(self.text_area.index('end-1c').split('.')[0])
        line_numbers_content = "\n".join(str(i) for i in range(1, line_count + 1))

        # แสดงเลขบรรทัด
        self.line_numbers.insert('1.0', line_numbers_content)
        self.line_numbers.config(state='disabled')

        # ซิงโครไนซ์การเลื่อนบรรทัด
        self.sync_scroll()
    
    def highlight_code(self, event=None):
        content = self.text_area.get("1.0", tk.END)
        self.text_area.tag_remove("highlight", "1.0", tk.END)

        color_mwindowing = {'G': 'red', 'N': 'wheat', 'M': 'pink', 'F': 'orange', 'O': 'aqua', 'S': 'coral'}

        lines = content.split('\n')
        for line_number, line in enumerate(lines, start=1):
            start_pos = f"{line_number}.0"
            for word in line.split():
                first_letter = word[0].upper()
                color = color_mwindowing.get(first_letter, None)
                if color:
                    start_index = f"{start_pos} +{line.index(word)}c"
                    end_index = f"{start_pos} +{line.index(word) + len(word)}c"
                    self.text_area.tag_add(f"highlight_word_{color}", start_index, end_index)
                    self.text_area.tag_config(f"highlight_word_{color}", foreground=color)

    def on_modify(self, event=None):
        self.is_modified = True
        self.update_line_numbers()
        self.highlight_code()

    def new_file(self):
        if self.is_modified and not self.confirm_discard_changes():
            return
        self.text_area.delete(1.0, tk.END)
        self.file_path = None
        self.is_modified = False
        self.update_line_numbers()
        self.highlight_code()

    def open_file(self):
        if self.is_modified and not self.confirm_discard_changes():
            return
        file_path = filedialog.askopenfilename(defaultextension=".c", filetypes=[("NC Files", "*.nc"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r") as file:
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(tk.END, file.read())
            self.file_path = file_path
            self.is_modified = False
            self.update_line_numbers()
            self.highlight_code()
    def save_file(self):
        if self.file_path:
            with open(self.file_path, "w") as file:
                file.write(self.text_area.get(1.0, tk.END))
            self.is_modified = False
        else:
            self.save_as_file()

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".nc", filetypes=[("NC Files", "*.nc"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text_area.get(1.0, tk.END))
            self.file_path = file_path
            self.is_modified = False

    def exit_window(self):
        if self.is_modified and not self.confirm_discard_changes():
            return
        self.root.quit()

    def confirm_discard_changes(self):
        # ถามผู้ใช้ว่าต้องการละทิ้งการเปลี่ยนแปลงหรือไม่
        return messagebox.askokcancel("Discard Changes", "You have unsaved changes. Do you want to discard them?")

    def on_text_scroll(self, *args):
        # เลื่อน Scrollbar และ Line Numbers ไปพร้อมกับ Text widget
        self.scrollbar.set(*args)
        self.line_numbers.yview_moveto(args[0])

    def on_scrollbar_scroll(self, *args):
        # เลื่อน Text widget และ Line Numbers พร้อมกันเมื่อ Scrollbar ถูกเลื่อน
        self.text_area.yview(*args)
        self.line_numbers.yview(*args)

    def sync_scroll(self):
        # ซิงโครไนซ์การเลื่อนระหว่าง Text widget และ Line Numbers
        first_visible_index = self.text_area.index("@0,0")
        last_visible_index = self.text_area.index("@0,%d" % (self.text_area.winfo_height()))
        self.line_numbers.yview_moveto(self.text_area.yview()[0])
############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################
############################################################################################################
# Extension modules
        
    def speed_cal(self): #FEED AND SPEED CALCULATOR
        # ข้อมูลพื้นฐานของวัสดุ (วัสดุ : ความเร็วพื้นผิวที่แนะนำ (Surface Speed))
        material_data = {
            "Aluminum": {"Metric": 300, "Inch": 1000},   # Metric เป็นเมตรต่อนาที, Inch เป็นฟุตต่อนาที
            "Brass": {"Metric": 150, "Inch": 500},
            "Cast Iron": {"Metric": 100, "Inch": 330},
            "Stainless Steel": {"Metric": 60, "Inch": 200},
            "Steel": {"Metric": 80, "Inch": 260},
            "Titanium": {"Metric": 40, "Inch": 130}
        }

        # ฟังก์ชันการคำนวณ RPM และอัตราการป้อน (Feed Rate)
        def calculate():
            try:
                # ดึงค่าจากฟิลด์การป้อนข้อมูล
                diameter = float(diameter_var.get())
                unit = unit_var.get()  # ตรวจสอบหน่วยวัดที่เลือก

                # ดึงค่าจากช่องป้อนข้อมูลหรือฐานข้อมูลวัสดุ
                speed = float(surface_speed_var.get()) if surface_speed_var.get() else material_data.get(material_var.get(), {}).get(unit, 100)

                # อัปเดตค่าในช่องป้อนข้อมูล Surface Speed
                surface_speed_var.set(f"{speed:.2f}")
                num_teeth = int(teeth_var.get())
                feed_per_tooth = float(feed_per_tooth_var.get())

                # แปลงหน่วยถ้าเลือก Metric
                if unit == "Metric":
                    rpm = (speed * 1000) / (3.14 * diameter)  # ใช้สูตร Metric
                else:
                    rpm = (speed * 12) / (3.14 * diameter)  # ใช้สูตร Inch
                
                rpm_var.set(f"{int(rpm)}")

                # คำนวณ Feed Rate
                feed_rate = rpm * feed_per_tooth * num_teeth
                feed_rate_var.set(f"{feed_rate:.2f}")
                
            except ValueError:
                rpm_var.set("Error")
                feed_rate_var.set("Error")

        # ฟังก์ชันการรีเซ็ตฟิลด์
        def reset():
            diameter_var.set("")
            surface_speed_var.set("")
            rpm_var.set("")
            feed_per_tooth_var.set("")
            feed_rate_var.set("")
            teeth_var.set("1")
            material_var.set("Aluminum")
            update_material_speed()  # อัปเดตความเร็วพื้นผิวตามวัสดุเริ่มต้น
            update_ui()  # อัปเดต UI ให้กลับเป็นหน่วยเริ่มต้น

        # ฟังก์ชันการอัปเดตค่าความเร็วพื้นผิวตามวัสดุที่เลือก
        def update_material_speed(*args):
            selected_material = material_var.get()
            unit = unit_var.get()  # ตรวจสอบหน่วยวัดที่เลือก
            if selected_material in material_data:
                speed = material_data[selected_material].get(unit, 0)
                surface_speed_var.set(f"{speed:.2f}")

        def update_ui(event=None):
            if unit_var.get() == "Inch":
                # Update labels and placeholders for Inch units
                diameter_label.config(text="Diameter (inches):")
                surface_speed_label.config(text="Surface Speed (ft/min):")
                feed_per_tooth_label.config(text="Feed per Tooth (inches):")
            else:
                # Update labels and placeholders for Metric units
                diameter_label.config(text="Diameter (mm):")
                surface_speed_label.config(text="Surface Speed (m/min):")
                feed_per_tooth_label.config(text="Feed per Tooth (mm):")

            # Update the material speed based on the selected unit
            update_material_speed()

        # Create Speed and Feed Calculation Window
        window = tk.Toplevel(self.root)
        window.title("Calculate Feed and Speed")
        window.geometry("400x640")
        window.iconbitmap('icon.ico')
        window.resizable(False, False)  # ล็อคขนาดหน้าต่าง ไม่ให้สามารถขยายหรือย่อได้
        
        # Variables for the calculation inputs
        diameter_var = tk.StringVar()
        surface_speed_var = tk.StringVar()
        rpm_var = tk.StringVar()
        feed_per_tooth_var = tk.StringVar()
        feed_rate_var = tk.StringVar()
        teeth_var = tk.StringVar(value="1")
        material_var = tk.StringVar(value="Aluminum")
        unit_var = tk.StringVar(value="Metric")  # Default unit

        # Labels and Entry fields for input
        material_label = ttk.Label(window, text="Material:")
        material_label.pack(pady=5)
        material_combobox = ttk.Combobox(window, textvariable=material_var, values=list(material_data.keys()), state="readonly")
        material_combobox.pack(pady=5)
        material_combobox.bind("<<ComboboxSelected>>", update_material_speed)

        unit_label = ttk.Label(window, text="Units:")
        unit_label.pack(pady=5)
        unit_combobox = ttk.Combobox(window, textvariable=unit_var, values=["Metric", "Inch"], state="readonly")
        unit_combobox.pack(pady=5)
        unit_combobox.bind("<<ComboboxSelected>>", update_ui)

        diameter_label = ttk.Label(window, text="Diameter (mm):")
        diameter_label.pack(pady=5)
        diameter_entry = ttk.Entry(window, textvariable=diameter_var)
        diameter_entry.pack(pady=5)

        surface_speed_label = ttk.Label(window, text="Surface Speed (m/min):")
        surface_speed_label.pack(pady=5)
        surface_speed_entry = ttk.Entry(window, textvariable=surface_speed_var)
        surface_speed_entry.pack(pady=5)

        teeth_label = ttk.Label(window, text="Number of Teeth:")
        teeth_label.pack(pady=5)
        teeth_entry = ttk.Entry(window, textvariable=teeth_var)
        teeth_entry.pack(pady=5)

        feed_per_tooth_label = ttk.Label(window, text="Feed per Tooth (mm):")
        feed_per_tooth_label.pack(pady=5)
        feed_per_tooth_entry = ttk.Entry(window, textvariable=feed_per_tooth_var)
        feed_per_tooth_entry.pack(pady=5)

        rpm_label = ttk.Label(window, text="RPM:")
        rpm_label.pack(pady=5)
        rpm_entry = ttk.Entry(window, textvariable=rpm_var, state="readonly")
        rpm_entry.pack(pady=5)

        feed_rate_label = ttk.Label(window, text="Feed Rate (mm/min):")
        feed_rate_label.pack(pady=5)
        feed_rate_entry = ttk.Entry(window, textvariable=feed_rate_var, state="readonly")
        feed_rate_entry.pack(pady=5)

        # Buttons for Calculate and Reset
        calculate_button = ttk.Button(window, text="Calculate", command=calculate)
        calculate_button.pack(pady=10)

        reset_button = ttk.Button(window, text="Reset", command=reset)
        reset_button.pack(pady=5)

###########################################################################################################

    def nc_gen1(self): # NC DRILL
        # ฟังก์ชันอ่านพิกัดศูนย์กลางวงกลมจากไฟล์ .dxf
        def read_circle_centers_dia_from_dxf(file_path):
            centers = []
            diameters = []

            try:
                doc = ezdxf.readfile(file_path)
            except IOError:
                messagebox.showerror("Error", f"ไม่สามารถเปิดไฟล์ '{file_path}' ได้")
                return []
            except ezdxf.DXFStructureError:
                messagebox.showerror("Error", f"ไฟล์ '{file_path}' ไม่ใช่ไฟล์ DXF ที่ถูกต้อง")
                return []
            
            for entity in doc.modelspace().query('CIRCLE'):
                center = entity.dxf.center
                centers.append((center.x, center.y))
                radius = entity.dxf.radius
                diameters.append(radius * 2)
            return centers, diameters

        # ฟังก์ชันสร้าง G-code
        def gendrill(coordinates, diameters, depth, spindle_speed, feed, retraction, safety, peck_size):
            gcode_lines = []
            gcode_lines.append(f"G0 G40 G80 G90 G98 ;")  # Use metric units
            gcode_lines.append(f"G90 G54 ;")  # Absolute coordinates
            gcode_lines.append(f"G17 ;")  # Absolute coordinates
            gcode_lines.append(f"M03 S{spindle_speed} ;")

            for i, ((x, y), diameters) in enumerate(zip(coordinates, diameters)):
                if i == 0:
                    gcode_lines.append(f"(DIA={diameters:.3f}mm) ;")
                    gcode_lines.append(f"G0 X{x:.3f} Y{y:.3f} (HOLE NO.{i+1}) ;")
                    gcode_lines.append(f"Z{safety} ;")
                    gcode_lines.append(f"G98 G83 Z{depth:.3f} R{retraction} Q{peck_size} F{feed};")
                else:
                    gcode_lines.append(f"G0 X{x:.3f} Y{y:.3f} (HOLE NO.{i+1}) ;")


            gcode_lines.append("G80 ;")
            gcode_lines.append("M05 ;")
            gcode_lines.append("G28 Z0.;")
            gcode_lines.append("M30 ;")

            return "\n".join(gcode_lines)

        # ฟังก์ชันการเลือกไฟล์ DXF
        def select_file():
            file_path = filedialog.askopenfilename(filetypes=[("DXF Files", "*.dxf")])
            if file_path:
                file_entry.delete(0, tk.END)
                file_entry.insert(0, file_path)

        # ฟังก์ชันสำหรับการสร้าง G-code
        def generate_gcode():
            file_path = file_entry.get()
            if not file_path:
                messagebox.showerror("Error", "กรุณาเลือกไฟล์ DXF ก่อน")
                return
            
            depth = depth_entry.get()
            spindle_speed = spindle_entry.get()
            feed = feed_entry.get()
            retraction = retraction_entry.get()
            safety = safety_entry.get()
            peck_size = peck_entry.get()

            # ตรวจสอบค่าต่าง ๆ
            try:
                depth = float(depth)
                spindle_speed = int(spindle_speed)
                feed = float(feed)
                retraction = float(retraction)
                safety = float(safety)
                peck_size = float(peck_size)
            except ValueError:
                messagebox.showerror("Error", "โปรดระบุค่าที่ถูกต้องในช่องกรอกข้อมูล")
                return

            # อ่านพิกัดวงกลมจากไฟล์ DXF
            coordinates, diameters = read_circle_centers_dia_from_dxf(file_path)

            if not coordinates or not diameters:
                messagebox.showerror("Error", "ไม่พบวงกลมในไฟล์ DXF ที่ระบุ")
                return

            # สร้าง G-code และแสดงผล
            gcode = gendrill(coordinates, diameters, depth, spindle_speed, feed, retraction, safety, peck_size)

            # Display generated G-code
            self.text_area.insert("1.0", gcode)
            self.update_line_numbers()
            self.highlight_code()

                # สร้างหน้าต่างหลัก
        app = tk.Toplevel(self.root)  # Choose your preferred theme here
        app.title("G-code DRILL")
        app.geometry("520x400")
        app.iconbitmap('icon.ico')
        app.resizable(False, False)  # ล็อคขนาดหน้าต่าง ไม่ให้สามารถขยายหรือย่อได้

        # File selection section
        file_label = ttk.Label(app, text="DXF File:")
        file_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        file_entry = ttk.Entry(app, width=40)
        file_entry.grid(row=0, column=1, padx=10, pady=10)
        file_button = ttk.Button(app, text="Browse", command=select_file)
        file_button.grid(row=0, column=2, padx=10, pady=10)

        # Parameter input section
        depth_label = ttk.Label(app, text="Depth (Negative Value):")
        depth_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        depth_entry = ttk.Entry(app)
        depth_entry.grid(row=1, column=1, padx=10, pady=10)
        depth_label = ttk.Label(app, text="mm.")
        depth_label.grid(row=1, column=2, padx=10, pady=10, sticky="w")


        spindle_label = ttk.Label(app, text="Spindle Speed:")
        spindle_label.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        spindle_entry = ttk.Entry(app)
        spindle_entry.grid(row=2, column=1, padx=10, pady=10)
        spindle_label = ttk.Label(app, text="RPM")
        spindle_label.grid(row=2, column=2, padx=10, pady=10, sticky="w")

        feed_label = ttk.Label(app, text="Cutting Feed:")
        feed_label.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        feed_entry = ttk.Entry(app)
        feed_entry.grid(row=3, column=1, padx=10, pady=10)
        feed_label = ttk.Label(app, text="mm / min")
        feed_label.grid(row=3, column=2, padx=10, pady=10, sticky="w")

        retraction_label = ttk.Label(app, text="Retraction:")
        retraction_label.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        retraction_entry = ttk.Entry(app)
        retraction_entry.grid(row=4, column=1, padx=10, pady=10)
        retraction_label = ttk.Label(app, text="mm.")
        retraction_label.grid(row=4, column=2, padx=10, pady=10, sticky="w")

        safety_label = ttk.Label(app, text="Safety Distance:")
        safety_label.grid(row=5, column=0, padx=10, pady=10, sticky="w")
        safety_entry = ttk.Entry(app)
        safety_entry.grid(row=5, column=1, padx=10, pady=10)
        safety_label = ttk.Label(app, text="mm.")
        safety_label.grid(row=5, column=2, padx=10, pady=10, sticky="w")

        peck_label = ttk.Label(app, text="Peck Size:")
        peck_label.grid(row=6, column=0, padx=10, pady=10, sticky="w")
        peck_entry = ttk.Entry(app)
        peck_entry.grid(row=6, column=1, padx=10, pady=10)
        peck_label = ttk.Label(app, text="mm.")
        peck_label.grid(row=6, column=2, padx=10, pady=10, sticky="w")

        # Button to generate G-code
        generate_button = ttk.Button(app, text="Generate G-code", command=generate_gcode, bootstyle="success")
        generate_button.grid(row=7, column=0, columnspan=3, pady=20)

########################################################################################################################

    def nc_gen2(self): # NC bore
        # ฟังก์ชันอ่านพิกัดศูนย์กลางวงกลมจากไฟล์ .dxf
        def read_circle_centers_dia_from_dxf(file_path):
            centers = []
            xx = []  # Initialize as list
            yy = []  # Initialize as list
            diameters = []

            try:
                doc = ezdxf.readfile(file_path)
            except IOError:
                messagebox.showerror("Error", f"ไม่สามารถเปิดไฟล์ '{file_path}' ได้")
                return [], [], [], []
            except ezdxf.DXFStructureError:
                messagebox.showerror("Error", f"ไฟล์ '{file_path}' ไม่ใช่ไฟล์ DXF ที่ถูกต้อง")
                return [], [], [], []

            for entity in doc.modelspace().query('CIRCLE'):
                center = entity.dxf.center
                centers.append((center.x, center.y))
                xx.append(center.x)  # Correct usage
                yy.append(center.y)  # Correct usage
                radius = entity.dxf.radius
                diameters.append(radius * 2)

            return centers, diameters, xx, yy

                # ฟังก์ชันสร้าง G-code
        def genmill(xx, yy, diameters, depth, spindle_speed, feed, retraction, safety, tool_size, step_down):
            gcode_lines = []
            
            # Initialize G-code with standard settings
            gcode_lines.append(f"G21 ; Set units to millimeters")
            gcode_lines.append(f"G90 G54 ; Absolute positioning mode and work coordinate system")
            gcode_lines.append(f"G17 ; Select XY plane")
            gcode_lines.append(f"M03 S{spindle_speed} ; Set spindle speed and start spindle clockwise")

            # Calculate the number of passes needed
            total_passes = int(abs(depth) / step_down)
            
            # Iterate over each hole's position and diameter
            for i, (x, y, diameter) in enumerate(zip( xx, yy, diameters)):
                r_feature = (diameter - tool_size) / 2  # Calculate radius for boring
                x_posp = x + r_feature
                x_posn = x - r_feature
                i_pos = r_feature

                gcode_lines.append(f"(HOLE NO.{i+1} - DIA={diameter:.3f}mm) ; Information about the hole")
                gcode_lines.append(f"G0 X{x:.3f} Y{y:.3f} ; Rapid move to the hole center")
                gcode_lines.append(f"G0 Z{safety:.3f} ; Move to safe height")
                gcode_lines.append(f"G0 Z{retraction:.3f} ; Move to retraction height")
                
                # Perform multiple passes
                for pass_num in range(total_passes):
                    z_pos = -(pass_num + 1) * step_down
                    gcode_lines.append(f"G1 Z{z_pos:.3f} F{feed} ; Drill to depth Z{z_pos:.3f}")
                    gcode_lines.append(f"G1 X{x_posp:.3f} Y{y:.3f} ; Move to start boring path")
                    gcode_lines.append(f"G3 X{x_posn:.3f} Y{y:.3f} I{-i_pos:.3f} ; Boring counter-clockwise half circle")
                    gcode_lines.append(f"G3 X{x_posp:.3f} Y{y:.3f} I{i_pos:.3f} ; Boring clockwise half circle")

                # Handle remaining depth if there's any
                remaining_depth = abs(depth) - total_passes * step_down
                if remaining_depth > 0:
                    z_pos = -abs(depth)
                    gcode_lines.append(f"G1 Z{z_pos:.3f} F{feed} ; Drill to final depth Z{z_pos:.3f}")
                    gcode_lines.append(f"G1 X{x_posp:.3f} Y{y:.3f} ; Move to start boring path")
                    gcode_lines.append(f"G3 X{x_posn:.3f} Y{y:.3f} I{-i_pos:.3f} ; Boring counter-clockwise half circle")
                    gcode_lines.append(f"G3 X{x_posp:.3f} Y{y:.3f} I{i_pos:.3f} ; Boring clockwise half circle")

                # Return to the safe height after finishing the hole
                gcode_lines.append(f"G0 Z{safety:.3f} ; Return to safe height")

            # End G-code sequence
            gcode_lines.append("G80 ; Cancel canned cycle")
            gcode_lines.append("M05 ; Stop spindle")
            gcode_lines.append("G28 Z0. ; Return to home position on Z-axis")
            gcode_lines.append("M30 ; End of program")

            return "\n".join(gcode_lines)

        # ฟังก์ชันการเลือกไฟล์ DXF
        def select_file():
            file_path = filedialog.askopenfilename(filetypes=[("DXF Files", "*.dxf")])
            if file_path:
                file_entry.delete(0, tk.END)
                file_entry.insert(0, file_path)

        # ฟังก์ชันสำหรับการสร้าง G-code
        def generate_gcode():
            file_path = file_entry.get()
            if not file_path:
                messagebox.showerror("Error", "กรุณาเลือกไฟล์ DXF ก่อน")
                return
            
            depth = depth_entry.get()
            spindle_speed = spindle_entry.get()
            feed = feed_entry.get()
            retraction = retraction_entry.get()
            safety = safety_entry.get()
            tool_size = tool_size_entry.get()
            step_down = step_down_entry.get()

            # ตรวจสอบค่าต่าง ๆ
            try:
                depth = float(depth)
                spindle_speed = int(spindle_speed)
                feed = float(feed)
                retraction = float(retraction)
                safety = float(safety)
                tool_size = float(tool_size)
                step_down = float(step_down)
            except ValueError:
                messagebox.showerror("Error", "โปรดระบุค่าที่ถูกต้องในช่องกรอกข้อมูล")
                return

            # อ่านพิกัดวงกลมจากไฟล์ DXF
            coordinates, diameters, xx, yy = read_circle_centers_dia_from_dxf(file_path)

            if not coordinates or not diameters:
                messagebox.showerror("Error", "ไม่พบวงกลมในไฟล์ DXF ที่ระบุ")
                return

            # สร้าง G-code และแสดงผล
            gcode = genmill( diameters, xx, yy, depth, spindle_speed, feed, retraction, safety, tool_size, step_down)

            # Display generated G-code
            self.text_area.insert("1.0", gcode)
            self.update_line_numbers()
            self.highlight_code()

                # สร้างหน้าต่างหลัก
        app = tk.Toplevel(self.root)  # Choose your preferred theme here
        app.title("G-code MILL HOLE")
        app.geometry("520x500")
        app.iconbitmap('icon.ico')
        app.resizable(False, False)  # ล็อคขนาดหน้าต่าง ไม่ให้สามารถขยายหรือย่อได้

        # File selection section
        file_label = ttk.Label(app, text="DXF File:")
        file_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        file_entry = ttk.Entry(app, width=40)
        file_entry.grid(row=0, column=1, padx=10, pady=10)
        file_button = ttk.Button(app, text="Browse", command=select_file)
        file_button.grid(row=0, column=2, padx=10, pady=10)

        tool_name_label = ttk.Label(app, text="Tool Name:")
        tool_name_label.grid(row=1, column=0, padx=5, pady=5)
        tool_name_entry = ttk.Entry(app)
        tool_name_entry.grid(row=1, column=1, padx=5, pady=5)

        tool_number_label = ttk.Label(app, text="Tool Number:")
        tool_number_label.grid(row=2, column=0, padx=5, pady=5)
        tool_number_entry = ttk.Entry(app)
        tool_number_entry.grid(row=2, column=1, padx=5, pady=5)

        tool_size_label = ttk.Label(app, text="Tool size:")
        tool_size_label.grid(row=3, column=0, padx=5, pady=5)
        tool_size_entry = ttk.Entry(app)
        tool_size_entry.grid(row=3, column=1, padx=5, pady=5)
        tool_size_label = ttk.Label(app, text="mm.")
        tool_size_label.grid(row=3, column=2, padx=5, pady=5)

        spindle_label = ttk.Label(app, text="Spindle Speed:")
        spindle_label.grid(row=4, column=0, padx=5, pady=5)
        spindle_entry = ttk.Entry(app)
        spindle_entry.grid(row=4, column=1, padx=5, pady=5)
        spindle_label = ttk.Label(app, text="RPM")
        spindle_label.grid(row=4, column=2, padx=5, pady=5)
           
        feed_label = ttk.Label(app, text="Feed:")
        feed_label.grid(row=5, column=0, padx=5, pady=5)
        feed_entry = ttk.Entry(app)
        feed_entry.grid(row=5, column=1, padx=5, pady=5)
        feed_label = ttk.Label(app, text="mm./min.")
        feed_label.grid(row=5, column=2, padx=5, pady=5)

        step_down_label = ttk.Label(app, text="Step down:")
        step_down_label.grid(row=6, column=0, padx=5, pady=5)
        step_down_entry = ttk.Entry(app)
        step_down_entry.grid(row=6, column=1, padx=5, pady=5)
        step_down_label = ttk.Label(app, text="mm.")
        step_down_label.grid(row=6, column=2, padx=5, pady=5)

        depth_label = ttk.Label(app, text="Depth:")
        depth_label.grid(row=7, column=0, padx=5, pady=5)
        depth_entry = ttk.Entry(app)
        depth_entry.grid(row=7, column=1, padx=5, pady=5)
        depth_label = ttk.Label(app, text="mm.")
        depth_label.grid(row=7, column=2, padx=5, pady=5)

        safety_label = ttk.Label(app, text="Safety Distance:")
        safety_label.grid(row=8, column=0, padx=5, pady=5)
        safety_entry = ttk.Entry(app)
        safety_entry.grid(row=8, column=1, padx=5, pady=5)
        safety_label = ttk.Label(app, text="mm.")
        safety_label.grid(row=8, column=2, padx=5, pady=5)

        retraction_label = ttk.Label(app, text="Retraction:")
        retraction_label.grid(row=9, column=0, padx=5, pady=5)
        retraction_entry = ttk.Entry(app)
        retraction_entry.grid(row=9, column=1, padx=5, pady=5)
        retraction_label = ttk.Label(app, text="mm.")
        retraction_label.grid(row=9, column=2, padx=5, pady=5)

        end_label = ttk.Label(app, text="End of code:")
        end_label.grid(row=10, column=0, padx=5, pady=5)
        end_entry = ttk.Entry(app)
        end_entry.grid(row=10, column=1, padx=5, pady=5)

        generate_button = ttk.Button(app, text="Generate G-code", command=generate_gcode, bootstyle="success")
        generate_button.grid(row=11, column=1, columnspan=2, pady=10)

if __name__ == "__main__":
    root = ttk.Window(themename="vapor")
    window = MachinistNotepad(root)
    root.mainloop()
