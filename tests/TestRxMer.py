#! /usr/bin/python3

import json
import matplotlib.pyplot as plt
from package.rx_mer_class import RX_MER
from package.pnmHeader_class import *

RX_MER_PATH_FILE = "/home/dev01/Projects/OpenPNM/data/rxmer"

if __name__ == "__main__":
    # Initialize PnmHeader
    pnm_header = PnmHeader(RX_MER_PATH_FILE)

    # Create RX_MER object
    rxMerPnm = RX_MER(pnm_header)

    rxMerPnm.run()

    # Get the RxMER data
    rxmer_data = rxMerPnm.rxmer_data

    # Extract RxMER values
    values = [value.getRxMER() for value in rxmer_data.values]

    # Plot the RxMER values
    plt.semilogy(values)

    # Set plot labels and title
    plt.xlabel('Index')
    plt.ylabel('RxMER (dB)')
    plt.title('RxMER Data')

    # Display the plot
    plt.show()
