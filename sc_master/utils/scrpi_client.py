import socket as skt
import json
from typing import List, Optional
from sc_master.utils.errors import DeviceClientError
from sc_master.utils.errors import ErrorCode


class ScRpiClient:
    """
    Client for the https://github.com/brunopk/sc-rpi

    Each method will provide an abstraction for each command, so for instance the `connect` method will invoke the 
    `connect` command on sc-rpi and will return the specified response for this command.

    """

    ####################################################################################################################
    #                                                PRIVATE ATTRIBUTES                                                #
    ####################################################################################################################

    _address: str

    _port: int

    _skt: Optional[skt.socket] = None

    _END_CHAR = '\n'

    _SCP_OK = 200

    ####################################################################################################################
    #                                               PRIVATE STATIC METHODS                                             #
    ####################################################################################################################

    def _send_request(self, cmd: dict):
        """
        Send request through the TCP socket

        :raises DeviceClientError:
        """

        try:
            msg = self._stringify_command(cmd).encode('utf-8')
            size = self._skt.send(msg)  # type: ignore
            msg = msg[size:]
            while len(msg) > 0:
                size = self._skt.send(msg)  # type: ignore
                msg = msg[size:]
        except Exception as ex:
            raise DeviceClientError(ErrorCode.DE_SCP_CLIENT_ERROR, ex)

    def _recv_response(self, cmd: dict) -> dict:
        """
        Receive response

        :raises DeviceClientError:
        """
        try:
            msg = ''
            end_char = self._END_CHAR.encode('utf-8')
            chunk = self._skt.recv(1)  # type: ignore
            while chunk != end_char:
                msg += chunk.decode('utf-8')
                chunk = self._skt.recv(1)  # type: ignore
        except Exception as ex:
            raise DeviceClientError(ErrorCode.DE_SCP_CLIENT_ERROR, ex, cmd)

        msg += str(chunk.decode('utf-8'))
        resp = json.loads(msg)

        if resp['status'] != self._SCP_OK:
            raise DeviceClientError(ErrorCode.DE_SCP_ERROR, resp, cmd)

        return resp['result']

    def _stringify_command(self, cmd: dict):
        return json.dumps(cmd) + self._END_CHAR

    ################################################################################################
    #                                       PUBLIC STATIC METHODS                                  #
    ################################################################################################

    def connect(self, address: str, port: int):
        """
        Connect to a device

        :param address: IP or hostname
        :param port: port number
        :raises DeviceClientError:
        """
        self._address = address
        self._port = port
        self._skt = skt.socket(skt.AF_INET, skt.SOCK_STREAM)
        try:
            self._skt.connect((address, port))
        except Exception as ex:
            raise DeviceClientError(ErrorCode.DE_SCP_TCP_CONNECTION_ERROR, ex, address, port)

    def disconnect(self):
        """
        Disconnect

        :raises DeviceClientError:
        """
        cmd = {"name": "disconnect"}
        self._send_request(cmd)

    def reset(self):
        """
        Remove all sections

        :raises DeviceClientError:
        """
        cmd = {"name": "reset"}
        self._send_request(cmd)
        return self._recv_response(cmd)

    def status(self) -> dict:
        """
        Gets information of the device

        :raises DeviceClientError:
        """
        cmd = {"name": "status"}
        self._send_request(cmd)
        return self._recv_response(cmd)

    def turn_on(self, section_id: str = None) -> dict:
        """
        Turns on a specific sections or the whole strip

        :raises DeviceClientError:
        """
        cmd = {'name': 'turn_on'}
        if section_id is not None:
            cmd['args'] = {  # type: ignore
                'section_id': section_id
            }
        self._send_request(cmd)
        return self._recv_response(cmd)

    def turn_off(self, section_id: str = None) -> dict:
        """
        Turns on a specific sections or the whole strip

        :raises DeviceClientError:
        """
        cmd = {'name': 'turn_off'}
        if section_id is not None:
            cmd['args'] = {  # type: ignore
                'section_id': section_id
            }
        self._send_request(cmd)
        return self._recv_response(cmd)

    def section_edit(self, section_id: str, start: int = None, end: int = None, color: str = None) -> dict:
        """
        Edit section

        :raises DeviceClientError:
        """
        cmd = {
            'name': 'section_edit',
            'args': {
                'section_id': section_id
            }
        }
        if start is not None:
            # noinspection PyTypeChecker
            cmd['args']['start'] = start
        if end is not None:
            # noinspection PyTypeChecker
            cmd['args']['end'] = end
        if color is not None:
            cmd['args']['color'] = color
        self._send_request(cmd)
        return self._recv_response(cmd)

    def section_add(self, args: dict) -> dict:
        """
        Creates sections

        :param args: command arguments (see https://github.com/brunopk/sc-rpi/blob/master/doc/commands.md#section_add)
        :raises DeviceClientError:
        :return: data on 'result' field (see https://github.com/brunopk/sc-rpi/blob/master/doc/commands.md#section_add)
        """
        cmd = {
            'name': 'section_add',
            'args': args
        }
        self._send_request(cmd)
        return self._recv_response(cmd)

    def section_remove(self, sections: List[str]) -> dict:
        """
        Removes sections specified in the list

        :raises DeviceClientError:
        """
        cmd = {
            'name': 'section_remove',
            'args': {
                'sections': sections
            }
        }
        self._send_request(cmd)
        return self._recv_response(cmd)
