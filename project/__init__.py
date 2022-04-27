import os
from enum import Enum
from pm4py.visualization.petri_net import visualizer as pn_viz

VIZ_PARAMS = {pn_viz.Variants.WO_DECORATION.value.Parameters.FORMAT: "png"}
OUTPUT_PATH = os.path.abspath(os.curdir + os.sep + "Output" + os.sep)


class PNetStatus(Enum):
    WRONG = 0
    FINE = 1


class PNetsStatus(Enum):
    ISOM = 0
    NON_CONV = 1
    FINE = 2
