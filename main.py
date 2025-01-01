import os

for a, b in os.environ.items():
    print(str(a).ljust(30), "=", b)
