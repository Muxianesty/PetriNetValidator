from validator import *
from enum import Enum
import os.path
from pm4py.objects.petri_net.obj import *
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


class MarkedPetriNet(object):
    pass

    def __init__(self, net: PetriNet, i_mkg: Marking = None, f_mkg: Marking = None):
        self.__net: PetriNet = net
        self.__i_mkg: Marking = Marking() if i_mkg is None else i_mkg
        self.__f_mkg: Marking = Marking() if f_mkg is None else f_mkg

    def __get_net(self) -> PetriNet:
        return self.__net

    def __get_i_mkg(self) -> Marking:
        return self.__i_mkg

    def __get_f_mkg(self) -> Marking:
        return self.__f_mkg

    net = property(__get_net)
    init_m = property(__get_i_mkg)
    fin_m = property(__get_f_mkg)


def parseNet(path: str):
    try:
        net, initial_m, final_m = pnml_imp.apply(os.path.abspath(path))
        if not wfn_alg.apply(net):
            return PNetStatus.NOT_WFN, None
        return PNetStatus.FINE, MarkedPetriNet(net, initial_m, final_m)
    except BaseException:
        return PNetStatus.ERROR, None


def getInitAndFinPlaces(m_net: MarkedPetriNet):
    initial_places = [p for p in m_net.net.places if len(p.in_arcs) == 0]
    final_places = [p for p in m_net.net.places if len(p.out_arcs) == 0]
    return initial_places, final_places


def getDirNameFromNets(first_path: str, second_path: str) -> str:
    return os.path.splitext(os.path.basename(first_path))[0] + "-" + os.path.splitext(os.path.basename(second_path))[0]


def visualizeNet(m_net: MarkedPetriNet, file_path: str):
    gviz = pn_viz.apply(m_net.net, initial_marking=m_net.init_m, final_marking=m_net.fin_m, parameters=VIZ_PARAMS)
    pn_viz.save(gviz, file_path)


def isLocalLabel(label: str) -> bool:
    return label is None or label.startswith('\n')


def labelDictionary(m_net: MarkedPetriNet) -> dict:
    result = {'\n': 0}
    for trs in m_net.net.transitions:
        if isLocalLabel(trs.label):
            result['\n'] += 1
        else:
            result[trs.label] += 1
    return result


def isomHash(m_net: MarkedPetriNet) -> int:
    result = int(0)
    data = list(m_net.net.arcs)
    size = int(len(data))
    for index in range(size):
        for inner_index in range(index, size):
            if data[index].source != data[inner_index].source and data[index].source != data[inner_index].target and \
                    data[index].target != data[inner_index].source and data[index].target != data[inner_index].target:
                result += data[index].weight * data[inner_index].weight
    return result
