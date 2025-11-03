#!/usr/bin/env python3
__version__ = "0.1.0"
__description__ = "NCD ProXR Relay Controller library. https://media.ncd.io/20170721183921/ProXR.pdf"

from socket import socket

class RelayController:
    IP_ADDRESS: str = "10.0.0.105"
    PORT: int = 2101
    COMMAND_STX: int = 0xFE
    nBANKS: int = 32

    def __init__(self, com: socket, kwargs = {}):
        self.__dict__.update(kwargs)
        self.com = com
    
    def __exit__(self, exception_type, exception_value, exception_traceback):
        self.com.close()

    def __enter__(self):
        self.com.connect((self.IP_ADDRESS, self.PORT))
        self.com.settimeout(0.5)
        self.light_controller_init()
        return self

    def light_controller_init(self) -> bool:
        # init_command = b'\xfe\x32\x8d\x02'
        # response = self.send_command(init_command, len=15)
        # if response != b'LightController':
        #     return False
        # print(response)
        # init_command_2 = b'\xfe\x32\x89\x01\xfe\x71\x02'
        # self.com.send(init_command_2)
        # response = self.com.recv(1)
        # print(response)
        # if response != b'\x55':
        #     return False
        # response = self.com.recv(1)
        # print(response)
        # if response != b'\x55':
        #     return False
        return True

    def send_command(self, command: bytes, len: int = 1) -> bytes:
        self.com.send(command)
        response = self.com.recv(len)
        return response
    
    def validate_response(self, response: bytes) -> bool:
        print(response)
        if response and response == b'\x55':
            return True
        return False

    def _command_builder(self, data: bytes) -> bytes:
        b: bytearray = bytearray()
        b.append(self.COMMAND_STX)  # STX
        b.extend(data)
        command = bytes(b)
        return command
    
    def _validate_port(self, port: int) -> bool:
        if port < 1 or port > 8:
            raise ValueError("Port must be between 1 and 8")
        return True
        
    def _validate_bank(self, bank: int) -> bool:
        if bank < 0 or bank > self.nBANKS:
            raise ValueError(f"Bank must be between 1 and {self.nBANKS}")
        return True
    
    """
    The E3C Command Set
    """

    def enable_all_devices(self) -> bool:
        """Tells all devices to respond to your commands."""
        command = self._command_builder(b'\xf8')
        response = self.send_command(command)
        return self.validate_response(response)
    
    def disable_all_devices(self) -> bool:
        """Tells all devices to ignore your commands."""
        command = self._command_builder(b'\xf9')
        response = self.send_command(command)
        return self.validate_response(response)
    
    def enable_selected_device(self) -> bool:
        """Tells a specific device to listen to your commands"""
        command = self._command_builder(b'\xfa')
        response = self.send_command(command)
        return self.validate_response(response)
    
    def disable_selected_device(self) -> bool:
        """Tells a specific device to ignore your commands"""
        command = self._command_builder(b'\xfb')
        response = self.send_command(command)
        return self.validate_response(response)
    
    def enable_selected_device_exclusive(self) -> bool:
        """Tells a specific device to listen to your commands, all other devices will ignore your commands."""
        command = self._command_builder(b'\xfc')
        response = self.send_command(command)
        return self.validate_response(response)
    
    def disable_selected_device_exclusive(self) -> bool:
        """Tells a specific device to ignore your commands, all others will listen."""
        command = self._command_builder(b'\xfd')
        response = self.send_command(command)
        return self.validate_response(response)
    
    """Extended E3C Commands"""

    def store_device_number(self) -> bool:
        """
        Stores the device number into the controller.
        The device number takes effect immediately.
        The enabled/disabled status of the device is unchanged
        """
        command = b'\xfe\xff'
        response = self.send_command(command)
        return self.validate_response(response)
    
    def recall_device_identification(self) -> bytes:
        """
        This command reports back 4 bytes of data:
        ProXR Device ID Part 1: 1
        ProXR Device ID Part 2: 0
        ProXR Firmware Version: 17 (or newer)
        ProXR Year of Firmware Production: 205 (or newer)
        ProXR E3C Device Number
        """
        command = b'\xfe\xf6'
        response = self.send_command(command, 4)
        return response
    
    def recall_device_number(self) -> bool:
        """Reads the stored device number from the controller"""
        command = self._command_builder(b'\xf7')
        response = self.send_command(command)
        return self.validate_response(response)
    
    """
    The ProXR Relay Command Set
    """

    """
    Controlling Individual Relays
    """
    
    def turn_off_relay(self, port: int) -> bool:
        """Turns off a specific relay in current bank."""
        self._validate_port(port)
        command: bytes = self._command_builder(
            bytes(port - 1) # 1 indexed port adusted to 0 indexed
        )
        response = self.send_command(command)
        return self.validate_response(response)

    def turn_off_bank_relay(self, bank: int, port: int) -> bool:
        """Turns off a specific relay in specified bank."""
        self._validate_port(port)
        self._validate_bank(bank)
        command: bytes = self._command_builder(
            bytes([port + 99, bank])
        )
        response = self.send_command(command)
        return self.validate_response(response)
    
    def turn_on_relay(self, port: int) -> bool:
        """Turns on a specific relay in current bank."""
        self._validate_port(port)
        command: bytes = self._command_builder(
            bytes(port + 7)
        )
        response = self.send_command(command)
        return self.validate_response(response)
    
    def turn_on_bank_relay(self, bank: int, port: int) -> bool:
        """Turns on a specific relay in specified bank."""
        self._validate_port(port)
        self._validate_bank(bank)
        command: bytes = self._command_builder(
            bytes([port + 107, bank])
        )
        response = self.send_command(command)
        return self.validate_response(response)
    
    """
    Reading the status of individual relays
    """

    def query_relay_status(self, port: int) -> bool:
        """Queries the status of a specific relay in current bank."""
        self._validate_port(port)
        command: bytes = self._command_builder(
            bytes(port + 15)
        )
        response = self.send_command(command)
        return self.validate_response(response)
    
    def query_bank_relay_status(self, bank: int, port: int) -> bool:
        """Queries the status of a specific relay in specified bank."""
        self._validate_port(port)
        self._validate_bank(bank)
        command: bytes = self._command_builder(
            bytes([port + 115, bank])
        )
        response = self.send_command(command)
        return self.validate_response(response)
    
    """
    Reading the status of relay banks
    """

    def query_status_all(self) -> bytes:
        """Queries the status of all relays in current bank."""
        command: bytes = self._command_builder(
            bytes([24])
        )
        response = self.send_command(command, 1)
        return response
    
    def query_bank_status(self, bank: int) -> bytes:
        """
        Queries the status of all relays in specified bank.
        This command allows you to read the status of a single bank of relays.
        A value of 0-255 is returned indicating the status of all 8 relays. The
        binary pattern of the value returned directly corresponds to the on/off
        status of each of the 8 relays in the selected relay bank. If the cur-
        rently selected relay bank is 0, or if you specify relay bank 0, then the
        status of all 32 relay banks will be sent. In this condition, your program
        should be written to read 32 bytes of data from the serial port.
        """
        self._validate_bank(bank)
        command: bytes = self._command_builder(
            bytes([124, bank])
        )
        response = self.send_command(command, 1)
        return response
    
    """
    Reporting Mode
    """

    def enable_reporting_mode(self) -> bool:
        """Enables reporting mode."""
        command = self._command_builder(bytes(27))
        response = self.send_command(command)
        return self.validate_response(response)
    
    def disable_reporting_mode(self) -> bool:
        """
        Disables reporting mode.
        This command sets and stores (in non-volatile EEPROM while in con-
        figuration mode only) the reporting mode status. Reporting mode, by
        default, is ON, meaning every time a command is sent to the controller,
        the controller will send an 85 back to the computer, indicating that the
        command has finished executing your instructions. We recommend
        leaving it on, but doing so requires 2-Way communication with the con-
        troller. You should turn it off if you intend to use 1-Way communication
        only. A delay between some commands may be required when using
        1-Way communications. For optimum reliability, leave reporting mode
        on and use 2-Way communications with the ProXR Series controllers.
        NOTE: Reporting Mode may be turned on or off at any time. The
        default power-up status of reporting mode is ONLY stored when
        the device is in configuration mode (all dip switches off when the
        controller is powered up).
        """
        command = self._command_builder(bytes(28))
        response = self.send_command(command)
        return self.validate_response(response)
    
    """
    All relays on/off
    """

    def enable_all_relays(self) -> bool:
        """Enables all relays."""
        command = self._command_builder(bytes(29))
        response = self.send_command(command)
        return self.validate_response(response)
    
    def enable_bank_relays(self, bank: int) -> bool:
        """Enables all relays in specified bank."""
        self._validate_bank(bank)
        command = self._command_builder(bytes([129, bank]))
        response = self.send_command(command)
        return self.validate_response(response)
    
    def disable_all_relays(self) -> bool:
        """Disables all relays."""
        command = self._command_builder(bytes(30))
        response = self.send_command(command)
        return self.validate_response(response)
    
    def disable_bank_relays(self, bank: int) -> bool:
        """Disables all relays in specified bank."""
        self._validate_bank(bank)
        command = self._command_builder(bytes([130, bank]))
        response = self.send_command(command)
        return self.validate_response(response)
    
    """
    Inverting Relays
    """

    def toggle_all_relays(self) -> bool:
        """Toggles all relays."""
        command = self._command_builder(bytes(31))
        response = self.send_command(command)
        return self.validate_response(response)

    def toggle_bank_relays(self, bank: int) -> bool:
        """Toggles all relays in specified bank."""
        self._validate_bank(bank)
        command = self._command_builder(bytes([131, bank]))
        response = self.send_command(command)
        return self.validate_response(response)
    
    """
    Reversing Relays
    """

    def reverse_all_relays(self) -> bool:
        """
        Reverses all relays.
        reverses bit order of all relay banks.
        """
        command = self._command_builder(bytes(32))
        response = self.send_command(command)
        return self.validate_response(response)
    
    def reverse_bank_relays(self, bank: int) -> bool:
        """Reverses all relays in specified bank."""
        self._validate_bank(bank)
        command = self._command_builder(bytes([132, bank]))
        response = self.send_command(command)
        return self.validate_response(response)
    
    """
    Test 2-way communications
    """

    def test_comms(self) -> bool:
        """
        Tests communication with the relay controller.
        his command is used to test 2-Way communications between the PC
        and the relay controller. This command does nothing except report
        back an ASCII character code 85 when executed.
        """
        command = self._command_builder(bytes(33))
        response = self.send_command(command, len=1)
        return self.validate_response(response)
    
    """
    Reading the currently selected relay bank
    """

    def query_selected_bank(self) -> int:
        """Queries the currently selected bank."""
        command = self._command_builder(bytes(34))
        response = self.send_command(command, len=1)
        if response:
            return int.from_bytes(response, 'big')
        return -1
    
    """
    Relay Refreshing Commands.

    Relay Refreshing is discussed heavily on pages 10 and 11, and are
    considered some of the most important “foundation” concepts for taking
    advantage of all the features the ProXR series controllers have to offer.
    Please reference these pages for detailed explanation and examples.
    """
    
    def enable_automatic_refreshing(self) -> bool:
        """Enables automatic refreshing."""
        command = self._command_builder(bytes(25))
        response = self.send_command(command)
        return self.validate_response(response)
    
    def disable_automatic_refreshing(self) -> bool:
        """Disables automatic refreshing."""
        command = self._command_builder(bytes(26))
        response = self.send_command(command)
        return self.validate_response(response)
    
    def store_relay_refreshing_mode(self) -> bool:
        """Stores the current relay refreshing mode."""
        command = self._command_builder(bytes(35))
        response = self.send_command(command)
        return self.validate_response(response)
    
    def query_relay_refreshing_mode(self) -> bool:
        """Queries the current relay refreshing mode."""
        command = self._command_builder(bytes(36))
        response = self.send_command(command, len=1)
        return self.validate_response(response)
    
    def refresh_relays(self) -> bool:
        """Refreshes the relays."""
        command = self._command_builder(bytes(37))
        response = self.send_command(command)
        return self.validate_response(response)
    
    """
    Set the status of a relay bank

    This command writes a byte of data directly to a relay bank. This al-
    lows you to easily set the status of 8 relays at one time. RelayData is a
    parameter value from 0-255. A value of 0 turns off all the relays. A
    value of 255 turns on all the relays. Other values set the status of the
    relays in the equivalent binary pattern of the RelayData parameter
    value.
    NOTE: A Bank Value of 0 applies this command to all relay banks.
    """

    def set_relay_status(self, relay_data: int) -> bool:
        """Sets the status of a relay bank."""
        if relay_data < 0 or relay_data > 255:
            raise ValueError("Relay data must be between 0 and 255")
        command = self._command_builder(
            bytes([40, relay_data])
        )
        response = self.send_command(command)
        return self.validate_response(response)
    
    def set_bank_relay_status(self, bank: int, relay_data: int) -> bool:
        """Sets the status of a relay bank."""
        self._validate_bank(bank)
        if relay_data < 0 or relay_data > 255:
            raise ValueError("Relay data must be between 0 and 255")
        command = self._command_builder(
            bytes([140, relay_data, bank])
        )
        response = self.send_command(command)
        return self.validate_response(response)
    
    """
    Power up relay status configuration
    This command stores the current status of the relays in a given bank
    into memory. The next time power is applied to the controller, relays
    will return to the stored on/off state. A bank value of 0 stores the pat-
    tern of all relays in all 26 banks.
    """

    def store_power_up_defaults(self, bank: int) -> bool:
        """Stores the power up defaults selected relay bank."""
        self._validate_bank(bank)
        command = self._command_builder(
            bytes([42])
        )
        response = self.send_command(command)
        return self.validate_response(response)
    
    def store_bank_power_up_defaults(self, bank: int) -> bool:
        """Stores the power up defaults for a bank."""
        self._validate_bank(bank)
        command = self._command_builder(
            bytes([142, bank])
        )
        response = self.send_command(command)
        return self.validate_response(response)

    def query_power_up_defaults(self) -> bytes:
        """Queries the power up defaults selected relay bank."""
        command = self._command_builder(
            bytes([43])
        )
        response = self.send_command(command, len=1)
        return response

    def query_bank_power_up_defaults(self, bank: int) -> bytes:
        """Queries the power up defaults for a bank."""
        self._validate_bank(bank)
        command = self._command_builder(
            bytes([143, bank])
        )
        response = self.send_command(command, len=1)
        return response
    
    """
    Changing Relay Banks

    All subsequent commands will be sent to the selected relay bank. This
    command only applies to commands values less than 100. Commands
    in the 100+ value range allow you to specify a relay bank as part of the
    command.
    """

    def select_relay_bank(self, bank: int) -> bool:
        """Selects the active relay bank."""
        self._validate_bank(bank)
        command = self._command_builder(
            bytes([49, bank])
        )
        response = self.send_command(command)
        return self.validate_response(response)
