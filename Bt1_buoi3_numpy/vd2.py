import numpy as np
import tkinter as tk
from tkinter import messagebox, ttk

# Hàm tính toán
def solve_matrix():
    try:
        operation = combo_operation.get()  # Lấy tên thao tác được chọn

        # Lấy số hàng và cột của ma trận A
        n_rows_A = int(entry_rows_A.get())
        n_cols_A = int(entry_cols_A.get())

        # Lấy số hàng và cột của ma trận B nếu cần
        if operation in ["Cộng", "Trừ", "Nhân", "Chia"]:
            n_rows_B = int(entry_rows_B.get())
            n_cols_B = int(entry_cols_B.get())

        # Nhập ma trận A
        matrix_A = []
        for i in range(n_rows_A):
            row = [float(entries_A[i][j].get()) for j in range(n_cols_A)]
            matrix_A.append(row)
        A = np.array(matrix_A)

        # Xử lý theo từng thao tác
        if operation in ["Cộng", "Trừ", "Nhân", "Chia"]:
            # Nhập ma trận B
            matrix_B = []
            for i in range(n_rows_B):
                row = [float(entries_B[i][j].get()) for j in range(n_cols_B)]
                matrix_B.append(row)
            B = np.array(matrix_B)

            # Kiểm tra kích thước ma trận phù hợp
            if operation in ["Cộng", "Trừ"]:
                if A.shape != B.shape:
                    messagebox.showerror("Lỗi", "Hai ma trận phải cùng kích thước để thực hiện phép cộng hoặc trừ.")
                    return
                result = A + B if operation == "Cộng" else A - B
            elif operation == "Nhân":
                if n_cols_A != n_rows_B:
                    messagebox.showerror("Lỗi", "Số cột của ma trận A phải bằng số hàng của ma trận B để nhân.")
                    return
                result = np.dot(A, B)
            elif operation == "Chia":
                if A.shape != B.shape:
                    messagebox.showerror("Lỗi", "Hai ma trận phải cùng kích thước để thực hiện phép chia phần tử.")
                    return
                result = np.divide(A, B)
        elif operation == "Tìm ma trận nghịch đảo":
            if n_rows_A != n_cols_A:
                messagebox.showerror("Lỗi", "Ma trận phải là vuông để tìm nghịch đảo.")
                return
            result = np.linalg.inv(A)
        elif operation == "Tìm hạng ma trận":
            result = np.linalg.matrix_rank(A)
        elif operation == "Giải hệ phương trình":
            # Lấy vector B
            vector_B = [float(entries_B[i].get()) for i in range(n_rows_A)]
            B = np.array(vector_B)

            if n_rows_A != n_cols_A:
                messagebox.showerror("Lỗi", "Ma trận hệ số phải là vuông để giải hệ phương trình.")
                return

            det_A = np.linalg.det(A)
            if np.isclose(det_A, 0):
                rank_A = np.linalg.matrix_rank(A)
                rank_augmented = np.linalg.matrix_rank(np.column_stack((A, B)))
                if rank_A == rank_augmented:
                    messagebox.showinfo("Kết quả", "Hệ phương trình có vô số nghiệm.")
                else:
                    messagebox.showinfo("Kết quả", "Hệ phương trình vô nghiệm.")
            else:
                result = np.linalg.solve(A, B)
        else:
            messagebox.showerror("Lỗi", "Vui lòng chọn một thao tác hợp lệ.")
            return

        if operation not in ["Giải hệ phương trình", "Tìm hạng ma trận"]:
            label_result.config(text=result)
            # messagebox.showinfo("Kết quả", f"Kết quả là:\n{result}")
        elif operation == "Giải hệ phương trình" and not np.isclose(det_A, 0):
            result_str = "\n".join([f"x{i+1} = {val}" for i, val in enumerate(result)])
            label_result.config(text=result_str)
            # messagebox.showinfo("Kết quả", f"Nghiệm của hệ phương trình là:\n{result_str}")

        elif operation == "Tìm hạng ma trận":
            label_result.config(text=result)
            # messagebox.showinfo("Kết quả", f"Hạng của ma trận là: {result}")

    except Exception as e:
        messagebox.showerror("Lỗi", f"Có lỗi xảy ra: {str(e)}")

# Cập nhật giao diện theo thao tác đã chọn
def update_interface(event):
    operation = combo_operation.get()
    clear_entries()

    # Hiển thị hoặc ẩn các mục nhập số hàng và cột
    if operation in ["Cộng", "Trừ", "Nhân", "Chia"]:
        frame_size_A.grid()
        frame_size_B.grid()
        create_matrix_inputs(2)
    elif operation in ["Tìm ma trận nghịch đảo", "Tìm hạng ma trận"]:
        frame_size_A.grid()
        frame_size_B.grid_remove()
        create_matrix_inputs(1)
    elif operation == "Giải hệ phương trình":
        frame_size_A.grid()
        frame_size_B.grid_remove()
        create_matrix_inputs(1)

def create_matrix_inputs(num_matrices):
    global entries_A, entries_B

    # Xóa các ô nhập liệu cũ
    for widget in frame_inputs.winfo_children():
        widget.destroy()

    # Lấy số hàng và cột của ma trận A
    try:
        n_rows_A = int(entry_rows_A.get())
        n_cols_A = int(entry_cols_A.get())
    except ValueError:
        messagebox.showerror("Lỗi", "Vui lòng nhập số hàng và cột hợp lệ cho ma trận A.")
        return

    entries_A = []
    entries_B = []

    # Tạo các ô nhập liệu cho ma trận A
    tk.Label(frame_inputs, text="Ma trận A").grid(row=0, column=0, columnspan=n_cols_A)
    for i in range(n_rows_A):
        row_entries = []
        for j in range(n_cols_A):
            entry = tk.Entry(frame_inputs, width=7)
            entry.grid(row=i + 1, column=j)
            row_entries.append(entry)
        entries_A.append(row_entries)

    # Tạo các ô nhập liệu cho ma trận B hoặc vector B
    if num_matrices == 2:
        # Lấy số hàng và cột của ma trận B
        try:
            n_rows_B = int(entry_rows_B.get())
            n_cols_B = int(entry_cols_B.get())
        except ValueError:
            messagebox.showerror("Lỗi", "Vui lòng nhập số hàng và cột hợp lệ cho ma trận B.")
            return

        tk.Label(frame_inputs, text="Ma trận B").grid(row=0, column=n_cols_A + 1, columnspan=n_cols_B)
        for i in range(n_rows_B):
            row_entries = []
            for j in range(n_cols_B):
                entry = tk.Entry(frame_inputs, width=7)
                entry.grid(row=i + 1, column=n_cols_A + 1 + j)
                row_entries.append(entry)
            entries_B.append(row_entries)
    elif num_matrices == 1 and combo_operation.get() == "Giải hệ phương trình":
        # Vector B
        tk.Label(frame_inputs, text="Vế phải B").grid(row=0, column=n_cols_A + 1)
        for i in range(n_rows_A):
            entry = tk.Entry(frame_inputs, width=7)
            entry.grid(row=i + 1, column=n_cols_A + 1)
            entries_B.append(entry)

# Xóa tất cả các ô nhập liệu
def clear_entries():
    for widget in frame_inputs.winfo_children():
        widget.destroy()

# Tạo cửa sổ giao diện chính
root = tk.Tk()
# root.minsize(height=300, width=300)
root.title("Máy tính ma trận")

# Chọn thao tác
label_operation = tk.Label(root, text="Chọn thao tác:")
label_operation.grid(row=0, column=0)
combo_operation = ttk.Combobox(root, values=["Cộng", "Trừ", "Nhân", "Chia", "Tìm ma trận nghịch đảo", "Tìm hạng ma trận", "Giải hệ phương trình"])
combo_operation.grid(row=0, column=1)
combo_operation.bind("<<ComboboxSelected>>", update_interface)

# Frame nhập số hàng và cột cho ma trận A
frame_size_A = tk.Frame(root)
label_rows_A = tk.Label(frame_size_A, text="Số hàng ma trận A:")
label_rows_A.grid(row=0, column=0)
entry_rows_A = tk.Entry(frame_size_A, width=5)
entry_rows_A.grid(row=0, column=1)
label_cols_A = tk.Label(frame_size_A, text="Số cột ma trận A:")
label_cols_A.grid(row=0, column=2)
entry_cols_A = tk.Entry(frame_size_A, width=5)
entry_cols_A.grid(row=0, column=3)
frame_size_A.grid(row=1, column=0, columnspan=4)

# Frame nhập số hàng và cột cho ma trận B
frame_size_B = tk.Frame(root)
label_rows_B = tk.Label(frame_size_B, text="Số hàng ma trận B:")
label_rows_B.grid(row=0, column=0)
entry_rows_B = tk.Entry(frame_size_B, width=5)
entry_rows_B.grid(row=0, column=1)
label_cols_B = tk.Label(frame_size_B, text="Số cột ma trận B:")
label_cols_B.grid(row=0, column=2)
entry_cols_B = tk.Entry(frame_size_B, width=5)
entry_cols_B.grid(row=0, column=3)
frame_size_B.grid(row=2, column=0, columnspan=4)

# Nút tạo ô nhập liệu
button_create = tk.Button(root, text="Tạo ô nhập liệu", command=lambda: create_matrix_inputs(2 if combo_operation.get() in ["Cộng", "Trừ", "Nhân", "Chia"] else 1))
button_create.grid(row=3, column=0, columnspan=4)

# Frame chứa các ô nhập liệu
frame_inputs = tk.Frame(root)
frame_inputs.grid(row=4, column=0, columnspan=4)

# Nút tính toán
button_solve = tk.Button(root, text="Tính toán", command=solve_matrix)
button_solve.grid(row=5, column=0, columnspan=2)

# Nhãn hiển thị kết quả
label_result = tk.Label(root, text="", justify="left")
label_result.grid(row=6, column=0, columnspan=2)

root.mainloop()
