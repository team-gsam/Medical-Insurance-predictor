import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import os
import pandas as pd
import pickle 
import sqlite3
import random
import string
import re
import traceback


# Step 1: Load the saved models and scaler from the pickle files
with open('regression_model.pkl', 'rb') as reg_model_file:
    reg_model = pickle.load(reg_model_file)

with open('classification_model.pkl', 'rb') as cls_model_file: 
    cls_model = pickle.load(cls_model_file) 

with open('scaler.pkl', 'rb') as scaler_file: 
    scaler = pickle.load(scaler_file) 

current_directory = os.getcwd()
current_user=0
def update(us):
    global current_user
    current_user=us
# ---------------- Main root ---------------- 
root = tk.Tk()
root.title("🩺 Medical Insurance Predictor 🛡️")
root.geometry("1280x720") 
root.minsize(800, 600) 
root.state('zoomed')
# Global image references
bg_photo = None
home_photo = None 
entries = {}  # Store input fields for easy access

# ---------------- Clear Screen ----------------
def clear_screen(): 
    for widget in root.winfo_children():
        widget.destroy()
    root.configure(bg="white")
    create_navbar()

# ---------------- First Page ----------------
def create_first_page():
    global first_frame, canvas1, start_text, bg_photo

    for widget in root.winfo_children():
        widget.destroy()

    first_frame = tk.Frame(root)
    first_frame.pack(fill="both", expand=True)

    # Create gradient background
    gradient_canvas = tk.Canvas(first_frame, width=root.winfo_screenwidth(), height=root.winfo_screenheight(), highlightthickness=0)
    gradient_canvas.pack(fill="both", expand=True)

    def create_gradient(canvas, width, height):
        canvas.delete("gradient")
        for i in range(height):
            r1, g1, b1 = 41, 128, 185  # #2980b9
            r2, g2, b2 = 52, 152, 219  # #3498db
            r = int(r1 + (r2 - r1) * (i / height))
            g = int(g1 + (g2 - g1) * (i / height))
            b = int(b1 + (b2 - b1) * (i / height))
            color = f"#{r:02x}{g:02x}{b:02x}"
            canvas.create_line(0, i, width, i, fill=color, tags="gradient")

    create_gradient(gradient_canvas, root.winfo_screenwidth(), root.winfo_screenheight())

    # Create content frame
    content_frame = tk.Frame(gradient_canvas, bg="white", padx=40, pady=40)
    gradient_canvas.create_window(root.winfo_screenwidth() // 2, root.winfo_screenheight() // 2, 
                                window=content_frame, anchor="center")

    # Title with animation
    title_frame = tk.Frame(content_frame, bg="white")
    title_frame.pack(pady=(0, 20))

    title_text = "🩺 Medical Insurance Predictor 🛡️"
    title_label = tk.Label(title_frame, text=title_text, font=("Arial", 32, "bold"), 
                          bg="white", fg="#2c3e50")
    title_label.pack()

    # Decorative line
    tk.Frame(title_frame, height=4, width=200, bg="#4CAF50").pack(pady=10)

    # Welcome message
    welcome_text = "Welcome to our advanced insurance prediction system.\nGet accurate cost estimates and policy recommendations."
    welcome_label = tk.Label(content_frame, text=welcome_text, font=("Arial", 14), 
                           bg="white", fg="#666666", wraplength=600)
    welcome_label.pack(pady=20)

    # Features section
    features_frame = tk.Frame(content_frame, bg="white")
    features_frame.pack(pady=20)

    features = [
        ("📊", "Accurate Cost Prediction"),
        ("💡", "Smart Policy Recommendations"),
        ("🔒", "Secure Data Handling"),
        ("⚡", "Quick Results")
    ]

    for icon, text in features:
        feature_frame = tk.Frame(features_frame, bg="white")
        feature_frame.pack(fill="x", pady=5)
        tk.Label(feature_frame, text=icon, font=("Arial", 16), bg="white", fg="#4CAF50").pack(side="left", padx=5)
        tk.Label(feature_frame, text=text, font=("Arial", 12), bg="white", fg="#2c3e50").pack(side="left")

    # Start button with animation
    start_btn = tk.Button(content_frame, text="Get Started →", command=show_login_page,
                         font=("Arial", 14, "bold"), bg="#4CAF50", fg="white",
                         padx=30, pady=15, relief="flat", cursor="hand2")
    start_btn.pack(pady=30)

    def animate_button():
        def pulse():
            start_btn.config(bg="#45a049")
            root.after(500, lambda: start_btn.config(bg="#4CAF50"))
            root.after(1000, pulse)
        pulse()

    animate_button()

# ---------------- Login Page ---------------- 

# In-memory user storage (username: password)
users = {}


def setup_background():
# Replace with actual image paths
    left_image_path = 'left.jpg'
    right_image_path = 'right.jpg'

    try:
        left_img = Image.open(left_image_path)
        right_img = Image.open(right_image_path)

        left_label = tk.Label(root)
        right_label = tk.Label(root)

        def update_images(event=None):
            root.update_idletasks()
            screen_width = root.winfo_width()
            screen_height = root.winfo_height()

            # Define image widths: 40% each, 20% gap
            left_width = int(screen_width * 0.4)
            right_width = int(screen_width * 0.4)
            spacing = int(screen_width * 0.2)

            # Resize images with full root height
            left_resized = left_img.resize((left_width, screen_height), Image.LANCZOS)
            left_img_tk = ImageTk.PhotoImage(left_resized)
            left_label.config(image=left_img_tk)
            left_label.image = left_img_tk

            right_resized = right_img.resize((right_width, screen_height), Image.LANCZOS)
            right_img_tk = ImageTk.PhotoImage(right_resized)
            right_label.config(image=right_img_tk)
            right_label.image = right_img_tk

            # Place images correctly
            left_label.place(x=0, y=0, width=left_width, height=screen_height)
            right_label.place(x=left_width + spacing, y=0, width=right_width, height=screen_height)

        # Force initial layout update
        root.after(100, update_images)
        root.bind("<Configure>", update_images)

    except FileNotFoundError as e:
        error_label = tk.Label(root, text=f"Error: Image not found - {e}", fg="red", font=("Arial", 14))
        error_label.pack(pady=20)
    except Exception as e:
        error_label = tk.Label(root, text=f"An unexpected error occurred: {e}", fg="red", font=("Arial", 14))
        error_label.pack(pady=20)
        traceback.print_exc()

def login_page():
    # Clear existing widgets
    for widget in root.winfo_children():
        widget.destroy()

    # Create main frame with gradient background
    login_frame = tk.Frame(root)
    login_frame.pack(fill="both", expand=True)

    # Create gradient background
    gradient_canvas = tk.Canvas(login_frame, width=root.winfo_screenwidth(), height=root.winfo_screenheight(), highlightthickness=0)
    gradient_canvas.pack(fill="both", expand=True)

    def create_gradient(canvas, width, height):
        canvas.delete("gradient")
        for i in range(height):
            r1, g1, b1 = 41, 128, 185  # #2980b9
            r2, g2, b2 = 52, 152, 219  # #3498db
            r = int(r1 + (r2 - r1) * (i / height))
            g = int(g1 + (g2 - g1) * (i / height))
            b = int(b1 + (b2 - b1) * (i / height))
            color = f"#{r:02x}{g:02x}{b:02x}"
            canvas.create_line(0, i, width, i, fill=color, tags="gradient")
    create_gradient(gradient_canvas, root.winfo_screenwidth(), root.winfo_screenheight())
    login_box = tk.Frame(gradient_canvas, bg="white", padx=40, pady=40)
    gradient_canvas.create_window(root.winfo_screenwidth() // 2, root.winfo_screenheight() // 2, 
                                window=login_box, anchor="center")
    tk.Label(login_box, text="Welcome Back!", font=("Arial", 24, "bold"), 
            bg="white", fg="#2c3e50").pack(pady=(0, 20))
    tk.Frame(login_box, height=3, width=100, bg="#4CAF50").pack(pady=5)
    username_frame = tk.Frame(login_box, bg="white")
    username_frame.pack(fill="x", pady=10)
    tk.Label(username_frame, text="Username", font=("Arial", 12), 
            bg="white", fg="#2c3e50").pack(anchor="w")
    username_entry = tk.Entry(username_frame, font=("Arial", 12), 
                            bg="#f5f5f5", fg="#333333", relief="solid", borderwidth=1)
    username_entry.pack(fill="x", pady=2)
    password_frame = tk.Frame(login_box, bg="white")
    password_frame.pack(fill="x", pady=10)
    tk.Label(password_frame, text="Password", font=("Arial", 12), 
            bg="white", fg="#2c3e50").pack(anchor="w")
    password_entry = tk.Entry(password_frame, font=("Arial", 12), 
                            bg="#f5f5f5", fg="#333333", relief="solid", 
                            borderwidth=1, show="•")
    password_entry.pack(fill="x", pady=2)
    login_btn = tk.Button(login_box, text="Login", 
                         command=lambda: handle_login(username_entry.get(), password_entry.get()),
                         font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
                         padx=20, pady=10, relief="flat", cursor="hand2")
    login_btn.pack(pady=20)
    register_frame = tk.Frame(login_box, bg="white")
    register_frame.pack(pady=10)
    tk.Label(register_frame, text="Don't have an account?", font=("Arial", 10), 
            bg="white", fg="#666666").pack(side="left")
    register_btn = tk.Button(register_frame, text="Register", command=register_page,
                           font=("Arial", 10, "bold"), bg="white", fg="#4CAF50",
                           relief="flat", cursor="hand2", borderwidth=0)
    register_btn.pack(side="left", padx=5)
    back_btn = tk.Button(login_box, text="← Back to Home", command=create_first_page,
                        font=("Arial", 10), bg="white", fg="#666666",
                        relief="flat", cursor="hand2", borderwidth=0)
    back_btn.pack(pady=10)

    # Add hover effects
    def on_enter(e):
        e.widget.config(bg="#45a049")

    def on_leave(e):
        e.widget.config(bg="#4CAF50")

    login_btn.bind("<Enter>", on_enter)
    login_btn.bind("<Leave>", on_leave)

# --- CAPTCHA generator ---
def generate_captcha():
    return ''.join(random.choices(string.ascii_uppercase, k=3)) + ''.join(random.choices(string.digits, k=3))

captcha_pattern = re.compile(r'^[A-Z]{3}[0-9]{3}$')
captcha_text = generate_captcha()  # Initial CAPTCHA

def register_page():
    global captcha_text  # To allow refreshing inside the nested function

    # Clear existing widgets
    for widget in root.winfo_children():
        widget.destroy()

    # Create main frame with gradient background
    register_frame = tk.Frame(root)
    register_frame.pack(fill="both", expand=True)

    # Create gradient background
    gradient_canvas = tk.Canvas(register_frame, width=root.winfo_screenwidth(), height=root.winfo_screenheight(), highlightthickness=0)
    gradient_canvas.pack(fill="both", expand=True)

    def create_gradient(canvas, width, height):
        canvas.delete("gradient")
        for i in range(height):
            r1, g1, b1 = 41, 128, 185  # #2980b9
            r2, g2, b2 = 52, 152, 219  # #3498db
            r = int(r1 + (r2 - r1) * (i / height))
            g = int(g1 + (g2 - g1) * (i / height))
            b = int(b1 + (b2 - b1) * (i / height))
            color = f"#{r:02x}{g:02x}{b:02x}"
            canvas.create_line(0, i, width, i, fill=color, tags="gradient")

    create_gradient(gradient_canvas, root.winfo_screenwidth(), root.winfo_screenheight())

    # Create registration box
    register_box = tk.Frame(gradient_canvas, bg="white", padx=40, pady=40)
    gradient_canvas.create_window(root.winfo_screenwidth() // 2, root.winfo_screenheight() // 2, 
                                window=register_box, anchor="center")

    # Title
    tk.Label(register_box, text="Create Account", font=("Arial", 24, "bold"), 
            bg="white", fg="#2c3e50").pack(pady=(0, 20))

    # Decorative line
    tk.Frame(register_box, height=3, width=100, bg="#4CAF50").pack(pady=5)

    # Username field
    username_frame = tk.Frame(register_box, bg="white")
    username_frame.pack(fill="x", pady=10)
    tk.Label(username_frame, text="Username", font=("Arial", 12), 
            bg="white", fg="#2c3e50").pack(anchor="w")
    username_entry = tk.Entry(username_frame, font=("Arial", 12), 
                            bg="#f5f5f5", fg="#333333", relief="solid", borderwidth=1)
    username_entry.pack(fill="x", pady=2)

    # Password field
    password_frame = tk.Frame(register_box, bg="white")
    password_frame.pack(fill="x", pady=10)
    tk.Label(password_frame, text="Password", font=("Arial", 12), 
            bg="white", fg="#2c3e50").pack(anchor="w")
    password_entry = tk.Entry(password_frame, font=("Arial", 12), 
                            bg="#f5f5f5", fg="#333333", relief="solid", 
                            borderwidth=1, show="•")
    password_entry.pack(fill="x", pady=2)

    # Confirm Password field
    confirm_frame = tk.Frame(register_box, bg="white")
    confirm_frame.pack(fill="x", pady=10)
    tk.Label(confirm_frame, text="Confirm Password", font=("Arial", 12), 
            bg="white", fg="#2c3e50").pack(anchor="w")
    confirm_entry = tk.Entry(confirm_frame, font=("Arial", 12), 
                           bg="#f5f5f5", fg="#333333", relief="solid", 
                           borderwidth=1, show="•")
    confirm_entry.pack(fill="x", pady=2)

    # CAPTCHA section
    captcha_frame = tk.Frame(register_box, bg="white")
    captcha_frame.pack(fill="x", pady=10)

    # CAPTCHA label and display
    captcha_label_frame = tk.Frame(captcha_frame, bg="white")
    captcha_label_frame.pack(fill="x", pady=5)
    tk.Label(captcha_label_frame, text="CAPTCHA", font=("Arial", 12), 
            bg="white", fg="#2c3e50").pack(side="left")
    
    # CAPTCHA display with refresh button
    captcha_display_frame = tk.Frame(captcha_frame, bg="white")
    captcha_display_frame.pack(fill="x", pady=5)
    
    captcha_display = tk.Label(captcha_display_frame, text=captcha_text, 
                             font=("Courier", 16, "bold"), bg="#f5f5f5", 
                             fg="#2c3e50", padx=10, pady=5)
    captcha_display.pack(side="left", padx=5)

    def refresh_captcha():
        global captcha_text
        captcha_text = generate_captcha()
        captcha_display.config(text=captcha_text)

    refresh_btn = tk.Button(captcha_display_frame, text="🔄", 
                          command=refresh_captcha, font=("Arial", 12),
                          bg="#f5f5f5", fg="#2c3e50", relief="flat",
                          cursor="hand2")
    refresh_btn.pack(side="left", padx=5)

    # CAPTCHA input
    captcha_input_frame = tk.Frame(captcha_frame, bg="white")
    captcha_input_frame.pack(fill="x", pady=5)
    captcha_entry = tk.Entry(captcha_input_frame, font=("Arial", 12), 
                           bg="#f5f5f5", fg="#333333", relief="solid", 
                           borderwidth=1)
    captcha_entry.pack(fill="x", pady=2)

    # Submit button
    def handle_register():
        username = username_entry.get().strip()
        password = password_entry.get()
        confirm_password = confirm_entry.get()
        captcha_input = captcha_entry.get().strip()

        if not username or not password or not captcha_input:
            messagebox.showerror("Error", "All fields are required.")
            return
        if password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match.")
            return
        if captcha_input != captcha_text or not captcha_pattern.fullmatch(captcha_input):
            messagebox.showerror("Error", "Incorrect CAPTCHA.")
            refresh_captcha()
            return

        # Save user to DB
        try:
            conn = sqlite3.connect('insurance_data.db')
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS login_details (
                    username TEXT PRIMARY KEY,
                    password TEXT NOT NULL
                )
            ''')
            c.execute('INSERT INTO login_details (name, password) VALUES (?, ?)', (username, confirm_password))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Registration successful! Please log in.")
            login_page()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists!")

    submit_btn = tk.Button(register_box, text="Register", command=handle_register,
                         font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
                         padx=20, pady=10, relief="flat", cursor="hand2")
    submit_btn.pack(pady=20)

    # Back to login button
    back_frame = tk.Frame(register_box, bg="white")
    back_frame.pack(pady=10)
    tk.Label(back_frame, text="Already have an account?", font=("Arial", 10), 
            bg="white", fg="#666666").pack(side="left")
    back_btn = tk.Button(back_frame, text="Login", command=login_page,
                        font=("Arial", 10, "bold"), bg="white", fg="#4CAF50",
                        relief="flat", cursor="hand2", borderwidth=0)
    back_btn.pack(side="left", padx=5)

    # Back to home button
    home_btn = tk.Button(register_box, text="← Back to Home", command=create_first_page,
                        font=("Arial", 10), bg="white", fg="#666666",
                        relief="flat", cursor="hand2", borderwidth=0)
    home_btn.pack(pady=10)

    # Add hover effects
    def on_enter(e):
        if e.widget == submit_btn:
            e.widget.config(bg="#45a049")
        elif e.widget in [refresh_btn, back_btn, home_btn]:
            e.widget.config(fg="#2c3e50")

    def on_leave(e):
        if e.widget == submit_btn:
            e.widget.config(bg="#4CAF50")
        elif e.widget in [refresh_btn, back_btn, home_btn]:
            e.widget.config(fg="#4CAF50")

    submit_btn.bind("<Enter>", on_enter)
    submit_btn.bind("<Leave>", on_leave)
    refresh_btn.bind("<Enter>", on_enter)
    refresh_btn.bind("<Leave>", on_leave)
    back_btn.bind("<Enter>", on_enter)
    back_btn.bind("<Leave>", on_leave)
    home_btn.bind("<Enter>", on_enter)
    home_btn.bind("<Leave>", on_leave)

def handle_login(username, password):
    # Basic login validation
    if username and password:
        # Check if user exists in database
        conn = sqlite3.connect('insurance_data.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM login_details WHERE name=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            update(user[0])  # Update current_user with user ID
            show_second_page()
        else:
            messagebox.showerror("Error", "Invalid username or password")
    else:
        messagebox.showerror("Error", "Please enter both username and password")

def show_second_page(event=None):
    if current_user == 0:
        show_login_page()
    else:
        clear_screen()
        create_second_page()

def show_login_page(event=None):
    clear_screen()
    login_page()

# ---------------- Second Page ----------------
input_data = {}
try:
    new_input_data = pd.read_excel('dataset11.xlsx')
except Exception as e:
    print("Error loading recommendations Excel file:", e)
    new_input_data = pd.DataFrame()

def create_second_page():
    global second_frame, home_photo, entries, input_data
    entries = {}  
    second_frame = tk.Frame(root)
    second_frame.pack(fill="both", expand=True)
    img_path = rf"{current_directory}\2.jpg"
    try:
        home_img = Image.open(img_path)
        home_img = home_img.resize((root.winfo_screenwidth() // 2, root.winfo_screenheight()), Image.LANCZOS)
        home_photo = ImageTk.PhotoImage(home_img)
    except Exception as e:
        print(f"Error loading left image: {e}")
        home_photo = None
    canvas_left = tk.Canvas(second_frame, width=root.winfo_screenwidth() // 2, height=root.winfo_screenheight(), highlightthickness=0)
    canvas_left.pack(side="left", fill="both", expand=True)
    if home_photo:
        canvas_left.create_image(0, 0, image=home_photo, anchor="nw")
    input_frame = tk.Frame(second_frame, bg="white")
    input_frame.pack(side="right", fill="both", expand=True, padx=50)
    tk.Label(input_frame, text="Insurance Cost Prediction", font=("Arial", 20, "bold"), fg="black", bg="white").pack(pady=20)
    def add_placeholder(entry, placeholder):
        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, tk.END) 
                entry.config(fg="black")

        def on_focus_out(event):
            if entry.get() == "":
                entry.insert(0, placeholder)
                entry.config(fg="grey")

        entry.insert(0, placeholder)
        entry.config(fg="grey", font=("Arial", 14), bg="#fefefe", bd=2, relief="solid")
        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    def create_input(label_text, placeholder_text):
        lbl = tk.Label(input_frame, text=label_text, font=("Arial", 12, "bold"), bg="#ffffff", fg="#2c3e50")
        lbl.pack(pady=(10, 0))

        entry = tk.Entry(input_frame, width=30)
        add_placeholder(entry, placeholder_text)
        entry.pack(pady=(2, 10), ipady=5)
        entries[label_text] = entry
    def create_gradient(canvas, width, height):
        canvas.delete("gradient")
        for i in range(height):
            r1, g1, b1 = 245, 246, 245  # #f5f6f5
            r2, g2, b2 = 255, 255, 255  # #ffffff
            r = int(r1 + (r2 - r1) * (i / height))
            g = int(g1 + (g2 - g1) * (i / height))
            b = int(b1 + (b2 - b1) * (i / height))
            color = f"#{r:02x}{g:02x}{b:02x}"
            canvas.create_line(0, i, width, i, fill=color, tags="gradient")

    def create_dropdown(label_text, options):
        lbl = tk.Label(input_frame, text=label_text, font=("Arial", 12, "bold"), bg="#ffffff", fg="#2c3e50")
        lbl.pack(pady=(10, 0))

        var = tk.StringVar()
        dropdown = ttk.Combobox(input_frame, textvariable=var, values=options, state="readonly", width=27, font=("Arial", 14))
        dropdown.set(options[0])  # Set default value
        dropdown.pack(pady=(2, 10), ipady=5)
        entries[label_text] = dropdown

    # Regular input fields
    input_labels = [
        ("Age", "Age"),
        ("BMI", "BMI"),
        ("Annual_Income", "Eg: 500000"),
    ] 

    for label, placeholder in input_labels:
        create_input(label, placeholder)

    # Dropdown fields
    dropdown_options = {
        "Gender": ["0-Male", "1-Female"],
        "Smoker": ["0-No", "1-Yes"],
        "Alcohol_Consumption": ["0-No", "1-Yes"],
        "Pre_Existing_Conditions": ["0-No", "1-Yes"]
    }

    for label, options in dropdown_options.items():
        create_dropdown(label, options)

    def on_predict(): 
        global input_data  

        try:
            input_data = {}
            for label, entry in entries.items():
                if isinstance(entry, ttk.Combobox):
                    # Extract numeric value from dropdown selection (e.g., "0-Male" -> "0")
                    value = entry.get()
                    if not value:  # Check if dropdown is empty
                        messagebox.showerror("Input Error", f"Please select a value for {label}")
                        return
                    input_data[label] = value.split('-')[0]
                else:
                    value = entry.get()
                    # Check if the value is empty or equals the placeholder text
                    if not value or value == "Age" or value == "BMI" or value == "Eg: 500000":
                        messagebox.showerror("Input Error", f"Please enter a value for {label}")
                        return
                    input_data[label] = value
            
            print("Raw Input Data:", input_data)
            
            # Convert all values to float and validate
            numeric_data = {}
            for key, value in input_data.items():
                try:
                    numeric_value = float(value)
                    if key in ["Age", "BMI", "Annual_Income"] and numeric_value <= 0:
                        messagebox.showerror("Input Error", f"{key} must be greater than 0")
                        return
                    numeric_data[key] = numeric_value
                except ValueError:
                    messagebox.showerror("Input Error", f"Please enter a valid number for {key}")
                    return
            
            print("Numeric Data:", numeric_data)
            
            # Define the correct feature order as used in model training
            feature_order = ['Age', 'Gender', 'BMI', 'Smoker', 'Alcohol_Consumption', 
                           'Annual_Income', 'Pre_Existing_Conditions']
            
            # Create DataFrame with numeric values in the correct order
            input_df = pd.DataFrame([numeric_data])[feature_order]
            print("DataFrame:", input_df)
            
            try:
                input_scaled = scaler.transform(input_df)
                print("Scaled Data:", input_scaled)
            except Exception as e:
                messagebox.showerror("Scaling Error", f"Error in scaling data: {str(e)}\nData: {input_df}")
                return

            try:
                reg_result = reg_model.predict(input_scaled)[0]
                cls_result = cls_model.predict(input_scaled)[0]
                print("Regression Result:", reg_result)
                print("Classification Result:", cls_result)
            except Exception as e:
                messagebox.showerror("Prediction Error", f"Error in prediction: {str(e)}\nScaled Data: {input_scaled}")
                return

            tier_map = {0: 'Basic', 1: 'Premium', 2: 'Standard'} 
            provider_map = {0: 'Private', 1: 'Government'}
            
            try:
                matching_rows = new_input_data[
                    (new_input_data['Policy_Tier_Encoded'] == cls_result[0]) &
                    (new_input_data['Provider_Type_Encoded'] == cls_result[1])
                ]
            except Exception as e:
                messagebox.showerror("Matching Error", f"Error finding matching policies: {str(e)}")
                return

            if not matching_rows.empty:
                common_policy = matching_rows['Recommended_Policy'].mode()[0]
                common_provider = matching_rows['Recommended_Provider'].mode()[0]       
            else:
                common_policy = "N/A"
                common_provider = "N/A" 

            result_msg = (
                f"--- Prediction Results ---\n\n"
                f"Insurance Cost Prediction: ₹{round(reg_result[0])}\n"
                f"Monthly Premium Prediction: ₹{round(reg_result[1])}\n\n"
                f"Recommended Policy Tier: {tier_map.get(cls_result[0], 'Unknown')}\n"
                f"Recommended Provider Type: {provider_map.get(cls_result[1], 'Unknown')}\n"
                f"Suggested Policy Name: {common_policy}\n\n" 
                f"Suggested Provider Name: {common_provider}\n\n"
                f"--- End of Prediction ---"
            )  

            canvas_left.delete("all")
            result_frame = tk.Frame(canvas_left, bg="white", highlightthickness=2, highlightbackground="#d3d3d3")
            gradient_canvas = tk.Canvas(result_frame, width=500, height=400, highlightthickness=0)
            gradient_canvas.pack(fill="both", expand=True)
            create_gradient(gradient_canvas, 500, 400)

            content_frame = tk.Frame(gradient_canvas, bg="white")
            gradient_canvas.create_window(250, 200, window=content_frame, anchor="center")

            tk.Label(content_frame, text="Prediction Result", font=("Arial", 18, "bold"), bg="white", fg="#2c3e50").pack(pady=(10, 10))
            labels = [
                ("Insurance Cost Prediction: ", f"₹{round(reg_result[0])}"),
                ("Monthly Premium Prediction: ", f"₹{round(reg_result[1])}"),
                ("Recommended Policy Tier: ", f"{tier_map.get(cls_result[0], 'Unknown')}"),
                ("Recommended Provider Type: ", f"{provider_map.get(cls_result[1], 'Unknown')}"),
                ("Suggested Policy Name: ", f"{common_policy}"),
                ("Suggested Provider Name: ", f"{common_provider}")
            ]
            for label, value in labels:
                frame = tk.Frame(content_frame, bg="white")
                frame.pack(fill="x", padx=10, pady=3)
                tk.Label(frame, text=label, font=("Arial", 14, "bold"), bg="white", fg="#2c3e50").pack(side="left")
                tk.Label(frame, text=value, font=("Arial", 14), bg="white", fg="#4CAF50").pack(side="left")

            canvas_left.create_window(root.winfo_screenwidth() // 4, root.winfo_screenheight() // 2, window=result_frame, anchor="center")

            
            try:
                conn = sqlite3.connect('insurance_data.db') 
                c = conn.cursor() 
                c.execute('''
                    INSERT INTO predictions (
                        age, gender, bmi, smoker, alcohol, income, conditions, 
                        predicted_cost, predicted_premium, policy_tier, provider_type,
                        suggested_policy, suggested_provider,role
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?,?)
                ''', (
                    numeric_data["Age"], numeric_data["Gender"], numeric_data["BMI"],
                    numeric_data["Smoker"], numeric_data["Alcohol_Consumption"], numeric_data["Annual_Income"],
                    numeric_data["Pre_Existing_Conditions"], round(reg_result[0]), round(reg_result[1]),
                    tier_map.get(cls_result[0], 'Unknown'), provider_map.get(cls_result[1], 'Unknown'), 
                    common_policy, common_provider, current_user
                ))
                conn.commit()
                conn.close()
            except Exception as e:
                messagebox.showerror("Database Error", f"Error saving prediction: {str(e)}")
                return
                
        except Exception as e:
            messagebox.showerror("Unexpected Error", f"An unexpected error occurred: {str(e)}")
            import traceback
            print("Full error traceback:")
            print(traceback.format_exc())

    predict_btn = tk.Button(input_frame, text="Predict", command=on_predict,
                            font=("Arial", 14, "bold"), bg="#4CAF50", fg="white", padx=10, pady=5) 
    predict_btn.pack(pady=20)

# ---------------- History Page ----------------
def create_history_page():
    clear_screen()
    frame = tk.Frame(root)
    frame.pack(fill="both", expand=True)

    conn = sqlite3.connect('insurance_data.db')
    c = conn.cursor()
    if(current_user== "admin"):
        c.execute("SELECT * FROM predictions ORDER BY timestamp DESC")
        rows = c.fetchall()
    else:
        c.execute("SELECT * FROM predictions WHERE role = ? ORDER BY timestamp DESC", (current_user,))
        rows = c.fetchall()

    conn.close()
 
    if not rows:
        tk.Label(frame, text="No prediction history found.", font=("Arial", 16), bg="white").pack(pady=20)
        return
    columns = [
        "Age", "Gender", "BMI", "Smoker(-no 1-yes)", "alcohol",
        "Income", "Existing Conditions",
        "Predicted Cost", "Monthly Premium", "policy tier", "policy type", "Policy", "Provider"
    ]

    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview",
                    background="white",
                    foreground="black",
                    rowheight=20,
                    fieldbackground="white",
                    font=("Arial", 10))
    style.configure("Treeview.Heading",
                    font=("Arial", 10, "bold"),
                    background="#2c3e50",
                    foreground="white")
    style.map("Treeview", background=[("selected", "#3498db")])

    tree = ttk.Treeview(frame, columns=columns, show='headings')

    for col in columns:
        tree.heading(col, text=col) 
        tree.column(col, width=120, anchor='center')

    for row in rows:
        row = list(row)        
        tree.insert("", "end", values=row[1:])

    h_scroll = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
    tree.configure(xscrollcommand=h_scroll.set)

    tree.pack(fill="both", expand=True)
    h_scroll.pack(fill="x")

# ---------------- Policies Page ----------------
def fetch_data():
    conn = sqlite3.connect("insurance_data.db")
    cur = conn.cursor()
    cur.execute("SELECT provider, policy_name FROM policy_list")  # provider first
    rows = cur.fetchall() 
    conn.close()

    policy_dict = {}
    for row in rows:
        provider, policy = row[0], row[1]
        policy_dict.setdefault(provider, []).append(policy)
    return policy_dict


def dis():
    clear_screen()
    frame = tk.Frame(root, bg="lightblue")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="Available Insurance Policies", font=("Arial", 16, "bold"), bg="lightblue").pack(pady=10)

    def display_policies(provider=None):
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        display_data = all_data if provider == "All" or provider is None else {provider: all_data.get(provider, [])}

        for prov, policies in display_data.items():
            provider_frame = tk.LabelFrame(
                scrollable_frame,
                text=prov,
                font=("Arial", 12, "bold"),
                bg="white",
                fg="black",
                bd=3,
                relief="solid"
            )
            provider_frame.pack(pady=10, fill="x", padx=10)

            for policy in policies:
                policy_label = ttk.Label(
                    provider_frame,
                    text=f"• {policy}",
                    font=("Arial", 12),
                    background="white",
                )
                policy_label.pack(anchor="w", padx=10, pady=2)

    def on_select(event):
        selected = provider_var.get()
        display_policies(selected)

    provider_var = tk.StringVar()
    provider_dropdown = ttk.Combobox(frame, textvariable=provider_var, state="readonly", width=30)
    provider_dropdown.pack(pady=10)

    canvas = tk.Canvas(frame, bg="lightblue")
    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    all_data = fetch_data()
    provider_dropdown['values'] = ["All"] + list(all_data.keys())
    provider_dropdown.set("All")
    provider_dropdown.bind("<<ComboboxSelected>>", on_select)

    display_policies()

# ---------------- Navigation Bar ----------------
def create_navbar():
    nav_frame = tk.Frame(root, bg="#232F3E", height=50)
    nav_frame.pack(fill="x", side="top")
 
    def create_menu_button(text, command):
        btn = tk.Label(nav_frame, text=text, font=("Arial", 16, "bold"), bg="#232F3E", fg="white", padx=20, pady=10, cursor="hand2")
        btn.pack(side="left", padx=20)
        
        def on_enter(event):
            btn.config(bg="#4CAF50", fg="white")
        
        def on_leave(event):
            btn.config(bg="#232F3E", fg="white") 
        
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
        btn.bind("<Button-1>", lambda event: command())

    def handle_home():
        if current_user == 0:
            show_login_page()
        else:
            clear_screen()
            create_second_page()

    def handle_logout():
        global current_user
        current_user = 0
        show_login_page()

    create_menu_button("Home", handle_home)
    create_menu_button("Policies", dis)
    create_menu_button("Histories", create_history_page)
    create_menu_button("BMI Calculator", create_bmi_calculator)
    create_menu_button("Contact Us", create_contact_page)
    if(current_user == "admin"):
        create_menu_button("Update", admin_update)
    
    # Add logout button on the right side
    logout_btn = tk.Label(nav_frame, text="Logout", font=("Arial", 16, "bold"), 
                         bg="#232F3E", fg="white", padx=20, pady=10, cursor="hand2")
    logout_btn.pack(side="right", padx=20)
    
    def on_enter(e):
        e.widget.config(bg="#e74c3c", fg="white")
    
    def on_leave(e):
        e.widget.config(bg="#232F3E", fg="white")
    
    logout_btn.bind("<Enter>", on_enter)
    logout_btn.bind("<Leave>", on_leave)
    logout_btn.bind("<Button-1>", lambda e: handle_logout())

def admin_update():
    clear_screen()
    
    # Create main frame with gradient background
    main_frame = tk.Frame(root)
    main_frame.pack(fill="both", expand=True)

    # Create gradient background
    gradient_canvas = tk.Canvas(main_frame, width=root.winfo_screenwidth(), height=root.winfo_screenheight(), highlightthickness=0)
    gradient_canvas.pack(fill="both", expand=True)

    def create_gradient(canvas, width, height):
        canvas.delete("gradient")
        for i in range(height):
            r1, g1, b1 = 41, 128, 185  # #2980b9
            r2, g2, b2 = 52, 152, 219  # #3498db
            r = int(r1 + (r2 - r1) * (i / height))
            g = int(g1 + (g2 - g1) * (i / height))
            b = int(b1 + (b2 - b1) * (i / height))
            color = f"#{r:02x}{g:02x}{b:02x}"
            canvas.create_line(0, i, width, i, fill=color, tags="gradient")

    create_gradient(gradient_canvas, root.winfo_screenwidth(), root.winfo_screenheight())

    # Create main content frame
    content_frame = tk.Frame(gradient_canvas, bg="white", padx=20, pady=20)
    gradient_canvas.create_window(root.winfo_screenwidth() // 2, root.winfo_screenheight() // 2, 
                                window=content_frame, anchor="center")

    # Title
    title_frame = tk.Frame(content_frame, bg="white")
    title_frame.pack(pady=(0, 20))
    tk.Label(title_frame, text="Admin Dashboard", font=("Arial", 28, "bold"), 
            bg="white", fg="#2c3e50").pack()
    tk.Frame(title_frame, height=3, width=150, bg="#4CAF50").pack(pady=5)

    # Create two columns layout
    columns_frame = tk.Frame(content_frame, bg="white")
    columns_frame.pack(fill="both", expand=True)

    # Right column - Content area
    right_frame = tk.Frame(columns_frame, bg="white", padx=20)
    right_frame.pack(side="right", fill="both", expand=True)

    def display_content():
        # Clear existing content
        for widget in right_frame.winfo_children():
            widget.destroy()

        # Add a placeholder message
        placeholder = tk.Label(right_frame, 
                             text="Select an option from the left menu to begin",
                             font=("Arial", 14), bg="white", fg="#666666")
        placeholder.pack(pady=50)

    def list_user():
        # Clear existing content
        for widget in right_frame.winfo_children():
            widget.destroy()

        # Title
        tk.Label(right_frame, text="User List", font=("Arial", 20, "bold"), 
                bg="white", fg="#2c3e50").pack(pady=(0, 20))

        # Create Treeview with custom style
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Custom.Treeview",
                      background="white",
                      foreground="black",
                      rowheight=30,
                      fieldbackground="white",
                      font=('Arial', 12))

        style.configure("Custom.Treeview.Heading",
                      font=('Arial', 13, 'bold'),
                      background="#4CAF50",
                      foreground="white")

        style.map("Custom.Treeview",
                background=[("selected", "#e0e0e0")])

        # Create Treeview
        tree = ttk.Treeview(right_frame, columns=("Name", "Password"),
                          show="headings", style="Custom.Treeview")
        tree.heading("Name", text="Name")
        tree.heading("Password", text="Password")
        tree.column("Name", width=200)
        tree.column("Password", width=200)
        tree.pack(fill="both", expand=True, pady=10)

        # Add scrollbar
        scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=tree.yview)
        scrollbar.pack(side="right", fill="y")
        tree.configure(yscrollcommand=scrollbar.set)

        # Fetch and display data
        try:
            conn = sqlite3.connect('insurance_data.db')     
            c = conn.cursor()
            c.execute("SELECT name, password FROM login_details")
            login_data = c.fetchall()
            conn.close()

            for row in login_data:
                tree.insert("", "end", values=row)
        except Exception as e:
            messagebox.showerror("Error", f"Error fetching user data: {str(e)}")

    def new_add_user():
        # Clear existing content
        for widget in right_frame.winfo_children():
            widget.destroy()

        # Title
        tk.Label(right_frame, text="Add New User", font=("Arial", 20, "bold"), 
                bg="white", fg="#2c3e50").pack(pady=(0, 20))

        # Form frame
        form_frame = tk.Frame(right_frame, bg="white")
        form_frame.pack(pady=20)

        # Username field
        username_frame = tk.Frame(form_frame, bg="white")
        username_frame.pack(fill="x", pady=10)
        tk.Label(username_frame, text="Username", font=("Arial", 12), 
                bg="white", fg="#2c3e50").pack(anchor="w")
        username_entry = tk.Entry(username_frame, font=("Arial", 12), 
                                bg="#f5f5f5", fg="#333333", relief="solid", 
                                borderwidth=1)
        username_entry.pack(fill="x", pady=2)

        # Password field
        password_frame = tk.Frame(form_frame, bg="white")
        password_frame.pack(fill="x", pady=10)
        tk.Label(password_frame, text="Password", font=("Arial", 12), 
                bg="white", fg="#2c3e50").pack(anchor="w")
        password_entry = tk.Entry(password_frame, font=("Arial", 12), 
                                bg="#f5f5f5", fg="#333333", relief="solid", 
                                borderwidth=1, show="•")
        password_entry.pack(fill="x", pady=2)

        def update_user():
            username = username_entry.get().strip()
            password = password_entry.get().strip()

            if not username or not password:
                messagebox.showwarning("Input Error", "Please fill in both fields.")
                return

            try:
                conn = sqlite3.connect('insurance_data.db')     
                c = conn.cursor()
                c.execute("INSERT INTO login_details (name, password) VALUES (?, ?)", 
                         (username, password))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", f"User '{username}' added successfully!")
                username_entry.delete(0, tk.END)
                password_entry.delete(0, tk.END)
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", "Username already exists!")
            except Exception as e:
                messagebox.showerror("Error", f"Error adding user: {str(e)}")

        # Submit button
        submit_btn = tk.Button(form_frame, text="Add User", command=update_user,
                             font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
                             padx=20, pady=10, relief="flat", cursor="hand2")
        submit_btn.pack(pady=20)

        # Add hover effect
        def on_enter(e):
            e.widget.config(bg="#45a049")

        def on_leave(e):
            e.widget.config(bg="#4CAF50")

        submit_btn.bind("<Enter>", on_enter)
        submit_btn.bind("<Leave>", on_leave)

    def remove_user():
        # Clear existing content
        for widget in right_frame.winfo_children():
            widget.destroy()

        # Title
        tk.Label(right_frame, text="Delete User", font=("Arial", 20, "bold"), 
                bg="white", fg="#2c3e50").pack(pady=(0, 20))

        # Form frame
        form_frame = tk.Frame(right_frame, bg="white")
        form_frame.pack(pady=20)

        # Username field
        username_frame = tk.Frame(form_frame, bg="white")
        username_frame.pack(fill="x", pady=10)
        tk.Label(username_frame, text="Username", font=("Arial", 12), 
                bg="white", fg="#2c3e50").pack(anchor="w")
        username_entry = tk.Entry(username_frame, font=("Arial", 12), 
                                bg="#f5f5f5", fg="#333333", relief="solid", 
                                borderwidth=1)
        username_entry.pack(fill="x", pady=2)

        # Password field
        password_frame = tk.Frame(form_frame, bg="white")
        password_frame.pack(fill="x", pady=10) 
        tk.Label(password_frame, text="Password", font=("Arial", 12), 
                bg="white", fg="#2c3e50").pack(anchor="w")
        password_entry = tk.Entry(password_frame, font=("Arial", 12), 
                                bg="#f5f5f5", fg="#333333", relief="solid", 
                                borderwidth=1, show="•")
        password_entry.pack(fill="x", pady=2)

        def delete_user():
            username = username_entry.get().strip()
            password = password_entry.get().strip()

            if not username or not password:
                messagebox.showwarning("Input Error", "Please fill in both fields.")
                return

            try:
                conn = sqlite3.connect('insurance_data.db')     
                c = conn.cursor()
                c.execute("DELETE FROM login_details WHERE name = ? AND password = ?", 
                         (username, password))
                if c.rowcount > 0:
                    conn.commit()
                    messagebox.showinfo("Success", f"User '{username}' deleted successfully!")
                else:
                    messagebox.showerror("Error", "User not found or password incorrect!")
                conn.close()
                username_entry.delete(0, tk.END)
                password_entry.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("Error", f"Error deleting user: {str(e)}")

        # Delete button
        delete_btn = tk.Button(form_frame, text="Delete User", command=delete_user,
                             font=("Arial", 12, "bold"), bg="#e74c3c", fg="white",
                             padx=20, pady=10, relief="flat", cursor="hand2")
        delete_btn.pack(pady=20)

        # Add hover effect
        def on_enter(e):
            e.widget.config(bg="#c0392b")

        def on_leave(e):
            e.widget.config(bg="#e74c3c")

        delete_btn.bind("<Enter>", on_enter)
        delete_btn.bind("<Leave>", on_leave)

    def new_policy():
        # Clear existing content
        for widget in right_frame.winfo_children():
            widget.destroy()

        # Title
        tk.Label(right_frame, text="Add New Policy", font=("Arial", 20, "bold"), 
                bg="white", fg="#2c3e50").pack(pady=(0, 20))

        # Form frame
        form_frame = tk.Frame(right_frame, bg="white")
        form_frame.pack(pady=20)

        # Policy name field
        policy_frame = tk.Frame(form_frame, bg="white")
        policy_frame.pack(fill="x", pady=10)
        tk.Label(policy_frame, text="Policy Name", font=("Arial", 12), 
                bg="white", fg="#2c3e50").pack(anchor="w")
        policy_entry = tk.Entry(policy_frame, font=("Arial", 12), 
                              bg="#f5f5f5", fg="#333333", relief="solid", 
                              borderwidth=1)
        policy_entry.pack(fill="x", pady=2)

        # Provider field
        provider_frame = tk.Frame(form_frame, bg="white")
        provider_frame.pack(fill="x", pady=10)
        tk.Label(provider_frame, text="Provider Name", font=("Arial", 12), 
                bg="white", fg="#2c3e50").pack(anchor="w")
        provider_entry = tk.Entry(provider_frame, font=("Arial", 12), 
                                bg="#f5f5f5", fg="#333333", relief="solid", 
                                borderwidth=1)
        provider_entry.pack(fill="x", pady=2)

        def add_policy():
            policy = policy_entry.get().strip()
            provider = provider_entry.get().strip()

            if not policy or not provider:
                messagebox.showwarning("Input Error", "Please fill in both fields.")
                return

            try:
                conn = sqlite3.connect('insurance_data.db')     
                c = conn.cursor()
                c.execute("INSERT INTO policy_list (policy_name, provider, status) VALUES (?, ?, ?)", 
                         (policy, provider, 0))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", f"Policy '{policy}' added successfully!")
                policy_entry.delete(0, tk.END)
                provider_entry.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("Error", f"Error adding policy: {str(e)}")

        # Add button
        add_btn = tk.Button(form_frame, text="Add Policy", command=add_policy,
                          font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
                          padx=20, pady=10, relief="flat", cursor="hand2")
        add_btn.pack(pady=20)

        # Add hover effect
        def on_enter(e):
            e.widget.config(bg="#45a049")

        def on_leave(e):
            e.widget.config(bg="#4CAF50")

        add_btn.bind("<Enter>", on_enter)
        add_btn.bind("<Leave>", on_leave)

    def delete_policy():
        # Clear existing content
        for widget in right_frame.winfo_children():
            widget.destroy()

        # Title
        tk.Label(right_frame, text="Delete Policy", font=("Arial", 20, "bold"), 
                bg="white", fg="#2c3e50").pack(pady=(0, 20))

        # Form frame
        form_frame = tk.Frame(right_frame, bg="white")
        form_frame.pack(pady=20)

        # Policy name field
        policy_frame = tk.Frame(form_frame, bg="white")
        policy_frame.pack(fill="x", pady=10)
        tk.Label(policy_frame, text="Policy Name", font=("Arial", 12), 
                bg="white", fg="#2c3e50").pack(anchor="w")
        policy_entry = tk.Entry(policy_frame, font=("Arial", 12), 
                              bg="#f5f5f5", fg="#333333", relief="solid", 
                              borderwidth=1)
        policy_entry.pack(fill="x", pady=2)

        # Provider field
        provider_frame = tk.Frame(form_frame, bg="white")
        provider_frame.pack(fill="x", pady=10)
        tk.Label(provider_frame, text="Provider Name", font=("Arial", 12), 
                bg="white", fg="#2c3e50").pack(anchor="w")
        provider_entry = tk.Entry(provider_frame, font=("Arial", 12), 
                                bg="#f5f5f5", fg="#333333", relief="solid", 
                                borderwidth=1)
        provider_entry.pack(fill="x", pady=2)

        def remove_policy():
            policy = policy_entry.get().strip()
            provider = provider_entry.get().strip()

            if not policy or not provider:
                messagebox.showwarning("Input Error", "Please fill in both fields.")
                return

            try:
                conn = sqlite3.connect('insurance_data.db')     
                c = conn.cursor()
                c.execute("DELETE FROM policy_list WHERE policy_name = ? AND provider = ?", 
                         (policy, provider))
                if c.rowcount > 0:
                    conn.commit()
                    messagebox.showinfo("Success", f"Policy '{policy}' deleted successfully!")
                else:
                    messagebox.showerror("Error", "Policy not found!")
                conn.close()
                policy_entry.delete(0, tk.END)
                provider_entry.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("Error", f"Error deleting policy: {str(e)}")

        # Delete button
        delete_btn = tk.Button(form_frame, text="Delete Policy", command=remove_policy,
                             font=("Arial", 12, "bold"), bg="#e74c3c", fg="white",
                             padx=20, pady=10, relief="flat", cursor="hand2")
        delete_btn.pack(pady=20)

        # Add hover effect
        def on_enter(e):
            e.widget.config(bg="#c0392b")

        def on_leave(e):
            e.widget.config(bg="#e74c3c")

        delete_btn.bind("<Enter>", on_enter)
        delete_btn.bind("<Leave>", on_leave)

    left_frame = tk.Frame(columns_frame, bg="white", padx=20)
    left_frame.pack(side="left", fill="y", padx=20)

    nav_buttons = [
        ("👥 View Users", list_user),
        ("➕ Add User", new_add_user),
        ("❌ Delete User", remove_user),
        ("📋 Add Policy", new_policy),
        ("🗑️ Delete Policy", delete_policy)
    ]

    for text, command in nav_buttons:
        btn = tk.Button(left_frame, text=text, command=command,
                       font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
                       padx=20, pady=10, relief="flat", cursor="hand2",
                       width=20)
        btn.pack(pady=10, fill="x")
        def on_enter(e):
            e.widget.config(bg="#45a049")

        def on_leave(e):
            e.widget.config(bg="#4CAF50")

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)
    back_btn = tk.Button(content_frame, text="← Back to Home", command=create_first_page,
                        font=("Arial", 10), bg="white", fg="#666666",
                        relief="flat", cursor="hand2", borderwidth=0)
    back_btn.pack(pady=20)

    # Add hover effect for back button
    def on_enter(e):
        e.widget.config(fg="#2c3e50")

    def on_leave(e):
        e.widget.config(fg="#666666")

    back_btn.bind("<Enter>", on_enter)
    back_btn.bind("<Leave>", on_leave)

    # Initialize with list_user view
    list_user()

# ---------------- Page Switch ----------------
def show_second_page(event=None):
    if current_user == 0:
        show_login_page()
    else:
        clear_screen()
        create_second_page()

def show_login_page(event=None):
    clear_screen()
    login_page()

# ---------------- Database Setup ----------------
def setup_database():
    conn = sqlite3.connect('insurance_data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            age TEXT,
            gender TEXT,
            bmi TEXT,
            smoker TEXT, 
            alcohol TEXT, 
            income TEXT,
            conditions TEXT,
            predicted_cost REAL,
            predicted_premium REAL,
            policy_tier TEXT,
            provider_type TEXT,
            suggested_policy TEXT,
            suggested_provider TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()


def create_admin_page():
    clear_screen()
    create_second_page()

def create_bmi_calculator():
    clear_screen()
    frame = tk.Frame(root, bg="white")
    frame.pack(fill="both", expand=True)
    gradient_canvas = tk.Canvas(frame, width=root.winfo_screenwidth(), height=root.winfo_screenheight(), highlightthickness=0)
    gradient_canvas.pack(fill="both", expand=True)

    def create_gradient(canvas, width, height):
        canvas.delete("gradient")
        for i in range(height):
            r1, g1, b1 = 245, 246, 245  
            r2, g2, b2 = 255, 255, 255  
            r = int(r1 + (r2 - r1) * (i / height))
            g = int(g1 + (g2 - g1) * (i / height))
            b = int(b1 + (b2 - b1) * (i / height))
            color = f"#{r:02x}{g:02x}{b:02x}"
            canvas.create_line(0, i, width, i, fill=color, tags="gradient")

    create_gradient(gradient_canvas, root.winfo_screenwidth(), root.winfo_screenheight())
    content_frame = tk.Frame(gradient_canvas, bg="white", padx=20, pady=20)
    gradient_canvas.create_window(root.winfo_screenwidth() // 2, root.winfo_screenheight() // 2, window=content_frame, anchor="center")
    tk.Label(content_frame, text="BMI Calculator", font=("Arial", 24, "bold"), bg="white", fg="#2c3e50").pack(pady=(0, 20))
    input_frame = tk.Frame(content_frame, bg="white")
    input_frame.pack(pady=10)
    height_frame = tk.Frame(input_frame, bg="white")
    height_frame.pack(pady=5)
    tk.Label(height_frame, text="Height (cm):", font=("Arial", 14), bg="white", fg="#2c3e50").pack(side="left", padx=5)
    height_entry = tk.Entry(height_frame, font=("Arial", 14), width=10)
    height_entry.pack(side="left", padx=5)
    weight_frame = tk.Frame(input_frame, bg="white")
    weight_frame.pack(pady=5)
    tk.Label(weight_frame, text="Weight (kg):", font=("Arial", 14), bg="white", fg="#2c3e50").pack(side="left", padx=5)
    weight_entry = tk.Entry(weight_frame, font=("Arial", 14), width=10)
    weight_entry.pack(side="left", padx=5)

    result_label = tk.Label(content_frame, text="", font=("Arial", 16), bg="white", fg="#4CAF50")
    result_label.pack(pady=20)
    category_label = tk.Label(content_frame, text="", font=("Arial", 14), bg="white", fg="#2c3e50")
    category_label.pack(pady=5)

    def calculate_bmi():
        try:
            height = float(height_entry.get())
            weight = float(weight_entry.get())
            
            if height <= 0 or weight <= 0:
                raise ValueError("Height and weight must be positive numbers")
            
            # Convert height from cm to m
            height_m = height / 100
            bmi = weight / (height_m * height_m)
            
            # Determine BMI category
            if bmi < 18.5:
                category = "Underweight"
                color = "#3498db"  # Blue
            elif 18.5 <= bmi < 25:
                category = "Normal weight"
                color = "#2ecc71"  # Green
            elif 25 <= bmi < 30:
                category = "Overweight"
                color = "#f1c40f"  # Yellow
            else:
                category = "Obese"
                color = "#e74c3c"  # Red
            
            result_label.config(text=f"Your BMI: {bmi:.2f}", fg=color)
            category_label.config(text=f"Category: {category}", fg=color)
            
        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", "Please enter valid numbers")

    # Calculate button
    calculate_btn = tk.Button(content_frame, text="Calculate BMI", command=calculate_bmi,
                            font=("Arial", 14, "bold"), bg="#4CAF50", fg="white", padx=10, pady=5)
    calculate_btn.pack(pady=20)

    # BMI chart
    chart_frame = tk.Frame(content_frame, bg="white")
    chart_frame.pack(pady=20)

    chart_text = """
    BMI Categories:
    Underweight: < 18.5
    Normal weight: 18.5 - 24.9
    Overweight: 25 - 29.9
    Obese: ≥ 30
    """
    tk.Label(chart_frame, text=chart_text, font=("Arial", 12), bg="white", fg="#2c3e50", justify="left").pack()

    # Back button
    back_btn = tk.Button(content_frame, text="Back to Home", command=create_first_page,
                        font=("Arial", 12), bg="#34495e", fg="white", padx=10, pady=5)
    back_btn.pack(pady=20)

def create_contact_page():
    clear_screen()
    # Create main frame with gradient background
    contact_frame = tk.Frame(root, bg="white")
    contact_frame.pack(fill="both", expand=True)

    # Create gradient background
    gradient_canvas = tk.Canvas(contact_frame, width=root.winfo_screenwidth(), height=root.winfo_screenheight(), highlightthickness=0)
    gradient_canvas.pack(fill="both", expand=True)

    def create_gradient(canvas, width, height):
        canvas.delete("gradient")
        for i in range(height):
            r1, g1, b1 = 240, 240, 245  
            r2, g2, b2 = 255, 255, 255  
            r = int(r1 + (r2 - r1) * (i / height))
            g = int(g1 + (g2 - g1) * (i / height))
            b = int(b1 + (b2 - b1) * (i / height))
            color = f"#{r:02x}{g:02x}{b:02x}"
            canvas.create_line(0, i, width, i, fill=color, tags="gradient")

    create_gradient(gradient_canvas, root.winfo_screenwidth(), root.winfo_screenheight())

    # Create main content frame
    main_content = tk.Frame(gradient_canvas, bg="white", padx=20, pady=20)
    gradient_canvas.create_window(root.winfo_screenwidth() // 2, root.winfo_screenheight() // 2, window=main_content, anchor="center")

    # Title with decorative line
    title_frame = tk.Frame(main_content, bg="white")
    title_frame.pack(pady=(0, 20))
    
    tk.Label(title_frame, text="Contact Us", font=("Arial", 28, "bold"), bg="white", fg="#2c3e50").pack()
    tk.Frame(title_frame, height=3, width=100, bg="#4CAF50").pack(pady=5)

    # Create two columns layout
    columns_frame = tk.Frame(main_content, bg="white")
    columns_frame.pack(fill="both", expand=True)

    # Left column - Contact Information
    left_frame = tk.Frame(columns_frame, bg="white", padx=20)
    left_frame.pack(side="left", fill="both", expand=True)

    # Contact information with icons
    contact_info = [
        ("📧", "Email", "kethavathsamba11@gmail.com"),
        ("📱", "Phone", "9908108215"),
        ("⏰", "Business Hours", "Monday - Friday: 9:00 AM - 5:00 PM"),
        ("🏢", "Location", "Hyderabad, Telangana, India")
    ]
 
    for icon, label, value in contact_info:
        info_frame = tk.Frame(left_frame, bg="white")
        info_frame.pack(fill="x", pady=10) 
        
        # Icon
        tk.Label(info_frame, text=icon, font=("Arial", 16), bg="white", fg="#4CAF50").pack(side="left", padx=5)
        
        # Label and value
        text_frame = tk.Frame(info_frame, bg="white")
        text_frame.pack(side="left", padx=5)
        tk.Label(text_frame, text=label, font=("Arial", 12, "bold"), bg="white", fg="#2c3e50").pack(anchor="w")
        tk.Label(text_frame, text=value, font=("Arial", 12), bg="white", fg="#666666").pack(anchor="w")

    # Right column - Contact Form
    right_frame = tk.Frame(columns_frame, bg="white", padx=20)
    right_frame.pack(side="right", fill="both", expand=True)

    # Contact form title
    tk.Label(right_frame, text="Send us a Message", font=("Arial", 16, "bold"), bg="white", fg="#2c3e50").pack(pady=(0, 15))

    # Form fields
    form_fields = [
        ("Name", "Enter your name"),
        ("Email", "Enter your email"),
        ("Subject", "Enter subject"),
        ("Message", "Enter your message")
    ]

    form_entries = {}
    for label, placeholder in form_fields:
        frame = tk.Frame(right_frame, bg="white")
        frame.pack(fill="x", pady=5)
        
        tk.Label(frame, text=label, font=("Arial", 10), bg="white", fg="#2c3e50").pack(anchor="w")
        
        if label == "Message":
            entry = tk.Text(frame, height=4, font=("Arial", 10), bg="#f5f5f5", fg="#333333",
                          relief="solid", borderwidth=1)
            entry.insert("1.0", placeholder)
        else:
            entry = tk.Entry(frame, font=("Arial", 10), bg="#f5f5f5", fg="#333333",
                           relief="solid", borderwidth=1)
            entry.insert(0, placeholder) 
        
        entry.pack(fill="x", pady=2)
        form_entries[label] = entry

    def submit_form():
        messagebox.showinfo("Success", "Your message has been sent successfully!")

    submit_btn = tk.Button(right_frame, text="Send Message", command=submit_form,
                          font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
                          padx=20, pady=10, relief="flat")
    submit_btn.pack(pady=20)

    social_frame = tk.Frame(main_content, bg="white")
    social_frame.pack(pady=20)

    social_links = [
        ("🌐", "Website"),
        ("💼", "LinkedIn")
    ]

    for icon, platform in social_links:
        btn = tk.Button(social_frame, text=f"{icon} {platform}", font=("Arial", 10),
                       bg="#f5f5f5", fg="#2c3e50", relief="flat", padx=10, pady=5)
        btn.pack(side="left", padx=10)

    back_btn = tk.Button(main_content, text="← Back to Home", command=create_first_page,
                        font=("Arial", 12), bg="#34495e", fg="white",
                        padx=15, pady=8, relief="flat")
    back_btn.pack(pady=20) 

# ---------------- Run ----------------
setup_database()
create_first_page()
root.mainloop() 