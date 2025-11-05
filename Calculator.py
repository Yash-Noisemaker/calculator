import tkinter as tk
from tkinter import *
import requests
import json
from datetime import datetime

# Color Scheme 
DARK_BG = "#1e1e1e"
DARK_FG = "#ffffff"
DARK_SECONDARY = "#2d2d2d"
DARK_ACCENT = "#3d3d3d"
DARK_HOVER = "#4a4a4a"
CALC_DISPLAY_BG = "#323232"
CALC_BUTTON_BG = "#404040"
CALC_OPERATOR_BG = "#ff9500"
CALC_SPECIAL_BG = "#a6a6a6"
SUCCESS_GREEN = "#4CAF50"
ERROR_RED = "#f44336"
INFO_BLUE = "#2196F3"

# Calculator
def update_display(value):
    """Update the display with button values"""
    current_text = display_var.get()
    if current_text == "0" or current_text == "Error":
        display_var.set(value)
    else:
        display_var.set(current_text + value)

def clear_display():
    """Clear the display"""
    display_var.set("0")

def backspace():
    """Remove the last character from display"""
    current_text = display_var.get()
    if current_text != "0" and current_text != "Error":
        if len(current_text) == 1:
            display_var.set("0")
        else:
            display_var.set(current_text[:-1])

def calculate_result():
    """Evaluate the expression and display result"""
    try:
        result = eval(display_var.get())
        display_var.set(str(result))
    except Exception as e:
        display_var.set("Error")

# Exchange Rates Functions
def show_calculator():
    """Show calculator interface"""
    exchange_rates_frame.pack_forget()
    unit_converter_frame.pack_forget()
    calculator_frame.pack(fill=tk.BOTH, expand=True)

def show_exchange_rates():
    """Show exchange rates interface"""
    calculator_frame.pack_forget()
    unit_converter_frame.pack_forget()
    exchange_rates_frame.pack(fill=tk.BOTH, expand=True)
    update_exchange_rates()

def show_unit_converter():
    """Show unit converter interface"""
    calculator_frame.pack_forget()
    exchange_rates_frame.pack_forget()
    unit_converter_frame.pack(fill=tk.BOTH, expand=True)

def update_exchange_rates():
    """Fetch and display current exchange rates"""
    try:
        
        response = requests.get("https://api.exchangerate-api.com/v4/latest/USD")
        data = response.json()
        
        rates = data['rates']
        last_updated = datetime.fromtimestamp(data['time_last_updated']).strftime('%Y-%m-%d %H:%M:%S')
        
        for widget in rates_frame.winfo_children():
            widget.destroy()
        
        
        time_label.config(text=f"Last Updated: {last_updated}")
        
        popular_currencies = {
            'EUR': 'Euro',
            'GBP': 'British Pound',
            'JPY': 'Japanese Yen',
            'CAD': 'Canadian Dollar',
            'AUD': 'Australian Dollar',
            'CHF': 'Swiss Franc',
            'CNY': 'Chinese Yuan',
            'INR': 'Indian Rupee'
        }
         
        header_frame = tk.Frame(rates_frame, bg=DARK_ACCENT)
        header_frame.pack(fill=tk.X, padx=5, pady=2)
        
        tk.Label(header_frame, text="Currency", font=("Arial", 12, "bold"), 
                bg=DARK_ACCENT, fg=DARK_FG, width=15, anchor="w").pack(side=tk.LEFT)
        tk.Label(header_frame, text="Rate (1 USD = )", font=("Arial", 12, "bold"), 
                bg=DARK_ACCENT, fg=DARK_FG, width=15, anchor="w").pack(side=tk.LEFT)
          
        for currency_code, currency_name in popular_currencies.items():
            if currency_code in rates:
                rate_frame = tk.Frame(rates_frame, bg=DARK_SECONDARY)
                rate_frame.pack(fill=tk.X, padx=5, pady=1)
                
                currency_text = f"{currency_code} - {currency_name}"
                rate_value = f"{rates[currency_code]:.4f}"
                
                tk.Label(rate_frame, text=currency_text, font=("Arial", 10), 
                        bg=DARK_SECONDARY, fg=DARK_FG, width=25, anchor="w").pack(side=tk.LEFT)
                tk.Label(rate_frame, text=rate_value, font=("Arial", 10), 
                        bg=DARK_SECONDARY, fg=DARK_FG, width=15, anchor="w").pack(side=tk.LEFT)
        
        status_label.config(text="Rates updated successfully!", fg=SUCCESS_GREEN)
        
    except Exception as e:
        status_label.config(text=f"Error fetching rates: {str(e)}", fg=ERROR_RED)

def convert_currency():
    """Convert currency based on user input"""
    try:
        amount = float(amount_entry.get())
        from_currency = from_currency_var.get().upper()
        to_currency = to_currency_var.get().upper()
        
        if not from_currency or not to_currency:
            status_label.config(text="Please select both currencies", fg=ERROR_RED)
            return
            
        response = requests.get(f"https://api.exchangerate-api.com/v4/latest/{from_currency}")
        data = response.json()
        
        if to_currency in data['rates']:
            rate = data['rates'][to_currency]
            converted_amount = amount * rate
            result_label.config(text=f"{amount} {from_currency} = {converted_amount:.2f} {to_currency}")
            status_label.config(text="Conversion successful!", fg=SUCCESS_GREEN)
        else:
            status_label.config(text="Invalid currency code", fg=ERROR_RED)
            
    except ValueError:
        status_label.config(text="Please enter a valid amount", fg=ERROR_RED)
    except Exception as e:
        status_label.config(text=f"Conversion error: {str(e)}", fg=ERROR_RED)

# Unit Converter Functions
def show_conversion_category(category):
    """Show the appropriate conversion interface based on category"""
    
    for frame in conversion_frames.values():
        frame.pack_forget()
     
    conversion_frames[category].pack(fill=tk.BOTH, expand=True)
        
    category_label.config(text=f"{category.capitalize()} Converter")
    
    result_var.set("")

def convert_units():
    """Convert units based on selected category and units"""
    try:
        value = float(entry_var.get())
        category = current_category.get()
        from_unit = from_unit_var.get()
        to_unit = to_unit_var.get()
        
        if not from_unit or not to_unit:
            result_var.set("Please select units")
            return
        
        # Conversion factors
        conversions = {
            'length': {
                'meters': 1,
                'kilometers': 1000,
                'centimeters': 0.01,
                'millimeters': 0.001,
                'miles': 1609.34,
                'yards': 0.9144,
                'feet': 0.3048,
                'inches': 0.0254
            },
            'area': {
                'sq meters': 1,
                'sq kilometers': 1000000,
                'sq miles': 2589988.11,
                'acres': 4046.86,
                'hectares': 10000,
                'sq feet': 0.092903,
                'sq yards': 0.836127,
                'sq inches': 0.00064516
            },
            'volume': {
                'liters': 1,
                'milliliters': 0.001,
                'cubic meters': 1000,
                'cubic feet': 28.3168,
                'cubic inches': 0.0163871,
                'gallons': 3.78541,
                'quarts': 0.946353,
                'pints': 0.473176
            },
            'speed': {
                'm/s': 1,
                'km/h': 0.277778,
                'mph': 0.44704,
                'knots': 0.514444,
                'ft/s': 0.3048
            },
            'weight': {
                'kilograms': 1,
                'grams': 0.001,
                'pounds': 0.453592,
                'ounces': 0.0283495,
                'tons': 1000,
                'metric tons': 1000
            },
            'temperature': {
                'celsius': 'celsius',
                'fahrenheit': 'fahrenheit', 
                'kelvin': 'kelvin'
            },
            'power': {
                'watts': 1,
                'kilowatts': 1000,
                'horsepower': 745.7,
                'btu/min': 17.584
            },
            'pressure': {
                'pascals': 1,
                'kilopascals': 1000,
                'bar': 100000,
                'psi': 6894.76,
                'atm': 101325
            }
        }
        
        if category in conversions and from_unit in conversions[category] and to_unit in conversions[category]:
            if category == 'temperature':
                # Temperature conversion
                if from_unit == 'celsius':
                    if to_unit == 'fahrenheit':
                        result = (value * 9/5) + 32
                    elif to_unit == 'kelvin':
                        result = value + 273.15
                    else:
                        result = value
                elif from_unit == 'fahrenheit':
                    if to_unit == 'celsius':
                        result = (value - 32) * 5/9
                    elif to_unit == 'kelvin':
                        result = (value - 32) * 5/9 + 273.15
                    else:
                        result = value
                elif from_unit == 'kelvin':
                    if to_unit == 'celsius':
                        result = value - 273.15
                    elif to_unit == 'fahrenheit':
                        result = (value - 273.15) * 9/5 + 32
                    else:
                        result = value
            else:
                # Standard conversion
                from_factor = conversions[category][from_unit]
                to_factor = conversions[category][to_unit]
                result = value * from_factor / to_factor
            
            result_var.set(f"{value:.4f} {from_unit} = {result:.6f} {to_unit}")
        else:
            result_var.set("Invalid unit selection")
            
    except ValueError:
        result_var.set("Please enter a valid number")


def configure_dark_theme():
    """Configure dark theme for all widgets"""
    # Configure style for OptionMenu
    root.option_add('*TCombobox*Listbox.background', DARK_SECONDARY)
    root.option_add('*TCombobox*Listbox.foreground', DARK_FG)
    root.option_add('*TCombobox*Listbox.selectBackground', DARK_HOVER)
    root.option_add('*TCombobox*Listbox.selectForeground', DARK_FG)

# Main window
root = tk.Tk()
root.title("Multi-Function Calculator :)")
root.geometry("500x600")
root.resizable(0, 0)  # Prevent resizing
root.configure(bg=DARK_BG)

configure_dark_theme()

# Menu Bar 
menu_bar = Menu(root, bg=DARK_SECONDARY, fg=DARK_FG, activebackground=DARK_HOVER, activeforeground=DARK_FG)

# Calculator menu
cal = Menu(menu_bar, tearoff=0, bg=DARK_SECONDARY, fg=DARK_FG, activebackground=DARK_HOVER, activeforeground=DARK_FG)
cal.add_command(label="Open Calculator", command=show_calculator)
menu_bar.add_cascade(label="Calculator", menu=cal)

# Exchange Rates menu
exchange = Menu(menu_bar, tearoff=0, bg=DARK_SECONDARY, fg=DARK_FG, activebackground=DARK_HOVER, activeforeground=DARK_FG)
exchange.add_command(label="Open Exchange Rates", command=show_exchange_rates)
menu_bar.add_cascade(label="Exchange Rates", menu=exchange)

# Unit Converter menu
unit_conv = Menu(menu_bar, tearoff=0, bg=DARK_SECONDARY, fg=DARK_FG, activebackground=DARK_HOVER, activeforeground=DARK_FG)
unit_conv.add_command(label="Length", command=lambda: show_unit_converter_category('length'))
unit_conv.add_command(label="Area", command=lambda: show_unit_converter_category('area'))
unit_conv.add_command(label="Volume", command=lambda: show_unit_converter_category('volume'))
unit_conv.add_command(label="Speed", command=lambda: show_unit_converter_category('speed'))
unit_conv.add_command(label="Weight", command=lambda: show_unit_converter_category('weight'))
unit_conv.add_command(label="Temperature", command=lambda: show_unit_converter_category('temperature'))
unit_conv.add_command(label="Power", command=lambda: show_unit_converter_category('power'))
unit_conv.add_command(label="Pressure", command=lambda: show_unit_converter_category('pressure'))
menu_bar.add_cascade(label="Unit Converter", menu=unit_conv)

root.config(menu=menu_bar)

# Main container frame
main_frame = tk.Frame(root, bg=DARK_BG)
main_frame.pack(fill=tk.BOTH, expand=True)

# Calculator Frame
calculator_frame = tk.Frame(main_frame, bg=DARK_BG)

# Display variable for calculator
display_var = tk.StringVar()
display_var.set("0")

# Display label for calculator
display_label = tk.Label(
    calculator_frame, 
    textvariable=display_var,
    font=("Arial", 20),
    anchor="e",
    bg=CALC_DISPLAY_BG,
    fg=DARK_FG,
    padx=10,
    pady=10,
    relief="sunken"
)
display_label.pack(fill=tk.X, padx=10, pady=10)

# Button layout for calculator
button_layout = [
    ('C', 1, 0), ('⌫', 1, 1), ('/', 1, 2), ('*', 1, 3),
    ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('-', 2, 3),
    ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('+', 3, 3),
    ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('=', 4, 3),
    ('0', 5, 0), ('.', 5, 1)
]

# Button frame for calculator
button_frame = tk.Frame(calculator_frame, bg=DARK_BG)
button_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Create and place calculator buttons
for (text, row, col) in button_layout:
    if text == '=':
        button = tk.Button(
            button_frame,
            text=text,
            font=("Arial", 16),
            bg=CALC_OPERATOR_BG,
            fg=DARK_FG,
            activebackground="#ffb143",
            activeforeground=DARK_FG,
            command=calculate_result
        )
        button.grid(
            row=row, 
            column=col, 
            rowspan=2,
            sticky="nsew", 
            padx=2, 
            pady=2
        )
    elif text == 'C':
        button = tk.Button(
            button_frame,
            text=text,
            font=("Arial", 16),
            bg=CALC_SPECIAL_BG,
            fg=DARK_BG,
            activebackground="#bfbfbf",
            activeforeground=DARK_BG,
            command=clear_display
        )
        button.grid(
            row=row, 
            column=col, 
            sticky="nsew", 
            padx=2, 
            pady=2
        )
    elif text == '⌫':
        button = tk.Button(
            button_frame,
            text=text,
            font=("Arial", 16),
            bg=CALC_SPECIAL_BG,
            fg=DARK_BG,
            activebackground="#bfbfbf",
            activeforeground=DARK_BG,
            command=backspace
        )
        button.grid(
            row=row, 
            column=col, 
            sticky="nsew", 
            padx=2, 
            pady=2
        )
    elif text in ['/', '*', '-', '+']:
        button = tk.Button(
            button_frame,
            text=text,
            font=("Arial", 16),
            bg=CALC_OPERATOR_BG,
            fg=DARK_FG,
            activebackground="#ffb143",
            activeforeground=DARK_FG,
            command=lambda t=text: update_display(t)
        )
        button.grid(
            row=row, 
            column=col, 
            sticky="nsew", 
            padx=2, 
            pady=2
        )
    else:
        button = tk.Button(
            button_frame,
            text=text,
            font=("Arial", 16),
            bg=CALC_BUTTON_BG,
            fg=DARK_FG,
            activebackground=DARK_HOVER,
            activeforeground=DARK_FG,
            command=lambda t=text: update_display(t)
        )
        button.grid(
            row=row, 
            column=col, 
            sticky="nsew", 
            padx=2, 
            pady=2
        )

# Configure grid weights for calculator
for i in range(6):
    button_frame.grid_rowconfigure(i, weight=1)
for i in range(4):
    button_frame.grid_columnconfigure(i, weight=1)

# Exchange Rates Frame
exchange_rates_frame = tk.Frame(main_frame, bg=DARK_BG)

# Title
title_label = tk.Label(
    exchange_rates_frame,
    text="Currency Exchange Rates",
    font=("Arial", 18, "bold"),
    bg=DARK_BG,
    fg=DARK_FG,
    pady=10
)
title_label.pack()

# Last updated time
time_label = tk.Label(
    exchange_rates_frame,
    text="Last Updated: --",
    font=("Arial", 10),
    bg=DARK_BG,
    fg="#aaaaaa",
)
time_label.pack()



rates_container = tk.Frame(exchange_rates_frame, bg=DARK_BG)
rates_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

canvas = tk.Canvas(rates_container, height=200, bg=DARK_BG, highlightthickness=0)
scrollbar = tk.Scrollbar(rates_container, orient="vertical", command=canvas.yview, bg=DARK_ACCENT)
scrollable_frame = tk.Frame(canvas, bg=DARK_BG)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set, bg=DARK_BG)

rates_frame = scrollable_frame

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# Currency conversion 
conversion_frame = tk.LabelFrame(
    exchange_rates_frame,
    text="Currency Converter",
    font=("Arial", 12, "bold"),
    bg=DARK_BG,
    fg=DARK_FG,
    padx=10,
    pady=10
)
conversion_frame.pack(fill=tk.X, padx=10, pady=10)

# Amount input
amount_frame = tk.Frame(conversion_frame, bg=DARK_BG)
amount_frame.pack(fill=tk.X, pady=5)

tk.Label(amount_frame, text="Amount:", font=("Arial", 10), bg=DARK_BG, fg=DARK_FG).pack(side=tk.LEFT)
amount_entry = tk.Entry(amount_frame, font=("Arial", 10), width=15, bg=DARK_SECONDARY, fg=DARK_FG, insertbackground=DARK_FG)
amount_entry.pack(side=tk.LEFT, padx=5)
amount_entry.insert(0, "1.00")

# Currency selection
currency_frame = tk.Frame(conversion_frame, bg=DARK_BG)
currency_frame.pack(fill=tk.X, pady=5)

tk.Label(currency_frame, text="From:", font=("Arial", 10), bg=DARK_BG, fg=DARK_FG).pack(side=tk.LEFT)
from_currency_var = tk.StringVar()
from_currency_entry = tk.Entry(currency_frame, textvariable=from_currency_var, 
                              font=("Arial", 10), width=8, bg=DARK_SECONDARY, fg=DARK_FG, insertbackground=DARK_FG)
from_currency_entry.pack(side=tk.LEFT, padx=5)
from_currency_entry.insert(0, "USD")

tk.Label(currency_frame, text="To:", font=("Arial", 10), bg=DARK_BG, fg=DARK_FG).pack(side=tk.LEFT)
to_currency_var = tk.StringVar()
to_currency_entry = tk.Entry(currency_frame, textvariable=to_currency_var, 
                            font=("Arial", 10), width=8, bg=DARK_SECONDARY, fg=DARK_FG, insertbackground=DARK_FG)
to_currency_entry.pack(side=tk.LEFT, padx=5)
to_currency_entry.insert(0, "EUR")

# Convert button
convert_button = tk.Button(
    conversion_frame,
    text="Convert",
    font=("Arial", 12, "bold"),
    bg=SUCCESS_GREEN,
    fg=DARK_FG,
    activebackground="#45a049",
    activeforeground=DARK_FG,
    command=convert_currency
)
convert_button.pack(pady=10)

# Result label
result_label = tk.Label(
    conversion_frame,
    text="",
    font=("Arial", 12, "bold"),
    bg=DARK_BG,
    fg=INFO_BLUE
)
result_label.pack()

# Status label
status_label = tk.Label(
    exchange_rates_frame,
    text="",
    font=("Arial", 10),
    bg=DARK_BG,
    pady=5
)
status_label.pack()

# Refresh button
refresh_button = tk.Button(
    exchange_rates_frame,
    text="Refresh Rates",
    font=("Arial", 10),
    bg=INFO_BLUE,
    fg=DARK_FG,
    activebackground="#1976D2",
    activeforeground=DARK_FG,
    command=update_exchange_rates
)
refresh_button.pack(pady=5)

# Unit Converter Frame
unit_converter_frame = tk.Frame(main_frame, bg=DARK_BG)

# Unit Converter Variables
current_category = tk.StringVar()
entry_var = tk.StringVar()
result_var = tk.StringVar()
from_unit_var = tk.StringVar()
to_unit_var = tk.StringVar()

# Unit categories and their units
unit_categories = {
    'length': ['meters', 'kilometers', 'centimeters', 'millimeters', 'miles', 'yards', 'feet', 'inches'],
    'area': ['sq meters', 'sq kilometers', 'sq miles', 'acres', 'hectares', 'sq feet', 'sq yards', 'sq inches'],
    'volume': ['liters', 'milliliters', 'cubic meters', 'cubic feet', 'cubic inches', 'gallons', 'quarts', 'pints'],
    'speed': ['m/s', 'km/h', 'mph', 'knots', 'ft/s'],
    'weight': ['kilograms', 'grams', 'pounds', 'ounces', 'tons', 'metric tons'],
    'temperature': ['celsius', 'fahrenheit', 'kelvin'],
    'power': ['watts', 'kilowatts', 'horsepower', 'btu/min'],
    'pressure': ['pascals', 'kilopascals', 'bar', 'psi', 'atm']
}

def show_unit_converter_category(category):
    """Show unit converter with specific category"""
    show_unit_converter()
    current_category.set(category)
    
    # Update unit dropdowns
    from_unit_dropdown['menu'].delete(0, 'end')
    to_unit_dropdown['menu'].delete(0, 'end')
    
    for unit in unit_categories[category]:
        from_unit_dropdown['menu'].add_command(label=unit, command=tk._setit(from_unit_var, unit))
        to_unit_dropdown['menu'].add_command(label=unit, command=tk._setit(to_unit_var, unit))
    
    # Set default values
    from_unit_var.set(unit_categories[category][0])
    to_unit_var.set(unit_categories[category][1])
    
    # Update category label
    category_label.config(text=f"{category.capitalize()} Converter")
    
    # Clear entries
    entry_var.set("")
    result_var.set("")

# Unit Converter UI
category_label = tk.Label(
    unit_converter_frame,
    text="Unit Converter",
    font=("Arial", 18, "bold"),
    bg=DARK_BG,
    fg=DARK_FG,
    pady=10
)
category_label.pack()

# Input frame
input_frame = tk.Frame(unit_converter_frame, bg=DARK_BG)
input_frame.pack(pady=10)

tk.Label(input_frame, text="Value:", font=("Arial", 12), bg=DARK_BG, fg=DARK_FG).pack(side=tk.LEFT)
entry = tk.Entry(input_frame, textvariable=entry_var, font=("Arial", 12), width=15, 
                bg=DARK_SECONDARY, fg=DARK_FG, insertbackground=DARK_FG)
entry.pack(side=tk.LEFT, padx=5)

# Unit selection frame
unit_selection_frame = tk.Frame(unit_converter_frame, bg=DARK_BG)
unit_selection_frame.pack(pady=10)

tk.Label(unit_selection_frame, text="From:", font=("Arial", 12), bg=DARK_BG, fg=DARK_FG).pack(side=tk.LEFT)
from_unit_dropdown = tk.OptionMenu(unit_selection_frame, from_unit_var, "")
from_unit_dropdown.config(font=("Arial", 10), bg=DARK_SECONDARY, fg=DARK_FG, 
                         activebackground=DARK_HOVER, activeforeground=DARK_FG)
from_unit_dropdown['menu'].config(bg=DARK_SECONDARY, fg=DARK_FG, 
                                 activebackground=DARK_HOVER, activeforeground=DARK_FG)
from_unit_dropdown.pack(side=tk.LEFT, padx=5)

tk.Label(unit_selection_frame, text="To:", font=("Arial", 12), bg=DARK_BG, fg=DARK_FG).pack(side=tk.LEFT)
to_unit_dropdown = tk.OptionMenu(unit_selection_frame, to_unit_var, "")
to_unit_dropdown.config(font=("Arial", 10), bg=DARK_SECONDARY, fg=DARK_FG,
                       activebackground=DARK_HOVER, activeforeground=DARK_FG)
to_unit_dropdown['menu'].config(bg=DARK_SECONDARY, fg=DARK_FG,
                               activebackground=DARK_HOVER, activeforeground=DARK_FG)
to_unit_dropdown.pack(side=tk.LEFT, padx=5)

# Convert button
convert_unit_button = tk.Button(
    unit_converter_frame,
    text="Convert",
    font=("Arial", 12, "bold"),
    bg=SUCCESS_GREEN,
    fg=DARK_FG,
    activebackground="#45a049",
    activeforeground=DARK_FG,
    command=convert_units
)
convert_unit_button.pack(pady=10)

# Result display
result_display = tk.Label(
    unit_converter_frame,
    textvariable=result_var,
    font=("Arial", 12, "bold"),
    bg=DARK_BG,
    fg=INFO_BLUE,
    pady=10
)
result_display.pack()

# Quick category buttons
quick_categories_frame = tk.Frame(unit_converter_frame, bg=DARK_BG)
quick_categories_frame.pack(pady=10)

categories = ['Length', 'Area', 'Volume', 'Speed', 'Weight', 'Temperature', 'Power', 'Pressure']
for i, category in enumerate(categories):
    btn = tk.Button(
        quick_categories_frame,
        text=category,
        font=("Arial", 9),
        bg=DARK_SECONDARY,
        fg=DARK_FG,
        activebackground=DARK_HOVER,
        activeforeground=DARK_FG,
        command=lambda c=category.lower(): show_unit_converter_category(c)
    )
    btn.grid(row=i//4, column=i%4, padx=2, pady=2, sticky="ew")


for i in range(4):
    quick_categories_frame.grid_columnconfigure(i, weight=1)

# Conversion frames dictionary (for future expansion)
conversion_frames = {}

# Add keyboard for calculator
def key_press(event):
    key = event.char
    if key in '0123456789':
        update_display(key)
    elif key in '+-*/':
        update_display(key)
    elif key == '\r' or key == '=':
        calculate_result()
    elif key == '\x08':
        backspace()
    elif key == '\x1b':
        clear_display()

root.bind('<Key>', key_press)

# Start with calculator visible
show_calculator()

# Start the application
root.mainloop()
