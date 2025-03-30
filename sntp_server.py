import socket, time

time_since_1900 = 2208988800


def sntp_pocket(time_delay: int) -> bytearray:
    correction_indicator_plus_version_plus_mode = b"\x24"
    strata = b"\0"
    interval = b"\0"
    accuracy = b"\xFA"
    delay = b"\0" * 4
    dispersion = b"\0" * 4
    indicator = b"\0" * 4
    refresh_time = b"\0" * 8
    initial_time = b"\0" * 8
    reception_time = b"\0" * 8
    current_time = time.time() - time_delay
    first_part_sending_time = int(current_time) + time_since_1900
    second_part_sending_time = int((current_time - first_part_sending_time) * (2 ** 32))

    sntp = bytearray(48)
    sntp[0:4] = correction_indicator_plus_version_plus_mode + strata + interval + accuracy
    sntp[4:8] = delay
    sntp[8:12] = dispersion
    sntp[12:16] = indicator
    sntp[16:24] = refresh_time
    sntp[24:32] = initial_time
    sntp[32:40] = reception_time
    sntp[40:44] = int_in_bytes(first_part_sending_time)
    sntp[44:48] = int_in_bytes(second_part_sending_time)

    return sntp


def int_in_bytes(value: int) -> list:
    iterations = 0
    temp_list = [0 for _ in range(32)]
    byte_list = [0 for _ in range(4)]
    while value > 0:
        temp_list[iterations] = value % 2
        value = value // 2
        iterations += 1

    first_byte = ""
    second_byte = ""
    third_byte = ""
    fourth_byte = ""
    for i in range(8):
        first_byte += str(temp_list[7 - i])
        second_byte += str(temp_list[15 - i])
        third_byte += str(temp_list[23 - i])
        fourth_byte += str(temp_list[31 - i])
    byte_list[3] = int(first_byte, 2)
    byte_list[2] = int(second_byte, 2)
    byte_list[1] = int(third_byte, 2)
    byte_list[0] = int(fourth_byte, 2)

    return byte_list


def echo_server(host='127.0.0.1', port=123):
    with open("config.txt", "r") as config:
        delay = int(config.readline())
    print(delay)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
        server_socket.bind((host, port))

        print(f"Эхо-сервер запущен на {host}:{port}")

        while True:
            print("______________________________________")
            data, client_address = server_socket.recvfrom(1024)
            print(f"Запрос от {client_address}")
            print(f"Данные {data}")
            server_socket.sendto(sntp_pocket(delay), client_address)


if __name__ == "__main__":
    echo_server()
