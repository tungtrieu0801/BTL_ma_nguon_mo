import tkinter as tk
from tkinter import ttk,messagebox
from styles import configure_styles
import mysql.connector
def classroom(root):
    #gọi hàm style căn chỉnh
    configure_styles()
    sell_window = tk.Toplevel(root)
    sell_window.title("Lớp học")
        # Lấy kích thước của màn hình
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    window_width = 700  # Thay đổi kích thước theo nhu cầu
    window_height = 500  # Thay đổi kích thước theo nhu cầu
    # Tính toán vị trí để cửa sổ xuất hiện giữa màn hình
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    # Đặt vị trí cửa sổ
    sell_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def close_window_2():
        sell_window.destroy()  # Đóng cửa sổ 2
        root.deiconify() 
    back_button = ttk.Button(sell_window, text="Quay lại", command=close_window_2, style='Back_Bbutton.TButton')
    back_button.grid(row=0, column=3, pady=10,padx=10)

    tree = ttk.Treeview(sell_window, columns=("LopHocID", "TenLop", "GiaoVienID"), show="headings")

    tree.heading("LopHocID", text="Mã lớp")
    tree.heading("TenLop", text="Tên lớp")
    tree.heading("GiaoVienID", text="Mã giáo viên")
    tree.column("LopHocID", width=225)
    tree.column("TenLop", width=225)
    tree.column("GiaoVienID", width=225)
    tree['height'] = 17

    # Connect to MySQL (adjust these details)
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456789",
        database="qlsv"
    )

    cursor = connection.cursor()

    # Fetch data from the MySQL table
    cursor.execute("SELECT * FROM LopHoc")
    rows = cursor.fetchall()

    # Insert data into the Treeview
    for row in rows:
        tree.insert("", "end", values=row)

    # Pack the Treeview to the window
    tree.grid(row=3, column=1, columnspan=3, rowspan=10, pady=10, padx=10, sticky="nsew")

    def add_class():
        # Open a new window for adding a new class
        add_window = tk.Toplevel(sell_window)
        add_window.title("Add New Class")

        # Entry widgets for user input
        class_id_entry = ttk.Entry(add_window, width=10)
        class_name_entry = ttk.Entry(add_window, width=20)
        teacher_id_entry = ttk.Entry(add_window, width=10)

        class_id_label = ttk.Label(add_window, text="Class ID:")
        class_name_label = ttk.Label(add_window, text="Class Name:")
        teacher_id_label = ttk.Label(add_window, text="Teacher ID:")

        class_id_label.grid(row=0, column=0, padx=5, pady=5)
        class_id_entry.grid(row=0, column=1, padx=5, pady=5)
        class_name_label.grid(row=1, column=0, padx=5, pady=5)
        class_name_entry.grid(row=1, column=1, padx=5, pady=5)
        teacher_id_label.grid(row=2, column=0, padx=5, pady=5)
        teacher_id_entry.grid(row=2, column=1, padx=5, pady=5)

        def insert_class():
            try:
                # Get values from the entry widgets
                class_id = int(class_id_entry.get())
                class_name = class_name_entry.get()
                teacher_id = int(teacher_id_entry.get())

                # Insert the new class into the database
                insert_query = f"INSERT INTO LopHoc (LopHocID, TenLop, GiaoVienID) VALUES ({class_id}, '{class_name}', {teacher_id})"
                cursor = connection.cursor()
                cursor.execute(insert_query)
                connection.commit()

                # Update the Treeview with the new data
                tree.insert("", "end", values=(class_id, class_name, teacher_id))

                # Close the add_window
                add_window.destroy()

            except ValueError as e:
                # Handle the case where conversion to int fails
                tk.messagebox.showerror("Error", f"Invalid input: {e}")
            except mysql.connector.Error as err:
                # Handle MySQL errors
                tk.messagebox.showerror("MySQL Error", f"MySQL Error: {err}")

        # Button to trigger the data insertion
        insert_button = ttk.Button(add_window, text="Add Class", command=insert_class)
        insert_button.grid(row=3, column=0, columnspan=2, pady=10)

    def edit_class():
        # Function to handle editing an existing class
        selected_item = tree.selection()

        if not selected_item:
            tk.messagebox.showwarning("Warning", "Please select a class to edit.")
            return

        # Get the existing values of the selected class
        existing_values = tree.item(selected_item)['values']

        # Open a new window for editing
        edit_window = tk.Toplevel(sell_window)
        edit_window.title("Edit Class")

        # Entry widgets for user input
        class_id_entry = ttk.Entry(edit_window, width=10)
        class_name_entry = ttk.Entry(edit_window, width=20)
        teacher_id_entry = ttk.Entry(edit_window, width=10)

        class_id_label = ttk.Label(edit_window, text="Class ID:")
        class_name_label = ttk.Label(edit_window, text="Class Name:")
        teacher_id_label = ttk.Label(edit_window, text="Teacher ID:")

        class_id_label.grid(row=0, column=0, padx=5, pady=5)
        class_id_entry.grid(row=0, column=1, padx=5, pady=5)
        class_name_label.grid(row=1, column=0, padx=5, pady=5)
        class_name_entry.grid(row=1, column=1, padx=5, pady=5)
        teacher_id_label.grid(row=2, column=0, padx=5, pady=5)
        teacher_id_entry.grid(row=2, column=1, padx=5, pady=5)

        def update_class():
            try:
                # Get values from the entry widgets
                class_id = int(class_id_entry.get())
                class_name = class_name_entry.get()
                teacher_id = int(teacher_id_entry.get())

                # Update the existing class in the database
                update_query = f"UPDATE LopHoc SET TenLop = '{class_name}', GiaoVienID = {teacher_id} WHERE LopHocID = {class_id}"
                cursor = connection.cursor()
                cursor.execute(update_query)
                connection.commit()

                # Update the Treeview with the updated data
                tree.item(selected_item, values=(class_id, class_name, teacher_id))

                # Close the edit_window
                edit_window.destroy()

            except ValueError as e:
                tk.messagebox.showerror("Error", f"Invalid input: {e}")
            except mysql.connector.Error as err:
                tk.messagebox.showerror("MySQL Error", f"MySQL Error: {err}")

        # Button to trigger the data update
        update_button = ttk.Button(edit_window, text="Update Class", command=update_class)
        update_button.grid(row=3, column=0, columnspan=2, pady=10)

    def delete_class():
        # Function to handle deleting an existing class
        selected_item = tree.selection()

        if not selected_item:
            tk.messagebox.showwarning("Warning", "Please select a class to delete.")
            return

        # Confirm the deletion
        confirm = tk.messagebox.askyesno("Confirm Deletion", "Are you sure you want to delete this class?")

        if confirm:
            # Get the ID of the selected class
            class_id = tree.item(selected_item)['values'][0]

            try:
                # Delete the class from the database
                delete_query = f"DELETE FROM LopHoc WHERE LopHocID = {class_id}"
                cursor = connection.cursor()
                cursor.execute(delete_query)
                connection.commit()

                # Remove the selected class from the Treeview
                tree.delete(selected_item)

            except mysql.connector.Error as err:
                tk.messagebox.showerror("MySQL Error", f"MySQL Error: {err}")

    # Button to trigger the data deletion
    delete_button = ttk.Button(sell_window, text="Xóa lớp", command=delete_class)
    delete_button.grid(row=1, column=2, pady=5, padx=10, sticky="ew")

    # Button to trigger the class editing
    edit_button = ttk.Button(sell_window, text="Sửa lớp", command=edit_class)
    edit_button.grid(row=1, column=3, pady=5, padx=10, sticky="ew")

    # Button to add a new class
    add_button = ttk.Button(sell_window, text="Thêm lớp", command=add_class)
    add_button.grid(row=1, column=1, pady=5, padx=10, sticky="ew")
    label = ttk.Label(sell_window, text="Dữ liệu Lớp học", style="GreenLabel.TLabel")
    label.grid(row=0, column=1, pady=10, padx=100, columnspan=2)

