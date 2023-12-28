import tkinter as tk
from tkinter import ttk,messagebox,filedialog
from styles import configure_styles
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
def display_score(root):
    #gọi hàm style căn chỉnh
    configure_styles()
    history_window = tk.Toplevel(root)
    history_window.title("Bảng điểm")
        # Lấy kích thước của màn hình
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    window_width = 1350  # Thay đổi kích thước theo nhu cầu
    window_height = 600  # Thay đổi kích thước theo nhu cầu
    # Tính toán vị trí để cửa sổ xuất hiện giữa màn hình
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    # Đặt vị trí cửa sổ
    history_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def close_window_2():
        history_window.destroy()  # Đóng cửa sổ 2
        root.deiconify() 
    back_button = ttk.Button(history_window, text="Quay lại", command=close_window_2, style='Back_Bbutton.TButton')
    back_button.grid(row=0, column=2, pady=10)

    total_students_label = ttk.Label(history_window, text="Tổng số học sinh: 0", style="GreenLabel.TLabel")
    total_students_label.grid(row=15, column=2, pady=10, columnspan=2)

    subjects = ["Diem_toan", "Diem_van", "Diem_anh", "Dao_duc", "Tn_Xh", "Lsu_Dly", "Khoa_hoc", "Tin_Congnghe",
                "The_chat", "Nghe_thuat"]
    def calculate_subject_averages():
        # Fetch data from the MySQL table
        cursor.execute("SELECT * FROM diemhocsinh")
        rows = cursor.fetchall()

        # Create a dictionary to store the sum and count for each subject
        subject_sum = {subject: 0 for subject in subjects}
        subject_count = {subject: 0 for subject in subjects}

        # Calculate the sum and count for each subject
        for row in rows:
            for i, subject in enumerate(subjects, start=4):  # Assuming subjects start from the 3rd column
                subject_sum[subject] += row[i]
                subject_count[subject] += 1

        # Calculate the average for each subject
        subject_averages = {subject: subject_sum[subject] / subject_count[subject] if subject_count[subject] > 0 else 0
                            for subject in subjects}

        return subject_averages
    def is_valid_float(value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def validate_input(action, index, value_if_allowed, prior_value, text, validation_type, trigger_type, widget_name):
        if action == '1':  # insert
            try:
                # Try converting the value to a float
                float_value = float(value_if_allowed)
                
                # Check if the float value is within the desired range
                if 0 <= float_value <= 10:
                    return True
                else:
                    return False
            except ValueError:
                return False
        else:  # delete
            return True


    def plot_bar_chart():
        # Calculate subject averages
        subject_averages = calculate_subject_averages()

        # Plot the bar chart
        subjects = list(subject_averages.keys())
        scores = list(subject_averages.values())

        plt.figure(figsize=(13, 6))
        plt.bar(subjects, scores, color='skyblue')
        plt.xlabel('Môn học')
        plt.ylabel('Điểm trung bình')
        plt.title('Phổ điểm theo môn học')

        # Show the plot
        plt.show()

    def on_button_click():
        # Handle button click event
        try:
            # Call the function to calculate averages and plot the bar chart
            plot_bar_chart()
        except Exception as e:
            # Handle any exceptions that might occur during the process
            messagebox.showerror("Lỗi", "Lỗi")

    def update_total_students_label():
        total_students = len(score_tree.get_children())
        total_students_label.config(text=f"Tổng số học sinh: {total_students}")

    sort_order = {}

    def sort_treeview(column):
        # Toggle the sort order (default to "asc" if not set)
        current_order = sort_order.get(column, "asc")
        new_order = "desc" if current_order == "asc" else "asc"
        sort_order[column] = new_order

        # Get all the items in the Treeview
        items = score_tree.get_children('')

        # Sort the items based on the selected column and sort order
        items = sorted(items, key=lambda x: score_tree.set(x, column), reverse=(new_order == "desc"))

        # Update the Treeview with the sorted items
        for index, item in enumerate(items):
            score_tree.move(item, '', index)

    def setup_sortable_treeview_columns():
        # Add sorting functionality to each column heading
        for col in ["HoTen", "HocSinhID","Ten_lop", "Diem_toan", "Diem_van", "Diem_anh",
                    "Dao_duc", "Tn_Xh", "Lsu_Dly", "Khoa_hoc", "Tin_Congnghe",
                    "The_chat", "Nghe_thuat"]:
            score_tree.heading(col, text=col, command=lambda c=col: sort_treeview(c))

    score_tree = ttk.Treeview(history_window, columns=("HoTen", "HocSinhID","Ten_lop","Diem_toan", "Diem_van", "Diem_anh"
                                                       ,"Dao_duc", "Tn_Xh","Lsu_Dly", "Khoa_hoc", "Tin_Congnghe"
                                                       ,"The_chat", "Nghe_thuat"),show="headings")
    setup_sortable_treeview_columns()
    score_tree.heading("HoTen",text="Họ Tên")
    score_tree.heading("HocSinhID", text="Mã học sinh")
    score_tree.heading("Ten_lop", text="Lớp")
    score_tree.heading("Diem_toan", text="Toán")
    score_tree.heading("Diem_van", text="Văn")
    score_tree.heading("Diem_anh", text="Anh")
    score_tree.heading("Dao_duc", text="Đạo đức")
    score_tree.heading("Tn_Xh", text="Tự nhiên, xã hội")
    score_tree.heading("Lsu_Dly", text="Lịch sử, địa lý")
    score_tree.heading("Khoa_hoc", text="Khoa học")
    score_tree.heading("Tin_Congnghe", text="Tin học, công nghệ")
    score_tree.heading("The_chat", text="Thể chất")
    score_tree.heading("Nghe_thuat", text="Nghệ thuật")
    score_tree.column("HoTen", width=100)
    score_tree.column("HocSinhID", width=100)
    score_tree.column("Ten_lop", width=100)
    score_tree.column("Diem_toan", width=100)
    score_tree.column("Diem_van", width=100)
    score_tree.column("Diem_anh", width=100)
    score_tree.column("Dao_duc", width=100)
    score_tree.column("Tn_Xh", width=100)
    score_tree.column("Lsu_Dly", width=100)
    score_tree.column("Khoa_hoc", width=100)
    score_tree.column("Tin_Congnghe", width=120)
    score_tree.column("The_chat", width=100)
    score_tree.column("Nghe_thuat", width=100)

    score_tree['height'] = 12
    # Connect to your MySQL database
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="080102",
        database="ma_ng_mo"
    )

    cursor = conn.cursor()
    # Fetch data from the MySQL table
    cursor.execute("SELECT HoTen, HocSinhID,Ten_lop, Diem_toan, Diem_van, Diem_anh, Dao_duc,Tn_Xh,Lsu_Dly"
                   ",Khoa_hoc,Tin_Congnghe,The_chat,Nghe_thuat FROM diemhocsinh")
    rows = cursor.fetchall()

    # Insert data into the Treeview
    for row in rows:
        score_tree.insert("", "end", values=row)
    update_total_students_label()
    score_tree.grid(row=4, column=2, columnspan=12, rowspan=10, pady=10, padx=10, sticky="nsew")

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
            update_total_students_label()

        except mysql.connector.Error as err:
            # Handle MySQL errors
            messagebox.showerror("Lôi", f"MySQL Error: {err}")

    def edit_score():
        selected_item = score_tree.selection()

        if not selected_item:
            messagebox.showwarning("Lỗi", "Vui lòng chọn học sinh để sửa điểm.")
            return

        selected_data = score_tree.item(selected_item, "values")
        original_hoc_sinh_id = selected_data[1]

        edit_score_window = tk.Toplevel(history_window)
        edit_score_window.title("Sửa điểm")

        hoc_sinh_id_var = tk.StringVar(value=original_hoc_sinh_id)

        name_label = ttk.Label(edit_score_window, text="Họ Tên:")
        name_combobox = ttk.Combobox(edit_score_window, width=20, state="readonly")
        name_combobox.grid(row=1, column=1, padx=5, pady=5)
        name_label.grid(row=1, column=0, padx=5, pady=5)
        try:
            query_hocsinh_info = "SELECT HoTen FROM HocSinh"
            hocsinh_info_df = pd.read_sql_query(query_hocsinh_info, conn)

            name_combobox["values"] = hocsinh_info_df["HoTen"].tolist()
            name_combobox.set(selected_data[0])

        except mysql.connector.Error as err:
            messagebox.showerror("MySQL Error", f"MySQL Error: {err}")

        class_label = ttk.Label(edit_score_window, text="Lớp:")
        class_combobox = ttk.Combobox(edit_score_window, width=20, state="readonly")
        class_combobox.grid(row=0, column=1, padx=5, pady=5)
        class_label.grid(row=0, column=0, padx=5, pady=5)
        try:
            query_class_info = "SELECT LopHocID FROM lophoc"
            class_info_df = pd.read_sql_query(query_class_info, conn)

            class_combobox["values"] = class_info_df["LopHocID"].tolist()
            class_combobox.set(selected_data[2])

        except mysql.connector.Error as err:
            messagebox.showerror("MySQL Error", f"MySQL Error: {err}")

        subject_vars = {}
        subject_entries = {}

        subjects = ["Diem_toan", "Diem_van", "Diem_anh", "Dao_duc", "Tn_Xh", "Lsu_Dly", "Khoa_hoc",
                    "Tin_Congnghe", "The_chat", "Nghe_thuat"]

        for i, subject in enumerate(subjects):
            subject_vars[subject] = tk.DoubleVar(value=float(selected_data[i + 3]))

            subject_label = ttk.Label(edit_score_window, text=f"Điểm {subject}:")
            subject_entry = ttk.Entry(
                edit_score_window, 
                textvariable=subject_vars[subject], 
                validate='key',
                validatecommand=(
                    edit_score_window.register(validate_input), 
                    '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W'
                )
            )

            subject_label.grid(row=i + 2, column=0, padx=5, pady=5, sticky="e")
            subject_entry.grid(row=i + 2, column=1, padx=5, pady=5, sticky="w")

            subject_entries[subject] = subject_entry

        def update_score():
            try:
                # Get the updated values from the entry widgets
                hoc_sinh_id = int(hoc_sinh_id_var.get())
                selected_name = name_combobox.get()
                selected_class = class_combobox.get()

                subject_values = {subject: float(var.get()) for subject, var in subject_vars.items()}

                # Update the score in the database
                update_query = f"UPDATE DiemHocSinh SET HoTen='{selected_name}', HocSinhID={hoc_sinh_id}, Ten_lop='{selected_class}', "
                for subject, value in subject_values.items():
                    update_query += f"{subject}={value}, "
                update_query = update_query.rstrip(', ')  # Remove the trailing comma
                update_query += f" WHERE HocSinhID={original_hoc_sinh_id}"

                cursor = conn.cursor()
                cursor.execute(update_query)
                conn.commit()

                # Update the Treeview with the new data
                updated_data = [selected_name, hoc_sinh_id, selected_class] + list(subject_values.values())
                score_tree.item(selected_item, values=updated_data)

                # Close the edit_score_window
                edit_score_window.destroy()

                # Display a success message
                messagebox.showinfo("Thành công", "Điểm đã được cập nhật thành công.")
                update_total_students_label()

            except Exception as e:
                messagebox.showerror("Lỗi", f"Đã xảy ra lỗi: {e}")


        update_button = ttk.Button(edit_score_window, text="Cập nhật", command=update_score)
        update_button.grid(row=len(subjects) + 2, column=0, columnspan=2, pady=10)

    def show_all_students():
        # Clear the Treeview
        score_tree.delete(*score_tree.get_children())

        try:
            # Fetch data from the MySQL table
            cursor.execute("SELECT HoTen, HocSinhID,Ten_lop, Diem_toan, Diem_van, Diem_anh, Dao_duc,Tn_Xh,Lsu_Dly"
                           ",Khoa_hoc,Tin_Congnghe,The_chat,Nghe_thuat FROM diemhocsinh")
            rows = cursor.fetchall()

            # Insert data into the Treeview
            for row in rows:
                score_tree.insert("", "end", values=row)
            update_total_students_label()

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
            query_search = f"SELECT HoTen, HocSinhID,Ten_lop, Diem_toan, Diem_van, Diem_anh, Dao_duc,Tn_Xh,Lsu_Dly,Khoa_hoc,Tin_Congnghe,The_chat,Nghe_thuat" \
                           f" FROM DiemHocSinh WHERE HoTen LIKE '%{search_criteria}%'"

            # Fetch data from the MySQL table
            cursor.execute(query_search)
            rows = cursor.fetchall()

            # Insert data into the Treeview
            for row in rows:
                score_tree.insert("", "end", values=row)
            update_total_students_label()

        except mysql.connector.Error as err:
            # Handle MySQL errors
            tk.messagebox.showerror("MySQL Error", f"MySQL Error: {err}")

    def export_to_excel():
        try:
            # Fetch data from the MySQL table
            cursor.execute("SELECT HoTen, HocSinhID,Ten_lop, Diem_toan, Diem_van, Diem_anh, Dao_duc,Tn_Xh,Lsu_Dly"
                           ",Khoa_hoc,Tin_Congnghe,The_chat,Nghe_thuat FROM diemhocsinh")
            rows = cursor.fetchall()

            # Create a DataFrame using the fetched data
            df = pd.DataFrame(rows, columns=["HoTen", "HocSinhID","Ten_lop", "Diem_toan", "Diem_van", "Diem_anh",
                                             "Dao_duc", "Tn_Xh", "Lsu_Dly", "Khoa_hoc", "Tin_Congnghe",
                                             "The_chat", "Nghe_thuat"])

            # Prompt the user for the output file path
            file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])

            if file_path:
                # Export the DataFrame to Excel
                df.to_excel(file_path, index=False)

                # Display a success message
                messagebox.showinfo("Thành công", f"Dữ liệu đã được xuất ra Excel.\nFile lưu tại: {file_path}")

        except mysql.connector.Error as err:
            # Handle MySQL errors
            tk.messagebox.showerror("MySQL Error", f"MySQL Error: {err}")

    def import_from_excel():
        try:
            # Prompt the user to select the input Excel file
            file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])

            if file_path:
                # Read data from Excel file into a DataFrame
                df = pd.read_excel(file_path)

                # Insert data into the MySQL table
                for index, row in df.iterrows():
                    # Assuming 'Ten_lop' is a string, so it should be enclosed in single quotes
                    insert_query = f"INSERT INTO diemhocsinh (HoTen, HocSinhID, Ten_lop, Diem_toan, Diem_van, Diem_anh, " \
                                   f"Dao_duc, Tn_Xh, Lsu_Dly, Khoa_hoc, Tin_Congnghe, The_chat, Nghe_thuat) " \
                                   f"VALUES ('{row['HoTen']}', {row['HocSinhID']}, '{row['Ten_lop']}', {row['Diem_toan']}, {row['Diem_van']}, " \
                                   f"{row['Diem_anh']}, {row['Dao_duc']}, {row['Tn_Xh']}, {row['Lsu_Dly']}, {row['Khoa_hoc']}, " \
                                   f"{row['Tin_Congnghe']}, {row['The_chat']}, {row['Nghe_thuat']})"
                    cursor = conn.cursor()
                    cursor.execute(insert_query)
                    conn.commit()

                # Display a success message
                messagebox.showinfo("Thành công", f"Dữ liệu đã được nhập từ Excel.\nFile: {file_path}")

                # Update the Treeview with the new data
                show_all_students()

        except pd.errors.EmptyDataError:
            # Handle empty Excel file
            messagebox.showwarning("Cảnh báo", "File Excel trống.")
        except mysql.connector.Error as err:
            # Handle MySQL errors
            messagebox.showerror("Lỗi", f"Dữ liệu lỗi")
    def delete_all_scores():
        confirm = messagebox.askyesno("Xác nhận", "Bạn có chắc muốn xóa tất cả điểm học sinh?")
        if confirm:
            try:
                # Execute a query to delete all records from the table
                delete_all_query = "DELETE FROM DiemHocSinh"
                cursor.execute(delete_all_query)
                conn.commit()

                # Clear the Treeview
                score_tree.delete(*score_tree.get_children())

                # Update the total_students_label
                update_total_students_label()

                # Display a success message
                messagebox.showinfo("Thành công", "Tất cả điểm học sinh đã được xóa.")

            except mysql.connector.Error as err:
                # Handle MySQL errors
                messagebox.showerror("Lỗi", f"MySQL Error: {err}")

    # Add a button to trigger the delete_all_scores function
    delete_all_button = ttk.Button(history_window, text="Xóa tất cả", command=delete_all_scores)
    delete_all_button.grid(row=2, column=8, pady=10, sticky="ew")
    show_all_button = ttk.Button(history_window, text="Hiển thị tất cả", command=show_all_students)
    show_all_button.grid(row=2, column=4, pady=10, sticky="ew")
    # Add a button to trigger the edit_score function
    edit_score_button = ttk.Button(history_window, text="Sửa điểm", command=edit_score)
    edit_score_button.grid(row=2, column=3, pady=10, sticky="ew")

    # Add a button to trigger the delete_score function
    delete_score_button = ttk.Button(history_window, text="Xóa", command=delete_score)
    delete_score_button.grid(row=2, column=2, pady=6, sticky="ew")

    search_entry = ttk.Entry(history_window, width=16)
    search_entry.grid(row=1, column=2, padx=5, pady=10, sticky="ew")


    # Add a button to trigger the search_scores function
    search_button = ttk.Button(history_window, text="Tìm kiếm theo tên", command=search_scores)
    search_button.grid(row=1, column=3, pady=10, sticky="ew")

    label = ttk.Label(history_window, text="Dữ liệu điểm học sinh", style="GreenLabel.TLabel")
    label.grid(row=0, column=4, pady=15,padx=100, columnspan=4)

    export_button = ttk.Button(history_window, text="Xuất ra Excel", command=export_to_excel)
    export_button.grid(row=2, column=5, pady=10, sticky="ew")

    import_button = ttk.Button(history_window, text="Nhập từ Excel", command=import_from_excel)
    import_button.grid(row=2, column=6, pady=10, sticky="ew")

    plot_button = ttk.Button(history_window, text="Hiển thị Phổ Điểm", command=on_button_click)
    plot_button.grid(row=2, column=7, pady=10, sticky="ew")