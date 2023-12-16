import tkinter as tk
from tkinter import ttk
from styles import configure_styles

def teacher(root):
    #gọi hàm style căn chỉnh
    configure_styles()
    home_window = tk.Toplevel(root)
    home_window.title("Home")
    
    # Lấy kích thước của màn hình
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    window_width = 1140  # Thay đổi kích thước theo nhu cầu
    window_height = 820  # Thay đổi kích thước theo nhu cầu
    # Tính toán vị trí để cửa sổ xuất hiện giữa màn hình
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    # Đặt vị trí cửa sổ
    home_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def close_window_2():
        home_window.destroy()  # Đóng cửa sổ 2
        root.deiconify() 
    back_button = ttk.Button(home_window, text="Back", command=close_window_2, style='Back_Bbutton.TButton')
    back_button.pack()

    label = tk.Label(home_window, text="Đây là nơi viết hàm teacher", font=("Arial", 46))  # Đặt kích thước font là 16
    label.pack(expand=True, fill="both")


 