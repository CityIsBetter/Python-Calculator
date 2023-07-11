import tkinter as tk
import math

SMALL_FONT_STYLE = ("Arial", 16)
LARGE_FONT_STYLE = ("Arial", 40, "bold")
DIGIT_FONT_STYLE = ("Arial", 24, "bold")
DEFAULT_FONT_STYLE = ("Arial", 20)

OFF_WHITE = '#f8f8ff'
WHITE = "#ffffff"
RED = "#F98B85"
D_RED = "#C76F6A"
LIGHT_BLUE = "#CCEDF5"
LIGHT_GRAY = "#f5f5f5"
LABEL_COLOR = "#25265E"

class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("375x667")

        self.window.title("Python Calculator")

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
        button.grid(row=5, column=3, columnspan=2, sticky=tk.NSEW)
        
    def create_buttons_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame

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