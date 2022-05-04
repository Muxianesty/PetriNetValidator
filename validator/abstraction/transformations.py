from pm4py.objects.petri_net.obj import PetriNet
from pm4py.objects.petri_net.utils.petri_utils import *


def apply_fpp_rule(target: PetriNet.Place, net: PetriNet, convertible: PetriNet.Place):
    if convertible not in net.places:
        return None, None
    src_arcs = convertible.in_arcs
    src_trs = set(arc.source for arc in src_arcs)
    dst_arcs = convertible.out_arcs
    dst_trs = set(arc.target for arc in dst_arcs)
    original_places = {convertible}
    original_transitions = src_trs.union(dst_trs)
    original_arcs = set().union(src_arcs).union(dst_arcs)
    for place in net.places:
        if place.in_arcs == src_arcs and place.out_arc == dst_arcs and place != convertible:
            original_places.add(place)
            original_arcs.update(place.in_arcs)
            original_arcs.update(place.out_arcs)
    original_subnet = deepcopy(PetriNet("FPP-1", original_places, original_transitions, original_arcs))
    for place in original_places:
        remove_place(net, place)
    convertible.name = target.name
    converted_subnet = deepcopy(PetriNet("FPP-2", {convertible}, original_transitions, src_arcs.union(dst_arcs)))
    return original_subnet, converted_subnet

def apply_fpt_rule(target: PetriNet.Transition, net: PetriNet, convertible: PetriNet.Transition):
    return None, None


def apply_lte_rule(target: PetriNet.Place, net: PetriNet, convertible: PetriNet.Transition):
    if convertible not in net.transitions or len(convertible.in_arcs) != 1 or len(convertible.out_arcs) != 1:
        return None, None
    src: PetriNet.Place = list(convertible.in_arcs)[0]
    dst: PetriNet.Place = list(convertible.out_arcs)[0]
    src_trs = set(arc.source for arc in src.in_arcs)
    dst_trs = set(arc.target for arc in dst.out_arcs)
    if len(src.out_arcs) != 1 or len(dst.in_arcs) != 1 or \
            (len(src.in_arcs) == 0 and len(dst.out_arcs) == 0) or len(src_trs.intersection(dst_trs)) != 0:
        return None, None
    original_places = {src, dst}
    original_transitions = src_trs.union(dst_trs).union([convertible])
    original_arcs = src.in_arcs.union(src.out_arcs).union(dst.in_arcs).union(dst.out_arcs)
    original_subnet = deepcopy(PetriNet("LTE-1", original_places, original_transitions, original_arcs, net.properties))
    dst.name = target.name
    for arc in src.in_arcs:
        add_arc_from_to(arc.source, dst, net, arc.weight, get_arc_type(arc))
    original_places.remove(src)
    remove_place(net, src)
    original_transitions.remove(convertible)
    remove_transition(net, convertible)
    converted_subnet = deepcopy(PetriNet("LTE-2", original_places, original_transitions,
                                         dst.in_arcs.union(dst.out_arcs), net.properties))
    return original_subnet, converted_subnet


def apply_peps_rule(target: PetriNet.Place, net: PetriNet, convertible: PetriNet.Place):
    if convertible not in net.places:
        return None, None
    place = PetriNet.Place(target.name, convertible.in_arcs, convertible.out_arcs)
    srcs_arcs = convertible.in_arcs
