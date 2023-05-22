

from module import analyze_grid_def
import os
folder_path=os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(folder_path,"data/gridSamples/part1.txt"),"r",encoding="utf-8") as f:
    grid_def=f.read()
    ag=analyze_grid_def.AnalyzeGrid()
    ag.analyze(grid_def) 
    ag.write(os.path.join(folder_path,"data/gridJsonSamples/part1.json"))
    #del ag.dc