from project.exceptions import *
from project.utils import *
from pm4py.objects.petri_net.obj import *
import shutil
import os


def checkIsom(first_net: PetriNet, second_net: PetriNet) -> bool:
    return False


def validateModels(interface: PetriNet, net: PetriNet, dir_path: str) -> PNetsStatus:
    if checkIsom(interface, net):
        return PNetsStatus.ISOM
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    os.mkdir(dir_path)
    visualizeNet(interface, dir_path + "interface.png")
    visualizeNet(net, dir_path + "net.png")
    return PNetsStatus.FINE


def start(first_path, second_path) -> None:
    first_status, interface = parseNet(first_path)
    second_status, net = parseNet(second_path)
    if first_status == PNetStatus.WRONG or second_status == PNetStatus.WRONG:
        raise NetNotParsableError("PN Validation: One model or both models couldn't be imported.")
    if not os.path.exists(OUTPUT_PATH):
        os.mkdir(OUTPUT_PATH)
    dir_path = OUTPUT_PATH + os.sep + getDirNameFromNets(first_path, second_path) + os.sep
    final_status = validateModels(interface, net, dir_path)
    if final_status == PNetsStatus.ISOM:
        print("PN Validation: Models are isomorphic.")
    elif final_status == PNetsStatus.NON_CONV:
        print("PN Validation: A model cannot be converted to the specified interface.")
    else:
        print("PN Validation: Conversion completed successfully.")
