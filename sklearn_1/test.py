import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.metrics import mean_squared_error, mean_absolute_error
import matplotlib.pyplot as plt
import numpy as np
from sklearn.impute import SimpleImputer

# Initialize GUI window
root = tk.Tk()
root.title("Water Potability Prediction")

df = None
model = None  # Biến toàn cục cho mô hình đã huấn luyện
X_train, y_train = None, None  # Biến toàn cục cho dữ liệu huấn luyện


# Load CSV Data function
def load_data():
  global df
  file_path = filedialog.askopenfilename()
  if file_path:
    try:
      # Load file CSV với mã hóa phù hợp
      df = pd.read_csv(file_path, encoding='ISO-8859-1')

      # Chỉ giữ lại các cột có dữ liệu số
      df_numeric = df.select_dtypes(include=[float, int])

      # Thực hiện imputation (xử lý missing values)
      imputer = SimpleImputer(strategy='mean')
      df_imputed = pd.DataFrame(imputer.fit_transform(df_numeric), columns=df_numeric.columns)

      messagebox.showinfo("Success", "Data loaded and processed successfully!")
    except Exception as e:
      messagebox.showerror("Error", f"Failed to load data: {e}")


# Function to train model and predict
def train_model():
  global df, model, X_train, y_train
  if df is None:
    messagebox.showerror("Error", "Please load a dataset first.")
    return

  # Handle missing values
  imputer = SimpleImputer(strategy='mean')
  df_imputed = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)

  # Split dataset into features and labels
  X = df_imputed.iloc[:, :-1]
  y = df_imputed.iloc[:, -1]

  # Train/test split
  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

  # Lưu kết quả sai số cho các thuật toán
  algorithms = {"KNN": KNeighborsClassifier(n_neighbors=3), "LR": LogisticRegression(max_iter=1000),
    "DTR": DecisionTreeClassifier(), "SV": SVC(kernel='linear')}

  errors = {}

  for name, algorithm in algorithms.items():
    algorithm.fit(X_train, y_train)
    y_pred = algorithm.predict(X_test)

    # Tính toán sai số
    mse = mean_squared_error(y_test, y_pred)
    errors[name] = mse

  # Hiển thị đồ thị so sánh sai số
  display_error_comparison(errors)


# Function to display error comparison
def display_error_comparison(errors):
  plt.figure(figsize=(10, 5))
  plt.bar(errors.keys(), errors.values(), color=['blue', 'orange', 'green', 'red'])
  plt.title('Comparison of Error Metrics by Algorithm')
  plt.xlabel('Algorithm')
  plt.ylabel('Mean Squared Error (MSE)')
  plt.show()


# Create input labels and entry fields
tk.Button(root, text="Load CSV Data", command=load_data).grid(row=0, column=0, columnspan=2, pady=10)

# Algorithm selection
algo_var = tk.StringVar(value="KNN")
tk.Label(root, text="Choose Algorithm:").grid(row=1, column=0, pady=10)
tk.OptionMenu(root, algo_var, "KNN", "LR", "DTR", "SV").grid(row=1, column=1)

# Section to input new data
tk.Label(root, text="ph").grid(row=2, column=0)
entry_ph = tk.Entry(root)
entry_ph.grid(row=2, column=1)

tk.Label(root, text="Hardness").grid(row=3, column=0)
entry_hardness = tk.Entry(root)
entry_hardness.grid(row=3, column=1)

tk.Label(root, text="Solids").grid(row=4, column=0)
entry_solids = tk.Entry(root)
entry_solids.grid(row=4, column=1)

tk.Label(root, text="Chloramines").grid(row=5, column=0)
entry_chloramines = tk.Entry(root)
entry_chloramines.grid(row=5, column=1)

tk.Label(root, text="Sulfate").grid(row=6, column=0)
entry_sulfate = tk.Entry(root)
entry_sulfate.grid(row=6, column=1)

tk.Label(root, text="Conductivity").grid(row=7, column=0)
entry_conductivity = tk.Entry(root)
entry_conductivity.grid(row=7, column=1)

tk.Label(root, text="Organic Carbon").grid(row=8, column=0)
entry_organic_carbon = tk.Entry(root)
entry_organic_carbon.grid(row=8, column=1)

tk.Label(root, text="Trihalomethanes").grid(row=9, column=0)
entry_trihalomethanes = tk.Entry(root)
entry_trihalomethanes.grid(row=9, column=1)

tk.Label(root, text="Turbidity").grid(row=10, column=0)
entry_turbidity = tk.Entry(root)
entry_turbidity.grid(row=10, column=1)


# Function to predict water potability based on new input data
def predict_potability():
  try:
    ph = float(entry_ph.get())
    hardness = float(entry_hardness.get())
    solids = float(entry_solids.get())
    chloramines = float(entry_chloramines.get())
    sulfate = float(entry_sulfate.get())
    conductivity = float(entry_conductivity.get())
    organic_carbon = float(entry_organic_carbon.get())
    trihalomethanes = float(entry_trihalomethanes.get())
    turbidity = float(entry_turbidity.get())

    # Input array for prediction
    new_data = np.array(
      [[ph, hardness, solids, chloramines, sulfate, conductivity, organic_carbon, trihalomethanes, turbidity]])

    # Sử dụng mô hình đã huấn luyện để dự đoán
    if model is not None:
      prediction = model.predict(new_data)[0]

      # Display prediction
      if prediction == 1:
        result = "Nước uống được"
      else:
        result = "Nước không uống được"

      messagebox.showinfo("Kết quả", result)
    else:
      messagebox.showerror("Error", "Mô hình chưa được huấn luyện.")

  except ValueError:
    messagebox.showerror("Lỗi", "Vui lòng nhập đầy đủ và đúng định dạng số liệu!")


# Button to predict potability
tk.Button(root, text="Predict Water Potability", command=predict_potability).grid(row=11, column=0, columnspan=2,
                                                                                  pady=10)

# Button to train model
tk.Button(root, text="Train Model", command=train_model).grid(row=12, column=0, columnspan=2, pady=10)

root.mainloop()
