import os
from pm4py.visualization.petri_net import visualizer as pn_viz

VIZ_PARAMS = {pn_viz.Variants.WO_DECORATION.value.Parameters.FORMAT: "png"}
OUTPUT_PATH = os.path.abspath(os.getcwd() + os.sep + "Output" + os.sep)
