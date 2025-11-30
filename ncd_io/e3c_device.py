from enum import Enum
from time import sleep
from socket import socket
from collections.abc import Iterable
from typing import SupportsBytes, SupportsIndex


class Commands(Enum):
    ENABLE_ALL_DEVICES = 248
    DISABLE_ALL_DEVICES = 249
    ENABLE_SELECTED_DEVICE = 250
    DISABLE_SELECTED_DEVICE = 251
    ENABLE_SELECTED_DEVICE_EXCLUSIVE = 252
    DISABLE_SELECTED_DEVICE_EXCLUSIVE = 253
    STORE_DEVICE_NUMBER = 255
    RECALL_DEVICE_IDENTIFICATION = 246
    RECALL_DEVICE_NUMBER = 247


class DeviceIdentifier:
    DEVICE_ID: int
    FIRMWARE_VERSION: int
    FIRMWARE_YEAR: int

    def __init__(self, dev_id: int, fw_version: int, fw_year: int) -> None:
        self.DEVICE_ID = dev_id
        self.FIRMWARE_VERSION = fw_version
        self.FIRMWARE_YEAR = fw_year

    @classmethod
    def from_bytes(cls, data: bytes):
        if len(data) != 4:
            raise ValueError("Data must be 4 bytes long")
        DEVICE_ID = data[0] | (data[1] << 8)
        FIRMWARE_VERSION = data[2]
        millennia = (data[3] // 100) * 1000
        FIRMWARE_YEAR = (data[3] % 100) + millennia
        return cls(DEVICE_ID, FIRMWARE_VERSION, FIRMWARE_YEAR)


class E3CDevice:
    IP_ADDRESS: str = "10.0.0.105"
    PORT: int = 2101
    COMMAND_STX: int = 254
    REPORT_SUCESS = 85
    REPORTING_MODE: bool = True

    def __init__(self, com: socket, kwargs=None):
        if kwargs:
            self.__dict__.update(kwargs)
        self.com = com

    def __exit__(self, exception_type, exception_value, exception_traceback):
        self.com.close()

    def __enter__(self):
        self.com.connect((self.IP_ADDRESS, self.PORT))
        self.com.settimeout(1)
        return self

    def send_command(self, command: bytes, len: int = 1) -> bytes:
        # Send Command
        self.com.send(command)
        # TODO: remove, leave to socket implementation
        sleep(0.5)

        # Escape if not reporting mode
        if not self.REPORTING_MODE:
            return b""

        # Receive Response
        response = self.com.recv(len)
        return response

    def validate_res_success(self, response: bytes) -> bool:
        # Escape if not reporting mode
        if not self.REPORTING_MODE:
            return True

        # Validate Response
        if response and response == bytes([self.REPORT_SUCESS]):
            return True
        return False

    def _command_builder(
        self, data: bytes | Iterable[SupportsIndex] | SupportsIndex | SupportsBytes
    ) -> bytes:
        # Ensure data is bytes
        if type(data) is not bytes:
            data = bytes(data)

        # Join STX and data
        command = bytes([self.COMMAND_STX]) + data
        return command

    # """
    # The E3C Command Set
    # """

    def enable_all_devices(self) -> bool:
        """Tells all devices to respond to your commands."""
        command = self._command_builder([Commands.ENABLE_ALL_DEVICES.value])
        response = self.send_command(command)
        return self.validate_res_success(response)

    def disable_all_devices(self) -> bool:
        """Tells all devices to ignore your commands."""
        command = self._command_builder([Commands.DISABLE_ALL_DEVICES.value])
        response = self.send_command(command)
        return self.validate_res_success(response)

    def enable_selected_device(self) -> bool:
        """Tells a specific device to listen to your commands"""
        command = self._command_builder([Commands.ENABLE_SELECTED_DEVICE.value])
        response = self.send_command(command)
        return self.validate_res_success(response)

    def disable_selected_device(self) -> bool:
        """Tells a specific device to ignore your commands"""
        command = self._command_builder([Commands.DISABLE_SELECTED_DEVICE.value])
        response = self.send_command(command)
        return self.validate_res_success(response)

    def enable_selected_device_exclusive(self) -> bool:
        """Tells a specific device to listen to your commands, all other devices will ignore your commands."""
        command = self._command_builder(
            [Commands.ENABLE_SELECTED_DEVICE_EXCLUSIVE.value]
        )
        response = self.send_command(command)
        return self.validate_res_success(response)

    def disable_selected_device_exclusive(self) -> bool:
        """Tells a specific device to ignore your commands, all others will listen."""
        command = self._command_builder(
            [Commands.DISABLE_SELECTED_DEVICE_EXCLUSIVE.value]
        )
        response = self.send_command(command)
        return self.validate_res_success(response)

    # """
    # Extended E3C Commands
    # """

    def store_device_number(self) -> bool:
        """
        Stores the device number into the controller.
        The device number takes effect immediately.
        The enabled/disabled status of the device is unchanged
        """
        command = self._command_builder([Commands.STORE_DEVICE_NUMBER.value])
        response = self.send_command(command)
        return self.validate_res_success(response)

    def recall_device_identification(self) -> DeviceIdentifier:
        """
        This command reports back 4 bytes of data:
        ProXR Device ID Part 1: 1
        ProXR Device ID Part 2: 0
        ProXR Firmware Version: 17 (or newer)
        ProXR Year of Firmware Production: 205 (or newer)
        ProXR E3C Device Number
        """
        command = self._command_builder([Commands.RECALL_DEVICE_IDENTIFICATION.value])
        response = self.send_command(command, 4)
        return DeviceIdentifier.from_bytes(response)

    def recall_device_number(self) -> bool:
        """Reads the stored device number from the controller"""
        command = self._command_builder([Commands.RECALL_DEVICE_NUMBER.value])
        response = self.send_command(command)
        return self.validate_res_success(response)
