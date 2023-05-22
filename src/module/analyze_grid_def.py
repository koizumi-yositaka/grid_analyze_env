import os
import json
import re



import sys

sys.path.append(os.getcwd())
from module import tool
'''
定義文から、定義内容のJSONファイルを作成する
'''  
class AnalyzeGrid(object):


    def analyze(self,grid_def):
        """
        ファイルから定義文を読み込んで、グリッドの定義項目を表したJSONファイルをもとに分解する
        
        delete_comment関数でコメントを削除する
        get_items関数で定義文の分解を行う
        分解され定義項目IDとvalueを要素としたdictがdef_dict_aryに追加されていく
        """
        current_folder_path=os.path.abspath(os.path.dirname(__file__))
        parent_folder_path=os.path.abspath(os.path.join(current_folder_path,os.pardir))
        grid_def=grid_def.replace('\n','')
        # JSONファイルを開く
        with open(os.path.join(parent_folder_path,"data/grid.json"), "r",encoding="utf-8") as f:
            # JSONデータを読み込む
            data = json.load(f)
            grid_def=self.delete_comment(grid_def)
            self.def_dict_ary=self.get_items(data,grid_def)
            return self.def_dict_ary
    
            
    def write(self,file_path):
        """フォルダにdef_dict_aryを書き込む

        Args:
            dirname (str): 書き込み先のファイルのパス
        """
        with open(file_path,"w+",encoding="utf-8") as j:
            json.dump(self.def_dict_ary,j,indent=4,ensure_ascii=False)
        
    def delete_comment(self,grid_def):

        pattern = re.compile(r'/\*\*.*?\*/', re.DOTALL)
        return re.sub(pattern, "", grid_def)

    def get_items(self,data,grid_def):
        """
        グリッド定義の大分類の25項目それぞれで、get_optionsを行い、optionを取得していく

        Args:
            data (list): gridの定義構造を表したもの
            grid_def (str): 定義文

        Returns:
            list: 分解され定義項目IDとvalueを要素としたdictのlist
        """
        if "items" in data:
            #区切り文字のうち最大個数の「~」が付与されたものを取得
            delimiter=tool.get_delimiter(grid_def,data["delimiter"])
            def_ary=grid_def.split(delimiter)   
            def_dict_ary=[]
            #分解された25項目それぞれでget_optionsを実行
            for item,defs in zip(data["items"],def_ary):
                
                self.get_options(item,defs,def_dict_ary)
            
            return def_dict_ary
            
    def get_options(self,item,grid_def,def_dict_ary):
        """
        

        Args:
            item (_type_): options/optionNameをキーに持つobj
            grid_def (_type_): itemNameの部分の定義
        """
        #区切り文字で分解した後のもの
        def_ary=[]
        delimiter=""
        #書式が複数ある場合には、今のところ一つ目の書式を採用する
        if isinstance(item["signature"],list):
            selected_signatures=0#選択された書式
            signatures=item["signature"]
            # print(grid_def,signatures)
            elem=signatures[selected_signatures]
            for key, value in elem.items():
                item[key]=value
        delimiter=item["delimiter"]
        #{}と()に囲まれた部分は区切り文字で区切らない
        protect_pattern_ary=[{"s":"{","e":"}"},{"s":"(","e":")"}]
   
        def_ary=self.get_def_ary(grid_def,delimiter,protect_pattern_ary)
        #文末の空白と~を削除する
        pattern = r"\s*~\s*$"
        #値が全て空文字かどうか
        flag_all_empty=True
        for i in range(len(def_ary)):
            
            def_ary[i] = re.sub(pattern, "", def_ary[i] )
            if def_ary[i]!="":flag_all_empty=False
    
        #子の定義項目がjsonデータにある場合
        if "options" in item:
            #子の定義項目がない
            if item["options"]=="":
                
                del item["options"]#オプションキーは削除
                
                if "dekimiter" in item :del item["delimiter"]#区切り文字の情報は削除
                #値の設定
                defaultVal=""
                if "defaultVal" in item:
                    defaultVal=item["defaultVal"]
                    del item["defaultVal"]
                if flag_all_empty:
                    item["value"] =[str(defaultVal)]
                else:
                    item["value"]=[str(val) for val in def_ary  ]
                   
                
                #collection
                
                #self.dc.collect_def_sample(item)
                #そのまま出力
                #print(item["optionName"],":",def_ary)
                def_dict_ary.append(item)
            #子の定義項目が存在する
            else:
                for option,defs in zip(item["options"],def_ary):
                    #print(option["optionName"],"++++++",defs)
                    self.get_options(option,defs,def_dict_ary)
    

    def omit_del_pos(self,start_chara,end_chara,defs,del_pos_ary):
        """start_charaとend_charaに囲まれた区切り文字を無視するため

        Args:
            start_chara (str): 区切り文字を無視する文字列の最初の文字。例："{"
            end_chara (str):  区切り文字を無視する文字列の最後の文字。例："}"
            defs (str): 区切り文字で分割する対象の文字列
            del_pos_ary (list): defsにある区切り文字のindex

        Returns:
            list: del_pos_aryのうちstart_charaとend_charaに囲まれた部分は無視したもの
        """
        #st_pos_ary：開始文字のindexのリスト
        st_pos_ary=[]
        start_pos=defs.find(start_chara)
        while start_pos!=-1:
           st_pos_ary.append(start_pos) 
           start_pos=defs.find(start_chara,start_pos+len(start_chara))
     
        
        #end_pos_ary：終了文字のindexのリスト
        end_pos_ary=[]
        end_pos=defs.find(end_chara)
        while end_pos!=-1:
           end_pos_ary.append(end_pos) 
           end_pos=defs.find(end_chara,end_pos+len(end_chara))
       
        
        #st_pos_aryとend_pos_aryが空の場合は省略を行わない
        if len(st_pos_ary)<1 or len(end_pos_ary)<1:
            return del_pos_ary
        #protect_ary：無視する範囲を示した辞書型のリスト
        # [{"s":区切り文字を無視する文字列の始まりのindex,"e":区切り文字を無視する文字列の終わりのindex},...]
        protect_ary=[]
        #start_pos_index：区切り文字を無視する文字列の始まりのindex
        start_pos_index=0
        #end_pos_index：区切り文字を無視する文字列の終わりのindex
        end_pos_index=len(end_pos_ary)-1
        #無視する範囲を示した辞書型をリストに追加していく
        for i in range(len(end_pos_ary)):
            
            for j in range(len(st_pos_ary)):
                if end_pos_ary[j]<st_pos_ary[i]:
                    end_pos_index=i-1
                    protect_ary.append({"s":st_pos_ary[start_pos_index],"e":end_pos_ary[end_pos_index]-1})
                    start_pos_index=i
                    end_pos_index=len(end_pos_ary)-1
                    break
            continue
        #最後の無視する範囲を示した辞書型を追加
        protect_ary.append({"s":st_pos_ary[start_pos_index],"e":end_pos_ary[end_pos_index]-1})
        #protect_aryによってdel_pos_aryを省略していく、省略したいindexは-1に変換する
        for i,del_pos in enumerate(del_pos_ary):
            for protect_pos in protect_ary:
                if del_pos >= protect_pos["s"] and del_pos<=protect_pos["e"]:
                    del_pos_ary[i]=-1
        return del_pos_ary

    def get_def_ary(self,defs,delimiter,protect_pattern_ary):
        """_summary_

        Args:
            defs (str): 区切り文字で分割する対象の文字列
            delimiter (str): 区切り文字
            protect_pattern_ary (list): 無視する範囲を示した辞書型のリスト

        Returns:
            list: 区切り文字で分割した結果のリスト
        """
        del_pos_ary=[]
        delimiter_ary=[]
        flag_multi_delimiter=False
        ##区切り文字によって定義項目を子要素に細分化する
        #特殊な区切り文字(複数の区切り文字つまり「@」を含む)の場合
        if delimiter=="":
            del_pos_ary=[]
        elif "@" in delimiter:
            flag_multi_delimiter=True
            delimiter_ary=delimiter.split("@")
            for i in range(len(delimiter_ary)):
                delimiter_ary[i]=tool.get_delimiter(defs,delimiter_ary[i])
                index=defs.find(delimiter_ary[i])
                if index < 0:
                    pass
                else:
                    del_pos_ary.append(index)
                                        
        #区切り文字が１種類存在している場合、それを分解し配列化する→子要素に分解      
        else:
            delimiter=tool.get_delimiter(defs,delimiter)
            pos=defs.find(delimiter)
            del_pos_ary = []
            while pos!=-1:
                del_pos_ary.append(pos)
                pos=defs.find(delimiter,pos+len(delimiter))
                
        #print(delimiter,del_pos_ary)
        #del_pos_aryをprotect_pattern_aryに従って、omit_del_posを用いて省略する
        for protect_pattern in protect_pattern_ary:
            del_pos_ary=self.omit_del_pos(protect_pattern["s"],protect_pattern["e"],defs,del_pos_ary)
        def_ary=[]
        index=0
        for i in range(len(del_pos_ary)):
            if del_pos_ary[i]<0: continue
            def_ary.append(defs[index:del_pos_ary[i]])
            #複数の区切り文字
            if flag_multi_delimiter:
                index=del_pos_ary[i]+len(delimiter_ary[i])
            #単数の区切り文字
            else:
                index=del_pos_ary[i]+len(delimiter)
        def_ary.append(defs[index:])
        return def_ary
