from pm4py.objects.petri_net.obj import PetriNet
from pm4py.objects.petri_net.utils.petri_utils import *


def apply_fpp_rule(target: PetriNet.Place, net: PetriNet, convertable: PetriNet.Place):
    if convertable not in net.places:
        return None, None
    place = PetriNet.Place(target.name, convertable.in_arcs, convertable.out_arcs)
    srcs_arcs = convertable.in_arcs
    trgts_arcs = convertable.out_arcs
    convertibles = [p for p in net.places if p.in_arcs == srcs_arcs and p.out_arc == trgts_arcs]
    for arc in srcs_arcs:
        start = arc.source

def apply_fpt_rule(target: PetriNet.Transition, net: PetriNet, convertable: PetriNet.Transition):
    return None, None


def apply_lte_rule(target: PetriNet.Place, net: PetriNet, convertable: PetriNet.Transition):
    if convertable not in net.transitions or len(convertable.in_arcs) != 1 or len(convertable.out_arcs) != 1:
        return None, None
    src : PetriNet.Place = list(convertable.in_arcs)[0]
    dst : PetriNet.Place = list(convertable.out_arcs)[0]
    src_trs = set(arc.source for arc in src.in_arcs)
    dst_trs = set(arc.target for arc in dst.out_arcs)
    if len(src.out_arcs) != 1 or len(dst.in_arcs) != 1 or \
            (len(src.in_arcs) == 0 and len(dst.out_arcs) == 0) or len(src_trs.intersection(dst_trs)) != 0:
        return None, None
    original_places = {src, dst}
    original_transitions = src_trs.union(dst_trs).union([convertable])
    original_arcs = src.in_arcs.union(src.out_arcs).union(dst.in_arcs).union(dst.out_arcs)
    original_subnet = deepcopy(PetriNet("LTE-1", original_places, original_transitions, original_arcs, net.properties))
    dst.name = target.name
    for arc in src.in_arcs:
        add_arc_from_to(arc.source, dst, net, arc.weight, get_arc_type(arc))
    original_places.remove(src)
    remove_place(net, src)
    original_transitions.remove(convertable)
    remove_transition(net, convertable)
    converted_subnet = deepcopy(PetriNet("LTE-2", original_places, original_transitions,
                                         dst.in_arcs.union(dst.out_arcs), net.properties))
    return original_subnet, converted_subnet


def apply_peps_rule(target: PetriNet.Place, net: PetriNet, convertable: PetriNet.Place):
    if convertable not in net.places:
        return None, None
    place = PetriNet.Place(target.name, convertable.in_arcs, convertable.out_arcs)
    srcs_arcs = convertable.in_arcs