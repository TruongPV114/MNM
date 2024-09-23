import numpy as np
import tkinter as tk
from tkinter import messagebox, simpledialog

# Function to load data from CSV file
def load_data(file_path):
    """Load data from a CSV file into a numpy array."""
    try:
        data = np.genfromtxt(file_path, delimiter=',', dtype=str, encoding='utf-8', skip_header=1)
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        return np.array([])

# Function to save data back to CSV
def save_data(file_path, data):
    """Save the updated data back to CSV."""
    header = "ID,Tên,Môn học,Điểm"
    np.savetxt(file_path, data, delimiter=',', fmt='%s', header=header, comments='', encoding='utf-8')

# Search student information by ID
def search_student(data, student_id):
    """Search for a student's information by ID."""
    if data.size == 0:
        return "Dữ liệu không được tải."

    student_data = data[data[:, 0] == student_id]
    if student_data.size == 0:
        return f"Không tìm thấy thông tin cho sinh viên có ID {student_id}."
    else:
        return "\n".join([", ".join(row) for row in student_data])

# Search grades of a specific subject
def search_subject(data, subject_name):
    """Search for grades of a specific subject."""
    if data.size == 0:
        return "Dữ liệu không được tải."

    subject_data = data[data[:, 2] == subject_name]
    if subject_data.size == 0:
        return f"Không tìm thấy điểm cho môn học {subject_name}."
    else:
        return "\n".join([f"ID: {row[0]}, Tên: {row[1]}, Điểm: {row[3]}" for row in subject_data])

# Calculate average grade of a student
def calculate_average(data, student_id):
    """Calculate the average grade for a specific student using numpy."""
    if data.size == 0:
        return "Dữ liệu không được tải."

    student_data = data[data[:, 0] == student_id]
    if student_data.size == 0:
        return f"Không tìm thấy thông tin cho sinh viên có ID {student_id}."
    else:
        try:
            grades = student_data[:, 3].astype(float)  # Convert grades to float
            average_grade = np.mean(grades)
            return f"Trung bình cộng điểm của sinh viên có ID {student_id} là {average_grade:.2f}."
        except ValueError:
            return "Có lỗi khi chuyển đổi điểm sang số thực. Vui lòng kiểm tra dữ liệu."

# Add a new student
def add_student(data, new_student):
    """Thêm một sinh viên mới vào data."""
    # Chỉ thêm sinh viên mới mà không cần kiểm tra ID trùng lặp
    return np.vstack([data, new_student])


# Edit a student's information
def edit_student(data, student_id, new_student_info):
    """Chỉnh sửa thông tin sinh viên theo ID và tên môn học."""
    subject_name = new_student_info[2]  # Lấy tên môn học từ thông tin mới

    # Tìm các dòng khớp với ID sinh viên và tên môn học
    for i in range(data.shape[0]):
        if data[i, 0] == student_id and data[i, 2] == subject_name:
            # Nếu tìm thấy, cập nhật thông tin
            data[i] = new_student_info
            return True  # Cập nhật thành công
    return False  # Không tìm thấy sinh viên hoặc môn học khớp


# Delete a student by ID
def delete_student(data, student_id):
    """Delete a student by ID."""
    return data[data[:, 0] != student_id]

# Generate statistics about students
def statistics(data):
    """Thống kê thông tin về sinh viên và điểm trung bình của từng môn học."""
    if data.size == 0:
        return "Dữ liệu không có sẵn."

    # Đếm số lượng sinh viên duy nhất (ID không trùng lặp)
    unique_students = np.unique(data[:, 0])  # Cột 0 là ID sinh viên
    num_students = len(unique_students)

    # Tính điểm trung bình của từng môn học
    subjects = np.unique(data[:, 2])  # Cột 2 là tên môn học
    subject_averages = {}

    for subject in subjects:
        # Lấy tất cả các dòng có môn học khớp
        subject_data = data[data[:, 2] == subject]
        try:
            # Lấy cột điểm (cột 3), chuyển đổi sang float và tính trung bình
            grades = subject_data[:, 3].astype(float)
            subject_averages[subject] = np.mean(grades)
        except ValueError:
            subject_averages[subject] = "Dữ liệu không hợp lệ"

    # Xây dựng kết quả thống kê
    result = f"Số lượng sinh viên: {num_students}\n"
    result += "Điểm trung bình của từng môn học:\n"
    for subject, average in subject_averages.items():
        result += f"- {subject}: {average:.2f}\n"

    return result


# Handling user actions
def search_action():
    global data  # Declare global to ensure data is used as a global variable
    choice = choice_var.get()
    student_id = id_entry.get()
    subject_name = subject_entry.get()

    if choice == '1':  # Search student info
        result = search_student(data, student_id)
    elif choice == '2':  # Search subject grades
        result = search_subject(data, subject_name)
    elif choice == '3':  # Calculate average grades
        result = calculate_average(data, student_id)
    elif choice == '4':  # Add new student or append grades for existing student
        new_name = name_entry.get()
        new_subject = subject_entry.get()
        new_grade = grade_entry.get()

        new_student_data = [student_id, new_name, new_subject, new_grade]
        data = add_student(data, new_student_data)
        save_data('data.csv', data)
        result = f"Đã thêm dữ liệu cho sinh viên có ID {student_id}."
    elif choice == '5':  # Edit student
        new_name = name_entry.get()
        new_subject = subject_entry.get()
        new_grade = grade_entry.get()

        new_student_info = [student_id, new_name, new_subject, new_grade]

        if edit_student(data, student_id, new_student_info):
            save_data('data.csv', data)
            result = f"Đã chỉnh sửa thông tin môn {new_subject} của sinh viên có ID {student_id}."
        else:
            result = f"Không tìm thấy sinh viên có ID {student_id} và môn {new_subject}."
    elif choice == '6':  # Delete student
        if any(data[:, 0] == student_id):
            data = delete_student(data, student_id)
            save_data('data.csv', data)
            result = f"Đã xóa sinh viên có ID {student_id}."
        else:
            result = f"Không tìm thấy sinh viên có ID {student_id}."
    elif choice == '7':  # View statistics
        result = statistics(data)
    else:
        result = "Lựa chọn không hợp lệ."

    messagebox.showinfo("Kết quả", result)





# Main function to create the GUI
def main():
    global data  # Declare global here to ensure it's global throughout the program
    file_path = 'data.csv'  # Đặt đường dẫn đến file dữ liệu của bạn
    data = load_data(file_path)

    # Create main window
    root = tk.Tk()
    root.title("Quản lý thông tin sinh viên")

    # Add widgets
    tk.Label(root, text="Chọn hành động:").pack(pady=5)

    global choice_var
    choice_var = tk.StringVar(value='1')

    tk.Radiobutton(root, text="Tìm kiếm thông tin sinh viên", variable=choice_var, value='1').pack(anchor='w')
    tk.Radiobutton(root, text="Tìm kiếm điểm môn học", variable=choice_var, value='2').pack(anchor='w')
    tk.Radiobutton(root, text="Tính TBC điểm của sinh viên", variable=choice_var, value='3').pack(anchor='w')
    tk.Radiobutton(root, text="Thêm sinh viên mới", variable=choice_var, value='4').pack(anchor='w')
    tk.Radiobutton(root, text="Chỉnh sửa thông tin sinh viên", variable=choice_var, value='5').pack(anchor='w')
    tk.Radiobutton(root, text="Xóa sinh viên", variable=choice_var, value='6').pack(anchor='w')
    tk.Radiobutton(root, text="Xem thống kê", variable=choice_var, value='7').pack(anchor='w')

    tk.Label(root, text="ID sinh viên:").pack(pady=5)
    global id_entry
    id_entry = tk.Entry(root)
    id_entry.pack(pady=5)

    tk.Label(root, text="Tên sinh viên (nếu có):").pack(pady=5)
    global name_entry
    name_entry = tk.Entry(root)
    name_entry.pack(pady=5)

    tk.Label(root, text="Tên môn học (nếu có):").pack(pady=5)
    global subject_entry
    subject_entry = tk.Entry(root)
    subject_entry.pack(pady=5)

    tk.Label(root, text="Điểm số (nếu có):").pack(pady=5)
    global grade_entry
    grade_entry = tk.Entry(root)
    grade_entry.pack(pady=5)

    tk.Button(root, text="Thực hiện", command=search_action).pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
