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

import struct
import json
from io import BytesIO

class PnmHeader:
    FILE_TYPE_LENGTH = 4
    MAJOR_VERSION_LENGTH = 1
    MINOR_VERSION_LENGTH = 1
    CAPTURE_TIME_LENGTH = 4
    DS_CHANNEL_ID_LENGTH = 1
    CM_MAC_ADDRESS_LENGTH = 6

    def __init__(self, file_path=None, binary_data=None):
        """
        Initialize a PnmHeader object.

        Args:
            file_path (str): Path to the binary file containing the headers.
            binary_data (bytes): Binary data containing the headers.

        Raises:
            ValueError: If neither file_path nor binary_data is provided.
        """
        if file_path is not None:
            self.file_path = file_path
            self.binary_data = None
        elif binary_data is not None:
            self.file_path = None
            self.binary_data = binary_data
        else:
            raise ValueError("Either file_path or binary_data must be provided.")

    def read_headers(self):
        """
        Read and return the headers from the binary file.

        Returns:
            list: A list of dictionaries representing the headers.
        """
        headers = []
        with self._open_file() as file:
            while True:
                header = self._read_header(file)
                if not header:
                    break
                headers.append(header)
        return headers

    def _open_file(self):
        """
        Open the binary file for reading.

        Returns:
            file object: A file object opened in binary mode.
        """
        if self.file_path is not None:
            return open(self.file_path, 'rb')
        else:
            return BytesIO(self.binary_data)

    def _read_header(self, file):
        """
        Read and parse a single header from the binary file.

        Args:
            file (file object): A file object opened in binary mode.

        Returns:
            dict: A dictionary representing a single header.
        """
        header = {}
        # Read each field using struct.unpack
        file_type = file.read(self.FILE_TYPE_LENGTH)
        if not file_type:
            return None
        header['File Type'] = struct.unpack(f'{self.FILE_TYPE_LENGTH}s', file_type)[0]

        major_version = file.read(self.MAJOR_VERSION_LENGTH)
        header['Major Version'] = struct.unpack('B', major_version)[0]

        minor_version = file.read(self.MINOR_VERSION_LENGTH)
        header['Minor Version'] = struct.unpack('B', minor_version)[0]

        capture_time = file.read(self.CAPTURE_TIME_LENGTH)
        header['Capture Time'] = struct.unpack('I', capture_time)[0]

        ds_channel_id = file.read(self.DS_CHANNEL_ID_LENGTH)
        header['DS Channel Id'] = struct.unpack('B', ds_channel_id)[0]

        cm_mac_address = file.read(self.CM_MAC_ADDRESS_LENGTH)
        header['CM MAC Address'] = ':'.join(f'{byte:02X}' for byte in cm_mac_address)

        return header

    def write_headers_to_json(self, output_file):
        """
        Read the headers from the binary file and write them to a JSON file.

        Args:
            output_file (str): Path to the output JSON file.
        """
        headers = self.read_headers()
        with open(output_file, 'w') as file:
            json.dump(headers, file, indent=4)

    def get_headers_as_json_string(self):
        """
        Read the headers from the binary file and return them as a JSON string.

        Returns:
            str: JSON string representing the headers.
        """
        headers = self.read_headers()
        return json.dumps(headers, indent=4)

    def get_remaining_data_stream(self):
        """
        Get the remaining binary data as a stream.

        Returns:
            BytesIO: A BytesIO object containing the remaining binary data.
        """
        with self._open_file() as file:
            # Skip the header fields
            file.seek(self.total_header_length())
            # Create a BytesIO object and copy the remaining binary data into it
            remaining_data = BytesIO()
            remaining_data.write(file.read())
            remaining_data.seek(0)
            return remaining_data

    def total_header_length(self):
        """
        Calculate the total length of the header fields.

        Returns:
            int: The total length of the header fields.
        """
        return (
            self.FILE_TYPE_LENGTH +
            self.MAJOR_VERSION_LENGTH +
            self.MINOR_VERSION_LENGTH +
            self.CAPTURE_TIME_LENGTH +
            self.DS_CHANNEL_ID_LENGTH +
            self.CM_MAC_ADDRESS_LENGTH
        )

