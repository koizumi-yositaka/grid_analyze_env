import csv
test_expectations_csv_file_name="test/data/testExpectationsCsv/test1_exp.csv"
with open(test_expectations_csv_file_name,"r",encoding="utf-8") as tec:

    
    reader=csv.DictReader(tec,skipinitialspace=True)
    test_expectations=[]
    print(sum(1 for row in reader))
    for row in reader:
        # Noneのキーを削除する
        
        row = {k: v for k, v in row.items() if k is not None}
        # rowは辞書で各列の値を含む（Noneのキーは削除されている）
        test_expectations.append(row)
