import tkinter as tk
import math

SMALL_FONT_STYLE = ("Arial", 16)
LARGE_FONT_STYLE = ("Arial", 40, "bold")
DIGIT_FONT_STYLE = ("Arial", 24, "bold")
DEFAULT_FONT_STYLE = ("Arial", 20)

dark = False

OFF_WHITE ='#f8f8ff' 
WHITE = "#ffffff" 
RED = "#FF4D4D"
D_RED = "#C76F6A"
LIGHT_BLUE = "#25A7DA"
LIGHT_GRAY = "#f5f5f5"
LABEL_COLOR = "#25265E"

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class Calculator:
    
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("375x667")

        self.window.title("Python Calculator")
        self.window.iconbitmap(resource_path('icon.ico'))

        self.total_expression = ""
        self.current_expression = ""
        self.display_frame = self.create_display_frame()
        self.total_label, self.label = self.create_display_labels()
        self.digits = {
            7: (1, 1), 8: (1, 2), 9: (1, 3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            1: (3, 1), 2: (3, 2), 3: (3, 3),
            0: (4, 2), '.': (4, 1)
        } 
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}
        self.buttons_frame = self.create_buttons_frame()
        self.buttons_frame.rowconfigure(0, weight=1)
        self.buttons_frame.rowconfigure(5, weight=1)
        for x in range(1, 5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)
        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()
        self.menu()
        self.bind_keys()

    def bind_keys(self):
        self.window.bind("<Return>", lambda event: self.evaluate())
        self.window.bind("<BackSpace>", lambda event: self.backspace())
        for key in self.digits:
            self.window.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))

        for key in self.operations:
            self.window.bind(key, lambda event, operator=key: self.append_operator(operator))

    def create_special_buttons(self):
        self.create_clear_button()
        self.create_equals_button()
        self.create_sqaure_button()
        self.create_sqrt_button()
        self.create_backspace_button()
        self.create_sin_button()
        self.create_cos_button()
        self.create_tan_button()

    def create_display_labels(self):
        total_label = tk.Label(self.display_frame, text=self.total_expression, anchor=tk.E, fg=LABEL_COLOR, bg=LIGHT_GRAY, padx=24, font=SMALL_FONT_STYLE)
        total_label.pack(expand=True, fill="both")

        label = tk.Label(self.display_frame, text=self.total_expression, anchor=tk.E, fg=LABEL_COLOR, bg=LIGHT_GRAY, padx=24, font=LARGE_FONT_STYLE)
        label.pack(expand=True, fill="both")

        return total_label, label

    def create_display_frame(self):
        frame = tk.Frame(self.window, height=221, bg=LIGHT_GRAY)
        frame.pack(expand=True, fill="both")
        return frame
    
    def add_to_expression(self, value):
        self.current_expression += str(value)
        self.update_label()
    
    def create_digit_buttons(self):
        for digit, grid_value in self.digits.items():
            button = tk.Button(self.buttons_frame, text=str(digit), bg=WHITE, fg=LABEL_COLOR, font=DIGIT_FONT_STYLE, borderwidth=0, command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_value[0]+1, column=grid_value[1], sticky=tk.NSEW, padx=1, pady=1)

    def append_operator(self, operator):
        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ""
        self.update_total_label()
        self.update_label()

    def create_operator_buttons(self):
        i = 0
        for operator, symbol in self.operations.items():
            button = tk.Button(self.buttons_frame, text=symbol, bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=lambda x=operator: self.append_operator(x))
            button.grid(row=i+1, column=4, sticky=tk.NSEW, padx=1, pady=1)
            i += 1

    def clear(self):
        self.current_expression = ''
        self.total_expression = ''
        self.update_label()
        self.update_total_label()

    def create_clear_button(self):
        button = tk.Button(self.buttons_frame, text="C", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.clear)
        button.grid(row=1, column=1, sticky=tk.NSEW, padx=1, pady=1)

    def sqaure(self):
        self.current_expression = str(eval(f"{self.current_expression}**2"))
        self.update_label()

    def create_sqaure_button(self):
        button = tk.Button(self.buttons_frame, text="x\u00b2", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.sqaure)
        button.grid(row=1, column=2, sticky=tk.NSEW, padx=1, pady=1)

    def sqrt(self):
        self.current_expression = str(eval(f"{self.current_expression}**0.5"))
        self.update_label()

    def create_sqrt_button(self):
        button = tk.Button(self.buttons_frame, text="\u221ax", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.sqrt)
        button.grid(row=1, column=3, sticky=tk.NSEW, padx=1, pady=1)

    def backspace(self):
        self.current_expression = self.current_expression[:-1]
        self.update_label()

    def create_backspace_button(self):
        button = tk.Button(self.buttons_frame, text="←", bg=RED, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, activebackground=D_RED, borderwidth=0, command=self.backspace)
        button.grid(row=0, column=4, sticky=tk.NSEW, padx=1, pady=1)

    def calc_sin(self):
        angle = float(self.current_expression)
        self.current_expression = str(math.sin(angle))
        self.update_label()
    
    def create_sin_button(self):
        button = tk.Button(self.buttons_frame, text="Sin", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.calc_sin)
        button.grid(row=0, column=1, sticky=tk.NSEW, padx=1, pady=1)

    def calc_cos(self):
        angle = float(self.current_expression)
        self.current_expression = str(math.cos(angle))
        self.update_label()
    
    def create_cos_button(self):
        button = tk.Button(self.buttons_frame, text="Cos", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.calc_cos)
        button.grid(row=0, column=2, sticky=tk.NSEW, padx=1, pady=1)

    def calc_tan(self):
        angle = float(self.current_expression)
        self.current_expression = str(math.tan(angle))
        self.update_label()
    
    def create_tan_button(self):
        button = tk.Button(self.buttons_frame, text="Tan", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.calc_tan)
        button.grid(row=0, column=3, sticky=tk.NSEW, padx=1, pady=1)

    def evaluate(self):
        self.total_expression += self.current_expression
        self.update_total_label()
        try:
            self.current_expression = str(eval(self.total_expression))
            self.total_expression = ""
        except Exception as e:
            self.current_expression = "Math Error"
        self.update_label()
    
    def create_equals_button(self):
        button = tk.Button(self.buttons_frame, text="=", bg=LIGHT_BLUE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE, borderwidth=0, command=self.evaluate)
        button.grid(row=5, column=3, columnspan=2, sticky=tk.NSEW, padx=1, pady=1)
        
    def create_buttons_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame
    
    def set_light(self):
        global dark, OFF_WHITE, WHITE, LIGHT_GRAY, LABEL_COLOR
        OFF_WHITE ='#f8f8ff' 
        WHITE = "#ffffff"
        LIGHT_GRAY = "#f5f5f5"
        LABEL_COLOR = "#25265E"
        dark = False
        self.create_special_buttons()
        self.create_digit_buttons()
        self.create_operator_buttons()
        self.total_label.config(bg=LIGHT_GRAY, fg=LABEL_COLOR)
        self.label.config(bg=LIGHT_GRAY, fg=LABEL_COLOR)

    def set_dark(self):
        global dark, OFF_WHITE, WHITE, LIGHT_GRAY, LABEL_COLOR
        OFF_WHITE = "#383838"
        WHITE = "#505050"
        LIGHT_GRAY = "#202020"
        LABEL_COLOR = "#eee"
        dark = True
        self.create_special_buttons()
        self.create_digit_buttons()
        self.create_operator_buttons()
        self.total_label.config(bg=LIGHT_GRAY, fg=LABEL_COLOR)
        self.label.config(bg=LIGHT_GRAY, fg=LABEL_COLOR)

    def menu(self):
        def toggle_menu():
            def close_menu():
                menu.destroy()
                btn.config(text="≡")
                btn.config(command=toggle_menu)

            menu = tk.Frame(self.window, bg=LIGHT_GRAY)
            menu.place(x=0, y=50, height=120, width=100)
            Light_btn = tk.Button(menu, text="Light", font=DIGIT_FONT_STYLE, fg="#eee", bg=RED, activebackground=LIGHT_BLUE, borderwidth=0, command=self.set_light)
            Light_btn.place(x=0, y=0)
            Dark_btn = tk.Button(menu, text="Dark ", font=DIGIT_FONT_STYLE, fg="#eee", bg=RED, activebackground=LIGHT_BLUE, borderwidth=0, command= self.set_dark)
            Dark_btn.place(x=0, y=60)

            btn.config(text="X")
            btn.config(command=close_menu)

        btn = tk.Button(self.display_frame, text='≡',bg=LIGHT_BLUE, fg="#333", font=("Bold", 20), borderwidth=0, command=toggle_menu)
        btn.pack(side=tk.LEFT)
        btn.place(x=0, y=0)
        
    def update_total_label(self):
        expression = self.total_expression
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f'{symbol}')
        self.total_label.config(text=expression)

    def update_label(self):
        self.label.config(text=self.current_expression[:11])
    def run(self):
        self.window.mainloop()

if __name__ == '__main__':
    calc = Calculator()
    calc.run()