#! /usr/bin/python3

import json
from package.rx_mer_class import RX_MER, RxMerDataValue, RxMerData
from package.pnmHeader_class import *

RX_MER_PATH_FILE = "/home/dev01/Projects/OpenPNM/data/rxmer"

if __name__ == "__main__":
    # Initialize PnmHeader
    pnm_header = PnmHeader(RX_MER_PATH_FILE)

    # Create RX_MER object
    rxMerPnm = RX_MER(pnm_header)

    rxMerPnm.run()

    # Get the RxMER data
    rxmer_data = rxMerPnm.get_rxmer_data()

    # Convert RxMER data to JSON
    rxmer_json = rxmer_data.toJson()
    print(rxmer_json)
