import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.simpledialog
from styles import configure_styles
import mysql.connector
from openpyxl import Workbook

def classroom(root):
    # Gọi hàm style căn chỉnh
    configure_styles()
    sell_window = tk.Toplevel(root)
    sell_window.title("Lớp học")
    # Lấy kích thước của màn hình
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    window_width = 700  # Thay đổi kích thước theo nhu cầu
    window_height = 550  # Thay đổi kích thước theo nhu cầu
    # Tính toán vị trí để cửa sổ xuất hiện giữa màn hình
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2

    # Đặt vị trí cửa sổ
    sell_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def close_window_2():
        sell_window.destroy()  # Đóng cửa sổ thứ 2
        root.deiconify()

    back_button = ttk.Button(sell_window, text="Quay lại", command=close_window_2, style='Back_Bbutton.TButton')
    back_button.grid(row=0, column=1, pady=10, padx=10)
    label = ttk.Label(sell_window, text="Dữ liệu lớp học", style="GreenLabel.TLabel")
    label.grid(row=0, column=2, pady=10, padx=100, columnspan=4)

    tree = ttk.Treeview(sell_window, columns=("TenLop", "tonghocsinh", "tengiaovien"), show="headings")

    tree.heading("TenLop", text="Tên lớp")
    tree.heading("tonghocsinh", text="Tổng học sinh")
    tree.heading("tengiaovien", text="Giáo viên")
    tree.column("TenLop", width=225)
    tree.column("tonghocsinh", width=225)
    tree.column("tengiaovien", width=225)
    tree['height'] = 17

    # Connect to MySQL (adjust these details)
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="080102",
        database="ma_ng_mo"
    )

    cursor = connection.cursor()

    # Fetch data from the MySQL table
    cursor.execute("SELECT TenLop,tonghocsinh,tengiaovien FROM LopHoc")
    rows = cursor.fetchall()

    # Insert data into the Treeview
    for row in rows:
        tree.insert("", "end", values=row)

    # Pack the Treeview to the window
    tree.grid(row=3, column=1, columnspan=3, rowspan=10, pady=10, padx=10, sticky="nsew")
    # Display the total number of classes
    total_classes_label = ttk.Label(sell_window, text=f"Tổng số lớp học: {len(rows)}", style="GreenLabel.TLabel")
    total_classes_label.place(relx=0.4, rely=0.85)

    def edit_class():
        selected_item = tree.selection()

        if not selected_item:
            messagebox.showinfo("Thông báo", "Vui lòng chọn một lớp để sửa.")
            return

        # Get the values of the selected row
        selected_values = tree.item(selected_item, 'values')

        # Create a simple dialog for editing
        edit_dialog = tkinter.simpledialog.Toplevel(sell_window)
        edit_dialog.title("Sửa thông tin lớp học")

        # Create Entry widgets to allow editing
        ten_lop_entry = ttk.Entry(edit_dialog)
        tong_so_hoc_sinh_entry = ttk.Entry(edit_dialog)

        # Use a Combobox for selecting the teacher name
        ten_giao_vien_combobox = ttk.Combobox(edit_dialog, values=get_teacher_names())
        ttk.Label(edit_dialog, text="Tên giáo viên:").grid(row=2, column=0, padx=10, pady=5, sticky="e")
        ten_giao_vien_combobox.grid(row=2, column=1, padx=10, pady=5)
        ten_giao_vien_combobox.set(selected_values[2] if selected_values[2] else "")  # Set the initial value

        # Set other labels and entry widgets
        # ttk.Label(edit_dialog, text="Tên lớp:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        # ten_lop_entry.grid(row=0, column=1, padx=10, pady=5)
        ten_lop_entry.insert(0, selected_values[0] if selected_values[0] else "")

        ttk.Label(edit_dialog, text="Tổng số học sinh:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        tong_so_hoc_sinh_entry.grid(row=1, column=1, padx=10, pady=5)
        tong_so_hoc_sinh_entry.insert(0, selected_values[1] if selected_values[1] else "")

        def save_changes():
            # Get the edited values
            edited_ten_lop = ten_lop_entry.get()
            edited_tong_so_hoc_sinh = tong_so_hoc_sinh_entry.get()
            edited_ten_giao_vien = ten_giao_vien_combobox.get()

            # Update the Treeview with the edited values
            tree.item(selected_item, values=(edited_ten_lop, edited_tong_so_hoc_sinh, edited_ten_giao_vien))
            # Update the database
            update_query = "UPDATE LopHoc SET TenLop=%s, tonghocsinh=%s, tengiaovien=%s WHERE TenLop=%s"
            update_values = (edited_ten_lop, edited_tong_so_hoc_sinh, edited_ten_giao_vien, selected_values[0])

            try:
                cursor.execute(update_query, update_values)
                connection.commit()
                messagebox.showinfo("Thông báo", "Dữ liệu đã được cập nhật thành công.")
            except mysql.connector.Error as err:
                messagebox.showerror("Lỗi", f"Lỗi MySQL: {err}")
                connection.rollback()

            # Close the edit dialog
            edit_dialog.destroy()

        ttk.Button(edit_dialog, text="Lưu", command=save_changes).grid(row=3, column=0, columnspan=2, pady=10)

    def get_teacher_names():
        # Connect to MySQL (adjust these details)
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="080102",
            database="ma_ng_mo"
        )

        cursor = connection.cursor()

        # Fetch teacher names from the giaovien table
        cursor.execute("SELECT HoTen FROM giaovien")
        teacher_names = [row[0] for row in cursor.fetchall()]

        # Close the database connection
        connection.close()

        return teacher_names

    def export_to_excel():
        try:
            # Create a new Workbook and select the active sheet
            workbook = Workbook()
            sheet = workbook.active

            # Add column headers
            headers = ["Tên lớp", "Tổng học sinh", "Giáo viên"]
            sheet.append(headers)

            # Fetch data from the MySQL table
            cursor.execute("SELECT TenLop, tonghocsinh, tengiaovien FROM LopHoc")
            rows = cursor.fetchall()

            # Insert data into the Excel sheet
            for row in rows:
                sheet.append(row)

            # Save the workbook to a file
            workbook.save("lop_hoc_data.xlsx")
            messagebox.showinfo("Thông báo", "Dữ liệu đã được xuất ra file Excel thành công.")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Xuất Excel thất bại: {e}")

    edit_button = ttk.Button(sell_window, text="Sửa", command=edit_class )
    edit_button.place(relx=0.05, rely=0.88)

    export_button = ttk.Button(sell_window, text=" Xuất Excel ", command=export_to_excel )
    export_button.place(relx=0.2, rely=0.88)



