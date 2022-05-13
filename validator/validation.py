from validator.exceptions import NetNotParsableError
from validator.utils import *
from validator.refinement.transformations import *
from validator.abstraction.transformations import *
import shutil
import os


def compareNets(first_net: MarkedPetriNet, second_net: MarkedPetriNet) -> int:
    if len(first_net.net.transitions) < len(second_net.net.transitions) or \
            len(first_net.net.places) < len(second_net.net.places):
        return 1
    elif len(first_net.net.transitions) > len(second_net.net.transitions) or \
            len(first_net.net.places) > len(second_net.net.places):
        return -1
    return 0 if isomHash(first_net) == isomHash(second_net) else 1


def validateModels(interface: MarkedPetriNet, m_net: MarkedPetriNet,
                   dir_path: str, wfn_checked: bool = False) -> PNetsStatus:
    if not dir_path.endswith(os.sep):
        dir_path += os.sep
    if not wfn_checked:
        if not wfn_alg.apply(interface.net) or not wfn_alg.apply(m_net.net):
            return PNetsStatus.NOT_WFN
    mode = compareNets(interface, m_net)
    if mode == 0:
        return PNetsStatus.ISOM
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    os.mkdir(dir_path)
    int_dict: dict = labelDictionary(interface)
    int_plcs_count = len(interface.net.places)
    net_dict: dict = labelDictionary(m_net)
    net_plcs_count = len(m_net.net.places)
    if len(int_dict) != len(net_dict):
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
        return PNetsStatus.NON_CONV
    visualizeNet(interface, dir_path + "interface.png")
    visualizeNet(m_net, dir_path + "net.png")
    counter = int(1)
    need_to_continue: bool = True
    while need_to_continue:
        original, converted = None, None
        for net_key in net_dict:
            if mode > 0 and len(int_dict[net_key]) < len(net_dict[net_key]):
                if int_plcs_count < net_plcs_count and isLocalLabel(net_key):
                    for trs in net_dict[net_key]:
                        original, converted = apply_lte_rule(m_net, trs)
                        if original is not None:
                            net_plcs_count -= 1
                            net_dict[net_key].remove(trs)
                            break
                else:
                    original, converted = apply_fpt_rule(m_net, net_dict[net_key][0], net_dict[net_key][-1])
                    if original is not None:
                        net_dict[net_key].pop()
            elif mode < 0 and len(int_dict[net_key]) > len(net_dict[net_key]):
                if int_plcs_count > net_plcs_count and isLocalLabel(net_key):
                    plcs_lst = list(m_net.net.places)
                    size = len(m_net.net.places)
                    marked = [False] * size
                    for index in range(size):
                        if not marked[index]:
                            in_labels = set(arc.source.label for arc in plcs_lst[index].in_arcs)
                            out_labels = set(arc.target.label for arc in plcs_lst[index].out_arcs)
                            in_net_src = 0
                            in_net_dst = 0
                            for inner_index in range(index + 1, size):
                                if not marked[index]:
                                    p_in_labels = set(arc.source.label for arc in plcs_lst[inner_index].in_arcs)
                                    p_out_labels = set(arc.target.label for arc in plcs_lst[inner_index].out_arc)
                                    if in_labels == p_in_labels and {EMPTY_LABEL} == p_out_labels:
                                        in_net_src += 1
                                        marked[inner_index] = True
                                    if {EMPTY_LABEL} == p_in_labels and out_labels == p_out_labels:
                                        in_net_dst += 1
                                        marked[inner_index] = True
                            marked[index] = True
                            in_int_src = 0
                            in_int_dst = 0
                            for place in interface.net.places:
                                p_in_labels = set(arc.source.label for arc in place.in_arcs)
                                p_out_labels = set(arc.target.label for arc in place.out_arc)
                                if in_labels == p_in_labels and {EMPTY_LABEL} == p_out_labels:
                                    in_int_src += 1
                                if {EMPTY_LABEL} == p_in_labels and out_labels == p_out_labels:
                                    in_int_dst += 1
                            if in_int_src > in_net_src or in_int_dst > in_net_dst:
                                original, converted, new_trs = apply_lti_rule(m_net, plcs_lst[index])
                                if original is not None:
                                    net_plcs_count += 1
                                    net_dict[net_key].append(new_trs)
                                    break
                else:
                    original, converted, new_trs = apply_ipt_rule(m_net, net_dict[net_key][0])
                    if original is not None:
                        net_dict[net_key].append(new_trs)
            if original is not None:
                break
        if original is None and int_plcs_count != net_plcs_count:
            plcs_lst = list(m_net.net.places)
            size = len(m_net.net.places)
            marked = [False] * size
            for index in range(size):
                if not marked[index]:
                    in_labels = set(arc.source.label for arc in plcs_lst[index].in_arcs)
                    out_labels = set(arc.target.label for arc in plcs_lst[index].out_arcs)
                    in_net_src = 1
                    for inner_index in range(index + 1, size):
                        if not marked[index]:
                            p_in_labels = set(arc.source.label for arc in plcs_lst[inner_index].in_arcs)
                            p_out_labels = set(arc.target.label for arc in plcs_lst[inner_index].out_arcs)
                            if in_labels == p_in_labels and out_labels == p_out_labels:
                                in_net_src += 1
                                marked[inner_index] = True
                    marked[index] = True
                    in_int_src = 0
                    for place in interface.net.places:
                        p_in_labels = set(arc.source.label for arc in place.in_arcs)
                        p_out_labels = set(arc.target.label for arc in place.out_arcs)
                        if in_labels == p_in_labels and out_labels == p_out_labels:
                            in_int_src += 1
                    if mode > 0 and int_plcs_count < net_plcs_count and in_int_src < in_net_src:
                        original, converted = apply_fpp_rule(m_net, plcs_lst[index])
                        net_plcs_count -= 1
                    elif mode < 0 and int_plcs_count > net_plcs_count and in_int_src > in_net_src:
                        original, converted = apply_ipp_rule(m_net, plcs_lst[index])
                        net_plcs_count += 1
                    if original is not None:
                        break
        if original is not None and os.path.exists(dir_path):
            visualizeNet(original, dir_path + str(counter) + "-1.png")
            visualizeNet(converted, dir_path + str(counter) + "-2.png")
            counter += 1
        else:
            need_to_continue = False
    if compareNets(interface, m_net) == 0:
        visualizeNet(m_net, dir_path + "converted.png")
        return PNetsStatus.FINE
    else:
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
        return PNetsStatus.NON_CONV


def start(first_path, second_path) -> None:
    first_status, interface = parseNet(first_path)
    second_status, net = parseNet(second_path)
    if first_status == PNetStatus.ERROR or second_status == PNetStatus.ERROR:
        raise NetNotParsableError("PN Validation: One model or both models couldn't be imported.")
    elif first_status == PNetStatus.NOT_WFN or second_status == PNetStatus.NOT_WFN:
        print("PN Validation: One model or both imported models were not WorkFlow Nets -\n"
              "Petri Nets with a singular place for input and a singular place for output.")
        return
    if not os.path.exists(OUTPUT_PATH):
        os.mkdir(OUTPUT_PATH)
    dir_path = OUTPUT_PATH + os.sep + getDirNameFromNets(first_path, second_path) + os.sep
    final_status = validateModels(interface, net, dir_path, True)
    if final_status == PNetsStatus.ISOM:
        print("PN Validation: Models are isomorphic.")
    elif final_status == PNetsStatus.NON_CONV:
        print("PN Validation: A model cannot be converted to the specified interface.")
    else:
        print("PN Validation: Conversion completed successfully.")
