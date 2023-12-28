import tkinter as tk
from tkinter import ttk,messagebox,filedialog
from styles import configure_styles
import mysql.connector
import pandas as pd
def display_student(root):
    #gọi hàm style căn chỉnh
    configure_styles()
    warehourse_window = tk.Toplevel(root)
    warehourse_window.title("Học sinh")
        # Lấy kích thước của màn hình
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    window_width = 1140  # Thay đổi kích thước theo nhu cầu
    window_height = 585  # Thay đổi kích thước theo nhu cầu
    # Tính toán vị trí để cửa sổ xuất hiện giữa màn hình
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    # Đặt vị trí cửa sổ
    warehourse_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def close_window_2():
        warehourse_window.destroy()  # Đóng cửa sổ 2
        root.deiconify()
    back_button = ttk.Button(warehourse_window, text="Quay lại", command=close_window_2, style='Back_Bbutton.TButton')
    back_button.grid(row=0, column=1, pady=10)

    # Label to display the total number of students
    total_students_label = ttk.Label(warehourse_window, text="Tổng số học sinh: ", style="GreenLabel.TLabel")
    total_students_label.grid(row=13, column=1, pady=10, columnspan=2)

    def update_total_students_label():
        # Update the total students label with the current count
        total_students_label["text"] = f"Tổng số học sinh: {tree.get_children().__len__()}"

    # Dictionary to store the current sort order for each column
    sort_order = {}

    def sort_treeview(column):
        # Toggle the sort order (default to "asc" if not set)
        current_order = sort_order.get(column, "asc")
        new_order = "desc" if current_order == "asc" else "asc"
        sort_order[column] = new_order

        # Get all the items in the Treeview
        items = tree.get_children('')

        # Sort the items based on the selected column and sort order
        items = sorted(items, key=lambda x: tree.set(x, column), reverse=(new_order == "desc"))

        # Update the Treeview with the sorted items
        for index, item in enumerate(items):
            tree.move(item, '', index)

    def setup_sortable_treeview_columns():
        # Add sorting functionality to each column heading
        for col in ["HoTen", "HocSinhID", "NgaySinh", "QueQuan", "LopHocID"]:
            tree.heading(col, text=col, command=lambda c=col: sort_treeview(c))

    tree = ttk.Treeview(warehourse_window, columns=("HocSinhID", "HoTen", "NgaySinh","QueQuan", "LopHocID"), show="headings")
    setup_sortable_treeview_columns()
    tree.heading("HocSinhID", text="Mã học sinh")
    tree.heading("QueQuan", text="Quê quán")
    tree.heading("HoTen", text="Họ Tên")
    tree.heading("NgaySinh", text="Ngày Sinh")
    tree.heading("LopHocID", text="Mã lớp")
    tree.column("HocSinhID",width=220)
    tree.column("HoTen", width=220)
    tree.column("NgaySinh", width=220)
    tree.column("QueQuan", width=220)
    tree.column("LopHocID", width=220)
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
    cursor.execute("SELECT * FROM HocSinh")
    rows = cursor.fetchall()

    # Insert data into the Treeview
    for row in rows:
        tree.insert("", "end", values=row)
    update_total_students_label()
    tree.grid(row=3, column=1, columnspan=5, rowspan=10, pady=10, padx=10, sticky="nsew")

    def add_student():
        # Open a new window for adding a new student
        add_window = tk.Toplevel(warehourse_window)
        add_window.title("Thêm")

        # Entry widgets for user input
        id_entry = ttk.Entry(add_window, width=10)
        name_entry = ttk.Entry(add_window, width=20)
        dob_entry = ttk.Entry(add_window, width=15)
        que_entry = ttk.Entry(add_window, width=15)

        id_label = ttk.Label(add_window, text="Mã học sinh:")
        name_label = ttk.Label(add_window, text="Họ Tên:")
        dob_label = ttk.Label(add_window, text="Ngày Sinh (năm-tháng-ngày):")
        que_label = ttk.Label(add_window, text="Quê quán:")

        id_label.grid(row=0, column=0, padx=5, pady=5)
        id_entry.grid(row=0, column=1, padx=5, pady=5)
        name_label.grid(row=1, column=0, padx=5, pady=5)
        name_entry.grid(row=1, column=1, padx=5, pady=5)
        dob_label.grid(row=2, column=0, padx=5, pady=5)
        dob_entry.grid(row=2, column=1, padx=5, pady=5)
        que_label.grid(row=3, column=0, padx=5, pady=5)
        que_entry.grid(row=3, column=1, padx=5, pady=5)

        # Modified: Use ComboBox for class selection
        class_label = ttk.Label(add_window, text="Lớp Học:")
        class_combobox = ttk.Combobox(add_window, width=20, state="readonly")
        class_combobox.grid(row=4, column=1, padx=5, pady=5)
        class_label.grid(row=4, column=0, padx=5, pady=5)

        try:
            # Modified: Fetch class information from the database
            query_lophoc_info = "SELECT LopHocID FROM LopHoc"
            lophoc_info_df = pd.read_sql_query(query_lophoc_info, conn)

            # Modified: Populate the ComboBox with class IDs
            class_combobox["values"] = lophoc_info_df["LopHocID"].tolist()
            class_combobox.set("Chọn lớp")  # Set the default value

        except mysql.connector.Error as err:
            messagebox.showerror("MySQL Error", f"MySQL Error: {err}")

        def insert_student():
            try:
                # Get values from the entry widgets and ComboBox
                student_id = int(id_entry.get())
                student_name = name_entry.get()
                student_dob = dob_entry.get()
                student_que = que_entry.get()
                student_class_id = class_combobox.get()

                # Insert the new student into the database
                insert_query = f"INSERT INTO HocSinh (HocSinhID, HoTen, NgaySinh, QueQuan, LopHocID) VALUES ({student_id}, '{student_name}', '{student_dob}', '{student_que}', '{student_class_id}')"
                cursor = conn.cursor()
                cursor.execute(insert_query)
                conn.commit()

                # Update the Treeview with the new data
                tree.insert("", "end", values=(student_id, student_name, student_dob, student_que, student_class_id))
                # Update the total students label
                update_total_students_label()

                class_combobox.set("Chọn lớp")
                # Close the add_window
                add_window.destroy()

            except ValueError as e:
                # Handle the case where conversion to int fails
                tk.messagebox.showerror("Error", f"Invalid input: {e}")
            except mysql.connector.Error as err:
                # Handle MySQL errors
                tk.messagebox.showerror("MySQL Error", f"MySQL Error: {err}")

        # Button to trigger the data insertion
        insert_button = ttk.Button(add_window, text="Thêm", command=insert_student)
        insert_button.grid(row=5, column=0, columnspan=2, pady=10)

    def edit_student():
        selected_item = tree.selection()
        if not selected_item:
            tk.messagebox.showwarning("Warning", "Vui lòng chọn học sinh để sửa.")
            return

        # Open a new window for editing the selected student
        edit_window = tk.Toplevel(warehourse_window)
        edit_window.title("Sửa dữ liệu học sinh")

        # Retrieve the values of the selected student
        selected_values = tree.item(selected_item, 'values')

        # Entry widgets for user input with default values
        id_entry_edit = ttk.Entry(edit_window, width=10)
        id_entry_edit.insert(0, selected_values[0])  # Set the default value

        name_entry_edit = ttk.Entry(edit_window, width=20)
        name_entry_edit.insert(0, selected_values[1])

        dob_entry_edit = ttk.Entry(edit_window, width=15)
        dob_entry_edit.insert(0, selected_values[2])

        que_entry_edit = ttk.Entry(edit_window, width=15)
        que_entry_edit.insert(0, selected_values[3])

        # ComboBox for selecting class ID
        class_id_combobox_edit = ttk.Combobox(edit_window, width=10, state="readonly")
        class_id_combobox_edit.grid(row=4, column=1, padx=5, pady=5)
        class_id_label_edit = ttk.Label(edit_window, text="Lớp Học ID:")
        class_id_label_edit.grid(row=4, column=0, padx=5, pady=5)

        try:
            # Fetch class IDs from the database
            query_lophoc_info = "SELECT LopHocID FROM LopHoc"
            lophoc_info_df = pd.read_sql_query(query_lophoc_info, conn)

            # Add class IDs to the ComboBox
            class_id_combobox_edit["values"] = lophoc_info_df["LopHocID"].tolist()
            class_id_combobox_edit.set(selected_values[4])  # Set the default value

        except mysql.connector.Error as err:
            tk.messagebox.showerror("MySQL Error", f"MySQL Error: {err}")

        name_label_edit = ttk.Label(edit_window, text="Họ Tên:")
        dob_label_edit = ttk.Label(edit_window, text="Ngày Sinh (năm-tháng-ngày):")
        que_label_edit = ttk.Label(edit_window, text="Quê quán:")

        name_label_edit.grid(row=1, column=0, padx=5, pady=5)
        name_entry_edit.grid(row=1, column=1, padx=5, pady=5)
        dob_label_edit.grid(row=2, column=0, padx=5, pady=5)
        dob_entry_edit.grid(row=2, column=1, padx=5, pady=5)
        que_label_edit.grid(row=3, column=0, padx=5, pady=5)
        que_entry_edit.grid(row=3, column=1, padx=5, pady=5)

        # class ID label and ComboBox moved to row 4
        class_id_label_edit.grid(row=4, column=0, padx=5, pady=5)
        class_id_combobox_edit.grid(row=4, column=1, padx=5, pady=5)

        def update_student():
            try:
                # Get values from the entry widgets
                student_id_edit = int(id_entry_edit.get())
                student_name_edit = name_entry_edit.get()
                student_dob_edit = dob_entry_edit.get()
                student_que_edit = que_entry_edit.get()
                student_class_id_edit = class_id_combobox_edit.get()

                # Update the student in the database
                update_query = f"UPDATE HocSinh SET HoTen = '{student_name_edit}', NgaySinh = '{student_dob_edit}', QueQuan = '{student_que_edit}', LopHocID = '{student_class_id_edit}' WHERE HocSinhID = {student_id_edit}"
                cursor = conn.cursor()
                cursor.execute(update_query)
                conn.commit()

                # Update the Treeview with the edited data
                tree.item(selected_item, values=(
                student_id_edit, student_name_edit, student_dob_edit, student_que_edit, student_class_id_edit))

                # Update the total students label
                update_total_students_label()

                # Close the edit_window
                edit_window.destroy()

            except ValueError as e:
                tk.messagebox.showerror("Error", f"Invalid input: {e}")
            except mysql.connector.Error as err:
                tk.messagebox.showerror("MySQL Error", f"MySQL Error: {err}")

        # Button to trigger the data update
        update_button = ttk.Button(edit_window, text="Cập nhập", command=update_student)
        update_button.grid(row=5, column=0, columnspan=2, pady=10)

    def delete_student():
        selected_item = tree.selection()
        if not selected_item:
            tk.messagebox.showwarning("Warning", "Vui lòng chọn học sinh để xóa.")
            return

        # Confirm the deletion with the user
        confirm = tk.messagebox.askyesno("Chấp nhận", "Bạn muốn xóa học sinh này?")
        if not confirm:
            return

        # Get the ID of the selected student
        student_id_delete = tree.item(selected_item, 'values')[0]

        try:
            # Delete the student from the database
            delete_query = f"DELETE FROM HocSinh WHERE HocSinhID = {student_id_delete}"
            cursor = conn.cursor()
            cursor.execute(delete_query)
            conn.commit()

            # Remove the selected item from the Treeview
            tree.delete(selected_item)
            # Update the total students label
            update_total_students_label()

        except mysql.connector.Error as err:
            # Handle MySQL errors
            tk.messagebox.showerror("MySQL Error", f"MySQL Error: {err}")

    def search_student():
        search_value = search_entry.get().strip()
        if not search_value:
            messagebox.showwarning("Lỗi", "Vui lòng nhập tên học sinh tìm kiếm.")
            return
        # Clear the Treeview
        tree.delete(*tree.get_children())

        try:
            cursor = conn.cursor()
            # Dynamically generate the SQL query based on the search value
            search_query =f"SELECT * FROM HocSinh WHERE HoTen LIKE '%{search_value}%'"
            cursor.execute(search_query)
            rows = cursor.fetchall()

            # Clear the Treeview
            tree.delete(*tree.get_children())

            # Insert data into the Treeview
            for row in rows:
                tree.insert("", "end", values=row)
            update_total_students_label()
        except mysql.connector.Error as err:
            # Handle MySQL errors
            tk.messagebox.showerror("MySQL Error", f"MySQL Error: {err}")

    def show_all_students():
        # Clear the Treeview
        tree.delete(*tree.get_children())

        try:
            # Fetch data from the MySQL table
            cursor.execute("SELECT * FROM HocSinh")
            rows = cursor.fetchall()

            # Insert data into the Treeview
            for row in rows:
                tree.insert("", "end", values=row)

            # Update the total students label
            update_total_students_label()

        except mysql.connector.Error as err:
            # Handle MySQL errors
            tk.messagebox.showerror("MySQL Error", f"MySQL Error: {err}")

    def export_to_excel():
        try:
            # Fetch all data from the database
            query_all = "SELECT * FROM HocSinh"
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
                # Modified: Read data from the Excel file using Pandas
                df_import = pd.read_excel(file_path)

                # Validate the Excel file structure (adjust column names accordingly)
                required_columns = {"HocSinhID", "HoTen", "NgaySinh", "QueQuan", "LopHocID"}
                if not required_columns.issubset(df_import.columns):
                    tk.messagebox.showerror("Error", "Invalid Excel file structure. Required columns are missing.")
                    return

                # Insert data into the database
                for row_import in df_import.itertuples(index=False):
                    insert_query = f"INSERT INTO HocSinh (HocSinhID, HoTen, NgaySinh, QueQuan, LopHocID) VALUES ({row_import.HocSinhID}, '{row_import.HoTen}', '{row_import.NgaySinh}', '{row_import.QueQuan}', '{row_import.LopHocID}')"
                    cursor = conn.cursor()
                    cursor.execute(insert_query)
                    conn.commit()

                # Refresh the Treeview with the new data
                show_all_students()

                # Update the total students label
                update_total_students_label()

                tk.messagebox.showinfo("Thành công", "Dữ liệu lấy từ file execl thành công.")
        except mysql.connector.Error as err:
            tk.messagebox.showerror("MySQL Error", f"MySQL Error: {err}")
        except Exception as e:
            tk.messagebox.showerror("Error", f"An error occurred: {e}")

    show_all_button = ttk.Button(warehourse_window, text="Hiển thị tất cả", command=show_all_students)
    show_all_button.grid(row=1, column=3, pady=10, sticky="ew")

    # Button to trigger the search
    search_button = ttk.Button(warehourse_window, text="Tìm kiếm", command=search_student)
    search_button.grid(row=1, column=2, pady=10, sticky="ew")

    # Entry widget for user input in search
    search_entry = ttk.Entry(warehourse_window, width=20)
    search_entry.grid(row=1, column=1, padx=5, pady=10, sticky="ew")

    add_button = ttk.Button(warehourse_window, text="Thêm", command=add_student)
    add_button.grid(row=2, column=1, pady=10, padx=10, sticky="ew")

    # Button to trigger the edit
    edit_button = ttk.Button(warehourse_window, text="Sửa", command=edit_student)
    edit_button.grid(row=2, column=2, pady=10, padx=10, sticky="ew")

    # Button to trigger the delete
    delete_button = ttk.Button(warehourse_window, text="Xóa", command=delete_student)
    delete_button.grid(row=2, column=3, pady=10, padx=10, sticky="ew")

    export_button = ttk.Button(warehourse_window, text="Xuất ra excel", command=export_to_excel)
    export_button.grid(row=1, column=4, pady=10, sticky="ew")

    import_button = ttk.Button(warehourse_window, text="Nhập bằng excel", command=import_from_excel)
    import_button.grid(row=2, column=4, pady=10, sticky="ew")

    label = ttk.Label(warehourse_window, text="Dữ liệu học sinh", style="GreenLabel.TLabel")
    label.grid(row=0, column=2, pady=10,padx=100, columnspan=4)