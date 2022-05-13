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
    target_p = [place for place in interface.net.places if place.name == "p2"][0]
    convertible_p = [place for place in net.net.places if place.name == "p1"][0]
    target_t = [transition for transition in interface.net.transitions if transition.name == "t2"][0]
    convertible_t = [transition for transition in net.net.transitions if transition.name == "t2"][0]
    visualizeNet(interface, dir_path + "interface.png")
    visualizeNet(net, dir_path + "net.png")
    original, converted = apply_fpp_rule(net, target_p)
    visualizeNet(original, dir_path + "1-1.png")
    visualizeNet(converted, dir_path + "1-2.png")
    original_t, converted_t = apply_fpt_rule(net, target_t)
    visualizeNet(original_t, dir_path + "2-1.png")
    visualizeNet(converted_t, dir_path + "2-2.png")
    visualizeNet(net, dir_path + "converted.png")
