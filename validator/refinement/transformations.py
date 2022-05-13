from pm4py.objects.petri_net.obj import PetriNet
from pm4py.objects.petri_net.utils.petri_utils import *
from validator.utils import *


def apply_ipp_rule(m_net: MarkedPetriNet, target: PetriNet.Place):
    if target not in m_net.net.places:
        return None, None, None
    original_places = {target}
    original_transitions = \
        set(arc.source for arc in target.in_arcs).union(set(arc.target for arc in target.out_arcs))
    original_arcs = target.in_arcs.union(target.out_arcs)
    original_subnet = \
        deepcopy(MarkedPetriNet(PetriNet("IPP-1", original_places, original_transitions,
                                         original_arcs, m_net.net.properties), m_net.init_m, m_net.fin_m))
    place = add_place(m_net.net)
    for arc in target.in_arcs:
        original_arcs.add(add_arc_from_to(arc.source, place, m_net.net, arc.weight, get_arc_type(arc)))
    for arc in target.out_arcs:
        original_arcs.add(add_arc_from_to(place, arc.target, m_net.net, arc.weight, get_arc_type(arc)))
    original_places.add(place)
    converted_subnet = \
        deepcopy(MarkedPetriNet(PetriNet("IPP-2", original_places, original_transitions,
                                         original_arcs, m_net.net.properties), m_net.init_m, m_net.fin_m))
    return original_subnet, converted_subnet, place


def apply_ipt_rule(m_net: MarkedPetriNet, target: PetriNet.Transition):
    if target not in m_net.net.transitions:
        return None, None, None
    original_places = \
        set(arc.source for arc in target.in_arcs).union(set(arc.target for arc in target.out_arcs))
    original_transitions = {target}
    original_arcs = target.in_arcs.union(target.out_arcs)
    original_subnet = \
        deepcopy(MarkedPetriNet(PetriNet("IPT-1", original_places, original_transitions,
                                         original_arcs, m_net.net.properties), m_net.init_m, m_net.fin_m))
    transition = add_transition(m_net.net, label=target.label)
    for arc in target.in_arcs:
        original_arcs.add(add_arc_from_to(arc.source, transition, m_net.net, arc.weight, get_arc_type(arc)))
    for arc in target.out_arcs:
        original_arcs.add(add_arc_from_to(transition, arc.target, m_net.net, arc.weight, get_arc_type(arc)))
    original_transitions.add(transition)
    converted_subnet = \
        deepcopy(MarkedPetriNet(PetriNet("IPT-2", original_places, original_transitions,
                                         original_arcs, m_net.net.properties), m_net.init_m, m_net.fin_m))
    return original_subnet, converted_subnet, transition


def apply_lti_rule(m_net: MarkedPetriNet, target: PetriNet.Place):
    if target not in m_net.net.places:
        return None, None, None
    original_places = {target}
    target_src_trs = set([arc.source for arc in target.in_arcs])
    target_dst_trs = set([arc.target for arc in target.out_arcs])
    if len(target_src_trs) == 1 and isLocalLabel(list(target_src_trs)[0].label) or \
        len(target_dst_trs) == 1 and isLocalLabel(list(target_dst_trs)[0].label) or \
            len(target_src_trs.intersection(target_dst_trs)) != 0:
        return None, None, None
    original_transitions = target_src_trs.union(target_dst_trs)
    original_subnet = deepcopy(MarkedPetriNet(PetriNet("LTI-1", original_places, original_transitions,
                                                       target.in_arcs.union(target.out_arcs), m_net.net.properties),
                                              m_net.init_m, m_net.fin_m))
    transition = add_transition(m_net.net, label=EMPTY_LABEL)
    place = add_place(m_net.net)
    copy_set = set(target.out_arcs)
    for arc in copy_set:
        add_arc_from_to(place, arc.target, m_net.net, arc.weight, get_arc_type(arc))
        remove_arc(m_net.net, arc)
    trs_src_arc = add_arc_from_to(target, transition, m_net.net)
    trs_dst_arc = add_arc_from_to(transition, place, m_net.net)
    original_places.add(place)
    original_transitions.add(transition)
    converted_arcs = target.in_arcs.union(place.out_arcs)
    converted_arcs.add(trs_src_arc)
    converted_arcs.add(trs_dst_arc)
    converted_subnet = \
        deepcopy(MarkedPetriNet(PetriNet("LTI-2", original_places, original_transitions,
                                         converted_arcs, m_net.net.properties), m_net.init_m, m_net.fin_m))
    return original_subnet, converted_subnet, transition


def apply_psi_rule():
    return None, None
