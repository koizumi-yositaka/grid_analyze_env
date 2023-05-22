

from module import analyze_grid_def
import os

with open("data/gridSamples/part1.txt","r",encoding="utf-8") as f:
    grid_def=f.read()
    ag=analyze_grid_def.AnalyzeGrid()
    ag.analyze(grid_def) 
    ag.write("data/gridJsonSamples/part1.json")
    #del ag.dc