import sys
import os
import json
import csv

sys.path.append(os.path.join(os.getcwd(),"src"))

from module import build_grid_def
import pytest

@pytest.fixture
def init():
    bg=build_grid_def.BuildGridDef()
    return bg


test_get_value_from_inputdata_by_id_params=[
    ("1",["value1"]),
    ("2",["False"]),
    ("3",["1234"]),
    ("4",[""])
]
@pytest.mark.parametrize("id,expectations",test_get_value_from_inputdata_by_id_params)
def test_get_value_from_inputdata_by_id(init,id,expectations):
    sample_str_json='[{"grid_id":"grid_1","value":["value1"]},{"grid_id":"grid_2","value":["False"]},{"grid_id":"grid_3","value":["1234"]}]'
    init.load_grid_items(sample_str_json)
    assert (init.get_value_from_inputdata_by_id(id))==expectations
    
test_build_options_params=[
    ("test/data/testGridItemsJson/test01.json",",","test/data/testExpectationsTxt/test01.txt"),#通常の結合
    ("test/data/testGridItemsJson/test02.json",",","test/data/testExpectationsTxt/test02.txt"),#デフォルト値と入力値が同じ場合は省略
    ("test/data/testGridItemsJson/test03.json",",","test/data/testExpectationsTxt/test03.txt"),#全てのオプションが空文字の場合は空文字を返す
    ("test/data/testGridItemsJson/test04.json","#@$@=","test/data/testExpectationsTxt/test04.txt"),#区切り文字が@を含む
    ("test/data/testGridItemsJson/test05.json","=","test/data/testExpectationsTxt/test05.txt"),#区切り文字が重複
    ("test/data/testGridItemsJson/test06.json","#@$@=","test/data/testExpectationsTxt/test06.txt"),#区切り文字が@を含むかつ区切り文字が重複
    ("test/data/testGridItemsJson/test07.json",",","test/data/testExpectationsTxt/test07.txt"),#2層の場合の通常結合
    ("test/data/testGridItemsJson/test08.json","#","test/data/testExpectationsTxt/test08.txt"),#2層の場合かつ区切り文字重複
    ("test/data/testGridItemsJson/test09.json",",","test/data/testExpectationsTxt/test09.txt"),#2層の場合かつ全てのオプションが空文字
    ("test/data/testGridItemsJson/test10.json","#@$@=","test/data/testExpectationsTxt/test10.txt"),#2層の場合かつ@を含む
    ("test/data/testGridItemsJson/test11.json","#@$@=","test/data/testExpectationsTxt/test11.txt"),#2層の場合かつ@を含む
]
@pytest.mark.parametrize("test_grid_json_file,delimiter,test_expectations_text_file",test_build_options_params)
def test_build_options(init,test_grid_json_file,delimiter,test_expectations_text_file):
    with open(test_grid_json_file,"r",encoding="utf-8") as tgj,open(test_expectations_text_file,"r",encoding="utf-8") as tet:
        test_grid_json=json.load(tgj)
        test_expectations_text=tet.read()
        assert (init.build_options(test_grid_json,delimiter))==test_expectations_text
        
        
def test_set_value_to_grid_item(init):
    test_grid_json_file="test/data/testBuildGridJson/test01.json"
    test_expectations_csv_file="test/data/testBuildExpectationsCsv/test01.csv"
    with open(test_grid_json_file,"r",encoding="utf-8") as tgj,open("src/data/grid.json","r",encoding="utf-8") as gj,open(test_expectations_csv_file,"r",encoding="utf-8") as tec:
        test_grid_json=json.load(tgj)
        grid_data_json=json.load(gj)
        reader=csv.DictReader(tec,skipinitialspace=True)
        init.input_json_data=test_grid_json
        #第一回層でしか値の設定がされていない
        result_value_dict_ary=init.set_value_to_grid_item(grid_data_json["items"])
        
        for row in reader:
            grid_id=row["grid_id"]
            grid_value=row["value"]
            

            for result_value_obj in result_value_dict_ary:
                
                if grid_id==result_value_obj["option_id"]:
                    assert result_value_obj["value"]==grid_value,f"{row['grid_id']}"

                    break
            assert False,f"idが一致するものがありません。id:{row['grid_id']},期待値:{result_value_obj['option_id']}"


def get_option_value_ary(options,result_ary):
    result_ary=[]
    result_dict={"grid_id":"","value":""}
    for option in options:
        if option["options"]!="":
            get_option_value_ary(option["options"],result_ary)
            
        else:
            result_dict["grid_id"]=option["option_id"]
            result_dict["value"]=option["option_id"]
            result_ary.append(result_dict)
    
    return result_ary
