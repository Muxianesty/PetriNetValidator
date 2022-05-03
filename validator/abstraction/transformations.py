from pm4py.objects.petri_net.obj import PetriNet
from pm4py.objects.petri_net.utils.petri_utils import *


def apply_lte_rule(target: PetriNet.Place, net: PetriNet, convertible: PetriNet.Transition):
    if convertible not in net.transitions or len(convertible.in_arcs) != 1 or len(convertible.out_arcs) != 1:
        return
    src = list(convertible.in_arcs)[0]
    dst = list(convertible.out_arcs)[0]
    if len(src.out_arcs) != 1 or len(dst.in_arcs) != 1 or \
            (len(src.in_arcs) == 0 and len(dst.out_arcs) == 0) or len(src.in_arcs.intersection(dst.out_arcs)) != 0:
        return
    place = PetriNet.Place(target.name)
    net.places.add(place)
    net.places.remove(src)
    net.places.remove(dst)
    net.transitions.remove(convertible)
    for arc in src.in_arcs:
        trans = arc.source
        trans.out_arcs.remove(arc)
        net.arcs.remove(arc)
        add_arc_from_to(trans, place, net, arc.weight, get_arc_type(arc))
    for arc in dst.out_arcs:
        trans = arc.target
        trans.in_arcs.remove(arc)
        net.arcs.remove(arc)
        add_arc_from_to(place, trans, net, arc.weight, get_arc_type(arc))
    return place
