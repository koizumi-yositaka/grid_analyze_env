def get_delimiter(defs,delimiter):
    """定義文(defs)の中に使われている、区切り文字(delimiter)に最大でいくつのチルダ「~」が付いているかを判別し、そのチルダをつけた区切り文字を返す

    Args:
        defs (_type_): _description_
        delimiter (_type_): _description_

    Returns:
        _type_: _description_
    """
    if type(defs)!=str:return delimiter
    count=0
    #最大の区切り文字の~の個数の特定
    while True:
        temp_delimiter="~"*count+delimiter
        
    
        if len(defs.split(temp_delimiter))==1:
            count=count-1
            break
        count+=1
    delimiter="~"*count+delimiter
    return delimiter


