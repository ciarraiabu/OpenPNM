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
import base64
from typing import Optional, Union, List, Dict
from package.log import Log


class PnmHeader:
    PNM_FILE_TYPE_LENGTH: int = 4
    MAJOR_VERSION_LENGTH: int = 1
    MINOR_VERSION_LENGTH: int = 1
    CAPTURE_TIME_LENGTH: int = 4
    DS_CHANNEL_ID_LENGTH: int = 1
    CM_MAC_ADDRESS_LENGTH: int = 6
    PNM_FILE_TYPE_KEY: str = 'File Type'
    MAJOR_VERSION_KEY: str = 'Major Version'
    MINOR_VERSION_KEY: str = 'Minor Version'
    CAPTURE_TIME_KEY: str = 'Capture Time'
    DS_CHANNEL_ID_KEY: str = 'DS Channel Id'
    CM_MAC_ADDRESS_KEY: str = 'CM MAC Address'

    def __init__(self, file_path: Optional[str] = None, binary_data: Optional[bytes] = None):
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
        if bool(file_path) ^ bool(binary_data):  # Ensure only one of them is provided
            if file_path:
                if not os.path.exists(file_path):
                    raise FileNotFoundError("File not found: {}".format(file_path))
                self.file_path: str = file_path
                self.binary_data: Optional[bytes] = None
            else:  # binary_data
                if not isinstance(binary_data, bytes):
                    raise TypeError("Binary data must be of type bytes.")
                self.file_path: Optional[str] = None
                self.binary_data: bytes = binary_data
        else:
            raise ValueError("Either file_path or binary_data must be provided, but not both.")
        
        self.header_read = False

        self._read_headers()

    def _open_file(self) -> Optional[io.BufferedReader]:
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

    def _read_header(self, file: io.BufferedReader) -> \
            Union[Dict[str, Union[str, int]], None, bytes]:
        """
        Read and parse a single header from the binary file.

        Args:
            file (file object): A file object opened in binary mode.

        Returns:
            dict: A dictionary representing the header fields.
            bytes: The remaining binary data as PNM_DATA.
        """
        header: Dict[str, Union[str, int]] = {}

        # Read each field using struct.unpack and advance the file position
        file_type = file.read(self.PNM_FILE_TYPE_LENGTH)
        if len(file_type) < self.PNM_FILE_TYPE_LENGTH:
            Log.error("Incomplete file type")
            return None, None
        header[self.PNM_FILE_TYPE_KEY] = struct.unpack(f'{self.PNM_FILE_TYPE_LENGTH}s', file_type)[0]

        major_version = file.read(self.MAJOR_VERSION_LENGTH)
        if len(major_version) < self.MAJOR_VERSION_LENGTH:
            Log.error("Incomplete major version")
            return None, None
        header[self.MAJOR_VERSION_KEY] = struct.unpack('B', major_version)[0]

        minor_version = file.read(self.MINOR_VERSION_LENGTH)
        if len(minor_version) < self.MINOR_VERSION_LENGTH:
            Log.error("Incomplete minor version")
            return None, None
        header[self.MINOR_VERSION_KEY] = struct.unpack('B', minor_version)[0]

        capture_time = file.read(self.CAPTURE_TIME_LENGTH)
        if len(capture_time) < self.CAPTURE_TIME_LENGTH:
            Log.error("Incomplete capture time")
            return None, None
        header[self.CAPTURE_TIME_KEY] = struct.unpack('I', capture_time)[0]

        ds_channel_id = file.read(self.DS_CHANNEL_ID_LENGTH)
        if len(ds_channel_id) < self.DS_CHANNEL_ID_LENGTH:
            Log.error("Incomplete DS channel ID")
            return None, None
        header[self.DS_CHANNEL_ID_KEY] = struct.unpack('B', ds_channel_id)[0]

        cm_mac_address = file.read(self.CM_MAC_ADDRESS_LENGTH)
        if len(cm_mac_address) < self.CM_MAC_ADDRESS_LENGTH:
            Log.warning("Incomplete CM MAC address")
            header[self.CM_MAC_ADDRESS_KEY] = None
        else:
            header[self.CM_MAC_ADDRESS_KEY] = ':'.join(f'{byte:02X}' for byte in cm_mac_address)


        # Read the remaining data as PNM_DATA
        pnm_data = file.read()

        Log.debug("PNM_HEADER: " + header.__str__())

        return header, pnm_data
    
    def _read_header_once(self):
        if self.header_read:
            return
        
        with self._open_file() as file:
            header, pnm_data = self._read_header(file)
            if header is not None and pnm_data is not None:
                header['PNM_DATA'] = pnm_data
                self.header = header
        
        self.header_read = True

    def _read_headers(self) -> List[Dict[str, Union[str, int]]]:
        """
        Read and return the headers from the binary file.

        Returns:
            list: A list of dictionaries representing the headers.
        """
        self._read_header_once()
        
        if self.header:
            return [self.header]
        
        return []

    def write_headers_to_json(self, output_file: str):
        """
        Read the headers from the binary file and write them to a JSON file.

        Args:
            output_file (str): Path to the output JSON file.
        """
        self._read_header_once()
        
        if self.header:
            with open(output_file, 'w') as file:
                json.dump([self.header], file, indent=4)

    def get_headers_as_json_string(self) -> str:
        """
        Read the headers from the binary file and return them as a JSON string.

        Returns:
            str: JSON string representing the headers.
        """
        self._read_header_once()
        
        if self.header:
            return json.dumps([self.header], indent=4)
        
        return ""

    def get_remaining_data_stream(self) -> Optional[io.BytesIO]:
        """
        Get the remaining binary data as a stream.

        Returns:
            io.BytesIO: A BytesIO object containing the remaining binary data.
        """
        self._read_header_once()
        
        if self.header:
            with self._open_file() as file:
                # Skip the header fields
                file.seek(self.total_header_length())
                # Create a BytesIO object and copy the remaining data to it
                remaining_data = io.BytesIO()
                remaining_data.write(file.read())
                remaining_data.seek(0)
                return remaining_data
        
        return None

    def total_header_length(self) -> int:
        """
        Calculate the total length of the header fields.

        Returns:
            int: Total length of the header fields.
        """
        return (
            self.PNM_FILE_TYPE_LENGTH +
            self.MAJOR_VERSION_LENGTH +
            self.MINOR_VERSION_LENGTH +
            self.CAPTURE_TIME_LENGTH +
            self.DS_CHANNEL_ID_LENGTH +
            self.CM_MAC_ADDRESS_LENGTH
        )

    def toJson(self) -> str:
        """
        Combine the header and PNM_DATA into a JSON output.

        Returns:
            str: JSON string representing the header and PNM_DATA.
        """
        self._read_header_once()
        
        if self.header:
            pnm_data = self.get_remaining_data_stream().read()
            hex_data = pnm_data.hex()
            self.header['PNM_DATA'] = hex_data
            return json.dumps([self.header], indent=4, default=self._json_serializable)
        
        return ""

    def _json_serializable(self, obj):
        """Convert non-serializable objects to a serializable format."""
        if isinstance(obj, bytes):
            return obj.decode('utf-8')
        raise TypeError(f"Object of type '{obj.__class__.__name__}' is not JSON serializable.")

    def getPnmData(self) -> Optional[io.BytesIO]:
        """
        Get the PNM_DATA as a binary stream.

        Returns:
            io.BytesIO: A BytesIO object containing the PNM_DATA.
        """
        self._read_header_once()

        if self.header:
            pnm_data = self.header.get('PNM_DATA')
            if pnm_data is not None:
                pnm_stream = io.BytesIO(pnm_data)
                pnm_stream.seek(0)
                return pnm_stream

        return None
