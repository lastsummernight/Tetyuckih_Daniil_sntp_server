import socket
import struct
import time

sntp_server = "127.0.0.1"  # "time.google.com"
ntp_port = 123
ntp_packet_size = 48
time_since_1900 = 2208988800


def get_time():
    with (socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket):
        ntp_request_packet = b'\x23' + 47 * b'\0'
        try:
            client_socket.sendto(ntp_request_packet, (sntp_server, ntp_port))
            response, _ = client_socket.recvfrom(ntp_packet_size)
            print(response)
            receive = struct.unpack('>12I', response)
            receive_seconds = receive[10]
            receive_mseconds = receive[11] / float(2 ** 32)

            timestamp = receive_seconds - time_since_1900 + receive_mseconds
            return time.ctime(timestamp)

        except Exception as e:
            print(f"Error: {e}")
            return None


if __name__ == "__main__":
    current_time = get_time()

    if current_time:
        print("Current time from SNTP server:", current_time)
