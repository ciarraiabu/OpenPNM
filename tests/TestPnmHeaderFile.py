#! /usr/bin/python3

from package.constants import *
from package.log import *
from package.pnmHeader_class import *

RX_MER_PATH_FILE = "/home/dev01/Projects/OpenPNM/data/rxmer"

rxmerPnm = PnmHeader(file_path=RX_MER_PATH_FILE)

pnm_data_length = rxmerPnm.get_pnm_data_length()
if pnm_data_length is not None:
    print("PNM_DATA_LENGTH:", pnm_data_length)
else:
    print("Unable to retrieve PNM_DATA length.")
