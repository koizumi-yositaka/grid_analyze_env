import json
import copy

# def aaa(items,def_ary):

#     for item in items:
#         item_temp=item.copy()
#         if "options" in item_temp:
#             del item_temp["options"]
#             def_ary.append(item_temp)
#             aaa(item["options"],def_ary)
# with open("grid.json","r") as j:
#     data = json.load(j)
#     items=data["items"]
#     def_ary=[]
    
#     aaa(items,def_ary)
   
#     with open("griddefs/gridCollection/gridCollection.json","w") as j:
#         json.dump(def_ary,j,indent=4,ensure_ascii=False)

class DefCollect(object):
    def __init__(self):
        
        try:
            with open("griddefs/gridCollection/gridCollection.json","r",encoding="utf-8") as j:
                self.data = json.load(j) 
        except json.decoder.JSONDecodeError as e:
            print(e)

            self.intialyze_collection()
    def intialyze_collection(self):
        with open("grid.json","r",encoding="utf-8") as j:
            data = json.load(j)
            items=data["items"]
            def_ary=[]
            
            self.read_item(items,def_ary)
            self.data=def_ary

    def read_item(self,items,def_ary):
        for item in items:
            item_temp=item.copy()
            if "options" in item_temp:
                del item_temp["options"]
                def_ary.append(item_temp)
                self.read_item(item["options"],def_ary)         

    def collect_def_sample(self,item_dict):
        if "option_id" in item_dict:
            item_id=item_dict["option_id"]
        else:
            return
        item_values=item_dict["value"]
    
        for i,item in enumerate(self.data):
            if item_id==item["option_id"]:
                for item_value in item_values:
                    if isinstance(item_value,str):item_value=item_value.strip()
                    
                    if item_value == "":continue
                    if "valueSample" in item:
                        valSample=item["valueSample"]
                   
                        if item_value not in valSample:
                            item["valueSample"].append(item_value)
                    else:
                        item["valueSample"]=[item_value]
                #Commnet
                
                self.data[i]=item
               
    def __del__(self):
  
       #print(self.data)
        with open("griddefs/gridCollection/gridCollection.json","w",encoding="utf-8") as j:
            json.dump(self.data,j,indent=4,ensure_ascii=False)



#dc=DefCollect()
# item_dicts=[
#     {
#         "option_id":"1_1_8_1",

#         "value":["","ddd"]   
#     },
#     {
#         "option_id":"1_1_8_2",
#         "value":["","ddd"]   
#     }
# ]
# for item_dict in item_dicts:
#     dc.collect_def_sample(item_dict)
# del dc