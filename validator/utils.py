from validator import *
from enum import Enum
import os.path
from pm4py.objects.petri_net.obj import PetriNet
from pm4py.objects.petri_net.importer import importer as pnml_imp
from pm4py.algo.analysis.workflow_net import algorithm as wfn_alg


class PNetStatus(Enum):
    ERROR = 0
    NOT_WFN = 1
    FINE = 2


class PNetsStatus(Enum):
    ISOM = 0
    NOT_WFN = PNetStatus.NOT_WFN
    NON_CONV = 2
    FINE = 3


def parseNet(path: str):
    try:
        net = pnml_imp.apply(os.path.abspath(path))[0]
        if not wfn_alg.apply(net):
            return PNetStatus.NOT_WFN, None
        return PNetStatus.FINE, net
    except BaseException:
        return PNetStatus.ERROR, None


def getInitAndFinPlaces(net: PetriNet):
    initial_places = [p for p in net.places if len(p.in_arcs) == 0]
    final_places = [p for p in net.places if len(p.out_arcs) == 0]
    return initial_places, final_places


def getDirNameFromNets(first_path: str, second_path: str) -> str:
    return os.path.splitext(os.path.basename(first_path))[0] + "-" + os.path.splitext(os.path.basename(second_path))[0]


def visualizeNet(net: PetriNet, file_path: str):
    gviz = pn_viz.apply(net, parameters=VIZ_PARAMS)
    pn_viz.save(gviz, file_path)


def isLocalLabel(label: str) -> bool:
    return label is None or label.startswith('\n')


def labelDictionary(net: PetriNet) -> dict:
    result = {'\n': 0}
    for trs in net.transitions:
        if isLocalLabel(trs.label):
            result['\n'] += 1
        else:
            result[trs.label] += 1
    return result


def isomHash(net: PetriNet) -> int:
    result = int(0)
    data = list(net.arcs)
    size = int(len(data))
    for index in range(size):
        for inner_index in range(index, size):
            if data[index].source != data[inner_index].source and data[index].source != data[inner_index].target and \
                    data[index].target != data[inner_index].source and data[index].target != data[inner_index].target:
                result += data[index].weight * data[inner_index].weight
    return result
