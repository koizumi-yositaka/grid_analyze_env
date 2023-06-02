import json
import os
import sys

sys.path.append(os.getcwd())
from module import tool

class BuildGridDef(object):
    def __init__(self):
        self.STR_TILDE="~"
        
    def load_grid_items(self,str_input_json_data):
        self.input_json_data = json.loads(str_input_json_data) 
            
    def get_options(self,option_ary):
        """
        optionsバリューが空文字でない場合にはこの項目がオプションを持っているとして再起的にこの関数を呼ぶ。
        optionsバリューが空文字の時は、値の設定されるはずの画面上の項目(最深の項目)だと判別し、get_value_from_inputdata_by_id関数を用いて値を取得する
        
        取得した入力データを区切り文字で接続して文字列にし、その項目のvalueキーに対応するバリューに設定する
        この時、区切り文字は接続する全ての定義文と重複しない数の「~」を付与したものとする。複数個の区切り文字が存在する(@で接続されている場合)も全ての場合で考慮する
        
        Args:
            option_ary (list): _description_

        Returns:
            list:option_aryにvalueというその階層の定義文を設定したもの 
        """
        for option in option_ary:
            if "options" in option:
                if option["options"]!="":
                    self.get_options(option["options"])
                else:
                    input_value=self.get_value_from_inputdata_by_id(option["option_id"])
                    delimiter="," if option["delimiter"]=="" else option["delimiter"]

                    if input_value is not None:
                        max_count=0
                        for v in input_value:
                          for d in delimiter.split("@"):
                            count=tool.get_delimiter(v,d).count(self.STR_TILDE)
                            if count>max_count:max_count=count 
                        delimiter=self.STR_TILDE*(max_count+1)+delimiter 
                        
                        
                        #if input_value!="": print(str(option["value"]))
                        option["value"]=delimiter.join(input_value)
            else:
                #TODO    
                print("option未設定エラー")

        return option_ary   
                

    def build_options(self,options,delimiter):
        """ 
        TODO get_optionsと統合できそう
        get_optionsで設定された入力内容をもとに定義文を構築していく。
        
        optionsそれぞれで以下の処理を行う
            optionにvalueが設定されていない場合はその項目のoptionsとdelimiterを用いて再起的にこの関数を呼びvalueを設定する。
            optionにvalueが設定されている場合は、valueが空文字でない時にflg_all_emptyをtrueとする
            どちらの場合でも、設定されたもしくは、設定されているvalueをoption_value_aryに追加する
            
        取得した入力データを区切り文字で接続して文字列にして返す。
        この時、区切り文字は接続する全ての定義文と重複しない数の「~」を付与したものとする。複数個の区切り文字が存在する(@で接続されている場合)も全ての場合で考慮する
        そして、options全てでvalueが空文字の場合(flg_all_emptyがtureの場合)は空文字を返す
            

        Args:
            options (list): 定義項目のオプション情報の一覧、それぞれのdictがoptionsとdelimiterを必ず持つ。
            delimiter (str): optionsのそれぞれの定義文を接続するための区切り文字

        Returns:
            str: オプション全ての定義文を区切り文字で接続した文字列
        """
       
        max_count=-1
        option_value_ary=[]
        flg_all_empty=True
        str_result=""
        
        for option in options:
            defaultVal=""
            if "defaultVal" in option:defaultVal=option["defaultVal"]
            if "value" not in option:
                if option["options"]=="":
                    #TODO
                    print("最深に値がセットされていないエラー")
                option["value"]=self.build_options(option["options"],option["delimiter"])
               
            if option["value"]!="":
                if str(defaultVal).lower()==str(option["value"]).lower():
                    option["value"]=""
                else:
                    flg_all_empty=False
            option_value_ary.append(option["value"])
            for d in delimiter.split("@"):
                count=tool.get_delimiter(option["value"],d).count(self.STR_TILDE)
                if count>max_count:max_count=count
        if flg_all_empty:
            return str_result
        if "@" in delimiter:
            str_result=option_value_ary[0]
            for i,d in enumerate(delimiter.split("@")):
                str_result=str_result+(self.STR_TILDE*(max_count+1)+d)+option_value_ary[i+1]
            
        else:       
            delimiter=self.STR_TILDE*(max_count+1)+delimiter
            str_result=delimiter.join(option_value_ary)
        return str_result
            
    def get_value_from_inputdata_by_id(self,id):
        """
        初期化時に設定したinput_json_dataからgrid_idをキーとして検索し、valueを返す
        全て、文字型にする

        Args:
            id (str): 取得したい項目の画面上のgrid_id

        Returns:
            list: 初期化時に設定したinput_json_dataからgrid_idをキーとして検索し、valueを返す。未設定の場合は空文字を返す
        """
        for input_item in self.input_json_data:
            if input_item["grid_id"]=="grid_"+id:
                return [str(result_value) for result_value in input_item["value"]]
        
        return [""]
         
    def build_grid_def(self):
        current_folder_path=os.path.abspath(os.path.dirname(__file__))
        parent_folder_path=os.path.abspath(os.path.join(current_folder_path,os.pardir))
        # JSONファイルを開く
        with open(os.path.join(parent_folder_path,"data/grid.json"), "r",encoding="utf-8") as f:
            # JSONデータを読み込む
            data = json.load(f)
            grid_items=data["items"]
            #画面上の入力値を設定する
            option_ary=self.get_options(grid_items)

            
            delimiter=data["delimiter"]
            #定義文の構築
            result=self.build_options(option_ary,delimiter)
            #print(type(result))
            return result


   
