import csv

# CSVファイルを読み込む
filename = "nuturition_quiz.csv"  # 同じディレクトリにあるファイル
row_index = 2  # 取得したい行（0-based index）
column_index = 2  # 取得したい列（0-based index）

with open(filename, mode="r", encoding="utf-8") as file:
    reader = csv.reader(file)
    rows = list(reader)  # CSVをリスト化

# 特定の行と列のデータを取得
if row_index < len(rows) and column_index < len(rows[row_index]):
    data = rows[row_index][column_index]
    print(f"取得したデータ: {data}")
    print(rows)
else:
    print("指定した行または列が存在しません。")
