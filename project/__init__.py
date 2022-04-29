import os
from enum import Enum
from pm4py.visualization.petri_net import visualizer as pn_viz

VIZ_PARAMS = {pn_viz.Variants.WO_DECORATION.value.Parameters.FORMAT: "png"}
OUTPUT_PATH = os.path.abspath(os.curdir + os.sep + "Output" + os.sep)


class PNetStatus(Enum):
    ERROR = 0
    NOT_WFN = 1
    FINE = 2


class PNetsStatus(Enum):
    ISOM = 0
    NOT_WFN = PNetStatus.NOT_WFN
    NON_CONV = 2
    FINE = 3
