# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2,
# as published by the Free Software Foundation.
#
# Project: OpenPNM
# Author: Maurice M. Garcia
# Contact: mgarcia01752@outlook.com
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301, USA.

from package.constants import *
from package.log import *
from package.pnmHeader_class import PnmHeader


class RX_MER:
    def __init__(self, pnm_header: PnmHeader):
        """
        Initialize the RX_MER object.

        Args:
            pnm_header (PnmHeader): Instance of the PnmHeader class.
        """
        self.pnm_header = pnm_header

    def process_data(self):
        """
        Process the data received from PNM_HEADER.

        This method can be modified to perform the desired operations on the data.

        """
        header = self.pnm_header.header
        pnm_data = header.get('PNM_DATA')
        Log.debug("Processing data from PNM_HEADER: " + str(pnm_data))
        # Perform the desired operations on the data here

    def run(self):
        """
        Run the RX_MER processing.

        This method can be modified to fit the desired workflow.

        """
        self.process_data()
