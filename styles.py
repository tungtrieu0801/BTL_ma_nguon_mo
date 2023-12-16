# styles.py

import tkinter as tk
from tkinter import ttk

def configure_styles():
    style = ttk.Style()
    style.configure("Back_Bbutton.TButton",
                foreground="green",   # Màu chữ
                font=("Arial", 12),    # Phông chữ và kích thước
                padding=(10, 10),      # Khoảng cách giữa nội dung và biên (điều chỉnh chiều rộng và chiều cao ở đây)
                width=8,               # Chiều rộng của nút (giảm giá trị ở đây)
                borderwidth=5,         # Độ dày viền
                relief="flat"          # Kiểu viền
                )
def configure_for_main():
    style = ttk.Style()
    style.configure("Home.TButton",
                    foreground="green",  
                    font=("Arial", 12),  
                    padding=(20, 50),     
                    width=10,             
                    borderwidth=10,       
                    relief="flat",       
                    )
def configure_label_style():
    style = ttk.Style()
    style.configure("GreenLabel.TLabel",
                    font=("Arial", 30, "bold"),
                    foreground="green"
                    )