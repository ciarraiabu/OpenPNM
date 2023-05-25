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
import io
import os
from package.log import Log

class PnmHeader:
    FILE_TYPE_LENGTH: int = 4
    MAJOR_VERSION_LENGTH: int = 1
    MINOR_VERSION_LENGTH: int = 1
    CAPTURE_TIME_LENGTH: int = 4
    DS_CHANNEL_ID_LENGTH: int = 1
    CM_MAC_ADDRESS_LENGTH: int = 6

    def __init__(self, file_path: str = None, binary_data: bytes = None) -> None:
        """
        Initialize a PnmHeader object.

        Args:
            file_path (str): Path to the binary file containing the headers.
            binary_data (bytes): Binary data containing the headers.

        Raises:
            ValueError: If neither file_path nor binary_data is provided
                        or if both file_path and binary_data are provided.
            FileNotFoundError: If the file_path does not exist.
            TypeError: If the binary_data is not of type bytes.
        """
        if bool(file_path) ^ bool(binary_data):
            if file_path:
                if not os.path.exists(file_path):
                    raise FileNotFoundError("File not found: {}".format(file_path))
                self.file_path = file_path
                self.binary_data = None
            else:  # binary_data
                if not isinstance(binary_data, bytes):
                    raise TypeError("Binary data must be of type bytes.")
                self.file_path = None
                self.binary_data = binary_data
        else:
            raise ValueError("Either file_path or binary_data must be provided, but not both.")

    def read_headers(self) -> list:
        """
        Read and return the headers from the binary file.

        Returns:
            list: A list of dictionaries representing the headers.
        """
        headers = []
        with self._open_file() as file:
            header, pnm_data = self._read_header(file)
            if header is not None and pnm_data is not None:
                header['PNM_DATA'] = pnm_data
                headers.append(header)
        return headers

    def _open_file(self) -> io.FileIO:
        """
        Open the binary file for reading.

        Returns:
            file object: A file object opened in binary mode.
        """
        try:
            if self.file_path is not None:
                return open(self.file_path, 'rb')
            else:
                return io.BytesIO(self.binary_data)
        except FileNotFoundError:
            Log.error("File not found: %s", self.file_path)
            return None
        except IOError as e:
            Log.error("An error occurred while opening the file: %s", str(e))
            return None

    def _read_header(self, file: io.FileIO) -> tuple[dict, bytes]:
        """
        Read and parse a single header from the binary file.

        Args:
            file (file object): A file object opened in binary mode.

        Returns:
            tuple[dict, bytes]: A tuple containing a dictionary representing the header fields
                               and the remaining binary data as PNM_DATA.
        """
        header = {}

        file_type = file.read(self.FILE_TYPE_LENGTH)
        if len(file_type) < self.FILE_TYPE_LENGTH:
            Log.error("Incomplete file type")
            return None, None
        header['File Type'] = struct.unpack(f'{self.FILE_TYPE_LENGTH}s', file_type)[0]

        major_version = self._read_field(file, self.MAJOR_VERSION_LENGTH, 'B', "Major Version")
        minor_version = self._read_field(file, self.MINOR_VERSION_LENGTH, 'B', "Minor Version")
        capture_time = self._read_field(file, self.CAPTURE_TIME_LENGTH, 'I', "Capture Time")
        ds_channel_id = self._read_field(file, self.DS_CHANNEL_ID_LENGTH, 'B', "DS Channel Id")
        cm_mac_address = self._read_field(file, self.CM_MAC_ADDRESS_LENGTH, '6s', "CM MAC Address")
        if cm_mac_address is not None:
            cm_mac_address = ':'.join(f'{byte:02X}' for byte in cm_mac_address)

        pnm_data = file.read()

        header['Major Version'] = major_version
        header['Minor Version'] = minor_version
        header['Capture Time'] = capture_time
        header['DS Channel Id'] = ds_channel_id
        header['CM MAC Address'] = cm_mac_address

        Log.debug("PNM_HEADER: " + header.__str__())

        return header, pnm_data

    def _read_field(self, file: io.FileIO, length: int, format_str: str, field_name: str) -> any:
        """
        Read a field from the binary file using struct.unpack and advance the file position.

        Args:
            file (file object): A file object opened in binary mode.
            length (int): Length of the field to read.
            format_str (str): Format string for struct.unpack.
            field_name (str): Name of the field.

        Returns:
            any: The unpacked value of the field.
        """
        field_data = file.read(length)
        if len(field_data) < length:
            Log.error("Incomplete %s", field_name)
            return None
        return struct.unpack(format_str, field_data)[0]

    def write_headers_to_json(self, output_file: str) -> None:
        """
        Read the headers from the binary file and write them to a JSON file.

        Args:
            output_file (str): Path to the output JSON file.
        """
        headers = self.read_headers()
        with open(output_file, 'w') as file:
            json.dump(headers, file, indent=4)

    def get_headers_as_json_string(self) -> str:
        """
        Read the headers from the binary file and return them as a JSON string.

        Returns:
            str: JSON string representing the headers.
        """
        headers = self.read_headers()
        return json.dumps(headers, indent=4)

    def get_remaining_data_stream(self) -> io.BytesIO:
        """
        Get the remaining binary data as a stream.

        Returns:
            io.BytesIO: A BytesIO object containing the remaining binary data.
        """
        with self._open_file() as file:
            file.seek(self.total_header_length())
            remaining_data = io.BytesIO()
            remaining_data.write(file.read())
            remaining_data.seek(0)
            return remaining_data

    def total_header_length(self) -> int:
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
