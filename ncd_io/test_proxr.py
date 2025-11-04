import socket
from unittest import TestCase, mock

from ncd_io.proxr import RelayController


class TestRelayController(TestCase):
    def setUp(self):
        self.mock_socket = mock.MagicMock(spec=socket.socket)
        self.relay_controller = RelayController(com=self.mock_socket)

    def test_send_command_sends_and_receives(self):
        command = b"\xfe\x6c\x01"
        expected_response = b"\x55"
        self.mock_socket.recv.return_value = expected_response

        response = self.relay_controller.send_command(command, len=2)

        self.mock_socket.send.assert_called_with(command)
        self.mock_socket.recv.assert_called_with(2)
        self.assertEqual(response, expected_response)

    def test_validate_response_valid(self):
        response = b"\x55"
        self.assertTrue(self.relay_controller.validate_response(response))

    def test_validate_response_invalid(self):
        response = b"\x00"
        self.assertFalse(self.relay_controller.validate_response(response))

    def test_control_active_timers(self):
        state = 0xAAAA
        expected_response = b"\x55"
        self.mock_socket.recv.return_value = expected_response

        response = self.relay_controller.control_active_timers(state)
        expected_command = b"\xfe\x32\x83\xaa\xaa"
        self.mock_socket.send.assert_called_with(expected_command)
        self.mock_socket.recv.assert_called_with(1)
        self.assertEqual(response, True)


if __name__ == "__main__":
    import unittest

    unittest.main()
