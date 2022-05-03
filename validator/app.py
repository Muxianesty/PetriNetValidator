from validator.exceptions import NetNotParsableError
from validator.utils import *
from validator.refinement import *
from validator.abstraction import *
import shutil
import os


def checkIsom(first_net: PetriNet, second_net: PetriNet) -> bool:
    if len(first_net.places) != len(second_net.places) or len(first_net.arcs) != len(second_net.arcs) or len(
            first_net.transitions) != len(second_net.transitions):
        return False
    return True if isomHash(first_net) == isomHash(second_net) else False


def validateModels(interface: PetriNet, net: PetriNet, dir_path: str, wfn_checked: bool = False) -> PNetsStatus:
    if not wfn_checked:
        if not wfn_alg.apply(interface) or not wfn_alg.apply(net):
            return PNetsStatus.NOT_WFN
    if checkIsom(interface, net):
        return PNetsStatus.ISOM
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    os.mkdir(dir_path)
    visualizeNet(interface, dir_path + "interface.png")
    visualizeNet(net, dir_path + "net.png")
    counter = int(1)
    return PNetsStatus.FINE if checkIsom(interface, net) else PNetsStatus.NON_CONV


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
