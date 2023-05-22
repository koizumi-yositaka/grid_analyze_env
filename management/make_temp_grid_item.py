import json
id_ary=["grid_1_1_1","grid_1_1_2","grid_1_1_3","grid_1_1_4","grid_1_1_5_1","grid_1_1_5_2","grid_1_1_5_3","grid_1_1_6","grid_1_1_7_1","grid_1_1_7_2","grid_1_1_7_3","grid_1_1_7_4_1","grid_1_1_7_4_2","grid_1_1_7_4_3_1","grid_1_1_7_4_3_2","grid_1_1_7_4_3_3","grid_1_1_7_4_4","grid_1_1_7_4_5","grid_1_1_7_5_1","grid_1_1_7_5_2","grid_1_1_8_1","grid_1_1_8_2","grid_1_1_8_3","grid_1_1_8_4","grid_1_1_9","grid_1_1_10","grid_1_1_11","grid_1_1_12","grid_1_1_13","grid_1_1_14","grid_1_1_15_1","grid_1_1_15_2_1","grid_1_1_15_2_2","grid_1_1_15_3","grid_1_1_16_1_1","grid_1_1_16_1_2","grid_1_1_16_2_1","grid_1_1_16_2_2","grid_1_1_16_3","grid_1_1_16_4","grid_1_2_1_1","grid_1_2_1_2","grid_1_2_2_1","grid_1_2_2_2","grid_1_2_2_3","grid_1_2_2_4","grid_1_2_2_5","grid_1_3","grid_1_4","grid_1_5","grid_1_6_1_1","grid_1_6_1_2_1","grid_1_6_1_2_2","grid_1_6_1_3","grid_1_6_2","grid_1_6_3_1","grid_1_6_3_2_1","grid_1_6_3_2_2","grid_1_6_4","grid_1_6_5","grid_1_6_6","grid_1_7","grid_1_8","grid_1_9","grid_1_10","grid_1_11_1","grid_1_11_2","grid_1_12","grid_1_13","grid_1_14","grid_1_15","grid_1_16","grid_1_17","grid_1_18","grid_1_19","grid_1_20","grid_1_21_1_1","grid_1_21_1_2","grid_1_21_2","grid_1_21_3","grid_1_21_4","grid_1_21_5","grid_1_21_6_1","grid_1_21_6_2","grid_1_21_6_3","grid_1_21_7","grid_1_21_8","grid_1_21_9","grid_1_21_10","grid_1_21_11","grid_1_21_12","grid_1_21_13","grid_1_21_14","grid_1_22","grid_1_23","grid_1_24","grid_1_25"]


# for j_item in j_data:
    
#     for data_item in data:
#         if "grid_"+data_item["option_id"]==j_item["grid_id"]:
#             print(data_item["option_id"])
#             j_item["description"]=data_item["description"]
#             print(result_ary)
#             result_ary.append(j_item)
#             break
# print(result_ary)
def get_options(options,result_ary):
    
    for option in options:
        if "options" in option and option["options"]!="":
            get_options(option["options"],result_ary)
        else:
            
            result_obj={}
            result_obj["grid_id"]="grid_"+option["option_id"]
            
            result_obj["name"]=option["name"]
            result_obj["description"]=option["description"]
            result_obj["value"]=[""]
            result_obj["defaultVal"]=""
            if "defaultVal" in option:result_obj["defaultVal"]=str(option["defaultVal"])
            
            
            result_ary.append(result_obj)
            #result_ary.append(result_obj)
    return result_ary
result_ary=[]
with open("data/grid.json","r",encoding="utf-8") as f:
    grid_json_ary=json.load(f)
    print("sum")
    #print(len(get_options(grid_json_ary["items"],result_ary)) == len(id_ary))
    result_ary=[]
    #print(len(get_options(grid_json_ary["items"],result_ary)))
    # for res in result_ary:
    #     if res["grid_id"] not in id_ary:print(res["grid_id"])
    #print(len(id_ary))
    get_options(grid_json_ary["items"],result_ary)
    with open("data/gridItem.json","w",encoding="utf-8") as f:
        json.dump(result_ary,f,indent=4,ensure_ascii=False)  
'''
with open("griddefs/gridCollection/gridCollection.json","r",encoding="utf-8") as f:
    grid_json_ary=json.load(f)
for grid_json_items in grid_json_ary:
    if "grid_"+grid_json_items["option_id"] in id_ary:
        #print(grid_json_items["option_id"])
        append_obj={}
        append_obj["grid_id"]="grid_"+grid_json_items["option_id"]
        append_obj["name"]=grid_json_items["name"]
        append_obj["description"]=grid_json_items["description"]
        append_obj["value"]=[""]
        if "defaultVal" in grid_json_items:append_obj["defaultVal"]=str(grid_json_items["defaultVal"])
        result_ary.append(append_obj)
        
        
        
 
with open("gridItem.json","w",encoding="utf-8") as f:
    json.dump(result_ary,f,indent=4,ensure_ascii=False)  
    
'''