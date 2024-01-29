import tkinter as tk
from tkinter import filedialog, messagebox
import math
from tkinter import simpledialog
import pandas as pd


class NCEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("NC EDITOR")
        self.file_path = None  # Initialize file_path to a default value, or to whatever is appropriate for your application

# Set the title icon
        icon_path = "SNcC.ico"  # Replace with the actual path to your icon file
        root.iconbitmap(icon_path)

# Configure classic programming color theme with green text
        self.root.configure(bg="#282C34")

# Create a frame to hold line numbers and the text editor
        frame = tk.Frame(root, bg="#282C34")
        frame.pack(expand=True, fill="both")

# Create a Text widget for line numbers
        self.line_numbers = tk.Text(frame, width=4, padx=5, bg="#282C34", fg="white", wrap="none", borderwidth=0, highlightthickness=0)
        self.line_numbers.pack(side="left", fill="y")

# Configure line numbers Text widget as read-only
        self.line_numbers.config(state="disabled")

# Create a Text widget for the main editor
        self.text_editor = tk.Text(frame, wrap="none", undo=True, autoseparators=True, bg="#282C34", fg="lime", insertbackground='white', selectbackground="#3E4451")
        self.text_editor.pack(expand=True, fill="both")


# Bind the function to be called when the text is modified
        self.text_editor.bind("<<Modified>>", self.write_dir)

# Bind the write_dir method to key release event
        self.text_editor.bind("<KeyRelease>", self.write_dir)

# Create a menu bar
        menu_bar = tk.Menu(root, bg="#282C34", fg="white")
        root.config(menu=menu_bar)

# Create File menu
        file_menu = tk.Menu(menu_bar, tearoff=0, bg="#282C34", fg="white")
        menu_bar.add_cascade(label="File", menu=file_menu)

# Add keyboard shortcuts to menu items
        file_menu.add_command(label="New", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Open", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Save As", command=self.save_as_file, accelerator="Ctrl+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=root.destroy, accelerator="Alt+F4")
        
# Create Edit menu
        edit_menu = tk.Menu(menu_bar, tearoff=0, bg="#282C34", fg="white")
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

        # Add keyboard shortcuts to menu items
        edit_menu.add_command(label="Undo", command=self.text_editor.edit_undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Redo", command=self.text_editor.edit_redo, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Find", command=self.find_text, accelerator="Ctrl+F")
        edit_menu.add_command(label="Replace", command=self.replace_text, accelerator="Ctrl+H")
# Create tools menu
        tools_menu = tk.Menu(menu_bar, tearoff=0, bg="#282C34", fg="white")
        menu_bar.add_cascade(label="Tools", menu=tools_menu)

        tools_menu.add_command(label="Auto Number", command=self.auto_number)
        tools_menu.add_command(label="Kill N Numbers  (coming soon)")
        tools_menu.add_separator()
        tools_menu.add_command(label="Calculate Feed and Speed", command=self.show_feed_speed_dialog)

        application_menu = tk.Menu(menu_bar, tearoff=0, bg="#282C34", fg="white")
        menu_bar.add_cascade(label="Application", menu=application_menu)

        application_menu.add_command(label="CAM Drill", command=self.generate_gcode_tool)
        application_menu.add_command(label="External Turning", command=self.external_turning_tool)
        application_menu.add_command(label="Thread Turning", command=self.thread_turning_tool)
        application_menu.add_command(label="Taper Turning (coming soon)")
        
# Bind keyboard shortcuts to methods
        root.bind("<Control-n>", self.new_file)
        root.bind("<Control-o>", self.open_file)
        root.bind("<Control-s>", self.save_file)
        root.bind("<Control-Shift-s>", self.save_as_file)
        root.bind("<Alt-F4>", root.destroy)

        root.bind("<Control-z>", self.text_editor.edit_undo)
        root.bind("<Control-y>", self.text_editor.edit_redo)
        root.bind("<Control-f>", self.find_text)
        root.bind("<Control-h>", self.replace_text)

    def highlight_code(self, event):
        # Get the current content of the text editor
        content = self.text_editor.get("1.0", tk.END)

        # Clear previous tags
        self.text_editor.tag_remove("highlight", "1.0", tk.END)

        # Define color mappings for specific letters
        color_mapping = {'G': 'red', 'N': 'wheat', 'M': 'pink', 'F': 'orange', 'O': 'aqua', 'S': 'coral'}

        # Split content into lines
        lines = content.split('\n')

        for line_number, line in enumerate(lines, start=1):
            start_pos = f"{line_number}.0"
            end_pos = f"{line_number}.end"

            # Iterate over each word in the line
            for word in line.split():
                # Get the first letter of the word
                first_letter = word[0].upper()

                # Highlight the word based on the first letter
                color = color_mapping.get(first_letter, None)

                if color:
                    # Add tags for highlighting
                    start_index = start_pos + f" +{line.index(word)}c"
                    end_index = start_pos + f" +{line.index(word) + len(word)}c"
                    self.text_editor.tag_add(f"highlight_word_{color}", start_index, end_index)
                    self.text_editor.tag_config(f"highlight_word_{color}", foreground=color)


    def update_line_numbers(self, event=None):
# Get the current content of the text editor
        content = self.text_editor.get("1.0", tk.END)

# Update line numbers Text widget with line count
        line_count = content.count("\n") + 1
        line_numbers_text = "\n".join(str(i) for i in range(1, line_count + 1))
        
# Configure line numbers Text widget as read-only
        self.line_numbers.config(state="normal")
        self.line_numbers.delete("1.0", tk.END)
        self.line_numbers.insert("1.0", line_numbers_text)
        self.line_numbers.config(state="disabled")

    def new_file(self, event=None):
        self.text_editor.delete("1.0", tk.END)
        self.file_path = None
        self.write_dir()

    def open_file(self, event=None):
        file_path = filedialog.askopenfilename(defaultextension=".nc", filetypes=[("NC Files", "*.nc"), ("GCODE Files", "*.gcode"), ("All", "*.")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
            self.text_editor.delete("1.0", tk.END)
            self.text_editor.insert(tk.END, content)
            self.file_path = file_path
            self.write_dir()

    def save_file(self, event=None):
        if self.file_path:
            content = self.text_editor.get("1.0", tk.END)
            with open(self.file_path, "w") as file:
                file.write(content)
            print(f"File saved: {self.file_path}")
            self.write_dir()
        else:
            self.save_as_file()

    def save_as_file(self, event=None):
        file_path = filedialog.asksaveasfilename(defaultextension=".nc", filetypes=[("NC Files", "*.nc"), ("GCODE Files", "*.gcode"), ("All", "*.")])
        if file_path:
            content = self.text_editor.get("1.0", tk.END)
            with open(file_path, "w") as file:
                file.write(content)
            self.file_path = file_path
            print(f"File saved: {self.file_path}")
            self.write_dir()

    def find_text(self, event=None):
        find_dialog = tk.Toplevel(self.root)
        find_dialog.title("Find")

        icon_path = "SNcC.ico"  # Replace with the actual path to your icon file
        root.iconbitmap(icon_path)


        find_label = tk.Label(find_dialog, text="Find:")
        find_label.grid(row=0, column=0, padx=5, pady=5)

        find_entry = tk.Entry(find_dialog)
        find_entry.grid(row=0, column=1, padx=5, pady=5)

        find_button = tk.Button(find_dialog, text="Find", command=lambda: self.search_text(find_entry.get()))
        find_button.grid(row=0, column=2, padx=5, pady=5)

        next_button = tk.Button(find_dialog, text="Next", command=self.next_occurrence)
        next_button.grid(row=0, column=3, padx=5, pady=5)

        prev_button = tk.Button(find_dialog, text="Previous", command=self.prev_occurrence)
        prev_button.grid(row=0, column=4, padx=5, pady=5)

    def search_text(self, query):
        start_index = self.text_editor.index(tk.SEL_FIRST) if self.text_editor.tag_ranges(tk.SEL) else "1.0"

        # Remove any existing selection and previous highlighting
        self.text_editor.tag_remove(tk.SEL, "1.0", tk.END)
        self.text_editor.tag_remove("search", "1.0", tk.END)

        # Perform the search starting from the current cursor position
        found_index = self.text_editor.search(query, start_index, tk.END, nocase=True)

        if found_index:
            # Highlight the found text with a different tag
            end_index = f"{found_index}+{len(query)}c"
            self.text_editor.tag_add("search", found_index, end_index)
            self.text_editor.tag_configure("search", background="yellow", foreground="black")

            # Set the cursor at the end of the found text
            self.text_editor.mark_set(tk.INSERT, end_index)

            # Scroll to the found text if needed
            self.text_editor.see(tk.INSERT)
        else:
            messagebox.showinfo("Search", "No more occurrences found.")

    def next_occurrence(self):
        # Move the cursor to the next occurrence of the search term
        self.search_text(self.find_entry.get())

    def prev_occurrence(self):
        # Move the cursor to the previous occurrence of the search term
        query = self.find_entry.get()
        start_index = self.text_editor.index(tk.SEL_FIRST) if self.text_editor.tag_ranges(tk.SEL) else "end-1c"
        found_index = self.text_editor.search(query, "1.0", start_index, nocase=True, backwards=True)

        if found_index:
            self.text_editor.tag_remove(tk.SEL, "1.0", tk.END)
            self.text_editor.tag_remove("search", "1.0", tk.END)

            end_index = f"{found_index}+{len(query)}c"
            self.text_editor.tag_add("search", found_index, end_index)
            self.text_editor.tag_configure("search", background="yellow", foreground="black")

            self.text_editor.mark_set(tk.INSERT, end_index)
            self.text_editor.see(tk.INSERT)
        else:
            messagebox.showinfo("Search", "No previous occurrences found.")

    def replace_text(self, event=None):
        replace_dialog = tk.Toplevel(self.root)
        replace_dialog.title("Replace")

        icon_path = "SNcC.ico"  # Replace with the actual path to your icon file
        root.iconbitmap(icon_path)


        find_label = tk.Label(replace_dialog, text="Find:")
        find_label.grid(row=0, column=0, padx=5, pady=5)

        find_entry = tk.Entry(replace_dialog)
        find_entry.grid(row=0, column=1, padx=5, pady=5)

        replace_label = tk.Label(replace_dialog, text="Replace with:")
        replace_label.grid(row=1, column=0, padx=5, pady=5)

        replace_entry = tk.Entry(replace_dialog)
        replace_entry.grid(row=1, column=1, padx=5, pady=5)

        replace_button = tk.Button(replace_dialog, text="Replace", command=lambda: self.replace_text_occurrences(find_entry.get(), replace_entry.get()))
        replace_button.grid(row=2, column=0, columnspan=2, pady=5)

    def replace_text_occurrences(self, query, replacement):
        start_pos = self.text_editor.search(query, "1.0", stopindex=tk.END, nocase=True)
        while start_pos:
            end_pos = f"{start_pos}+{len(query)}c"
            self.text_editor.delete(start_pos, end_pos)
            self.text_editor.insert(start_pos, replacement)
            start_pos = self.text_editor.search(query, end_pos, stopindex=tk.END, nocase=True)
        self.write_dir()

    def auto_number(self, event=None):
        content = self.text_editor.get("1.0", tk.END).splitlines()
        numbered_content = []

        for i, line in enumerate(content):
# Check if the line contains '%' or 'O000'
            if '%' not in line and 'O000' not in line:
                numbered_content.append(f"N{i+1} {line}")
            else:
                numbered_content.append(line)

        numbered_text = "\n".join(numbered_content)
        self.text_editor.delete("1.0", tk.END)
        self.text_editor.insert(tk.END, numbered_text)
        self.write_dir()

    def show_feed_speed_dialog(self, event=None):
        feed_speed_dialog = tk.Toplevel(self.root)
        feed_speed_dialog.title("Calculate Feed and Speed")
        feed_speed_dialog.transient(self.root)  # Make the dialog transient to the main window

        icon_path = "SNcC.ico"  # Replace with the actual path to your icon file
        root.iconbitmap(icon_path)


        cutting_speed_label = tk.Label(feed_speed_dialog, text="Cutting Speed (mm/min):")
        cutting_speed_label.grid(row=0, column=0, padx=5, pady=5)

        cutting_speed_entry = tk.Entry(feed_speed_dialog)
        cutting_speed_entry.grid(row=0, column=1, padx=5, pady=5)

        tool_diameter_label = tk.Label(feed_speed_dialog, text="Tool Diameter (mm):")
        tool_diameter_label.grid(row=1, column=0, padx=5, pady=5)

        tool_diameter_entry = tk.Entry(feed_speed_dialog)
        tool_diameter_entry.grid(row=1, column=1, padx=5, pady=5)

        feed_per_tooth_label = tk.Label(feed_speed_dialog, text="Feed per Tooth (mm/tooth):")
        feed_per_tooth_label.grid(row=2, column=0, padx=5, pady=5)

        feed_per_tooth_entry = tk.Entry(feed_speed_dialog)
        feed_per_tooth_entry.grid(row=2, column=1, padx=5, pady=5)

        num_teeth_label = tk.Label(feed_speed_dialog, text="Number of Teeth:")
        num_teeth_label.grid(row=3, column=0, padx=5, pady=5)

        num_teeth_entry = tk.Entry(feed_speed_dialog)
        num_teeth_entry.grid(row=3, column=1, padx=5, pady=5)

        calculate_button = tk.Button(feed_speed_dialog, text="Calculate", command=lambda: self.calculate_feed_speed(
            cutting_speed_entry.get(), tool_diameter_entry.get(), feed_per_tooth_entry.get(), num_teeth_entry.get(), feed_speed_dialog))
        calculate_button.grid(row=5, column=0, columnspan=2, pady=10)

    def calculate_feed_speed(self, cutting_speed_str, tool_diameter_str, feed_per_tooth_str, num_teeth_str, feed_speed_dialog):
        try:
            cutting_speed = float(cutting_speed_str)
            tool_diameter = float(tool_diameter_str)
            feed_per_tooth = float(feed_per_tooth_str)
            num_teeth = float(num_teeth_str)

            spindle_speed, feed_rate = self.calculate_feed_speed_values(cutting_speed, tool_diameter, feed_per_tooth, num_teeth)

            result_text = f"Spindle Speed: {spindle_speed:.0f} RPM\nFeed Rate: {feed_rate:.0f} mm/min"
            result_label = tk.Label(feed_speed_dialog, text=result_text)
            result_label.grid(row=4, column=0, columnspan=2, pady=10)

        except ValueError:
            tk.messagebox.showerror("Error", "Please enter valid numeric values for cutting speed, tool diameter, feed per tooth, and number of teeth.")

    def calculate_feed_speed_values(self, cutting_speed, tool_diameter, feed_per_tooth, num_teeth):
        cutting_speed_mm_min = cutting_speed
        spindle_speed = (cutting_speed_mm_min * 1000) / (math.pi * tool_diameter)
        feed_rate = spindle_speed * feed_per_tooth * num_teeth
        return spindle_speed, feed_rate
    
    def write_dir(self, event=None):
        content = self.text_editor.get("1.0", tk.END)
        self.text_editor.tag_remove("comment", "1.0", tk.END)
        self.text_editor.tag_remove("command", "1.0", tk.END)
        self.update_line_numbers()

        if self.file_path:
            self.root.title(f"NC Editor - {self.file_path}")
        else:
            self.root.title("NC Editor")

        # Highlight newly added text
        start_line, _ = map(int, self.text_editor.index("insert").split("."))
        start_pos = f"{start_line}.0"
        end_pos = tk.END
        new_text = self.text_editor.get(start_pos, end_pos)

        # Call the highlight_code method
        self.highlight_code(None)

    def generate_gcode_from_excel(self, excel_file, tool_name, tool_number, spindle_speed, safety_dis, depth, retract, feed, end):
        try:
            df = pd.read_excel(excel_file)
            gcode_commands = []

            gcode_commands.append(f"(Tool name: {tool_name})")
            gcode_commands.append(f" T{tool_number}")
            gcode_commands.append(f" M3 S{spindle_speed}")
            gcode_commands.append(f" M8")
            gcode_commands.append(f" G90 G54")
            gcode_commands.append(f" G17")
            
            for index, row in df.iterrows():
                try:
                    x = row['X']
                    y = row['Y']
                    gcode_line = f" G0 X{x} Y{y}"                            
                    gcode_commands.append(gcode_line)
                    #gcode_commands.append(f" G98 G81 Z{depth} R{retract} F{feed}")

                    if index ==0:
                        gcode_commands.append(f" G0 Z{safety_dis}")
                        gcode_commands.append(f" G98 G81 Z{depth} R{retract} F{feed} ")

                    for column, value in row.items():
                        if column not in ['X', 'Y']:
                            gcode_commands.append(f"(Column: {column}, Value: {value})")
          
                except KeyError as e:
                    print(f"Error: {e} column not found in the Excel file.")

            gcode_commands.append(f" G80")
            gcode_commands.append(f" M5")
            gcode_commands.append(f" M9")
            gcode_commands.append(f" G91 G28 Z0.")
            gcode_commands.append(f" {end}")
     
            return gcode_commands
        except Exception as e:
            print(f"Error: {e}")
            return None

    def generate_gcode_tool(self):
    # Display a file dialog to get the Excel file path
        excel_file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])

    # Check if the user selected a file
        if excel_file_path:
        # Create a new window for user input
            input_window = tk.Toplevel(self.root)
            input_window.title("Generate Drill Code")
            input_window.transient(self.root)  # Make the dialog transient to the main window
            icon_path = "SNcC.ico"  # Replace with the actual path to your icon file
            root.iconbitmap(icon_path)


            tool_name_label = tk.Label(input_window, text="Tool Name:")
            tool_name_label.grid(row=0, column=0, padx=5, pady=5)

            tool_name_entry = tk.Entry(input_window)
            tool_name_entry.grid(row=0, column=1, padx=5, pady=5)

            tool_number_label = tk.Label(input_window, text="Tool Number:")
            tool_number_label.grid(row=1, column=0, padx=5, pady=5)

            tool_number_entry = tk.Entry(input_window)
            tool_number_entry.grid(row=1, column=1, padx=5, pady=5)

            spindle_speed_label = tk.Label(input_window, text="Spindle Speed:")
            spindle_speed_label.grid(row=2, column=0, padx=5, pady=5)

            spindle_speed_entry = tk.Entry(input_window)
            spindle_speed_entry.grid(row=2, column=1, padx=5, pady=5)

            feed_label = tk.Label(input_window, text="Feed:")
            feed_label.grid(row=3, column=0, padx=5, pady=5)

            feed_entry = tk.Entry(input_window)
            feed_entry.grid(row=3, column=1, padx=5, pady=5)

            depth_label = tk.Label(input_window, text="Depth:")
            depth_label.grid(row=4, column=0, padx=5, pady=5)

            depth_entry = tk.Entry(input_window)
            depth_entry.grid(row=4, column=1, padx=5, pady=5)

            safety_dis_label = tk.Label(input_window, text="Safety Distance:")
            safety_dis_label.grid(row=5, column=0, padx=5, pady=5)

            safety_dis_entry = tk.Entry(input_window)
            safety_dis_entry.grid(row=5, column=1, padx=5, pady=5)
            
            retract_label = tk.Label(input_window, text="Retraction:")
            retract_label.grid(row=6, column=0, padx=5, pady=5)

            retract_entry = tk.Entry(input_window)
            retract_entry.grid(row=6, column=1, padx=5, pady=5)

            end_label = tk.Label(input_window, text="End of code:")
            end_label.grid(row=7, column=0, padx=5, pady=5)

            end_entry = tk.Entry(input_window)
            end_entry.grid(row=7, column=1, padx=5, pady=5)

            calculate_button = tk.Button(input_window, text="Generate G-code", command=lambda: self.generate_gcode_from_input(
                excel_file_path, tool_name_entry.get(), tool_number_entry.get(), spindle_speed_entry.get(), safety_dis_entry.get(), depth_entry.get(), retract_entry.get(), feed_entry.get(), end_entry.get(), input_window))
            calculate_button.grid(row=8, column=0, columnspan=2, pady=10)

    def generate_gcode_from_input(self, excel_file, tool_name, tool_number, spindle_speed, safety_dis, depth, retract, feed, end, input_window):
        try:
        # Call the appropriate method to generate G-code
            gcode_points = self.generate_gcode_from_excel(excel_file, tool_name, tool_number, spindle_speed, safety_dis, depth, retract, feed, end)

            if gcode_points:
            # Insert the generated G-code into the editor
                for point in gcode_points:
                    self.text_editor.insert(tk.END, point + "\n")

            # Notify the user that G-code has been inserted
                messagebox.showinfo("G-code Generation", "G-code generated and inserted into the editor.")
            else:
            # Notify the user of an error during G-code generation
                messagebox.showerror("Error", "Error during G-code generation.")

        finally:
        # Close the input window after generating G-code
            input_window.destroy()
    # Define the function for generating G code
            
    def external_turning(self,x1, x2, z, ap, e, u, w, f, s, t, m):
            # Calculate number of passes required
            passes = int((x1 - x2) / ap)

            # Initialize G Code string
            gcode = ''

            # Head of Program
            gcode += ' %;\n'
            gcode += ' G21;\n'
            gcode += ' G18;\n'
            gcode += ' T{:};\n'.format(t + t)
            gcode += ' G50 S3500;\n'
            gcode += ' M03 S{:.0f};\n'.format(s)
            gcode += ' G00 X{:.3f} Z2.000 M08;\n'.format(x1 + 2, )
            gcode += ' G01 X{:.3f} Z{:.3f}. F{:.3f};\n'.format(x1 + u, z - z, f)

            # Generate G Code loops
            for i in range(passes):
                # Calculate the X position for this pass
                x_pos = x1 - (i + 1) * ap
                z_pos = z

                # Add G01 command to move to X and Z positions, with f set to None after the first line
                if i == 0:
                    gcode += ' G01 X{:.3f} Z{:.3f};\n'.format(x_pos + u, z_pos - z_pos, )
                    gcode += ' G01 X{:.3f} Z{:.3f};\n'.format(x_pos + u, z_pos + w, )
                    gcode += ' G01 X{:.3f} Z{:.3f};\n'.format(x_pos + e, z_pos + w, )
                    gcode += ' G01 X{:.3f} Z{:.3f};\n'.format(x_pos + e + 1, z_pos + w + 1, )
                    gcode += ' G00 X{:.3f} Z{:.3f};\n'.format(x_pos + e + 1, (z_pos - z_pos) + e + 1)
                else:
                    gcode += ' G01 X{:.3f} Z{:.3f} F{:.3f};\n'.format(x_pos + u, z_pos - z_pos, f, )
                    gcode += ' G01 X{:.3f} Z{:.3f};\n'.format(x_pos + u, z_pos + w, )
                    gcode += ' G01 X{:.3f} Z{:.3f};\n'.format(x_pos + e, z_pos + w, )
                    gcode += ' G01 X{:.3f} Z{:.3f};\n'.format(x_pos + e + 1, z_pos + w + 1, )
                    gcode += ' G00 X{:.3f} Z{:.3f};\n'.format(x_pos + e + 1, (z_pos - z_pos) + e + 1)

            # Add final G01 command to move to the X2 and Z positions, with f set to None
            gcode += ' G01 X{:.3f} Z{:.3f} F{:.3f};\n'.format(x2, z - z, f)
            gcode += ' G01 X{:.3f} Z{:.3f};\n'.format(x2, z, )
            gcode += ' G01 X{:.3f} Z{:.3f};\n'.format(x1 + e, z)
            gcode += ' G00 X{:.3f} Z2.000;\n'.format(x1 + 2, )
            gcode += ' M05;\n'
            gcode += ' M09;\n'
            gcode += ' G00 U0. W0.;\n'
            gcode += ' T{:};\n'.format(t + "00")
            gcode += ' {:};\n'.format(m)
            gcode += ' %;\n'

            # Return the generated G Code
            return gcode

    def external_turning_button_click(self, x1, x2, z, ap, e, u, w, f, s, t, m, input_window):
        # get values from entry fields
        x1 = float(self.x1_entry.get()) # Raw Diameter
        x2 = float(self.x2_entry.get()) # Finish Diameter
        z = float(self.z_entry.get()) # Length
        ap = float(self.ap_entry.get()) # Depth Of Cut
        e = float(self.e_entry.get()) # Escape Hi
        u = float(self.u_entry.get()) # Allowance x
        w = float(self.w_entry.get()) # Allowance z
        f = float(self.f_entry.get()) # Feed
        s = float(self.s_entry.get()) # Spindle Speed
        m = str(self.m_entry.get()) # M01 M00 M30
        t = str(self.t_entry.get()) # Tool No.
        gcode = self.external_turning(x1, x2, z, ap, e, u, w, f, s, t, m)

        # display G-code in text box

        try:
        # Call the appropriate method to generate G-code
            lathe_points = self.external_turning(x1, x2, z, ap, e, u, w, f, s, t, m)

            if lathe_points:
            # Insert the generated G-code into the editor
                for point in lathe_points:
                    self.text_editor.insert(tk.END, point)

            # Notify the user that G-code has been inserted
                messagebox.showinfo("G-code Generation", "G-code generated and inserted into the editor.")
            else:
            # Notify the user of an error during G-code generation
                messagebox.showerror("Error", "Error during G-code generation.")

        finally:
        # Close the input window after generating G-code
            input_window.destroy()
      
    def external_turning_tool(self):
        # create tkinter window
        root = tk.Tk()
        root.title("G-code Generator Turning")
        self.gcode_text = None  # Add this line to initialize the attribute

        icon_path = "SNcC.ico"  # Replace with the actual path to your icon file
        root.iconbitmap(icon_path)

        # create labels and entry fields
        tk.Label(root, text="Raw diameter:").grid(row=0, column=0)
        self.x1_entry = tk.Entry(root)
        self.x1_entry.grid(row=0, column=1)
        tk.Label(root, text="mm.").grid(row=0, column=2)

        tk.Label(root, text="Finish diameter:").grid(row=1, column=0)
        self.x2_entry = tk.Entry(root)
        self.x2_entry.grid(row=1, column=1)
        tk.Label(root, text="mm.").grid(row=1, column=2)

        tk.Label(root, text="Length:").grid(row=2, column=0)
        self.z_entry = tk.Entry(root)
        self.z_entry.grid(row=2, column=1)
        tk.Label(root, text="mm.").grid(row=2, column=2)

        tk.Label(root, text="Depth of cut:").grid(row=3, column=0)
        self.ap_entry = tk.Entry(root)
        self.ap_entry.grid(row=3, column=1)
        tk.Label(root, text="mm.").grid(row=3, column=2)

        tk.Label(root, text="Escape hi:").grid(row=4, column=0)
        self.e_entry = tk.Entry(root)
        self.e_entry.grid(row=4, column=1)
        tk.Label(root, text="mm.").grid(row=4, column=2)

        tk.Label(root, text="Allowance X:").grid(row=5, column=0)
        self.u_entry = tk.Entry(root)
        self.u_entry.grid(row=5, column=1)
        tk.Label(root, text="mm.").grid(row=5, column=2)

        tk.Label(root, text="Allowance Z:").grid(row=6, column=0)
        self.w_entry = tk.Entry(root)
        self.w_entry.grid(row=6, column=1)
        tk.Label(root, text="mm.").grid(row=6, column=2)

        tk.Label(root, text="Feed:").grid(row=7, column=0)
        self.f_entry = tk.Entry(root)
        self.f_entry.grid(row=7, column=1)
        tk.Label(root, text="mm.").grid(row=7, column=2)

        tk.Label(root, text="Spindle speed:").grid(row=8, column=0)
        self.s_entry = tk.Entry(root)
        self.s_entry.grid(row=8, column=1)
        tk.Label(root, text="mm.").grid(row=8, column=2)

        tk.Label(root, text="M00 M01 M30:").grid(row=9, column=0)
        self.m_entry = tk.Entry(root)
        self.m_entry.grid(row=9, column=1)
        tk.Label(root, text="mm.").grid(row=9, column=2)

        tk.Label(root, text="Tool No.:").grid(row=10, column=0)
        self.t_entry = tk.Entry(root)
        self.t_entry.grid(row=10, column=1)

        # create generate button
        generate_button = tk.Button(root, text="Generate G-code", command=lambda: self.external_turning_button_click(
            self.x1_entry.get(), self.x2_entry.get(), self.z_entry.get(),
            self.ap_entry.get(), self.e_entry.get(), self.u_entry.get(),
            self.w_entry.get(), self.f_entry.get(), self.s_entry.get(), self.t_entry.get(), self.m_entry.get(), self.input_window))
        generate_button.grid(row=11, column=0)
      
        # save the input_window attribute
        self.input_window = root

    def thread_turning(self,x1, x2, s_z, e_z, ap, e, u, f, s, t, m):
            # Calculate number of passes required
            passes = int((x1 - x2) / ap)

            # Initialize G Code string
            gcode = ''

            # Head of Program
            gcode += ' %;\n'         
            gcode += ' G21;\n'
            gcode += ' T{:};\n'.format(t + t)
            gcode += ' G18;\n'
            gcode += ' G50 S3500;\n'
            gcode += ' G97 M03 S{:.0f};\n'.format(s)
            gcode += ' G00 G54 X{:.3f} Z{:.3f};\n'.format(x1 + e, s_z + 2 )
            gcode += ' G92 G01 X{:.3f} Z{:.3f}. F{:.3f};\n'.format(x1 + u, e_z , f)

            # Generate G Code loops
            for i in range(passes):
                # Calculate the X position for this pass
                x_pos = x1 - (i + 1) * ap
              
                # Add G01 command to move to X and Z positions, with f set to None after the first line
                if i == 0:
                    gcode += ' G01 X{:.3f};\n'.format(x_pos + u )
                else:
                    gcode += ' G01 X{:.3f};\n'.format(x_pos + u )

            # Add final G01 command to move to the X2 and Z positions, with f set to None
            gcode += ' G01 X{:.3f};\n'.format(x2 )
            gcode += ' G00 X{:.3f};\n'.format(x1 + e, )
            gcode += ' M05;\n'
            gcode += ' M09;\n'
            gcode += ' G28 U0. W0.;\n'
            gcode += ' T{:};\n'.format(t + "00")
            gcode += ' {:};\n'.format(m)
            gcode += ' %;\n'

            # Return the generated G Code
            return gcode

    def thread_turning_button_click(self, x1, x2, s_z, e_z, ap, e, u, f, s, t, m, input_window):
        # get values from entry fields
        x1 = float(self.x1_entry.get()) # Thread Daimeter
        x2 = float(self.x2_entry.get()) # Minor Daimeter
        s_z = float(self.s_z_entry.get()) # Start Z
        e_z = float(self.e_z_entry.get()) # End Z
        ap = float(self.ap_entry.get()) # Depth Of Cut
        e = float(self.e_entry.get()) # Escape Hi
        u = float(self.u_entry.get()) # Allowance X
        f = float(self.f_entry.get()) # Pitch
        s = float(self.s_entry.get()) # Spindle Speed
        m = str(self.m_entry.get()) # M01 M00 M30
        t = str(self.t_entry.get()) # Tool No.
        gcode = self.thread_turning(x1, x2, s_z, e_z, ap, e, u, f, s, t, m)

        # display G-code in text box

        try:
        # Call the appropriate method to generate G-code
            lathe_points = self.thread_turning(x1, x2, s_z, e_z, ap, e, u, f, s, t, m)

            if lathe_points:
            # Insert the generated G-code into the editor
                for point in lathe_points:
                    self.text_editor.insert(tk.END, point)

            # Notify the user that G-code has been inserted
                messagebox.showinfo("G-code Generation", "G-code generated and inserted into the editor.")
            else:
            # Notify the user of an error during G-code generation
                messagebox.showerror("Error", "Error during G-code generation.")

        finally:
        # Close the input window after generating G-code
            input_window.destroy()
      
    def thread_turning_tool(self):
        # create tkinter window
        root = tk.Tk()
        root.title("G-code Generator Threading")
        self.gcode_text = None  # Add this line to initialize the attribute

        icon_path = "SNcC.ico"  # Replace with the actual path to your icon file
        root.iconbitmap(icon_path)
   
        # create labels and entry fields
        tk.Label(root, text="Thread diameter:").grid(row=0, column=0)
        self.x1_entry = tk.Entry(root)
        self.x1_entry.grid(row=0, column=1)
        tk.Label(root, text="mm.").grid(row=0, column=2)

        tk.Label(root, text="Minor diameter:").grid(row=1, column=0)
        self.x2_entry = tk.Entry(root)
        self.x2_entry.grid(row=1, column=1)
        tk.Label(root, text="mm.").grid(row=1, column=2)

        tk.Label(root, text="Start").grid(row=2, column=0)
        self.s_z_entry = tk.Entry(root)
        self.s_z_entry.grid(row=2, column=1)
        tk.Label(root, text="mm.").grid(row=2, column=2)
 
        tk.Label(root, text="End").grid(row=3, column=0)
        self.e_z_entry = tk.Entry(root)
        self.e_z_entry.grid(row=3, column=1)
        tk.Label(root, text="mm.").grid(row=3, column=2)

        tk.Label(root, text="Depth of cut:").grid(row=4, column=0)
        self.ap_entry = tk.Entry(root)
        self.ap_entry.grid(row=4, column=1)
        tk.Label(root, text="mm.").grid(row=4, column=2)

        tk.Label(root, text="Escape hi:").grid(row=5, column=0)
        self.e_entry = tk.Entry(root)
        self.e_entry.grid(row=5, column=1)
        tk.Label(root, text="mm.").grid(row=5, column=2)

        tk.Label(root, text="Allowance X:").grid(row=6, column=0)
        self.u_entry = tk.Entry(root)
        self.u_entry.grid(row=6, column=1)
        tk.Label(root, text="mm.").grid(row=6, column=2)

        tk.Label(root, text="Pitch:").grid(row=7, column=0)
        self.f_entry = tk.Entry(root)
        self.f_entry.grid(row=7, column=1)
        tk.Label(root, text="mm.").grid(row=7, column=2)

        tk.Label(root, text="Spindle speed:").grid(row=8, column=0)
        self.s_entry = tk.Entry(root)
        self.s_entry.grid(row=8, column=1)
        tk.Label(root, text="mm.").grid(row=8, column=2)

        tk.Label(root, text="M01 M00 M30:").grid(row=9, column=0)
        self.m_entry = tk.Entry(root)
        self.m_entry.grid(row=9, column=1)
    
        tk.Label(root, text="Tool No.:").grid(row=10, column=0)
        self.t_entry = tk.Entry(root)
        self.t_entry.grid(row=10, column=1)

        # create generate button
        generate_button = tk.Button(root, text="Generate G-code", command=lambda: self.thread_turning_button_click(
            self.x1_entry.get(), self.x2_entry.get(), self.s_z_entry.get(),
            self.e_z_entry.get(),
            self.ap_entry.get(), self.e_entry.get(), self.u_entry.get(), self.f_entry.get(), self.s_entry.get(), self.t_entry.get(), self.m_entry.get(), self.input_window))
        generate_button.grid(row=11, column=0)
      
        # save the input_window attribute
        self.input_window = root        

if __name__ == "__main__":
    root = tk.Tk()
    editor = NCEditor(root)
    root.mainloop()
