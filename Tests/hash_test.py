from validator.validation import *
from validator.utils import *
from validator.abstraction.transformations import *
import sys

if __name__ == "__main__":
    first_status, interface = parseNet(sys.argv[1])
    second_status, net = parseNet(sys.argv[2])
    print(True if compareNets(interface, net) == 0 else False)
