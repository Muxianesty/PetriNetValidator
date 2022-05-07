from pm4py.objects.petri_net.obj import PetriNet
from pm4py.objects.petri_net.utils.petri_utils import *
from validator.utils import *


def apply_fpp_rule(net: PetriNet, target: PetriNet.Place):
    if target not in net.places:
        return None, None
    src_arcs = target.in_arcs
    src_trs = set(arc.source for arc in src_arcs)
    dst_arcs = target.out_arcs
    dst_trs = set(arc.target for arc in dst_arcs)
    original_transitions = src_trs.union(dst_trs)
    original_arcs = src_arcs.union(dst_arcs)
    other = None
    for place in net.places:
        place_in_trs = set(arc.source for arc in place.in_arcs)
        place_out_trs = set(arc.target for arc in place.out_arcs)
        if place != target and place_in_trs == src_trs and place_out_trs == dst_trs:
            original_arcs.update(place.in_arcs)
            original_arcs.update(place.out_arcs)
            other = place
            break
    if other is None:
        return None, None
    original_subnet = deepcopy(PetriNet("FPP-1", {target, other}, original_transitions,
                                        original_arcs, net.properties))
    remove_place(net, other)
    converted_subnet = deepcopy(PetriNet("FPP-2", {target}, original_transitions,
                                         src_arcs.union(dst_arcs), net.properties))
    return original_subnet, converted_subnet


def apply_fpt_rule(net: PetriNet, target: PetriNet.Transition):
    if target not in net.transitions:
        return None, None
    src_arcs = target.in_arcs
    src_trs = set(arc.source for arc in src_arcs)
    dst_arcs = target.out_arcs
    dst_trs = set(arc.target for arc in dst_arcs)
    original_places = src_trs.union(dst_trs)
    original_arcs = src_arcs.union(dst_arcs)
    other = None
    for transition in net.transitions:
        trs_in_plcs = set(arc.source for arc in transition.in_arcs)
        trs_out_plcs = set(arc.target for arc in transition.out_arcs)
        if transition != target and transition.label == target.label and \
                trs_in_plcs == src_trs and trs_out_plcs == dst_trs:
            original_arcs.update(transition.in_arcs)
            original_arcs.update(transition.out_arcs)
            other = transition
            break
    if other is None:
        return None, None
    original_subnet = deepcopy(PetriNet("FPT-1", original_places, {target, other},
                                        original_arcs, net.properties))
    remove_transition(net, other)
    converted_subnet = deepcopy(PetriNet("FPT-2", original_places, {target},
                                         src_arcs.union(dst_arcs), net.properties))
    return original_subnet, converted_subnet


def apply_lte_rule(target: PetriNet.Transition, net: PetriNet):
    if target not in net.transitions or not isLocalLabel(target.label) or len(target.in_arcs) != 1 or \
            len(target.out_arcs) != 1:
        return None, None
    src_arc: PetriNet.Arc = list(target.in_arcs)[0]
    dst_arc: PetriNet.Arc = list(target.out_arcs)[0]
    src: PetriNet.Place = src_arc.source
    dst: PetriNet.Place = dst_arc.target
    src_trs = set(arc.source for arc in src.in_arcs)
    dst_trs = set(arc.target for arc in dst.out_arcs)
    if src_arc.weight != 1 or dst_arc.weight != 1 or len(src.out_arcs) != 1 or len(dst.in_arcs) != 1 or \
            (len(src.in_arcs) == 0 and len(dst.out_arcs) == 0) or len(src_trs.intersection(dst_trs)) != 0:
        return None, None
    original_places = {src, dst}
    original_transitions = src_trs.union(dst_trs).union({target})
    original_arcs = src.in_arcs.union(src.out_arcs).union(dst.in_arcs).union(dst.out_arcs)
    original_subnet = \
        deepcopy(PetriNet("LTE-1", original_places, original_transitions, original_arcs, net.properties))
    dst.name = target.name
    for arc in src.in_arcs:
        add_arc_from_to(arc.source, dst, net, arc.weight, get_arc_type(arc))
    original_places.remove(src)
    remove_place(net, src)
    original_transitions.remove(target)
    remove_transition(net, target)
    converted_subnet = deepcopy(PetriNet("LTE-2", original_places, original_transitions,
                                         dst.in_arcs.union(dst.out_arcs), net.properties))
    return original_subnet, converted_subnet


def apply_peps_rule(target: PetriNet.Place, net: PetriNet, convertible: PetriNet.Place):
    return None, None
