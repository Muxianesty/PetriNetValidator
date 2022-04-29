from project import *
import os.path
from pm4py.objects.petri_net.obj import PetriNet
from pm4py.objects.petri_net.importer import importer as pnml_imp
from pm4py.algo.analysis.workflow_net import algorithm as wfn_alg


def parseNet(path: str):
    try:
        net = pnml_imp.apply(os.path.abspath(path))[0]
        if not wfn_alg.apply(net):
            return PNetStatus.NOT_WFN
        return PNetStatus.FINE, net
    except BaseException:
        return PNetStatus.ERROR


def getInitAndFinPlaces(net: PetriNet):
    initial_places = [p for p in net.places if len(p.in_arcs) == 0]
    final_places = [p for p in net.places if len(p.out_arcs) == 0]
    return initial_places, final_places


def getDirNameFromNets(first_path: str, second_path: str) -> str:
    return os.path.splitext(os.path.basename(first_path))[0] + "-" + os.path.splitext(os.path.basename(second_path))[0]


def visualizeNet(net: PetriNet, file_path: str):
    gviz = pn_viz.apply(net, parameters=VIZ_PARAMS)
    pn_viz.save(gviz, file_path)


def isomHash(net: PetriNet, init_places=None) -> int:
    result = int(0)
    init_places = init_places if init_places is not None else getInitAndFinPlaces(net)[0]

    return result
