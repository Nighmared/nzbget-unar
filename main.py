import os
import sys

POSTPROCESS_SUCCESS = 93

for a, b in os.environ.items():
    print(str(a).ljust(30), "=", b)


sys.exit(POSTPROCESS_SUCCESS)
