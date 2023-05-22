

import sys
import os
sys.path.append(os.getcwd())
from src.module import tool
import pytest

#defs,delimiter,expectationsのリスト
test_get_delimiter_params=[
    ("aaaa/bbbb~/cccc~~/","/","~~/"),
    (1,"/","/"),
    (False,"/","/")
]
@pytest.mark.parametrize("defs,delimiter,expectations",test_get_delimiter_params)
def test_get_delimiter(defs,delimiter,expectations):
    assert (tool.get_delimiter(defs,delimiter))==expectations
    
