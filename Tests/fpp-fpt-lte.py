from validator.validation import *
from validator.utils import *
from validator.refinement.transformations import *
from validator.abstraction.transformations import *
import sys

if __name__ == "__main__":
    first_status, interface = parseNet(sys.argv[1])
    second_status, net = parseNet(sys.argv[2])
    dir_path = OUTPUT_PATH + os.sep + getDirNameFromNets(sys.argv[1], sys.argv[2]) + os.sep
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path)
    os.mkdir(dir_path)
    target_p = [place for place in interface.places if place.name == "p2"][0]
    convertible_p = [place for place in net.places if place.name == "p1"][0]
    target_t = [transition for transition in interface.transitions if transition.name == "t2"][0]
    convertible_t = [transition for transition in net.transitions if transition.name == "t2"][0]
    visualizeNet(interface, dir_path + "interface.png")
    visualizeNet(net, dir_path + "net.png")
    original, converted = apply_fpp_rule(target_p, net, convertible_p)
    visualizeNet(original, dir_path + "1-1.png")
    visualizeNet(converted, dir_path + "1-2.png")
    original, converted = apply_fpt_rule(target_t, net, convertible_t)
    visualizeNet(original, dir_path + "2-1.png")
    visualizeNet(converted, dir_path + "2-2.png")
    target_tpp = [place for place in interface.places if place.name == "p4"][0]
    convertible_tpp = [transition for transition in net.transitions if transition.name == "t6"][0]
    original, converted = apply_lte_rule(target_tpp, net, convertible_tpp)
    visualizeNet(original, dir_path + "3-1.png")
    visualizeNet(converted, dir_path + "3-2.png")
    visualizeNet(net, dir_path + "converted.png")
