import tkinter as tk
from tkinter import ttk
from styles import configure_styles
from tkinter import ttk,messagebox,filedialog
import mysql.connector
import pandas as pd
def teacher(root):
    #gọi hàm style căn chỉnh
    configure_styles()
    home_window = tk.Toplevel(root)
    home_window.title("Quản lí giáo viên")
    label = ttk.Label(home_window, text=" Quản lí giáo viên", style="GreenLabel.TLabel")
    label.grid(row=0, column=1, columnspan=2,padx=20,pady=10,sticky='nsew')
    # Lấy kích thước của màn hình
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    window_width = 620  # Thay đổi kích thước theo nhu cầu
    window_height =600 # Thay đổi kích thước theo nhu cầu
    # Tính toán vị trí để cửa sổ xuất hiện giữa màn hình
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    # Đặt vị trí cửa sổ
    home_window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    def close_window_2():
        home_window.destroy()  # Đóng cửa sổ 2
        root.deiconify() 
    back_button = ttk.Button(home_window, text="Back", command=close_window_2)
    back_button.grid(row=1, column=1, padx=40,pady=20,sticky='ew')

    tree = ttk.Treeview(home_window, columns=("HoTen", "MonDay", "ChucVu"), show="headings")

    tree.heading("HoTen", text="Họ Tên")
    tree.heading("MonDay", text="Môn dạy")
    tree.heading("ChucVu", text="Chức vụ")

    tree.column("HoTen", width=200)
    tree.column("MonDay", width=200)
    tree.column("ChucVu", width=200)
    tree['height'] = 15

    # Connect to your MySQL database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="080102",
        database="ma_ng_mo"
    )
    cursor = conn.cursor()

    # Fetch data from the MySQL table
    cursor.execute("SELECT * FROM GiaoVien")
    rows = cursor.fetchall()
        # Insert data into the Treeview
    for row in rows:
        tree.insert("", "end", values=row[1:],tags=(row[0],))


    tree.grid(row=3, column=1, columnspan=4, rowspan=10, pady=10, padx=10, sticky="nsew")
    def delete_teacher():
        selected_item = tree.selection()
        if not selected_item:
            tk.messagebox.showwarning("Warning", "Vui lòng chọn giáo viên để xóa.")
            return

        # Confirm the deletion with the user
        confirm = tk.messagebox.askyesno("Chấp nhận", "Bạn muốn xóa giáo viên này?")
        if not confirm:
            return
        # Lấy giá trị của "GiaoVienID" từ thuộc tính tag của item được chọn
        teacher_id_delete = tree.item(selected_item, 'tags')[0]
        try:
            # Delete the teacher from the database
            delete_query = f"DELETE FROM GiaoVien WHERE GiaoVienID = {teacher_id_delete}"
            cursor = conn.cursor()
            cursor.execute(delete_query)
            conn.commit()

            # Remove the selected item from the Treeview
            tree.delete(selected_item)

        except mysql.connector.Error as err:
            # Handle MySQL errors
            tk.messagebox.showerror("MySQL Error", f"MySQL Error: {err}")

    # Gọi hàm show_teacher_data để hiển thị dữ liệu ban đầu
        show_teacher_data()

    def add_teacher():
        # Open a new window for adding a new student
        add_window = tk.Toplevel(home_window)
        add_window.title("Thêm")

        # Entry widgets for user input
        id_entry = ttk.Entry(add_window, width=10)
        name_entry = ttk.Entry(add_window, width=20)
        dob_entry = ttk.Entry(add_window, width=15)
        position_entry = ttk.Entry(add_window, width=10)

        id_label = ttk.Label(add_window, text="Mã giáo viên:")
        name_label = ttk.Label(add_window, text="Họ Tên:")
        dob_label = ttk.Label(add_window, text="Môn dạy:")
        position_lable = ttk.Label(add_window, text="Chức Vụ:")

        id_label.grid(row=0, column=0, padx=5, pady=5)
        id_entry.grid(row=0, column=1, padx=5, pady=5)
        name_label.grid(row=1, column=0, padx=5, pady=5)
        name_entry.grid(row=1, column=1, padx=5, pady=5)
        dob_label.grid(row=2, column=0, padx=5, pady=5)
        dob_entry.grid(row=2, column=1, padx=5, pady=5)
        position_lable.grid(row=3, column=0, padx=5, pady=5)
        position_entry.grid(row=3, column=1, padx=5, pady=5)

        def insert_teacher():
            try:
                # Get values from the entry widgets
                teacher_id = int(id_entry.get())
                teacher_name = name_entry.get()
                teaching = dob_entry.get()
                position = position_entry.get()  # Sửa tên biến

                # Insert the new teacher into the database
                insert_query = f"INSERT INTO GiaoVien (GiaoVienID, HoTen, MonDay, ChucVu) VALUES ({teacher_id}, '{teacher_name}', '{teaching}', '{position}')"
                print(insert_query)
                cursor = conn.cursor()
                cursor.execute(insert_query)
                conn.commit()

                # Update the Treeview with the new data
                tree.insert("", "end", values=(teacher_name, teaching, position))
                show_teacher_data()
                # Close the add_window
                add_window.destroy()

            except ValueError as e:
                # Handle the case where conversion to int fails
                tk.messagebox.showerror("Error", f"Invalid input: {e}")
            except mysql.connector.Error as err:
                # Handle MySQL errors
                tk.messagebox.showerror("MySQL Error", f"MySQL Error: {err}")

        # Button to trigger the data insertion
        insert_button = ttk.Button(add_window, text="Thêm", command=insert_teacher)
        insert_button.grid(row=4, column=0, columnspan=2, pady=10)
    
    def edit_teacher():
        selected_item = tree.selection()
        if not selected_item:
            tk.messagebox.showwarning("Warning", "Vui lòng chọn giáo viên để sửa.")
            return

        # Open a new window for editing the selected student
        edit_window = tk.Toplevel(home_window)
        edit_window.title("Sửa dữ liệu giáo viên")

        # Retrieve the values of the selected student
        selected_values = tree.item(selected_item, 'values')
        id_edit= tree.item(selected_item, 'tags')[0]
        print(id_edit)
        # Entry widgets for user input with default values
        # Set the default value

        name_entry_edit = ttk.Entry(edit_window, width=20)
        name_entry_edit.insert(0, selected_values[0])

        dob_entry_edit = ttk.Entry(edit_window, width=15)
        dob_entry_edit.insert(0, selected_values[1])

        position_entry_edit = ttk.Entry(edit_window, width=10)
        position_entry_edit.insert(0, selected_values[2])

        
        name_label_edit = ttk.Label(edit_window, text="Họ Tên:")
        dob_label_edit = ttk.Label(edit_window, text="Môn dạy:")
        position_label_edit = ttk.Label(edit_window, text="Chức vụ:")

        
        name_label_edit.grid(row=1, column=0, padx=5, pady=5)
        name_entry_edit.grid(row=1, column=1, padx=5, pady=5)
        dob_label_edit.grid(row=2, column=0, padx=5, pady=5)
        dob_entry_edit.grid(row=2, column=1, padx=5, pady=5)
        position_label_edit.grid(row=3, column=0, padx=5, pady=5)
        position_entry_edit.grid(row=3, column=1, padx=5, pady=5)
        def update_teacher():
            try:
                # Get values from the entry widgets
                teacher_id_edit = int(id_edit)
                teacher_name_edit = name_entry_edit.get()
                teacher_dob_edit = dob_entry_edit.get()
                position_edit = position_entry_edit.get()

                # Update the student in the database
                update_query = f"UPDATE GiaoVien SET HoTen = '{teacher_name_edit}', MonDay = '{teacher_dob_edit}', ChucVu = '{position_edit}' WHERE GiaoVienID = {teacher_id_edit}"
                cursor = conn.cursor()
                cursor.execute(update_query)
                conn.commit()

                # Update the Treeview with the edited data
                tree.item(selected_item, values=(teacher_name_edit, teacher_dob_edit, position_edit))
                show_teacher_data()
                # Close the edit_window
                edit_window.destroy()
            
            except ValueError as e:
                # Handle the case where conversion to int fails
                tk.messagebox.showerror("Error", f"Invalid input: {e}")
            except mysql.connector.Error as err:
                # Handle MySQL errors
                tk.messagebox.showerror("MySQL Error", f"MySQL Error: {err}")

        
        # Button to trigger the data update
        update_button = ttk.Button(edit_window, text="Cập nhật", command=update_teacher)
        update_button.grid(row=4, column=0, columnspan=2, pady=10)

    def show_teacher_data():
        # Hàm thực hiện hiển thị dữ liệu giáo viên ban đầu
        tree.delete(*tree.get_children())
        try:
            # Fetch data from the MySQL table
            cursor.execute("SELECT * FROM GiaoVien")
            rows = cursor.fetchall()

            # Insert data into the Treeview
            for row in rows:
                tree.insert("", "end", values=row[1:],tags=(row[0],))

        except mysql.connector.Error as err:
            # Handle MySQL errors
            tk.messagebox.showerror("MySQL Error", f"MySQL Error: {err}")
    def export_to_excel():
        try:
            # Fetch all data from the database
            query_all = "SELECT * FROM GiaoVien"
            df_all = pd.read_sql_query(query_all, conn)

            # Prompt the user to choose a location to save the Excel file
            file_path = tk.filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])

            if file_path:
                # Save the data to the Excel file
                df_all.to_excel(file_path, index=False)
                tk.messagebox.showinfo("Thành công", "Dữ liệu chuyển sang file execl thành công.")
        except mysql.connector.Error as err:
            tk.messagebox.showerror("MySQL Error", f"MySQL Error: {err}")
        except Exception as e:
            tk.messagebox.showerror("Error", f"An error occurred: {e}")


    def import_from_excel():
        try:
            # Prompt the user to choose an Excel file to import
            file_path = tk.filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])

            if file_path:
                # Read data from the Excel file
                df_import = pd.read_excel(file_path)

                # Insert data into the database
                for row_import in df_import.itertuples(index=False):
                    insert_query = f"INSERT INTO GiaoVien (GiaoVienID, HoTen, MonDay, ChucVu) VALUES ({row_import.GiaoVienID}, '{row_import.HoTen}', '{row_import.MonDay}', {row_import.ChucVu})"
                    cursor = conn.cursor()
                    cursor.execute(insert_query)
                    conn.commit()

                # Refresh the Treeview with the new data
                show_teacher_data()
                tk.messagebox.showinfo("Thành công", "Dữ liệu lấy từ file execl thành công.")
        except mysql.connector.Error as err:
            tk.messagebox.showerror("MySQL Error", f"MySQL Error: {err}")
        except Exception as e:
            tk.messagebox.showerror("Error", f"An error occurred: {e}")

    # Thêm nút và entry để thêm giáo viên mới
    add_button = ttk.Button(home_window, text="Thêm giáo viên", command=add_teacher)
    add_button.grid(row=1, column=2,padx=40,pady=20, sticky="ew")
    # Thêm nút và entry để sửa thông tin giáo viên
    edit_button = ttk.Button(home_window, text="Sửa thông tin", command=edit_teacher)
    edit_button.grid(row=2, column=1, padx=40, pady=20, sticky="ew")
    # Thêm nút để xóa giáo viên
    delete_button = ttk.Button(home_window, text="Xóa giáo viên", command=delete_teacher)
    delete_button.grid(row=2, column=2, padx=40,pady=20, sticky="ew")

    export_button = ttk.Button(home_window, text="Xuất ra excel", command=export_to_excel)
    export_button.grid(row=1, column=3,padx=40, pady=20, sticky="ew")

    import_button = ttk.Button(home_window, text="Nhập bằng excel", command=import_from_excel)
    import_button.grid(row=2, column=3, padx=40,pady=20, sticky="ew")
    

