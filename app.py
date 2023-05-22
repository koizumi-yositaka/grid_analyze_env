

from src import analyze_grid_def
import os

for file_name in os.listdir("test/gridSamples"):
    if not file_name.endswith(".txt"):continue
    ag=analyze_grid_def.AnalyzeGrid("test/gridSamples/"+file_name)
    ag.analyze() 
    ag.write("test/gridJsonSamples")
    #del ag.dc