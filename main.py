import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import mysql.connector
from functools import partial
# from styles import configure_for_login
from PIL import Image, ImageTk
import os

import teacher

import score
import studentt
from tkinter import messagebox

from tkinter import *
from PIL import Image, ImageTk
import classs
file_path = os.path.dirname(os.path.realpath(__file__))
from styles import *
# Define your MySQL database connection parameters
db_config = {
    "host": "localhost",
    "user": "root",
    "password": "080102",
    "database": "ma_ng_mo",
}

script_dir = os.path.dirname(__file__)
image_path = os.path.join(script_dir, "images/admin_login_fixx.png")

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("1366x768")
        # Your login window components
        self.label1 = Label(root)
        self.label1.place(relx=0, rely=0, width=1366, height=768)
        self.img = PhotoImage(file=image_path)
        self.label1.configure(image=self.img)
        

        self.entry1 = Entry(root)
        self.entry1.place(relx=0.373, rely=0.273, width=374, height=24)
        self.entry1.configure(font="-family {Poppins} -size 10")
        self.entry1.configure(relief="flat")


        self.entry2 = Entry(root)
        self.entry2.place(relx=0.373, rely=0.384, width=374, height=24)
        self.entry2.configure(font="-family {Poppins} -size 10")
        self.entry2.configure(relief="flat")
        self.entry2.configure(show="*")


        self.button1 = Button(root)
        self.button1.place(relx=0.366, rely=0.685, width=356, height=43)
        self.button1.configure(relief="flat")
        self.button1.configure(overrelief="flat")
        self.button1.configure(activebackground="#D2463E")
        self.button1.configure(cursor="hand2")
        self.button1.configure(foreground="#ffffff")
        self.button1.configure(background="#D2463E")
        self.button1.configure(font="-family {Poppins SemiBold} -size 20")
        self.button1.configure(borderwidth="0")
        self.button1.configure(text="""Đăng nhập""")
        self.button1.configure(command=self.login)

        # configure_for_login()

    def login(self):
        # Retrieve username and password
        username = self.entry1.get()
        password = self.entry2.get()

        # Connect to MySQL database
        try:
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            # Execute a query to check if the username and password match
            query = "SELECT * FROM account WHERE emp_id = %s AND password = %s"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()

            if result:
                # Successful login
                print("Login successful!")
                messagebox.showinfo("Success", "Login successful!")
                # Call a function to open your main application window
                self.open_main_app()

            else:
                # Invalid credentials
                messagebox.showinfo("Fail", "Fail!")

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            # Close the database connection
            if conn.is_connected():
                cursor.close()
                conn.close()

    def open_main_app(self):
        # Close the login window
        self.root.destroy()

        # Call your main application window here
        # For example, create an instance of your main application class
        root = tk.Tk()
        app = MainApp(root)
        root.mainloop()


class MainApp:
    def __init__(self, root):
        # app = tk.Tk()  # Remove this line
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        window_width = 800
        window_height = 620

        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        root.title("Ứng dụng Tkinter")

        frame = ttk.Frame(root)
        frame.pack(pady=20, padx=20, fill="both", expand=True)
        style = ttk.Style()
        configure_for_main()
        configure_label_style()

        
        def load_and_resize_image(image_path, width, height):
            print(f"Loading image: {image_path}")
            image = Image.open(image_path)
            image.thumbnail((width, height))
            return ImageTk.PhotoImage(image)
        global image_home, image_sell, image_warehouse, image_history
        image_home = load_and_resize_image(os.path.join(file_path, "images/mentor.png"), 65, 65)
        image_sell = load_and_resize_image(os.path.join(file_path, "images/training.png"), 65, 65)
        image_warehouse = load_and_resize_image(os.path.join(file_path, "images/student.png"), 65, 65)
        image_history = load_and_resize_image(os.path.join(file_path, "images/score.png"), 65, 65)


        def open_new_window_from_main():
            root.withdraw()  # Use root instead of app
            teacher.teacher(root)

        def scoree():
            root.withdraw()  # Use root instead of app
            score.display_score(root)

        def classroom():
            root.withdraw()  # Use root instead of app
            classs.classroom(root)

        def student():
            root.withdraw()  # Use root instead of app
            studentt.display_student(root)

        def load_and_resize_image(image_path, width, height):
            image = Image.open(image_path)
            image.thumbnail((width, height))
            return ImageTk.PhotoImage(image)
        
        label = ttk.Label(frame, text="ỨNG DỤNG QUẢN LÍ SINH VIÊN", style="GreenLabel.TLabel")
        label.grid(row=0, column=0, columnspan=2, pady=(30, 0))

        button = ttk.Button(frame, image=image_home, text="Giáo viên   ",
                            compound='right', command=open_new_window_from_main, style="Home.TButton")
        button.grid(row=1, column=0, pady=40, padx=40)


        button = ttk.Button(frame, image=image_sell, text="Lớp học   ",
                            compound='right', style="Home.TButton", command=classroom)
        button.grid(row=1, column=1, pady=40, padx=30)

        # image_warehouse = load_and_resize_image(file_path + "/images/warehouse.png", 65, 65)
        button = ttk.Button(frame, image=image_warehouse, text="Học sinh   ",
                            compound='right', style="Home.TButton", command=student)
        button.grid(row=2, column=0, pady=40, padx=30)

        # image_history = load_and_resize_image(file_path + "/images/time-management.png", 65, 65)
        button = ttk.Button(frame, image=image_history, text="Score     ",
                            compound='right', style="Home.TButton", command=scoree)
        button.grid(row=2, column=1, pady=40, padx=30)

        style = ttk.Style()
        style.configure("Home.TButton", font=("Arial", 25, "bold"), borderwidth=2, foreground="green")

# Remove the following line
# app.mainloop()

# Create an instance of the LoginApp class
if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
