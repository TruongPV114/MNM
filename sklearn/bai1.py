import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import neighbors
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt

# Biến lưu trữ mô hình và thuật toán
model = None
selected_algorithm = None
y_test, y_predict = None, None  # Biến lưu trữ giá trị thật và dự đoán
mse_scores = {}
mae_scores = {}

# Tạo giao diện nhập liệu
root = tk.Tk()
root.title("Dự đoán Performance Index")

# Tạo nhãn và ô nhập liệu cho từng cột
labels = ["Hours Studied", "Previous Scores", "Extracurricular Activities", "Sleep Hours",
          "Sample Question Papers Practiced"]
entries = []

for i, label in enumerate(labels):
  tk.Label(root, text=label).grid(row=i, column=0)
  entry = tk.Entry(root)
  entry.grid(row=i, column=1)
  entries.append(entry)


# Hàm load dữ liệu từ file CSV và huấn luyện mô hình
def load_data():
  global model, selected_algorithm, y_test, y_predict, mse_scores, mae_scores
  try:
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
      df = pd.read_csv(file_path)

      # Train model using selected algorithm
      x = np.array(df.iloc[:, 0:5]).astype(np.float64)  # Các cột từ Hours Studied đến Sample Question Papers Practiced
      y = np.array(df.iloc[:, 5]).astype(np.float64)  # Cột Performance Index
      X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)

      # Khởi tạo mô hình dựa trên thuật toán đã chọn
      if selected_algorithm == "KNN":
        model = neighbors.KNeighborsRegressor(n_neighbors=3, p=2)
      elif selected_algorithm == "Linear Regression":
        model = LinearRegression()
      elif selected_algorithm == "Decision Tree":
        model = DecisionTreeRegressor()
      elif selected_algorithm == "Support Vector":
        model = SVR()

      model.fit(X_train, y_train)
      y_predict = model.predict(X_test)  # Dự đoán trên tập test

      mse = mean_squared_error(y_test, y_predict)
      mae = mean_absolute_error(y_test, y_predict)

      # Lưu trữ kết quả
      mse_scores[selected_algorithm] = mse
      mae_scores[selected_algorithm] = mae

      messagebox.showinfo("Thành công", f"Đã train mô hình với {selected_algorithm}!")
      plot_errors(y_test, y_predict)  # Vẽ biểu đồ sai số
      plot_metrics(mse, mae)  # Vẽ biểu đồ MSE, MAE
      plot_comparison()  # Vẽ biểu đồ so sánh các thuật toán
    else:
      messagebox.showerror("Lỗi", "Chưa chọn file!")
  except Exception as e:
    messagebox.showerror("Lỗi", f"Đã xảy ra lỗi khi tải dữ liệu: {e}")


# Hàm dự đoán kết quả
def predict_performance():
  global model
  if model is None:
    messagebox.showerror("Lỗi", "Vui lòng tải dữ liệu và chọn thuật toán trước khi dự đoán.")
    return
  try:
    # Lấy dữ liệu từ các ô nhập liệu
    input_data = np.array([float(entry.get()) for entry in entries]).reshape(1, -1)
    # Dự đoán Performance Index
    predicted_index = model.predict(input_data)[0]
    messagebox.showinfo("Kết quả", f"Performance Index dự đoán: {predicted_index:.2f}")
  except ValueError:
    messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ và chính xác các giá trị.")


# Hàm chọn thuật toán
def select_algorithm():
  global selected_algorithm
  selected_algorithm = algorithm_var.get()


# Hàm vẽ biểu đồ sai số
def plot_errors(y_test, y_predict):
  errors = y_test - y_predict
  error_counts = [np.sum(errors > 2), np.sum((errors <= 2) & (errors > 1)), np.sum(errors < 1)]

  plt.figure(figsize=(8, 5))
  plt.bar(['Sai số > 2', 'Sai số từ 1 đến 2', 'Sai số < 1'], error_counts, color=['red', 'orange', 'green'])
  plt.title('Biểu đồ sai số dự đoán')
  plt.ylabel('Số lượng')
  plt.show()


# Hàm vẽ biểu đồ cho MSE, MAE
def plot_metrics(mse, mae):
  metrics = [mse, mae]
  metric_names = ['MSE', 'MAE']

  plt.figure(figsize=(8, 5))
  plt.bar(metric_names, metrics, color=['blue', 'purple'])
  plt.title('Biểu đồ các chỉ số MSE và MAE')
  plt.ylabel('Giá trị')
  plt.show()


# Hàm so sánh các thuật toán dựa trên MSE và MAE
def plot_comparison():
  if len(mse_scores) > 1:
    algorithms = list(mse_scores.keys())
    mse_values = list(mse_scores.values())
    mae_values = list(mae_scores.values())

    plt.figure(figsize=(10, 6))

    # Biểu đồ so sánh MSE
    plt.subplot(1, 2, 1)
    plt.bar(algorithms, mse_values, color='blue')
    plt.title('So sánh MSE giữa các thuật toán')
    plt.ylabel('MSE')

    # Biểu đồ so sánh MAE
    plt.subplot(1, 2, 2)
    plt.bar(algorithms, mae_values, color='purple')
    plt.title('So sánh MAE giữa các thuật toán')
    plt.ylabel('MAE')

    plt.tight_layout()
    plt.show()


# Tạo nút Load Data
load_button = tk.Button(root, text="Load Data", command=load_data)
load_button.grid(row=len(labels), column=0)

# Tạo radio buttons để chọn thuật toán
algorithm_var = tk.StringVar(value="KNN")  # Mặc định là KNN
tk.Label(root, text="Chọn Thuật Toán:").grid(row=len(labels) + 1, column=0, columnspan=2)

algorithms = ["KNN", "Linear Regression", "Decision Tree", "Support Vector"]
for algorithm in algorithms:
  tk.Radiobutton(root, text=algorithm, variable=algorithm_var, value=algorithm, command=select_algorithm).grid(
    row=len(labels) + 2, column=algorithms.index(algorithm))

# Tạo nút dự đoán
predict_button = tk.Button(root, text="Dự đoán", command=predict_performance)
predict_button.grid(row=len(labels) + 3, column=0, columnspan=2)

# Khởi chạy giao diện
root.mainloop()
