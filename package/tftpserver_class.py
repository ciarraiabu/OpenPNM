import socket
import struct

# TFTP opcode constants
OPCODE_RRQ = 1
OPCODE_WRQ = 2
OPCODE_DATA = 3
OPCODE_ACK = 4
OPCODE_ERROR = 5

# TFTP error codes
ERROR_FILE_NOT_FOUND = 1
ERROR_ACCESS_VIOLATION = 2
ERROR_DISK_FULL = 3
ERROR_ILLEGAL_OPERATION = 4
ERROR_UNKNOWN_TID = 5
ERROR_FILE_EXISTS = 6
ERROR_UNKNOWN_USER = 7

# Maximum packet size
MAX_PACKET_SIZE = 516

# TFTP server class
class TFTPServer:
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = None

    def start(self):
        # Create a UDP socket
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Bind the socket to the specified host and port
        self.socket.bind((self.host, self.port))
        print(f"TFTP server started on {self.host}:{self.port}")

        # Main server loop
        while True:
            data, client_address = self.socket.recvfrom(MAX_PACKET_SIZE)

            opcode = struct.unpack('!H', data[:2])[0]

            if opcode == OPCODE_RRQ:
                self.handle_read_request(data, client_address)
            elif opcode == OPCODE_WRQ:
                self.handle_write_request(data, client_address)
            else:
                self.send_error_response(client_address, ERROR_ILLEGAL_OPERATION, "Invalid opcode")

    def handle_read_request(self, data, client_address):
        # Extract the filename from the RRQ packet
        filename = data[2:data.index(b'\x00', 2)].decode('ascii')

        # Check if the file exists
        try:
            with open(filename, 'rb') as file:
                # Send the file contents in blocks of 512 bytes
                block_number = 1
                while True:
                    file_data = file.read(512)
                    if not file_data:
                        break

                    packet = struct.pack('!H', OPCODE_DATA) + struct.pack('!H', block_number) + file_data
                    self.socket.sendto(packet, client_address)

                    # Wait for ACK from the client
                    ack_packet, _ = self.socket.recvfrom(MAX_PACKET_SIZE)
                    ack_opcode = struct.unpack('!H', ack_packet[:2])[0]
                    ack_block_number = struct.unpack('!H', ack_packet[2:4])[0]

                    if ack_opcode != OPCODE_ACK or ack_block_number != block_number:
                        break

                    block_number += 1
        except FileNotFoundError:
            self.send_error_response(client_address, ERROR_FILE_NOT_FOUND, "File not found")
        except PermissionError:
            self.send_error_response(client_address, ERROR_ACCESS_VIOLATION, "Access violation")
        except Exception as e:
            self.send_error_response(client_address, ERROR_UNKNOWN_TID, str(e))

    def handle_write_request(self, data, client_address):
        # Extract the filename from the WRQ packet
        filename = data[2:data.index(b'\x00', 2)].decode('ascii')

        try:
            with open(filename, 'wb') as file:
                block_number = 0

                while True:
                    block_number += 1

                    # Wait for DATA packet from the client
                    data_packet, _ = self.socket.recvfrom(MAX_PACKET_SIZE)
                    data_opcode = struct.unpack('!H', data_packet[:2])[0]
                    data_block_number = struct.unpack('!H', data_packet[2:4])[0]
                    data_payload = data_packet[4:]

                    if data_opcode != OPCODE_DATA or data_block_number != block_number:
                        break

                    file.write(data_payload)

                    # Send ACK packet to the client
                    ack_packet = struct.pack('!H', OPCODE_ACK) + struct.pack('!H', block_number)
                    self.socket.sendto(ack_packet, client_address)

                    if len(data_payload) < 512:
                        break

        except PermissionError:
            self.send_error_response(client_address, ERROR_ACCESS_VIOLATION, "Access violation")
        except Exception as e:
            self.send_error_response(client_address, ERROR_UNKNOWN_TID, str(e))

    def send_error_response(self, client_address, error_code, error_message):
        error_packet = struct.pack('!H', OPCODE_ERROR) + struct.pack('!H', error_code) + error_message.encode('ascii') + b'\x00'
        self.socket.sendto(error_packet, client_address)


# Start the TFTP server
server = TFTPServer('0.0.0.0', 69)
server.start()
