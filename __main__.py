# import the pyserial module
import socket
import sys
from time import sleep

from ncd_io.proxr import RelayController

# Table commands Working Documentation:
# | TABLE | BANK | PORT | ON STX  | ON HEX 1 | ON HEX 2 | ON BIN 1 | ON BIN 2 | ON DEC 1 | ON DEC 2 | OFF STX | OFF HEX 1 | OFF HEX 2 | OFF BIN 1 | OFF BIN 2 | OFF DEC 1 | OFF DEC 2 |
# |-------|------|------|---------|----------|----------|----------|----------|----------|----------|---------|-----------|-----------|-----------|-----------|-----------|-----------|
# | N/A   |    1 |    1 | FE      | 6C       |       01 | 01101100 | 00000001 |      108 |        1 | FE      | 64        |        01 |  01100100 |  00000001 |       100 |         1 |
# | N/A   |    1 |    2 | FE      | 6D       |       01 | 01101101 | 00000001 |      109 |        1 | FE      | 65        |        01 |  01100101 |  00000001 |       101 |         1 |
# | N/A   |    1 |    3 | FE      | 6E       |       01 | 01101110 | 00000001 |      110 |        1 | FE      | 66        |        01 |  01100110 |  00000001 |       102 |         1 |
# | 1     |    1 |    4 | FE      | 6F       |       01 | 01101111 | 00000001 |      111 |        1 | FE      | 67        |        01 |  01100111 |  00000001 |       103 |         1 |
# | 2     |    1 |    5 | FE      | 70       |       01 | 01110000 | 00000001 |      112 |        1 | FE      | 68        |        01 |  01101000 |  00000001 |       104 |         1 |
# | 3     |    1 |    6 | FE      | 71       |       01 | 01110001 | 00000001 |      113 |        1 | FE      | 69        |        01 |  01101001 |  00000001 |       105 |         1 |
# | 4     |    1 |    7 | FE      | 72       |       01 | 01110010 | 00000001 |      114 |        1 | FE      | 6A        |        01 |  01101010 |  00000001 |       106 |         1 |
# | 5     |    1 |    8 | FE      | 73       |       01 | 01110011 | 00000001 |      115 |        1 | FE      | 6B        |        01 |  01101011 |  00000001 |       107 |         1 |
# | 7     |    2 |    1 | FE      | 6C       |       02 | 01101100 | 00000010 |      108 |        2 | FE      | 64        |        02 |  01100100 |  00000010 |       100 |         2 |
# | 9     |    2 |    2 | FE      | 6D       |       02 | 01101101 | 00000010 |      109 |        2 | FE      | 65        |        02 |  01100101 |  00000010 |       101 |         2 |
# | 11    |    2 |    3 | FE      | 6E       |       02 | 01101110 | 00000010 |      110 |        2 | FE      | 66        |        02 |  01100110 |  00000010 |       102 |         2 |
# | 6     |    2 |    4 | FE      | 6F       |       02 | 01101111 | 00000010 |      111 |        2 | FE      | 67        |        02 |  01100111 |  00000010 |       103 |         2 |
# | 8     |    2 |    5 | FE      | 70       |       02 | 01110000 | 00000010 |      112 |        2 | FE      | 68        |        02 |  01101000 |  00000010 |       104 |         2 |
# | 10    |    2 |    6 | FE      | 71       |       02 | 01110001 | 00000010 |      113 |        2 | FE      | 69        |        02 |  01101001 |  00000010 |       105 |         2 |
# | N/A   |    2 |    7 | FE      | 72       |       02 | 01110010 | 00000010 |      114 |        2 | FE      | 6A        |        02 |  01101010 |  00000010 |       106 |         2 |
# | N/A   |    2 |    8 | FE      | 73       |       02 | 01110011 | 00000010 |      115 |        2 | FE      | 6B        |        02 |  01101011 |  00000010 |       107 |         2 |

table_pattern = [
    (0x00, 0x00),
    (0x04, 0x01),
    (0x05, 0x01),
    (0x06, 0x01),
    (0x07, 0x01),
    (0x08, 0x01),
    (0x04, 0x02),
    (0x01, 0x02),
    (0x05, 0x02),
    (0x02, 0x02),
    (0x06, 0x02),
    (0x03, 0x02),
]


# set up your socket with the desired settings.
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# instantiate the board object and pass it the network socket

with RelayController(com=sock) as board1:
    if sys.argv[1]:
        print(bin(int.from_bytes(board1.send_command(b"\xfe\x7c\x01", 1))))
        for table in sys.argv:
            if table == ".":
                continue
            port, bank = table_pattern[int(table)]
            if board1.turn_on_bank_relay(bank=bank, port=port):
                print(f"Relay {table} Enabled")
            else:
                print(f"Failed to Enable Relay {table}")
            sleep(10)
            if board1.turn_off_bank_relay(bank=bank, port=port):
                print(f"Relay {table} Disabled")
            else:
                print(f"Failed to Disable Relay {table}")
    else:
        print("Dancing through all relays!")
        for port, bank in table_pattern:
            if board1.turn_on_bank_relay(bank=bank, port=port):
                print(f"Relay {port} on Bank {bank} Enabled")
            else:
                print(f"Failed to Enable Relay {port} on Bank {bank}")
            sleep(1)
            if board1.turn_off_bank_relay(bank=bank, port=port):
                print(f"Relay {port} on Bank {bank} Disabled")
            else:
                print(f"Failed to Disable Relay {port} on Bank {bank}")
