from pm4py.objects.petri_net.obj import PetriNet
from pm4py.objects.petri_net.utils.petri_utils import *
from validator import *


def apply_ipp_rule(target: PetriNet.Place, net: PetriNet, convertible: PetriNet.Place):
    return None, None


def apply_ipt_rule(target: PetriNet.Transition, net: PetriNet, convertible: PetriNet.Transition):
    return None, None


def apply_lti_rule(target: PetriNet.Transition, net: PetriNet, convertible: PetriNet.Place):
    if convertible not in net.places or len(target.in_arcs) == 1 or len(target.out_arcs) == 1:
        return None, None
    target_src: PetriNet.Place = list(target.in_arcs)[0].source
    target_dst: PetriNet.Place = list(target.out_arcs)[0].target
    original_places = {convertible}
    conv_src_trs = set([arc.source for arc in convertible.in_arcs])
    conv_dst_trs = set([arc.target for arc in convertible.out_arcs])
    original_transitions = conv_src_trs.union(conv_dst_trs)
    original_subnet = deepcopy(PetriNet("LTI-1", original_places, original_transitions,
                                        convertible.in_arcs.union(convertible.out_arcs), net.properties))
    convertible.name = target_src.name
    transition = add_transition(net, target.name)
    place = add_place(net, target_dst.name)
    trs_src_arc = add_arc_from_to(convertible, transition, net)
    trs_dst_arc = add_arc_from_to(transition, place, net)
    copy = set(convertible.out_arcs)
    for arc in copy:
        add_arc_from_to(place, arc.target, net, arc.weight, get_arc_type(arc))
        remove_arc(net, arc)
    original_places.add(place)
    original_transitions.add(transition)
    converted_arcs = convertible.in_arcs.union(convertible.out_arcs).union(place.in_arcs).union(place.out_arcs)
    converted_subnet = \
        deepcopy(PetriNet("LTE-2", original_places, original_transitions, converted_arcs, net.properties))
    return original_subnet, converted_subnet
