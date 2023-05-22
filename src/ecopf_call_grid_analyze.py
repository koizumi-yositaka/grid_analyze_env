
import sys
from module import analyze_grid_def

#received_grid_def=sys.argv[1]
received_grid_def="dataGridT_Sub~!\n ~!\n~!\n~!\n~!\n@Item=H_Vfalse\n\n~!\n~!\n~!\n~!\n~!\n~!\n~!\n~!\n~!~/\nZSample_T_T_Project_Details,ZSample_V_T_Project_Details~/\nSID~/\n\n\\$test1@Master@\n\n~/\n~/\ntrue:true:true:true~/\n~/\n~/\nRelKey~/\n~/\n~/\n~/\n~/\ntrue~/\nSorts~/\n明細List~/\n~/\n~/\n~/\n~/\n~/\n~/\n~/\n~/"
ag=analyze_grid_def.AnalyzeGrid()
parsed_grid_def=ag.analyze(received_grid_def) 
print(parsed_grid_def)
