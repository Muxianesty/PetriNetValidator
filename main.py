import sys
from validator.validation import start

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("PN Validation: There must be at least two input arguments (paths to .pnml-files).")
    start(sys.argv[1], sys.argv[2])
