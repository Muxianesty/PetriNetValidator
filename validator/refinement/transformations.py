from pm4py.objects.petri_net.obj import PetriNet
from pm4py.objects.petri_net.utils.petri_utils import *


def apply_ipp_rule(target: PetriNet.Place, tg_net: PetriNet, net: PetriNet, convertible: PetriNet.Place):
    if target not in tg_net.places or convertible not in net.places:
        return None, None
    tg_src_trs = set(arc.source for arc in target.in_arcs)
    tg_dst_trs = set(arc.target for arc in target.out_arcs)
    targets = set()
    for place in tg_net.places:
        plc_src_trs = set(arc.source for arc in place.in_arcs)
        plc_dst_trs = set(arc.target for arc in place.out_arcs)
        if place != target and tg_src_trs == plc_src_trs and tg_dst_trs == plc_dst_trs:
            targets.add(place)
    original_places = {convertible}
    original_transitions = \
        set(arc.source for arc in convertible.in_arcs).union(set(arc.target for arc in convertible.out_arcs))
    original_arcs = convertible.in_arcs.union(convertible.out_arcs)
    original_subnet = \
        deepcopy(PetriNet("IPP-1", original_places, original_transitions, original_arcs, net.properties))
    convertible.name = target.name
    for tg in targets:
        place = add_place(net, tg.name)
        for arc in convertible.in_arcs:
            original_arcs.add(add_arc_from_to(arc.source, place, net, arc.weight, get_arc_type(arc)))
        for arc in convertible.out_arcs:
            original_arcs.add(add_arc_from_to(place, arc.target, net, arc.weight, get_arc_type(arc)))
        original_places.add(place)
    converted_subnet = \
        deepcopy(PetriNet("IPP-2", original_places, original_transitions, original_arcs, net.properties))
    return original_subnet, converted_subnet


def apply_ipt_rule(target: PetriNet.Transition, tg_net: PetriNet, net: PetriNet, convertible: PetriNet.Transition):
    if target not in tg_net.transitions or convertible not in net.transitions or target.label != convertible.label:
        return None, None
    tg_src_plcs = set(arc.source for arc in target.in_arcs)
    tg_dst_plcs = set(arc.target for arc in target.out_arcs)
    targets = set()
    for transition in tg_net.transitions:
        trs_src_plcs = set(arc.source for arc in transition.in_arcs)
        trs_dst_plcs = set(arc.target for arc in transition.out_arcs)
        if transition != target and tg_src_plcs == trs_src_plcs and tg_dst_plcs == trs_dst_plcs:
            targets.add(transition)
    original_places = \
        set(arc.source for arc in convertible.in_arcs).union(set(arc.target for arc in convertible.out_arcs))
    original_transitions = {convertible}
    original_arcs = convertible.in_arcs.union(convertible.out_arcs)
    original_subnet = \
        deepcopy(PetriNet("IPT-1", original_places, original_transitions, original_arcs, net.properties))
    convertible.name = target.name
    for tg in targets:
        transition = add_transition(net, tg.name, convertible.label)
        for arc in convertible.in_arcs:
            original_arcs.add(add_arc_from_to(arc.source, transition, net, arc.weight, get_arc_type(arc)))
        for arc in convertible.out_arcs:
            original_arcs.add(add_arc_from_to(transition, arc.target, net, arc.weight, get_arc_type(arc)))
        original_transitions.add(transition)
    converted_subnet = \
        deepcopy(PetriNet("IPT-2", original_places, original_transitions, original_arcs, net.properties))
    return original_subnet, converted_subnet


def apply_lti_rule(target: PetriNet.Transition, net: PetriNet, convertible: PetriNet.Place):
    if convertible not in net.places or len(target.in_arcs) == 1 or len(target.out_arcs) == 1:
        return None, None
    target_src: PetriNet.Place = list(target.in_arcs)[0].source
    target_dst: PetriNet.Place = list(target.out_arcs)[0].target
    original_places = {convertible}
    conv_src_trs = set([arc.source for arc in convertible.in_arcs])
    conv_dst_trs = set([arc.target for arc in convertible.out_arcs])
    if len(conv_src_trs.union(conv_dst_trs)) != 0:
        return None, None
    original_transitions = conv_src_trs.union(conv_dst_trs)
    original_subnet = deepcopy(PetriNet("LTI-1", original_places, original_transitions,
                                        convertible.in_arcs.union(convertible.out_arcs), net.properties))
    convertible.name = target_src.name
    transition = add_transition(net, target.name)
    place = add_place(net, target_dst.name)
    trs_src_arc = add_arc_from_to(convertible, transition, net)
    trs_dst_arc = add_arc_from_to(transition, place, net)
    copy_set = set(convertible.out_arcs)
    for arc in copy_set:
        add_arc_from_to(place, arc.target, net, arc.weight, get_arc_type(arc))
        remove_arc(net, arc)
    original_places.add(place)
    original_transitions.add(transition)
    converted_arcs = convertible.in_arcs.union(place.out_arcs)
    converted_arcs.add(trs_src_arc)
    converted_arcs.add(trs_dst_arc)
    converted_subnet = \
        deepcopy(PetriNet("LTI-2", original_places, original_transitions, converted_arcs, net.properties))
    return original_subnet, converted_subnet
