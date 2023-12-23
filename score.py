import tkinter as tk
from tkinter import ttk,messagebox,filedialog
from styles import configure_styles
import mysql.connector
import pandas as pd
def display_score(root):
    #gọi hàm style căn chỉnh
    configure_styles()
    history_window = tk.Toplevel(root)
    history_window.title("history")
        # Lấy kích thước của màn hình
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    window_width = 900  # Thay đổi kích thước theo nhu cầu
    window_height = 500  # Thay đổi kích thước theo nhu cầu
    # Tính toán vị trí để cửa sổ xuất hiện giữa màn hình
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    # Đặt vị trí cửa sổ
    history_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def close_window_2():
        history_window.destroy()  # Đóng cửa sổ 2
        root.deiconify() 
    back_button = ttk.Button(history_window, text="Quay lại", command=close_window_2, style='Back_Bbutton.TButton')
    back_button.grid(row=0, column=5, pady=10)

    score_tree = ttk.Treeview(history_window, columns=("HoTen", "HocSinhID","Diem_toan", "Diem_van", "Diem_anh","Diem_tb","Hoc_luc"),
                              show="headings")
    score_tree.heading("HoTen",text="Họ Tên")
    score_tree.heading("HocSinhID", text="Mã học sinh")
    score_tree.heading("Diem_toan", text="Điểm Toán")
    score_tree.heading("Diem_van", text="Điểm Văn")
    score_tree.heading("Diem_anh", text="Điểm Anh")
    score_tree.heading("Diem_tb", text="Điểm tb")
    score_tree.heading("Hoc_luc", text="Học lực")
    score_tree.column("HoTen", width=200)
    score_tree.column("HocSinhID", width=110)
    score_tree.column("Diem_toan", width=110)
    score_tree.column("Diem_van", width=110)
    score_tree.column("Diem_anh", width=110)
    score_tree.column("Diem_tb", width=120)
    score_tree.column("Hoc_luc", width=120)
    score_tree['height'] = 12
    # Connect to your MySQL database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456789",
        database="qlsv"
    )

    cursor = conn.cursor()
    # Fetch data from the MySQL table
    cursor.execute("SELECT * FROM diemhocsinh")
    rows = cursor.fetchall()

    # Insert data into the Treeview
    for row in rows:
        score_tree.insert("", "end", values=row)

    score_tree.grid(row=4, column=2, columnspan=5, rowspan=10, pady=10, padx=10, sticky="nsew")

    def add_score():
        add_score_window = tk.Toplevel(history_window)
        add_score_window.title("Thêm điểm")

        toan_entry = ttk.Entry(add_score_window, width=10)
        van_entry = ttk.Entry(add_score_window, width=10)
        anh_entry = ttk.Entry(add_score_window, width=10)

        toan_label = ttk.Label(add_score_window, text="Điểm Toán:")
        van_label = ttk.Label(add_score_window, text="Điểm Văn:")
        anh_label = ttk.Label(add_score_window, text="Điểm Anh:")

        # Add a Combobox for HocSinhID
        id_label = ttk.Label(add_score_window, text="Mã học sinh:")
        id_combobox = ttk.Combobox(add_score_window, width=10, state="readonly")
        id_combobox.grid(row=1, column=1, padx=5, pady=5)
        id_label.grid(row=1, column=0, padx=5, pady=5)
        # Add a Combobox for selecting the name of the student (HoTen)
        name_label = ttk.Label(add_score_window, text="Họ Tên:")
        name_combobox = ttk.Combobox(add_score_window, width=20, state="readonly")
        name_combobox.grid(row=1, column=3, padx=5, pady=5)
        name_label.grid(row=1, column=2, padx=5, pady=5)


        toan_label.grid(row=2, column=0, padx=5, pady=5)
        toan_entry.grid(row=2, column=1, padx=5, pady=5)
        van_label.grid(row=3, column=0, padx=5, pady=5)
        van_entry.grid(row=3, column=1, padx=5, pady=5)
        anh_label.grid(row=4, column=0, padx=5, pady=5)
        anh_entry.grid(row=4, column=1, padx=5, pady=5)

        # Fetch HocSinhID values from the HocSinh table
        try:
            query_hocsinh_info = "SELECT HocSinhID, HoTen FROM HocSinh"
            hocsinh_info_df = pd.read_sql_query(query_hocsinh_info, conn)

            # Add a placeholder as the initial value for the Combobox
            id_combobox["values"] =  hocsinh_info_df["HocSinhID"].astype(str).tolist()
            id_combobox.set("Chọn mã học sinh")  # Set the default value

            # Add a placeholder as the initial value for the Combobox
            name_combobox["values"] =hocsinh_info_df["HoTen"].tolist()
            name_combobox.set("Chọn họ tên")  # Set the default value

        except mysql.connector.Error as err:
            messagebox.showerror("MySQL Error", f"MySQL Error: {err}")

        def insert_score():
            try:
                hoc_sinh_id = int(id_combobox.get())
                selected_name = name_combobox.get()
                diem_toan = float(toan_entry.get())
                diem_van = float(van_entry.get())
                diem_anh = float(anh_entry.get())

                check_query = f"SELECT HocSinhID FROM DiemHocSinh WHERE HocSinhID = {hoc_sinh_id}"
                existing_ids = pd.read_sql_query(check_query, conn)["HocSinhID"].tolist()

                if existing_ids:
                    messagebox.showerror("Lỗi", "Mã học sinh đã có. Vui lòng nhập mã khác.")
                    return

                insert_query = f"INSERT INTO DiemHocSinh ( HoTen,HocSinhID, Diem_toan, Diem_van, Diem_anh) " \
                               f"VALUES ('{selected_name}', {hoc_sinh_id}, {diem_toan}, {diem_van}, {diem_anh})"
                cursor = conn.cursor()
                cursor.execute(insert_query)
                conn.commit()

                # Fetch the generated HoTen after the insertion
                query_HoTen = f"SELECT HoTen FROM DiemHocSinh WHERE HocSinhID = {hoc_sinh_id}"
                selected_name = pd.read_sql_query(query_HoTen, conn)["HoTen"].values[0]

                # Update the Treeview with the new data including the generated HoTen
                score_tree.insert("", "end",
                                  values=( selected_name,  hoc_sinh_id,diem_toan, diem_van, diem_anh))

                id_combobox.set("Chọn mã học sinh")  # Set the default value
                name_combobox.set("Chọn họ tên")  # Set the default value
                add_score_window.destroy()

            except ValueError as e:
                messagebox.showerror("Error", f"Invalid input: {e}")
            except mysql.connector.Error as err:
                messagebox.showerror("MySQL Error", f"MySQL Error: {err}")

        insert_button = ttk.Button(add_score_window, text="Thêm điểm", command=insert_score)
        insert_button.grid(row=5, column=0, columnspan=2, pady=10)

    def delete_score():
        selected_item = score_tree.selection()
        if not selected_item:
            messagebox.showwarning("Lỗi", "Vui lòng chọn học sinh để xóa điểm.")
            return

        # Confirm the deletion with the user
        confirm = messagebox.askyesno("Chấp nhận", "Bạn có muốn xóa điểm học sinh này?")
        if not confirm:
            return

        # Get the HoTen of the selected score
        diem_id_delete = score_tree.item(selected_item, 'values')[0]

        try:
            # Delete the score from the database
            delete_query = f"DELETE FROM DiemHocSinh WHERE HoTen = '{diem_id_delete}'"
            cursor = conn.cursor()
            cursor.execute(delete_query)
            conn.commit()

            # Remove the selected item from the Treeview
            score_tree.delete(selected_item)
            # Display a success message
            messagebox.showinfo("Thành công", "Điểm đã xóa thành công.")

        except mysql.connector.Error as err:
            # Handle MySQL errors
            messagebox.showerror("MySQL Error", f"MySQL Error: {err}")


    def edit_score():
        selected_item = score_tree.selection()

        if not selected_item:
            messagebox.showwarning("Lỗi", "Vui lòng chọn học sinh để sửa điểm.")
            return

        selected_data = score_tree.item(selected_item, "values")
        original_hoc_sinh_id = selected_data[1]

        edit_score_window = tk.Toplevel(history_window)
        edit_score_window.title("Sửa điểm")

        diem_toan_var = tk.DoubleVar()
        diem_van_var = tk.DoubleVar()
        diem_anh_var = tk.DoubleVar()

        # Add a Combobox for HocSinhID
        # id_label = ttk.Label(edit_score_window, text="Học Sinh ID:")
        id_combobox = ttk.Combobox(edit_score_window, width=10, state="readonly")
        # id_combobox.grid(row=1, column=1, padx=5, pady=5)
        # id_label.grid(row=1, column=0, padx=5, pady=5)

        # Add a Combobox for selecting the name of the student (HoTen)
        # name_label = ttk.Label(edit_score_window, text="Họ Tên:")
        name_combobox = ttk.Combobox(edit_score_window, width=20, state="readonly")
        # name_combobox.grid(row=1, column=1, padx=5, pady=5)
        # name_label.grid(row=1, column=0, padx=5, pady=5)
        try:
            query_hocsinh_info = "SELECT HocSinhID, HoTen FROM HocSinh"
            hocsinh_info_df = pd.read_sql_query(query_hocsinh_info, conn)

            # Add a placeholder as the initial value for the Combobox
            id_combobox["values"] = hocsinh_info_df["HocSinhID"].astype(str).tolist()
            id_combobox.set(original_hoc_sinh_id)  # Set the original value

            # Add a placeholder as the initial value for the Combobox
            name_combobox["values"] = hocsinh_info_df["HoTen"].tolist()
            name_combobox.set(selected_data[0])  # Set the original value

        except mysql.connector.Error as err:
            messagebox.showerror("MySQL Error", f"MySQL Error: {err}")

        # Populate the entry fields with the selected data
        diem_toan_var.set(selected_data[2])
        diem_van_var.set(selected_data[3])
        diem_anh_var.set(selected_data[4])

        toan_entry = ttk.Entry(edit_score_window, width=10, textvariable=diem_toan_var)
        van_entry = ttk.Entry(edit_score_window, width=10, textvariable=diem_van_var)
        anh_entry = ttk.Entry(edit_score_window, width=10, textvariable=diem_anh_var)

        toan_label = ttk.Label(edit_score_window, text="Điểm Toán:")
        van_label = ttk.Label(edit_score_window, text="Điểm Văn:")
        anh_label = ttk.Label(edit_score_window, text="Điểm Anh:")

        toan_label.grid(row=2, column=0, padx=5, pady=5)
        toan_entry.grid(row=2, column=1, padx=5, pady=5)
        van_label.grid(row=3, column=0, padx=5, pady=5)
        van_entry.grid(row=3, column=1, padx=5, pady=5)
        anh_label.grid(row=4, column=0, padx=5, pady=5)
        anh_entry.grid(row=4, column=1, padx=5, pady=5)

        def update_score():
            try:
                # Get the updated values from the entry widgets
                hoc_sinh_id = int(id_combobox.get())
                selected_name = name_combobox.get()
                diem_toan = float(diem_toan_var.get())
                diem_van = float(diem_van_var.get())
                diem_anh = float(diem_anh_var.get())

                # Update the score in the database
                update_query = f"UPDATE DiemHocSinh SET HoTen='{selected_name}',HocSinhID={hoc_sinh_id},  " \
                               f"Diem_toan={diem_toan}, Diem_van={diem_van}, Diem_anh={diem_anh} " \
                               f"WHERE HocSinhID={original_hoc_sinh_id}"
                cursor = conn.cursor()
                cursor.execute(update_query)
                conn.commit()

                # Update the Treeview with the new data
                updated_data = (selected_name, hoc_sinh_id,  diem_toan, diem_van, diem_anh)
                score_tree.item(selected_item, values=updated_data)

                # Close the edit_score_window
                edit_score_window.destroy()

            except ValueError as e:
                messagebox.showerror("Error", f"Invalid input: {e}")
            except mysql.connector.Error as err:
                messagebox.showerror("MySQL Error", f"MySQL Error: {err}")

        update_button = ttk.Button(edit_score_window, text="Cập nhập", command=update_score)
        update_button.grid(row=5, column=0, columnspan=2, pady=10)

    def show_all_students():
        # Clear the Treeview
        score_tree.delete(*score_tree.get_children())

        try:
            # Fetch data from the MySQL table
            cursor.execute("SELECT * FROM diemhocsinh")
            rows = cursor.fetchall()

            # Insert data into the Treeview
            for row in rows:
                score_tree.insert("", "end", values=row)

        except mysql.connector.Error as err:
            # Handle MySQL errors
            tk.messagebox.showerror("MySQL Error", f"MySQL Error: {err}")

    def search_scores():
        # Get the search criteria from the entry widget
        search_criteria = search_entry.get().strip()

        if not search_criteria:
            messagebox.showwarning("Lỗi", "Vui lòng nhập tên học sinh tìm kiếm.")
            return

        # Clear the Treeview
        score_tree.delete(*score_tree.get_children())

        try:
            # Fetch data from the database based on the search criteria
            query_search = f"SELECT * FROM DiemHocSinh WHERE HoTen LIKE '%{search_criteria}%'"

            # Fetch data from the MySQL table
            cursor.execute(query_search)
            rows = cursor.fetchall()

            # Insert data into the Treeview
            for row in rows:
                score_tree.insert("", "end", values=row)

        except mysql.connector.Error as err:
            # Handle MySQL errors
            tk.messagebox.showerror("MySQL Error", f"MySQL Error: {err}")

    def sort_by_name():
        # Clear the Treeview
        score_tree.delete(*score_tree.get_children())

        try:
            cursor.execute("SELECT * FROM DiemHocSinh ORDER BY HoTen")
            rows = cursor.fetchall()

            # Insert data into the Treeview
            for row in rows:
                score_tree.insert("", "end", values=row)

        except mysql.connector.Error as err:
            # Handle MySQL errors
            tk.messagebox.showerror("MySQL Error", f"MySQL Error: {err}")

    def sort_by_subject(subject):
        # Clear the Treeview
        score_tree.delete(*score_tree.get_children())

        try:
            cursor.execute(f"SELECT * FROM DiemHocSinh ORDER BY {subject} DESC")
            rows = cursor.fetchall()

            # Insert data into the Treeview
            for row in rows:
                score_tree.insert("", "end", values=row)

        except mysql.connector.Error as err:
            # Handle MySQL errors
            tk.messagebox.showerror("MySQL Error", f"MySQL Error: {err}")

    def analyze_performance():
        # Clear the Treeview
        score_tree.delete(*score_tree.get_children())

        try:
            # Fetch data from the database
            query_analyze = "SELECT HoTen, HocSinhID, Diem_toan, Diem_van, Diem_anh FROM DiemHocSinh"
            df_analyze = pd.read_sql_query(query_analyze, conn)

            # Calculate average scores and categorize performance
            for row_analyze in df_analyze.itertuples(index=False):
                ho_ten = row_analyze[0]
                hoc_sinh_id = row_analyze[1]
                diem_toan = row_analyze[2]
                diem_van = row_analyze[3]
                diem_anh = row_analyze[4]

                # Calculate average score
                Diem_tb = format((diem_toan + diem_van + diem_anh) / 3, '.2f')

                # Categorize performance
                Hoc_luc = categorize_performance(float(Diem_tb))

                # Insert data into the Treeview
                score_tree.insert("", "end", values=(
                ho_ten, hoc_sinh_id, diem_toan, diem_van, diem_anh, Diem_tb, Hoc_luc))

                # Update the analyzed data back to MySQL
                # update_query = f"UPDATE DiemHocSinh SET Diem_tb = {Diem_tb}, Hoc_luc = {Hoc_luc} " \
                #                f"WHERE HocSinhID = {hoc_sinh_id}"
                # cursor = conn.cursor()
                # cursor.execute(update_query)
                # conn.commit()
        except mysql.connector.Error as err:
            # Handle MySQL errors
            tk.messagebox.showerror("MySQL Error", f"MySQL Error: {err}")

    def categorize_performance(average_score):
        # Define performance level thresholds
        excellent_threshold = 8.0
        good_threshold = 6.5
        average_threshold = 5.0

        # Categorize performance based on average score
        if average_score >= excellent_threshold:
            return "Giỏi"
        elif average_score >= good_threshold:
            return "Khá"
        elif average_score >= average_threshold:
            return "Trung bình"
        else:
            return "Yếu"

    show_all_button = ttk.Button(history_window, text="Hiển thị tất cả", command=show_all_students)
    show_all_button.grid(row=2, column=5, pady=10, sticky="ew")
    # Add a button to trigger the edit_score function
    edit_score_button = ttk.Button(history_window, text="Sửa điểm", command=edit_score)
    edit_score_button.grid(row=2, column=4, pady=10, sticky="ew")

    # Add a button to trigger the delete_score function
    delete_score_button = ttk.Button(history_window, text="Xóa", command=delete_score)
    delete_score_button.grid(row=2, column=3, pady=10, sticky="ew")

    add_score_button = ttk.Button(history_window, text="Thêm", command=add_score)
    add_score_button.grid(row=2, column=2, pady=10, sticky="ew")

    analyze_performance_button = ttk.Button(history_window, text="Phân tích", command=analyze_performance)
    analyze_performance_button.grid(row=1, column=4, pady=10, sticky="ew")

    search_entry = ttk.Entry(history_window, width=20)
    search_entry.grid(row=1, column=2, padx=5, pady=10, sticky="ew")

    # Add a button to trigger the search_scores function
    search_button = ttk.Button(history_window, text="Tìm kiếm", command=search_scores)
    search_button.grid(row=1, column=3, pady=10, sticky="ew")

    sort_by_name_button = ttk.Button(history_window, text="Sắp xếp theo tên", command=sort_by_name)
    sort_by_name_button.grid(row=3, column=2, pady=10, sticky="ew")

    sort_by_toan_button = ttk.Button(history_window, text="Sắp xếp theo điểm Toán",
                                     command=lambda: sort_by_subject("Diem_toan"))
    sort_by_toan_button.grid(row=3, column=3, pady=10, sticky="ew")

    sort_by_van_button = ttk.Button(history_window, text="Sắp xếp theo điểm Văn",
                                    command=lambda: sort_by_subject("Diem_van"))
    sort_by_van_button.grid(row=3, column=4, pady=10, sticky="ew")

    sort_by_anh_button = ttk.Button(history_window, text="Sắp xếp theo điểm Anh",
                                    command=lambda: sort_by_subject("Diem_anh"))
    sort_by_anh_button.grid(row=3, column=5, pady=10, sticky="ew")

    label = ttk.Label(history_window, text="Dữ liệu điểm học sinh", style="GreenLabel.TLabel")
    label.grid(row=0, column=2, pady=10,padx=100, columnspan=2)
    