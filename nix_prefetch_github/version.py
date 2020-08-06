import os.path

HERE = os.path.dirname(__file__)
with open(os.path.join(HERE, "VERSION")) as f:
    VERSION_STRING = f.read()
