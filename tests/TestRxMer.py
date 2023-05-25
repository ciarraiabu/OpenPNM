#! /usr/bin/python3

from package.constants import *
from package.log import *
from package.pnmHeader_class import *

RX_MER_PATH_FILE = "/home/dev01/Projects/OpenPNM/data/rxmer"

rxmerPnm = PnmHeader(RX_MER_PATH_FILE)

rxmerPnm.read_headers()

print(rxmerPnm.toJson())
