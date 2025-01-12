import tkinter as tk
import tkinter.messagebox
import customtkinter as ctk
import cmath
import math
from converter import string_to_complex

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("dark-blue")

class App(ctk.CTk):

    width = 850
    height = 450

    def __init__(self):
        super().__init__()

        # configure window
        self.title("Simultaneous Linear Equations Solver")

        # Center the window
        screen_width = App.winfo_screenwidth(self)
        screen_height = App.winfo_screenheight(self)
        x = (screen_width / 2) - (App.width / 2)
        y = (screen_height / 2) - (App.height / 2)
        self.geometry(f"{App.width}x{App.height}+{int(x)}+{int(y)}")
        self.iconphoto(True, tk.PhotoImage(file='assets/logo.png'))  # App icon
        self.attributes('-alpha', 1.0)  # For transparency adjustment
        self.main_frame()

    def main_frame(self):
        
        # Reset configure from the info page
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure((0,1), weight=0)

        # Grid configuration
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(7, weight=1)

        # Equation Tabview
        self.tabview = ctk.CTkTabview(self, corner_radius=10)
        self.tabview.grid(row=1, column=0, padx=20, sticky="nsew", columnspan=9)
        self.tabview.add("2 Variables")
        self.tabview.add("3 Variables")
        self.tabview.add("4 Variables")
        self.tabview.set("3 Variables") # Default tab
        
        tab_column = {"2":(1, 3, 5), "3":(1, 3, 5, 7), "4":(1, 3, 5, 7, 9)}
        for tab in tab_column:
            self.tabview.tab(f"{tab} Variables").grid_rowconfigure((0, 1, 2, 3), weight=1)
            self.tabview.tab(f"{tab} Variables").grid_columnconfigure(tab_column[tab], weight=1) #Expand only the entries

        #Prepare to collect data from the entry widgets from all three tabs
        global second_entries_list, third_entries_list, fourth_entries_list
        second_entries_list = []
        third_entries_list = []
        fourth_entries_list = [] 

        # 2 Variables tabview
        for row in range(2): # Repeat the equation
            #Eq. index
            self.eqheadline = ctk.CTkLabel(self.tabview.tab("2 Variables"), text=f"Eq. {row+1}",
                                                      font=ctk.CTkFont(size=20, weight="bold"), text_color="Dark orange")
            self.eqheadline.grid(row=row, column=0, sticky="nswe", padx=10)

            #X Y Z variables labels
            for sequence, letter in enumerate(["X  +", "Y  ="]): # Column sequence
                self.label = ctk.CTkLabel(self.tabview.tab("2 Variables"), text=f"{letter}", font=ctk.CTkFont(size=20, weight="normal"))
                self.label.grid(row=row, column=2*sequence+2, sticky="nsew")

            # Input entry boxes column sequence
            for column in range(1, 6, 2): # Column sequence
                self.entry_value = ctk.CTkEntry(self.tabview.tab("2 Variables"), font=ctk.CTkFont(size=16, weight="normal"))
                self.entry_value.grid(row=row, column=column, padx=(20, 5), pady=10, sticky="we")
                second_entries_list.append(self.entry_value)

        # 3 Variables tabview
        for row in range(3): # Repeat the equation
            #Eq. index
            self.eqheadline = ctk.CTkLabel(self.tabview.tab("3 Variables"), text=f"Eq. {row+1}",
                                                      font=ctk.CTkFont(size=20, weight="bold"), text_color="Dark orange")
            self.eqheadline.grid(row=row, column=0, sticky="nsew", padx=10)

            #X Y Z variables labels
            for sequence, letter in enumerate(["X  +", "Y  +", "Z  ="]): # Column sequence
                self.label = ctk.CTkLabel(self.tabview.tab("3 Variables"), text=f"{letter}", font=ctk.CTkFont(size=20, weight="normal"))
                self.label.grid(row=row, column=2*sequence+2, sticky="nsew")

            # Input entry boxes column sequence
            for column in range(1, 8, 2): # Column sequence
                self.entry_value = ctk.CTkEntry(self.tabview.tab("3 Variables"), font=ctk.CTkFont(size=16, weight="normal"))
                self.entry_value.grid(row=row, column=column, padx=(20, 5), pady=10, sticky="we")
                third_entries_list.append(self.entry_value)

        # 4 Variables tabview
        for row in range(4): # Repeat the equation
            #Eq. index
            self.eqheadline = ctk.CTkLabel(self.tabview.tab("4 Variables"), text=f"Eq. {row+1}",
                                                      font=ctk.CTkFont(size=20, weight="bold"), text_color="Dark orange")
            self.eqheadline.grid(row=row, column=0, sticky="nswe", padx=10)
     
            #W X Y Z variables labels
            for sequence, letter in enumerate(["W  +", "X  +", "Y  +", "Z  ="]): # Column sequence
                self.label = ctk.CTkLabel(self.tabview.tab("4 Variables"), text=f"{letter}", font=ctk.CTkFont(size=20, weight="normal"))
                self.label.grid(row=row, column=2*sequence+2, sticky="nsew")


            # Input entry boxes
            for column in range(1, 10, 2):
                self.entry_value = ctk.CTkEntry(self.tabview.tab("4 Variables"), font=ctk.CTkFont(size=16, weight="normal"))
                self.entry_value.grid(row=row, column=column, padx=(20, 5), pady=10, sticky="we")
                fourth_entries_list.append(self.entry_value)

        # Upper panel ////////////////////////////////////

            #Decimal places
        self.decimal_places_label = ctk.CTkLabel(self, text="Decimal places:", font=ctk.CTkFont(size=16, weight="normal"))
        self.decimal_places_label.grid(row=2, column=0, padx=(20,5), pady=(20,10), sticky="nswe")

        decimal_place = [] # Don't want to write a list of strings
        for i in range(10, 16):
            decimal_place.append(f"{i}")
            
        self.decimal_places = ctk.CTkOptionMenu(self, values=decimal_place, width=50)
        self.decimal_places.grid(row=2, column=1, padx=(5,10), pady=(20,10))
        self.decimal_places.set("10") # Default value


            # Ouput mode selection
        self.output_mode_label = ctk.CTkLabel(self, text="Output mode:", font=ctk.CTkFont(size=16, weight="normal"))
        self.output_mode_label.grid(row=2, column=2, padx=5, pady=(20,10), sticky="nsew")

        self.output_mode = ctk.CTkOptionMenu(self, width=50, values=["a+bj", "r∠θ"])
        self.output_mode.grid(row=2, column=3, padx=5, pady=(20,10), sticky="nswe")

            # Angle unit selection
        self.angle_unit_label = ctk.CTkLabel(self, text="Angle unit:", font=ctk.CTkFont(size=16, weight="normal"))
        self.angle_unit_label.grid(row=2, column=4, padx=5, pady=(20,10), sticky="nsew")

        self.angle_unit_mode = ctk.CTkOptionMenu(self, values=["Degree", "Radian"], width=50)
        self.angle_unit_mode.grid(row=2, column=5, columnspan=2, padx=5, pady=(20,10), sticky="nswe")


            # Reset button
        self.resetbutton = ctk.CTkButton(self, command=self.reset, text="Reset",text_color="black", font=ctk.CTkFont(size=16, weight="normal"), fg_color="dark orange", hover_color="gray")
        self.resetbutton.grid(row=2, column=8, padx=(5,20), pady=(20,10))

            # Transparency
        self.transparency = ctk.CTkSlider(self, width=30, from_=0.3, to=1, command=self.slide_transparency)
        self.transparency.grid(row=0, column=0, padx=15, pady=(20,0), sticky="we")
        self.transparency.set(self.attributes('-alpha'))  # Track the transparency

            # Info button
        self.info_button = ctk.CTkButton(self, command=self.info_page, text="?", corner_radius=60, font=ctk.CTkFont(size=15, weight="normal"),
                                             fg_color="transparent", border_width=2, width=30, text_color=("gray10", "#DCE4EE"))
        self.info_button.grid(row=0, column=8, padx=20, pady=(20,0), sticky="e")

        # Lower panel ////////////////////////////////
        
            # Conversion
        self.conversion_label = ctk.CTkLabel(self, text="a+b ↔︎ r∠θ:", font=ctk.CTkFont(size=16, weight="normal"))
        self.conversion_label.grid(row=3, column=0, padx=(20,5), pady=(0,20), sticky="e")

        self.convert_bar = ctk.CTkEntry(self, font=ctk.CTkFont(size=16, weight="normal"))
        self.convert_bar.grid(row=3, column=1, columnspan=2, padx=5, pady=(0,20), sticky="we")

        self.convert_button = ctk.CTkButton(self, command=self.convert, text="Convert", width=80, font=ctk.CTkFont(size=12, weight="normal"),
                                             fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"))
        self.convert_button.grid(row=3, column=3, padx=5, pady=(0,20))

            # Log button
        self.log_button = ctk.CTkButton(self, command=lambda: self.insert_symbol("log["), text="log[☐,☐]", font=ctk.CTkFont(size=15, weight="normal"),
                                             fg_color="transparent", border_width=2, width=50, text_color=("gray10", "#DCE4EE"))
        self.log_button.grid(row=3, column=4, padx=5, pady=(0,20))

            # Phasor button
        self.angle_button = ctk.CTkButton(self, command=lambda: self.insert_symbol("∠["), text="r∠☐", font=ctk.CTkFont(size=15, weight="normal"),
                                             fg_color="transparent", border_width=2, width=50, text_color=("gray10", "#DCE4EE"))
        self.angle_button.grid(row=3, column=5, padx=5, pady=(0,20))

            # Pi button
        self.pi_button = ctk.CTkButton(self, command=lambda: self.insert_symbol("π"), text="π", font=ctk.CTkFont(size=15, weight="normal"),
                                             fg_color="transparent", border_width=2, width=30, text_color=("gray10", "#DCE4EE"))
        self.pi_button.grid(row=3, column=6, padx=5, pady=(0,20))

            # Calculate button
        self.calculate = ctk.CTkButton(self, command=lambda: self.cramer(self.get_tab_info()), text="Calculate", 
                                       font=ctk.CTkFont(size=16, weight="normal"), fg_color="Green", hover_color="Gray")
        self.calculate.grid(row=3, column=8, padx=(5,20), pady=(0,20))

    def reset(self): # Clear all entries
        for frame in (self, self.tabview.tab(self.tabview._current_name)):
            for widget in App.winfo_children(frame): #Empty all the entries in current tab
                if isinstance(widget, ctk.CTkEntry):
                    widget.delete(0, "end")

    def get_entries(self, widget_list): #Obtain, convert, and store inputs from entries 
        angle_mode = self.angle_unit_mode.get()
        current_entries_input = []
        for widget in widget_list:
            if widget.get() != "":
                status = string_to_complex(widget.get(), angle_mode)
                if status not in ["invalid", "Math Error"]:
                    current_entries_input.append(string_to_complex(widget.get(), angle_mode))
                elif status == "Math Error":
                    self.showwarning("Math error")
                else:
                    self.showwarning("Invalid inputs")
                    break
            else:
                self.showwarning("Please fill all entries properly")
                break
        return current_entries_input

    def get_tab_info(self):
        current_tab = self.tabview._current_name
        if current_tab == "2 Variables":
            return self.get_entries(second_entries_list)
        elif current_tab == "3 Variables":
            return self.get_entries(third_entries_list)
        elif current_tab == "4 Variables":
            return self.get_entries(fourth_entries_list)
        
    def convert(self):

        value = self.convert_bar.get()
        angle_mode = self.angle_unit_mode.get()
        if string_to_complex(value, angle_mode) != "Math Error":
            if value != "":
                try:
                    if "∠" in value:
                        result = string_to_complex(value, angle_mode)
                        self.convert_bar.delete(0, ctk.END)
                        result = self.round_complex(result)
                        if abs(result.imag) == 0:
                            self.convert_bar.insert(ctk.END, str(result.real))
                        elif abs(result.real) == 0:
                            self.convert_bar.insert(ctk.END, str(f"{result.imag}j"))
                        else:
                            self.convert_bar.insert(ctk.END, str(result).strip("()"))

                    elif "∠" not in value:
                        complex_num = string_to_complex(value, angle_mode)

                        if angle_mode == "Degree":
                            phase_angle = math.degrees(cmath.phase(complex_num))
                        elif angle_mode == "Radian":
                            phase_angle = cmath.phase(complex_num)

                        rounded_degree = round(phase_angle, ndigits=int(self.decimal_places.get()))
                        amplitude = round(abs(complex_num), ndigits=int(self.decimal_places.get()))
                        self.convert_bar.delete(0, ctk.END)
                        self.convert_bar.insert(ctk.END, f"{amplitude}∠[{rounded_degree}]")

                except (ValueError, AttributeError, TypeError):
                    self.showwarning("Invalid input")
            else:
                self.showwarning("Please fill the entry properly")
        else:
            self.showwarning("Math error")

    def insert_symbol(self, symbol):
        focused_widget = App.focus_get(self) # Get the currently focused widget
        if isinstance(focused_widget, tk.Entry):
            focused_widget.insert(ctk.INSERT, symbol) # .insert() mean focus a the current position

    def show_result(self, msg):
        tkinter.messagebox.showinfo(title=None, message=msg)

    def showwarning(self, msg):
        tkinter.messagebox.showwarning(title=None, message=msg)

    def rounded(self, num):
        output_mode = self.output_mode.get()
        angle_mode = self.angle_unit_mode.get()

        if output_mode == "a+bj": #Rectangular form
            result = self.round_complex(num)

            # Return only value which is not zero
            if abs(result.imag) == 0: 
                return result.real
            elif abs(result.real) == 0:
                return (f"{result.imag}j")
            elif abs(result) == 0:
                return 0
            else:
                return (f"{result}").strip("()")
            
        elif output_mode == "r∠θ": #Polar form - Phasor
            phase_angle = cmath.phase(num) #Radian
            if angle_mode == "Degree":
                phase = math.degrees(phase_angle) #Degree
            elif angle_mode == "Radian":
                phase = phase_angle # Radian

            rounded_phase = round(phase, ndigits=int(self.decimal_places.get()))
            amplitude = round(abs(num), ndigits=int(self.decimal_places.get()))
            return f"{amplitude}∠[{rounded_phase}]"

    def round_complex(self, num):
        decimal_places = self.decimal_places.get()
        rounded_real = round(num.real, ndigits=int(decimal_places))
        rounded_imag = round(num.imag, ndigits=int(decimal_places))
        rounded_complex = complex(rounded_real, rounded_imag)
        return rounded_complex

    def cramer(self, widgets_list):
        try:
            fm = widgets_list

            if len(fm) == 6: #2x2 matrix
                matrix = [[fm[0], fm[1]], [fm[3], fm[4]]]
                matrix_x = [[fm[2], fm[1]],
                            [fm[5], fm[4]]]
                matrix_y = [[fm[0], fm[2]],
                            [fm[3], fm[5]]]
                x = self.det2x2(matrix_x)/self.det2x2(matrix)
                y = self.det2x2(matrix_y)/self.det2x2(matrix)
                self.show_result(f"x = {self.rounded(x)}\ny = {self.rounded(y)}")

            elif len(fm) == 12: #3x3 matrix
                matrix =  [[fm[0], fm[1], fm[2]],
                            [fm[4], fm[5], fm[6]],
                            [fm[8], fm[9], fm[10]],]
                matrix_x =  [[fm[3], fm[1], fm[2]],
                            [fm[7], fm[5], fm[6]],
                            [fm[11], fm[9], fm[10]]]
                matrix_y =  [[fm[0], fm[3], fm[2]],
                            [fm[4], fm[7], fm[6]],
                            [fm[8], fm[11], fm[10]]]
                matrix_z =  [[fm[0], fm[1], fm[3]],
                            [fm[4], fm[5], fm[7]],
                            [fm[8], fm[9], fm[11]]]
                
                x = self.det3x3(matrix_x)/self.det3x3(matrix)
                y  = self.det3x3(matrix_y)/self.det3x3(matrix)
                z  = self.det3x3(matrix_z)/self.det3x3(matrix)
                self.show_result(f"x = {self.rounded(x)}\ny = {self.rounded(y)}\nz = {self.rounded(z)}")

            elif len(fm) == 20: #4x4 matrix
                matrix = [[fm[0], fm[1], fm[2], fm[3]],
                            [fm[5], fm[6], fm[7], fm[8]],
                            [fm[10], fm[11], fm[12], fm[13]],
                            [fm[15], fm[16], fm[17], fm[18]]]
                
                matrix_w = [[fm[4], fm[1], fm[2], fm[3]],
                            [fm[9], fm[6], fm[7], fm[8]],
                            [fm[14], fm[11], fm[12], fm[13]],
                            [fm[19], fm[16], fm[17], fm[18]]]

                matrix_x = [[fm[0], fm[4], fm[2], fm[3]],
                            [fm[5], fm[9], fm[7], fm[8]],
                            [fm[10], fm[14], fm[12], fm[13]],
                            [fm[15], fm[19], fm[17], fm[18]]]   

                matrix_y = [[fm[0], fm[1], fm[4], fm[3]],
                            [fm[5], fm[6], fm[9], fm[8]],
                            [fm[10], fm[11], fm[14], fm[13]],
                            [fm[15], fm[16], fm[19], fm[18]]]
                
                matrix_z = [[fm[0], fm[1], fm[2], fm[4]],
                            [fm[5], fm[6], fm[7], fm[9]],
                            [fm[10], fm[11], fm[12], fm[14]],
                            [fm[15], fm[16], fm[17], fm[19]]]
                
                w = self.det4x4(matrix_w)/self.det4x4(matrix)
                x = self.det4x4(matrix_x)/self.det4x4(matrix)
                y  = self.det4x4(matrix_y)/self.det4x4(matrix)
                z  = self.det4x4(matrix_z)/self.det4x4(matrix)
                self.show_result(f"w = {self.rounded(w)}\nx = {self.rounded(x)}\ny = {self.rounded(y)}\nz = {self.rounded(z)}")
                
                
        except ZeroDivisionError:
            self.show_result("Infinite or no solution")

    def det2x2(self, matrix):
        det2 = matrix[0][0] * matrix[1][1] - matrix[1][0] * matrix[0][1]
        return det2
            
    def det3x3(self, matrix):
        temp_matrix = []
        for row in range(3):
            row_temp = [] # New temporary row for each iteration
            for column in range(5): #Included the added columns
                added_column = column%3 # Added columns for det operation
                row_temp.append(matrix[row][added_column]) # Add extra columns to each row
            temp_matrix.insert(row, row_temp) # Insert new modified row

        det3 = 0
        for i in range(len(matrix)):
            det3 += temp_matrix[0][i] * temp_matrix[1][i+1] * temp_matrix[2][i+2]
            det3 -= temp_matrix[2][i] * temp_matrix[1][i+1] * temp_matrix[0][i+2]
        return det3

    def det4x4(self, matrix):
        det4 = 0
        for num, element in enumerate(matrix[0]): #Revolving the first row of the matrix
            cofactored_matrix =[]
            for row in range(1, 4): #Operation within row 2-4 only
                temp_row = []
                for index, column in enumerate(range(4)): 
                    if index != num: # Need to remove the cofactered column one
                        temp_row.append(matrix[row][column])
                cofactored_matrix.append(temp_row)
            # Got one cofactored matrix here
            det4 += (-1) ** num * element * self.det3x3(cofactored_matrix) #Add up the product of cofactered numbers and elements
        return det4
    
    def slide_transparency(self, x):
        self.attributes('-alpha', self.transparency.get())

    def info_page(self):

        self.clearFrame()

        #Reset grid configurations
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(7, weight=0)

        # Scrollable info
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.scrollable_frame = ctk.CTkScrollableFrame(self, label_text=None)
        self.scrollable_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nswe", columnspan=3)
        self.scrollable_frame.grid_columnconfigure(1, weight=1)

        # Instruction
        self.instruction = ctk.CTkLabel(self.scrollable_frame, text="What does this program do?", font=ctk.CTkFont(size=28, weight="bold"))
        self.instruction.grid(row=0, column=0, padx=(20,5), pady=20, sticky="w", columnspan=2)
        self.instruction_label = ctk.CTkTextbox(self.scrollable_frame, width=250, font=ctk.CTkFont(size=16, weight="normal"), wrap="word", fg_color="transparent", height=150)
        self.instruction_label.grid(row=1, column=0, padx=(40, 100), pady=(20, 0), sticky="nsew", columnspan=2)
        self.instruction_label.insert("0.0", "This calculator solves systems of linear equations with four unknown variables. Enter the coefficients of the variables and the constants on the right side of each equation. All input fields must be filled. Use '0' for missing variables. For example, Equation: x + 2y - z = 3 can be written as 0w + x + 2y - z = 3. A minus operator is replaced by a plus operator and a negative coefficient of a variable. For instance, Equation: 2w - 3x + 4y − 5z = 10 should be written as 2w + -3x + 4y + −5z = 10. Decimal places in the results can be specified.")
        self.instruction_label.configure(state="disabled")

        # Supported input
        self.support_input = ctk.CTkLabel(self.scrollable_frame, text="Supported input", font=ctk.CTkFont(size=28, weight="bold"))
        self.support_input.grid(row=2, column=0, padx=(20,5), pady=20, sticky="w", columnspan=2)

        # Simple arithmetic function
        self.linear = ctk.CTkLabel(self.scrollable_frame, text="1. Simple arithmetic operation", font=ctk.CTkFont(size=20, weight="bold"), text_color="Dark orange")
        self.linear.grid(row=3, column=0, padx=(40,5), pady=(5), sticky="w", columnspan=2)
        self.linear_label = ctk.CTkLabel(self.scrollable_frame, text="For example, 1/2+3*4-5 will yield 7.5, formats below are supported as well.", font=ctk.CTkFont(size=16, weight="normal"))
        self.linear_label.grid(row=4, column=0, padx=(60,5), pady=5, sticky="w", columnspan=2)

        # Complex number
        self.complex = ctk.CTkLabel(self.scrollable_frame, text="2. Complex numbers", font=ctk.CTkFont(size=20, weight="bold"), text_color="Dark orange")
        self.complex.grid(row=5, column=0, padx=(40,5), pady=(5), sticky="w", columnspan=2)

        self.rectangular = ctk.CTkLabel(self.scrollable_frame, text="• Rectangular form (a+bj) —— e.g. 2+3j, -4-j", font=ctk.CTkFont(size=16, weight="normal"))
        self.rectangular.grid(row=6, column=0, padx=(60,5), pady=5, sticky="w", columnspan=2)

        self.polar = ctk.CTkLabel(self.scrollable_frame, text="• Polar form (r∠[θ]) when θ is the phase angle —— e.g. 4∠[30], -5∠[π/2]", font=ctk.CTkFont(size=16, weight="normal"))
        self.polar.grid(row=7, column=0, padx=(60,5), pady=5, sticky="w", columnspan=2)


        # Trigonometric function
        self.trigon = ctk.CTkLabel(self.scrollable_frame, text="3. Trigonometric functions", font=ctk.CTkFont(size=20, weight="bold"), text_color="Dark orange")
        self.trigon.grid(row=8, column=0, padx=(40,5), pady=(5), sticky="w", columnspan=2)
        self.trigon_label = ctk.CTkLabel(self.scrollable_frame, text="Written in func(θ): i.e. sin(θ), cos(θ), tan(θ), csc(θ), sec(θ), cot(θ)", font=ctk.CTkFont(size=16, weight="normal"))
        self.trigon_label.grid(row=9, column=0, padx=(60,5), pady=5, sticky="w", columnspan=2)

        # Logarithmic function
        self.log = ctk.CTkLabel(self.scrollable_frame, text="4. Logarithmic functions", font=ctk.CTkFont(size=20, weight="bold"), text_color="Dark orange")
        self.log.grid(row=10, column=0, padx=(40,5), pady=(5), sticky="w", columnspan=2)
        self.log_label = ctk.CTkLabel(self.scrollable_frame, text="Written in log[x,base]: e.g. log[3,5] will return the log value of 3 with base of 5.", font=ctk.CTkFont(size=16, weight="normal"))
        self.log_label.grid(row=11, column=0, padx=(60,5), pady=5, sticky="w", columnspan=2)
        self.log_label_2 = ctk.CTkLabel(self.scrollable_frame, text="Base will automatically be set to 10 if left undefined e.g. log[5]", font=ctk.CTkFont(size=16, weight="normal"))
        self.log_label_2.grid(row=12, column=0, padx=(60,5), pady=5, sticky="w", columnspan=2)

        # Members
        self.support_input = ctk.CTkLabel(self.scrollable_frame, text="Developers", font=ctk.CTkFont(size=28, weight="bold"))
        self.support_input.grid(row=13, column=0, padx=(20,5), pady=(40, 20), sticky="w", columnspan=2)

        devs = {"Thanawan Kraipattarakul": "415          Back-end developer", "Nuttiwut Daengmanee": "451          Algorithm specialist", "Taksarayut Sripapong": "452          UX/UI developer"}
        for i, student in enumerate(devs):
                self.student = ctk.CTkLabel(self.scrollable_frame, text=student, font=ctk.CTkFont(size=16, weight="normal"))
                self.student.grid(row=i+14, column=0, padx=(60,0), pady=(5,10), sticky="w")

                self.student_id = ctk.CTkLabel(self.scrollable_frame, text=f"66070500{devs[student]}", font=ctk.CTkFont(size=16, weight="normal"), text_color="grey")
                self.student_id.grid(row=i+14, column=1, padx=40, pady=(5,10), sticky="w")


        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self, values=["- Themes -","System", "Light", "Dark"],
                                                                       command=self.change_appearance_mode)
        self.appearance_mode_optionemenu.grid(row=1, column=0, padx=(20,5), pady=(3, 17), sticky="we")

        # Back button
        self.back = ctk.CTkButton(self, command=self.show_main, text="Back", font=ctk.CTkFont(size=16, weight="normal"))
        self.back.grid(row=1, column=2, padx=20, pady=(5,20), sticky="nswe")

    def clearFrame(self):
        # Destroy all widgets from frame
        for widget in App.winfo_children(self):
            widget.destroy()
    
    def change_appearance_mode(self, new_appearance_mode):
        if new_appearance_mode != "- Themes -":
            ctk.set_appearance_mode(new_appearance_mode)
    
    def show_main(self):
        self.clearFrame()
        self.main_frame()

if __name__ == "__main__":
    app = App()
    app.mainloop()
