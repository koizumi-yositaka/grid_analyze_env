import json
import csv
def get_options(grid_options,display_id_ary):
    for option in grid_options:
        if "options" in option:
            if option["options"]!="":
                get_options(option["options"],display_id_ary)
            else:
                result_obj={}
                result_obj["option_id"]=option["option_id"]
                result_obj["name"]=option["name"]
                result_obj["delimiter"]=option["delimiter"]
                # result_obj["description"]=option["description"]
                # result_obj["signature"]=option["signature"]
                # result_obj["isNeed"]=option["isNeed"] if "isNeed" in option else "false"
                # result_obj["defalutVal"]=option["defaultVal"] if "defaultVal" in option else ""
                             
                display_id_ary.append(result_obj)
    return display_id_ary
json_file="data/grid.json"
csv_file="management/grid.csv"
with open(json_file,"r",encoding="utf-8") as f,open(csv_file,"w",encoding="utf-8") as c:
    data=json.load(f)
    display_id_ary=[]
    result=get_options(data["items"],display_id_ary)
    writer=csv.writer(c)
    writer.writerow(result[0].keys())
    for row in result:
        writer.writerow(row.values())