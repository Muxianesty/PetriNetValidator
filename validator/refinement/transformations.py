from pm4py.objects.petri_net.obj import PetriNet
from pm4py.objects.petri_net.utils.petri_utils import *
from validator import *


def apply_ipp_rule(target: PetriNet.Place, net: PetriNet, convertible: PetriNet.Place):
    return None, None


def apply_ipt_rule(target: PetriNet.Transition, net: PetriNet, convertible: PetriNet.Transition):
    return None, None


def apply_lti_rule(target: PetriNet.Place, net: PetriNet, convertible: PetriNet.Transition):
    return None, None
