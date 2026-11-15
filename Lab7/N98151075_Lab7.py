import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

# CSV 在程式上一層，處理結果放在程式同一個資料夾
folder = __file__.rsplit("/", 1)[0]
input_file = folder + "/Bank_Customer.csv"
output_file = folder + "/Bank_Customer_Preprocessed.csv"

data = np.loadtxt(
    input_file, skiprows=1, dtype=str, delimiter=","
)
print("Original data shape:", data.shape)

# customer_id 只是識別碼，churn 是預測答案，都不放進特徵
numeric_columns = [1, 4, 5, 6, 7, 8, 9, 10]
numeric_data = data[:, numeric_columns].astype(float)

# 確認資料沒有預期以外的類別
assert np.all(np.isin(data[:, 2], ["France", "Germany", "Spain"]))
assert np.all(np.isin(data[:, 3], ["Female", "Male"]))

# 性別轉成 0、1
gender = (data[:, 3] == "Male").astype(float)

# 國家沒有大小順序，所以拆成兩個欄位
# France 兩欄都是 0，Germany 是 1、0，Spain 是 0、1
germany = (data[:, 2] == "Germany").astype(float)
spain = (data[:, 2] == "Spain").astype(float)

X = np.column_stack((numeric_data, gender, germany, spain))
y = data[:, -1].astype(int)

# 八成訓練、兩成測試，讓兩組的流失比例接近
x_train, x_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y,
)

# 標準化參數只從訓練資料計算，測試資料沿用相同參數
scaler = StandardScaler()
x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

# 輸出時保留原本的列順序，最後一欄仍是未標準化的 churn
pre_data = np.column_stack((scaler.transform(X), y))
assert np.isfinite(pre_data).all()
assert set(np.unique(y)) == {0, 1}

header = (
    "credit_score,age,tenure,balance,products_number,"
    "credit_card,active_member,estimated_salary,"
    "gender_male,country_Germany,country_Spain,churn"
)

np.savetxt(
    output_file,
    pre_data,
    delimiter=",",
    header=header,
    comments="",
    fmt=["%.8f"] * X.shape[1] + ["%d"],
)

# 用訓練資料建立模型，再預測測試資料
clf = LogisticRegression(max_iter=1000, random_state=42)
clf.fit(x_train, y_train)
pred = clf.predict(x_test)

print("Removed feature: customer_id")
print("Gender: Female=0, Male=1")
print("Country: France=00, Germany=10, Spain=01")
print("Training X / y:", x_train.shape, y_train.shape)
print("Testing X / y:", x_test.shape, y_test.shape)
print("Preprocessed data shape:", pre_data.shape)
print("All values numeric and finite:", np.isfinite(pre_data).all())
print("Saved:", output_file)
print("Predictions (first 20):", pred[:20])
print("Actual labels (first 20):", y_test[:20])
print("Accuracy: {:.2f}%".format(accuracy_score(y_test, pred) * 100))