class Binary:
    def __init__(self, binary_data):
        """
        Initialize a BinaryToHexConverter object.

        Args:
            binary_data (bytes or bytearray): Binary data to be converted to hexadecimal.
        """
        self.binary_data = binary_data

    def to_hex(self):
        """
        Convert the binary data to hexadecimal.

        Returns:
            str: Hexadecimal representation of the binary data.
        """
        hex_data = self._bytes_to_hex(self.binary_data)
        return hex_data

    @staticmethod
    def _bytes_to_hex(binary_data):
        """
        Convert bytes or bytearray to hexadecimal representation.

        Args:
            binary_data (bytes or bytearray): Binary data to be converted.

        Returns:
            str: Hexadecimal representation of the binary data.
        """
        hex_data = "".join(f"{byte:02x}" for byte in binary_data)
        return hex_data
