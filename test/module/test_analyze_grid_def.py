import sys
import os

sys.path.append(os.path.join(os.getcwd(),"src"))


'''
test時はanalyze_grid_def.pyのfromにsrc.を追加する
'''
from module import analyze_grid_def
import pytest
import csv

@pytest.fixture
def init():
    ag=analyze_grid_def.AnalyzeGrid()
    return ag
    

def test_delete_comment(init):
    assert (init.delete_comment("def1/**comment**/def2"))=="def1def2"
    assert (init.delete_comment("def1/*comment*/def2"))=="def1/*comment*/def2"
    assert (init.delete_comment("def1def2"))=="def1def2"
    
test_omit_del_pos_params=[
    ("{","}","aa,a{a,a}a",[2,6],[2,-1]),
    ("{","}","aa{a,a{a,a}a,a}aa",[4,8,12],[-1,-1,-1]),
    
]
@pytest.mark.parametrize("start_chara,end_chara,defs,del_pos_ary,expectations",test_omit_del_pos_params)

def test_omit_del_pos(init,start_chara,end_chara,defs,del_pos_ary,expectations):
    assert (init.omit_del_pos(start_chara,end_chara,defs,del_pos_ary))==expectations
   
test_get_def_ary_params=[
    ("a{a,a}a,a(,)a",",",[{"s":"{","e":"}"},{"s":"(","e":")"}],["a{a,a}a","a(,)a"]),
    ("ab#(c#d)e($f)$g","#@$",[{"s":"{","e":"}"},{"s":"(","e":")"}],["ab","(c#d)e($f)","g"])
] 
@pytest.mark.parametrize("defs,delimiter,protect_pattern_ary,expectations",test_get_def_ary_params)
def test_get_def_ary(init,defs,delimiter,protect_pattern_ary,expectations):
    assert (init.get_def_ary(defs,delimiter,protect_pattern_ary))==expectations
test_analyze_params=[
    ("test/data/testGridText/test1.txt","test/data/testExpectationsCsv/test1_exp.csv"),
    ("test/data/testGridText/test2.txt","test/data/testExpectationsCsv/test2_exp.csv")
]
@pytest.mark.parametrize("test_grid_text_file_name,test_expectations_csv_file_name",test_analyze_params)
def test_analyze(init,test_grid_text_file_name,test_expectations_csv_file_name):
    
    with open(test_grid_text_file_name,"r",encoding="utf-8") as tgt,open(test_expectations_csv_file_name,"r",encoding="utf-8") as tec:
        test_grid_text=tgt.read()
        init.analyze(test_grid_text)
        
        reader=csv.DictReader(tec,skipinitialspace=True)
        #assert (sum(1 for row in reader))==(len(init.def_dict_ary))
        test_expectations=[]
        for row in reader:
        # Noneのキーを削除する
        
            row = {k: v for k, v in row.items() if k is not None}
        # rowは辞書で各列の値を含む（Noneのキーは削除されている）
            test_expectations.append(row)

        for row in test_expectations:
            flg_match=False
            for def_dict in init.def_dict_ary:
                if row["id"]==def_dict["option_id"]:
                    flg_match=True
                    if [str(result_test).lower() for result_test in row["value"].split(",")]== [str(result_exp).lower() for result_exp in def_dict["value"]]:
                        break
                    else:
                        assert False,f"結果が期待値と異なります。id:{row['id']} 実際の値:{row['value'].split(',')} 期待値:{def_dict['value']}"
                else:
                    continue
        assert flg_match ,f"idが一致するものがありません。id:{row['id']}"