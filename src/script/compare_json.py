import build_grid_def 
import os
import json
import grid_def
import shutil

'''
テスト用のファイル
テスト方法
1、gridJsonSamples(グリッドのJSONファイル、サンプル)→
2、gridItemResult(画面入力項目を表現したJSONファイル(Itemファイル))→
3、gridDefsMadeByBuilder(Itemファイルを定義文に変換する)→
4、testResult(gridDefsMadeByBuilderの定義文をグリッドのJSONファイルに比較する)
5、gridJsonSamplesとtestResultの内容が同じかを判別する。
'''
def make_sure_same_data(before_data,after_data):
    is_success=True
    for before_data_item in before_data:
        for after_data_item in after_data:
            if before_data_item["grid_id"]=="grid_"+after_data_item["option_id"]:
            
                for before_data_item_val,after_data_item_val in zip(before_data_item["value"],after_data_item["value"]):
                    if str(before_data_item_val).lower()!=str(after_data_item_val).lower():
                        print(f'id:{before_data_item["grid_id"]}が異なります')
                        print(f'変換前は{before_data_item_val}')
                        print(f'変換後は{after_data_item_val}')
                        is_success=False
                        break
                        
                
       
    return is_success        
    #print(f'id:{before_data_item["grid_id"]}が一致するものがないです')    
        
           
for f in os.listdir("griddefs"):
    if f.endswith(".json"):shutil.copy2(os.path.join("griddefs",f),os.path.join("test/gridJsonSamples",f))
print("json化された定義データファイルの移動完了")
COUNT=2
C_COUNT=0
for grid_sample in os.listdir("test/gridItemResult"):
    with open(os.path.join("test/gridItemResult",grid_sample),"r",encoding="utf-8") as f:
        data=json.load(f)
        bg=build_grid_def.BuildGridDef(data)
        result_grid_def=bg.build_grid_def()
        txt_file_name=grid_sample.split(".")[0]
        with open(os.path.join("test/gridDefsMadeByBuilder",txt_file_name+".txt"),"w+",encoding="utf-8" )as built_file:
            #print(txt_file_name)
            built_file.write(result_grid_def)
        gd=grid_def.AnalyzeGrid(os.path.join("test/gridDefsMadeByBuilder",txt_file_name+".txt"))
        def_dict_ary=gd.analyze()
        gd.write(dirname="test/testResult")
print("構築完了")     
for file_name in os.listdir("test/gridItemResult"):
    before_data_file_path=os.path.join("test/gridItemResult",file_name)
    after_data_file_path=os.path.join("test/testResult",file_name)
    with open(before_data_file_path,"r",encoding="utf-8") as b_f:
        before_data=json.load(b_f)
        with open(after_data_file_path,"r",encoding="utf-8") as a_f:
            after_data=json.load(a_f)
            print(f'####{file_name}####')
            if make_sure_same_data(before_data,after_data):print(f'SUCCESS')
            C_COUNT+=1
            #if C_COUNT==COUNT:break
            #break
            
            

#bg=build_grid_def.BuildGridDef()