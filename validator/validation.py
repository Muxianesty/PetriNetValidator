from validator.exceptions import NetNotParsableError
from validator.utils import *
from validator.refinement import *
from validator.abstraction import *
import shutil
import os


def checkIsom(first_net: MarkedPetriNet, second_net: MarkedPetriNet) -> bool:
    if len(first_net.net.places) != len(second_net.net.places) or \
            len(first_net.net.arcs) != len(second_net.net.arcs) or \
            len(first_net.net.transitions) != len(second_net.net.transitions):
        return False
    return True if isomHash(first_net) == isomHash(second_net) else False


def validateModels(interface: MarkedPetriNet, net: MarkedPetriNet,
                   dir_path: str, wfn_checked: bool = False) -> PNetsStatus:
    if not dir_path.endswith(os.sep):
        dir_path += os.sep
    if not wfn_checked:
        if not wfn_alg.apply(interface.net) or not wfn_alg.apply(net.net):
            return PNetsStatus.NOT_WFN
    if checkIsom(interface, net):
        return PNetsStatus.ISOM
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    os.mkdir(dir_path)
    int_dict: dict = labelDictionary(interface)
    int_plcs_count = len(interface.net.places)
    net_dict: dict = labelDictionary(net)
    net_plcs_count = len(net.net.places)
    if len(int_dict.keys()) != len(net_dict.keys()):
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
        return PNetsStatus.NON_CONV
    visualizeNet(interface, dir_path + "interface.png")
    visualizeNet(net, dir_path + "net.png")
    counter = int(1)
    while True:
        need_to_continue: bool = False
        for net_key in net_dict.keys():
            original, converted = None, None
            if original is not None and converted is not None:
                visualizeNet(original, dir_path + str(counter) + "-1.png")
                visualizeNet(converted, dir_path + str(counter) + "-2.png")
                counter += 1
                need_to_continue = True
                break
        if not need_to_continue:
            for place in net.places:
                print()
        if not need_to_continue:
            break
    if checkIsom(interface, net):
        visualizeNet(net, dir_path + "converted.png")
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
