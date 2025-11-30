#!/usr/bin/env python3
__version__ = "0.1.0"
__description__ = (
    "NCD ProXR Relay Controller library. https://media.ncd.io/20170721183921/ProXR.pdf"
)

from enum import Enum
from collections.abc import Iterable
from typing import SupportsBytes, SupportsIndex
from ncd_io.e3c_device import E3CDevice


class Commands(Enum):
    TURN_OFF_RELAY_OFFSET = 0
    TURN_ON_RELAY_OFFSET = 8
    TURN_OFF_BANK_RELAY_OFFSET = 100
    TURN_ON_BANK_RELAY_OFFSET = 108
    QUERY_RELAY_STATUS_OFFSET = 16
    QUERY_BANK_RELAY_STATUS_OFFSET = 116
    QUERY_STATUS_ALL = 24
    QUERY_BANK_STATUS = 124
    ENABLE_REPORTING_MODE = 27
    DISABLE_REPORTING_MODE = 28
    ENABLE_ALL_RELAYS = 29
    ENABLE_BANK_RELAYS = 129
    DISABLE_ALL_RELAYS = 30
    DISABLE_BANK_RELAYS = 130
    TOGGLE_ALL_RELAYS = 31
    TOGGLE_BANK_RELAYS = 131
    REVERSE_ALL_RELAYS = 32
    REVERSE_BANK_RELAYS = 132
    TEST_COMMS = 33
    QUERY_SELECTED_BANK = 34
    ENABLE_AUTOMATIC_REFRESHING = 25
    DISABLE_AUTOMATIC_REFRESHING = 26
    STORE_RELAY_REFRESHING_MODE = 35
    QUERY_RELAY_REFRESHING_MODE = 36
    REFRESH_RELAYS = 37
    SET_RELAY_STATUS = 40
    SET_BANK_RELAY_STATUS = 140
    STORE_POWER_UP_DEFAULTS = 42
    STORE_BANK_POWER_UP_DEFAULTS = 142
    QUERY_POWER_UP_DEFAULTS = 43
    QUERY_BANK_POWER_UP_DEFAULTS = 143
    SELECT_RELAY_BANK = 49
    TIMER_AND_SETUP_STX = 50


class TimerSetupCommands(Enum):
    RUN_NEW_DURATION_TIMER_OFFSET = 50
    RUN_NEW_PULSE_TIMER_OFFSET = 70
    SETUP_DURATION_TIMER_OFFSET = 90
    SETUP_PULSE_TIMER_OFFSET = 110
    CONTROL_ACTIVE_TIMERS = 131
    QUERY_TIMER = 130
    SET_TIMER_CALIBRATION = 132
    QUERY_TIMER_CALIBRATION = 133
    ACTIVATE_CALIBRATION_MARKERS = 134
    DEACTIVATE_CALIBRATION_MARKERS = 135
    SET_REPS_VALUE = 137
    QUERY_REPS_VALUE = 136
    RECOVERY_ATTEMPT_TO_SAFE_PARAMS = 147
    SET_CHARACTER_DELAY_VALUE = 139
    QUERY_CHARACTER_DELAY_VALUE = 138
    SET_ATTACHED_BANKS_VALUE = 141
    QUERY_ATTACHED_BANKS_VALUE = 140
    SET_TEST_CYCLE_VALUE = 146
    QUERY_TEST_CYCLE_VALUE = 145
    RESTORE_FACTORY_DEFAULTS = 144


class Bank(Enum):
    BANK_1 = 1
    BANK_2 = 2
    BANK_3 = 3
    BANK_4 = 4
    BANK_5 = 5
    BANK_6 = 6
    BANK_7 = 7
    BANK_8 = 8
    BANK_9 = 9
    BANK_10 = 10
    BANK_11 = 11
    BANK_12 = 12
    BANK_13 = 13
    BANK_14 = 14
    BANK_15 = 15
    BANK_16 = 16
    BANK_17 = 17
    BANK_18 = 18
    BANK_19 = 19
    BANK_20 = 20
    BANK_21 = 21
    BANK_22 = 22
    BANK_23 = 23
    BANK_24 = 24
    BANK_25 = 25
    BANK_26 = 26
    BANK_27 = 27
    BANK_28 = 28
    BANK_29 = 29
    BANK_30 = 30
    BANK_31 = 31
    BANK_32 = 32


class Port(Enum):
    PORT_1 = 0
    PORT_2 = 1
    PORT_3 = 2
    PORT_4 = 3
    PORT_5 = 4
    PORT_6 = 5
    PORT_7 = 6
    PORT_8 = 7


class RelayController(E3CDevice):
    nBANKS: int = 32

    def _validate_timer_number(self, timer_number: int) -> bool:
        if timer_number < 0 or timer_number > 15:
            raise ValueError("Timer number must be between 0 and 15")
        return True

    def _timer_setup_command_builder(
        self, data: bytes | Iterable[SupportsIndex] | SupportsIndex | SupportsBytes
    ) -> bytes:
        # Ensure data is bytes
        if type(data) is not bytes:
            data = bytes(data)

        # Join STX and data
        command = bytes([
            self.COMMAND_STX,
            Commands.TIMER_AND_SETUP_STX.value
        ]) + data
        return command

    # """
    # Controlling Individual Relays
    # """

    def turn_off_relay(self, port: Port) -> bool:
        """Turns off a specific relay in current bank."""
        command: bytes = self._command_builder([
            port.value + Commands.TURN_OFF_RELAY_OFFSET.value
        ])
        response = self.send_command(command)
        return self.validate_res_success(response)

    def turn_off_bank_relay(self, bank: Bank, port: Port) -> bool:
        """Turns off a specific relay in specified bank."""
        command: bytes = self._command_builder([
            port.value + Commands.TURN_OFF_BANK_RELAY_OFFSET.value,
            bank.value
        ])
        response = self.send_command(command)
        return self.validate_res_success(response)

    def turn_on_relay(self, port: Port) -> bool:
        """Turns on a specific relay in current bank."""
        command: bytes = self._command_builder([
            port.value + Commands.TURN_ON_RELAY_OFFSET.value
        ])
        response = self.send_command(command)
        return self.validate_res_success(response)

    def turn_on_bank_relay(self, bank: Bank, port: Port) -> bool:
        """Turns on a specific relay in specified bank."""
        command: bytes = self._command_builder([
            port.value + Commands.TURN_ON_BANK_RELAY_OFFSET.value,
            bank.value
        ])
        response = self.send_command(command)
        return self.validate_res_success(response)

    # """
    # Reading the status of individual relays
    # """

    def query_relay_status(self, port: Port) -> bool:
        """Queries the status of a specific relay in current bank."""
        command: bytes = self._command_builder((
            port.value + Commands.QUERY_RELAY_STATUS_OFFSET.value
        ))
        response = self.send_command(command)
        return self.validate_res_success(response)

    def query_bank_relay_status(self, bank: Bank, port: Port) -> bool:
        """Queries the status of a specific relay in specified bank."""
        command: bytes = self._command_builder([
            port.value + Commands.QUERY_BANK_RELAY_STATUS_OFFSET.value,
            bank.value
        ])
        response = self.send_command(command)
        return self.validate_res_success(response)

    # """
    # Reading the status of relay banks

    # This command allows you to read the status of a single bank of relays.
    # A value of 0-255 is returned indicating the status of all 8 relays. The
    # binary pattern of the value returned directly corresponds to the on/off
    # status of each of the 8 relays in the selected relay bank. If the cur-
    # rently selected relay bank is 0, or if you specify relay bank 0, then the
    # status of all 32 relay banks will be sent. In this condition, your program
    # should be written to read 32 bytes of data from the serial port.
    # """

    def query_status_all(self) -> int:
        """Queries the status of all relays in current bank."""
        command: bytes = self._command_builder([
            Commands.QUERY_STATUS_ALL.value
        ])
        response = self.send_command(command, 1)
        if response and len(response) == 1:
            return int.from_bytes(response, "big")
        return -1

    def query_bank_status(self, bank: Bank) -> int:
        """Queries the status of all relays in specified bank."""
        command: bytes = self._command_builder([
            Commands.QUERY_BANK_STATUS.value,
            bank.value
        ])
        response = self.send_command(command, 1)
        if response and len(response) == 1:
            return int.from_bytes(response, "big")
        return -1

    # """
    # Reporting Mode

    # This command sets and stores (in non-volatile EEPROM while in con-
    # figuration mode only) the reporting mode status. Reporting mode, by
    # default, is ON, meaning every time a command is sent to the controller,
    # the controller will send an 85 back to the computer, indicating that the
    # command has finished executing your instructions. We recommend
    # leaving it on, but doing so requires 2-Way communication with the con-
    # troller. You should turn it off if you intend to use 1-Way communication
    # only. A delay between some commands may be required when using
    # 1-Way communications. For optimum reliability, leave reporting mode
    # on and use 2-Way communications with the ProXR Series controllers.
    # NOTE: Reporting Mode may be turned on or off at any time. The
    # default power-up status of reporting mode is ONLY stored when
    # the device is in configuration mode (all dip switches off when the
    # controller is powered up).
    # """

    def enable_reporting_mode(self) -> bool:
        """Enables reporting mode."""
        self.REPORTING_MODE = True
        command = self._command_builder([
            Commands.ENABLE_REPORTING_MODE.value
        ])
        response = self.send_command(command)
        return self.validate_res_success(response)

    def disable_reporting_mode(self) -> bool:
        """Disables reporting mode."""
        self.REPORTING_MODE = False
        command = self._command_builder([
            Commands.DISABLE_REPORTING_MODE.value
        ])
        response = self.send_command(command)
        return self.validate_res_success(response)

    # """
    # All relays on/off
    # """

    def enable_all_relays(self) -> bool:
        """Enables all relays."""
        command = self._command_builder([
            Commands.ENABLE_ALL_RELAYS.value
        ])
        response = self.send_command(command)
        return self.validate_res_success(response)

    def enable_bank_relays(self, bank: Bank) -> bool:
        """Enables all relays in specified bank."""
        command = self._command_builder([
            Commands.ENABLE_BANK_RELAYS.value, bank.value
        ])
        response = self.send_command(command)
        return self.validate_res_success(response)

    def disable_all_relays(self) -> bool:
        """Disables all relays."""
        command = self._command_builder([
            Commands.DISABLE_ALL_RELAYS.value
        ])
        response = self.send_command(command)
        return self.validate_res_success(response)

    def disable_bank_relays(self, bank: Bank) -> bool:
        """Disables all relays in specified bank."""
        command = self._command_builder([
            Commands.DISABLE_BANK_RELAYS.value,
            bank.value
        ])
        response = self.send_command(command)
        return self.validate_res_success(response)

    # """
    # Inverting Relays
    # """

    def toggle_all_relays(self) -> bool:
        """Toggles all relays."""
        command = self._command_builder([
            Commands.TOGGLE_ALL_RELAYS.value
        ])
        response = self.send_command(command)
        return self.validate_res_success(response)

    def toggle_bank_relays(self, bank: Bank) -> bool:
        """Toggles all relays in specified bank."""
        command = self._command_builder([
            Commands.TOGGLE_BANK_RELAYS.value,
            bank.value
        ])
        response = self.send_command(command)
        return self.validate_res_success(response)

    # """
    # Reversing Relays
    # """

    def reverse_all_relays(self) -> bool:
        """
        Reverses all relays.
        reverses bit order of all relay banks.
        """
        command = self._command_builder([
            Commands.REVERSE_ALL_RELAYS.value
        ])
        response = self.send_command(command)
        return self.validate_res_success(response)

    def reverse_bank_relays(self, bank: Bank) -> bool:
        """Reverses all relays in specified bank."""
        command = self._command_builder([
            Commands.REVERSE_BANK_RELAYS.value,
            bank.value
        ])
        response = self.send_command(command)
        return self.validate_res_success(response)

    # """
    # Test 2-way communications
    # """

    def test_comms(self) -> bool:
        """
        Tests communication with the relay controller.
        his command is used to test 2-Way communications between the PC
        and the relay controller. This command does nothing except report
        back an ASCII character code 85 when executed.
        """
        command = self._command_builder([
            Commands.TEST_COMMS.value
        ])
        response = self.send_command(command, len=1)
        return self.validate_res_success(response)

    # """
    # Reading the currently selected relay bank
    # """

    def query_selected_bank(self) -> int:
        """Queries the currently selected bank."""
        command = self._command_builder([
            Commands.QUERY_SELECTED_BANK.value
        ])
        response = self.send_command(command, len=1)
        if response:
            return int.from_bytes(response, "big")
        return -1

    # """
    # Relay Refreshing Commands.

    # Relay Refreshing is discussed heavily on pages 10 and 11, and are
    # considered some of the most important “foundation” concepts for taking
    # advantage of all the features the ProXR series controllers have to offer.
    # Please reference these pages for detailed explanation and examples.
    # """

    def enable_automatic_refreshing(self) -> bool:
        """Enables automatic refreshing."""
        command = self._command_builder([
            Commands.ENABLE_AUTOMATIC_REFRESHING.value
        ])
        response = self.send_command(command)
        return self.validate_res_success(response)

    def disable_automatic_refreshing(self) -> bool:
        """Disables automatic refreshing."""
        command = self._command_builder([
            Commands.DISABLE_AUTOMATIC_REFRESHING.value
        ])
        response = self.send_command(command)
        return self.validate_res_success(response)

    def store_relay_refreshing_mode(self) -> bool:
        """Stores the current relay refreshing mode."""
        command = self._command_builder([
            Commands.STORE_RELAY_REFRESHING_MODE.value
        ])
        response = self.send_command(command)
        return self.validate_res_success(response)

    def query_relay_refreshing_mode(self) -> int:
        """Queries the current relay refreshing mode."""
        command = self._command_builder([
            Commands.QUERY_RELAY_REFRESHING_MODE.value
        ])
        response = self.send_command(command, len=1)
        if response and len(response) == 1:
            return int.from_bytes(response, "big")
        return -1

    def refresh_relays(self) -> bool:
        """Refreshes the relays."""
        command = self._command_builder([
            Commands.REFRESH_RELAYS.value
        ])
        response = self.send_command(command)
        return self.validate_res_success(response)

    # """
    # Set the status of a relay bank

    # This command writes a byte of data directly to a relay bank. This al-
    # lows you to easily set the status of 8 relays at one time. RelayData is a
    # parameter value from 0-255. A value of 0 turns off all the relays. A
    # value of 255 turns on all the relays. Other values set the status of the
    # relays in the equivalent binary pattern of the RelayData parameter
    # value.
    # NOTE: A Bank Value of 0 applies this command to all relay banks.
    # """

    def set_relay_status(self, relay_data: int) -> bool:
        """Sets the status of a relay bank."""
        if relay_data < 0 or relay_data > 255:
            raise ValueError("Relay data must be between 0 and 255")
        command = self._command_builder([
            Commands.SET_RELAY_STATUS.value,
            relay_data
        ])
        response = self.send_command(command)
        return self.validate_res_success(response)

    def set_bank_relay_status(self, bank: Bank, relay_data: int) -> bool:
        """Sets the status of a relay bank."""
        if relay_data < 0 or relay_data > 255:
            raise ValueError("Relay data must be between 0 and 255")
        command = self._command_builder([
            Commands.SET_BANK_RELAY_STATUS.value,
            relay_data,
            bank.value
        ])
        response = self.send_command(command)
        return self.validate_res_success(response)

    """
    Power up relay status configuration
    This command stores the current status of the relays in a given bank
    into memory. The next time power is applied to the controller, relays
    will return to the stored on/off state. A bank value of 0 stores the pat-
    tern of all relays in all 26 banks.
    """

    def store_power_up_defaults(self) -> bool:
        """Stores the power up defaults selected relay bank."""
        command = self._command_builder([
            Commands.STORE_POWER_UP_DEFAULTS.value
        ])
        response = self.send_command(command)
        return self.validate_res_success(response)

    def store_bank_power_up_defaults(self, bank: Bank) -> bool:
        """Stores the power up defaults for a bank."""
        command = self._command_builder([
            Commands.STORE_BANK_POWER_UP_DEFAULTS.value,
            bank.value
        ])
        response = self.send_command(command)
        return self.validate_res_success(response)

    def query_power_up_defaults(self) -> bytes:
        """Queries the power up defaults selected relay bank."""
        command = self._command_builder([
            Commands.QUERY_POWER_UP_DEFAULTS.value
        ])
        response = self.send_command(command, len=26)
        return response

    def query_bank_power_up_defaults(self, bank: Bank) -> bytes:
        """Queries the power up defaults for a bank."""
        command = self._command_builder([
            Commands.QUERY_BANK_POWER_UP_DEFAULTS.value,
            bank.value
        ])
        if bank.value == 0:
            len = 26
        else:
            len = 1
        response = self.send_command(command, len)
        return response

    """
    Changing Relay Banks

    All subsequent commands will be sent to the selected relay bank. This
    command only applies to commands values less than 100. Commands
    in the 100+ value range allow you to specify a relay bank as part of the
    command.
    """

    def select_relay_bank(self, bank: Bank) -> bool:
        """Selects the active relay bank."""
        command = self._command_builder([
            Commands.SELECT_RELAY_BANK.value,
            bank.value
        ])
        response = self.send_command(command)
        return self.validate_res_success(response)

    """
    Cleanup Routines
    """

    def clear_serial_buffer(self) -> bool:
        """Clears the serial buffer."""
        while self.com.recv(1):
            # TODO: define serial buffer clear condition
            continue
        return True

    # """
    # Simple Timer Commands
    # """

    def run_new_duration_timer(
        self,
        timer_number: int,
        duration_h: int,
        duration_m: int,
        duration_s: int,
        relay: int,
    ):
        """Runs a new duration timer."""
        self._validate_timer_number(timer_number)
        # Uses different relay addressing scheme
        # self._validate_port(relay)
        command: bytes = self._timer_setup_command_builder([
            timer_number + TimerSetupCommands.RUN_NEW_DURATION_TIMER_OFFSET.value,
            duration_h,
            duration_m,
            duration_s,
            relay
        ])
        response = self.send_command(command)
        return self.validate_res_success(response)

    def run_new_pulse_timer(
        self, timer_number: int, pulse_h: int, pulse_m: int, pulse_s: int, relay: int
    ):
        """Runs a new pulse timer."""
        self._validate_timer_number(timer_number)
        # Uses different relay addressing scheme
        # self._validate_port(relay)
        command: bytes = self._timer_setup_command_builder([
            timer_number + TimerSetupCommands.RUN_NEW_PULSE_TIMER_OFFSET.value,
            pulse_h,
            pulse_m,
            pulse_s,
            relay
        ])
        response = self.send_command(command)
        return self.validate_res_success(response)

    # """
    # Advanced Timer comfiguration
    # """

    def setup_duration_timer(
        self,
        timer_number: int,
        duration_h: int,
        duration_m: int,
        duration_s: int,
        relay: int,
    ):
        """Sets up a duration timer."""
        self._validate_timer_number(timer_number)
        # Uses different relay addressing scheme
        # self._validate_port(relay)
        command: bytes = self._timer_setup_command_builder([
            timer_number + TimerSetupCommands.SETUP_DURATION_TIMER_OFFSET.value,
            duration_h,
            duration_m,
            duration_s,
            relay
        ])
        response = self.send_command(command)
        return self.validate_res_success(response)

    def setup_pulse_timer(
        self, timer_number: int, pulse_h: int, pulse_m: int, pulse_s: int, relay: int
    ):
        """Sets up a pulse timer."""
        self._validate_timer_number(timer_number)
        # Uses different relay addressing scheme
        # self._validate_port(relay)
        command: bytes = self._timer_setup_command_builder([
            timer_number + TimerSetupCommands.SETUP_PULSE_TIMER_OFFSET.value,
            pulse_h,
            pulse_m,
            pulse_s,
            relay
        ])
        response = self.send_command(command)
        return self.validate_res_success(response)

    def control_active_timers(self, timer_state: int):
        """Controls active timers."""
        if timer_state < 0 or timer_state > 0xFFFF:
            raise ValueError("Timer state must be between 0x00 and 0xFFFF")
        command: bytes = self._timer_setup_command_builder([
            TimerSetupCommands.CONTROL_ACTIVE_TIMERS.value,
            timer_state & 0xFF, # LSB
            (timer_state >> 8) & 0xFF # MSB
        ])
        response = self.send_command(command)
        return self.validate_res_success(response)

    def query_timer(self, timer_number: int) -> list[int]:
        """Query remaining time before expiery."""
        self._validate_timer_number(timer_number)
        command = self._timer_setup_command_builder([
            TimerSetupCommands.QUERY_TIMER.value,
            timer_number
        ])
        response = self.send_command(command)
        return list(response)

    def set_timer_calibration(self, timer_calibration_value: int) -> bool:
        """Sets timer calibration."""
        if timer_calibration_value < 0 or timer_calibration_value > 0xFFFF:
            raise ValueError("Timer state must be between 0x00 and 0xFFFF")
        command = self._timer_setup_command_builder([
            TimerSetupCommands.SET_TIMER_CALIBRATION.value,
            timer_calibration_value & 0xFF, # LSB
            (timer_calibration_value >> 8) & 0xFF # MSB
        ])
        response = self.send_command(command)
        return self.validate_res_success(response)

    def query_timer_calibration(self) -> int:
        """Queries timer calibration."""
        command = self._timer_setup_command_builder([
            TimerSetupCommands.QUERY_TIMER_CALIBRATION.value
        ])
        response = self.send_command(command, len=2)
        return int.from_bytes(response, 'little')

    def activate_calibration_markers(self) -> bool:
        """
        Activates calibration markers.
        Time calibrator markers are used to help calibrate the timer. When the
        calibrator markers have been activated, the controller will send our
        ASCII character code 90 at the beginning of any timing event. ASCII
        character code 91 will be sent at the end of any timing event. The time
        measured between the receiving 90 and 91 is used to help the user set
        the calibration value. These markers may prove useful if you need your
        PC to know when a timing even has occurred.
        """
        command = self._timer_setup_command_builder([
            TimerSetupCommands.ACTIVATE_CALIBRATION_MARKERS.value
        ])
        response = self.send_command(command)
        return self.validate_res_success(response)

    def deactivate_calibration_markers(self) -> bool:
        """Deactivates calibration markers."""
        command = self._timer_setup_command_builder([
            TimerSetupCommands.DEACTIVATE_CALIBRATION_MARKERS.value
        ])
        response = self.send_command(command)
        return self.validate_res_success(response)

    # """
    # Advanced Configuration Commands
    # """

    def set_reps_value(self, reps_value: int) -> bool:
        """Sets the REPS value for advanced timer operations."""
        if reps_value < 1 or reps_value > 255:
            raise ValueError("REPS value must be between 1 and 255")
        command = self._timer_setup_command_builder([
            TimerSetupCommands.SET_REPS_VALUE.value,
            reps_value
        ])
        response = self.send_command(command)
        # return self.validate_res_success(response)
        return True

    def query_reps_value(self) -> int:
        """Queries the REPS value for advanced timer operations."""
        command = self._timer_setup_command_builder([
            TimerSetupCommands.QUERY_REPS_VALUE.value
        ])
        response = self.send_command(command, len=1)
        if response:
            return int.from_bytes(response, "big")
        return -1

    def recovery_attempt_to_safe_params(self) -> bool:
        """Attempts to recover the device to safe parameters."""
        command = self._timer_setup_command_builder([
            TimerSetupCommands.RECOVERY_ATTEMPT_TO_SAFE_PARAMS.value
        ])
        response = self.send_command(command)
        return self.validate_res_success(response)

    def set_character_delay_value(self, delay_value: int) -> bool:
        """Sets the character delay value."""
        if delay_value < 0 or delay_value > 255:
            raise ValueError("Delay value must be between 0 and 255")
        command = self._timer_setup_command_builder([
            TimerSetupCommands.SET_CHARACTER_DELAY_VALUE.value,
            delay_value
        ])
        response = self.send_command(command)
        return self.validate_res_success(response)

    def query_character_delay_value(self) -> int:
        """Queries the character delay value."""
        command = self._timer_setup_command_builder([
            TimerSetupCommands.QUERY_CHARACTER_DELAY_VALUE.value
        ])
        response = self.send_command(command, len=1)
        if response:
            return int.from_bytes(response, "big")
        return -1

    def set_attached_banks_value(self, banks_value: int) -> bool:
        """Sets the attached banks value."""
        if banks_value < 1 or banks_value > 32:
            raise ValueError("Banks value must be between 1 and 32")
        command = self._timer_setup_command_builder([
            TimerSetupCommands.SET_ATTACHED_BANKS_VALUE.value,
            banks_value
        ])
        response = self.send_command(command)
        # success = self.validate_res_success(response)
        # For some unknow reason test unit is returning the string "LightController"
        success = response is not None
        if success:
            self.nBANKS = banks_value
        return success

    def query_attached_banks_value(self) -> int:
        """Queries the attached banks value."""
        command = self._timer_setup_command_builder([
            TimerSetupCommands.QUERY_ATTACHED_BANKS_VALUE.value
        ])
        response = self.send_command(command, len=1)
        if response:
            self.nBANKS = int.from_bytes(response, "big")
            return self.nBANKS
        return -1

    def set_test_cycle_value(self, cycle_value: int) -> bool:
        """Sets the test cycle value."""
        if cycle_value < 0 or cycle_value > 32:
            raise ValueError("Cycle value must be between 0 and 32")
        command = self._timer_setup_command_builder([
            TimerSetupCommands.SET_TEST_CYCLE_VALUE.value,
            cycle_value
        ])
        response = self.send_command(command)
        return self.validate_res_success(response)

    def query_test_cycle_value(self) -> int:
        """Queries the test cycle value."""
        command = self._timer_setup_command_builder([
            TimerSetupCommands.QUERY_TEST_CYCLE_VALUE.value
        ])
        response = self.send_command(command, len=1)
        if response:
            return int.from_bytes(response, "big")
        return -1

    def restore_factory_defaults(self) -> bool:
        """Restores factory default settings."""
        command = self._timer_setup_command_builder([
            TimerSetupCommands.RESTORE_FACTORY_DEFAULTS.value
        ])
        response = self.send_command(command)
        return self.validate_res_success(response)

    def quick_start(self) -> bool:
        """Configures the device with quick start settings."""
        # NOTE: Commands / Procedure as per TCP packet capture from Pool2001
        # 254 50 141 2 """returns b'LightController'"""
        self.enable_reporting_mode()
        self.enable_automatic_refreshing()
        res = self.set_attached_banks_value(2)
        if not res:
            return False
        # 254 50 137 1
        res = self.set_reps_value(1)
        if not res:
            return False
        # 254 131 2
        res = self.toggle_bank_relays(Bank.BANK_2)
        print(res)
        return res
