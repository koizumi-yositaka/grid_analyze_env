
import sys
from module import analyze_grid_def

received_grid_def=sys.argv[1]

ag=analyze_grid_def.AnalyzeGrid()
parsed_grid_def=ag.analyze(received_grid_def) 
print(parsed_grid_def)
