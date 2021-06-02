import json
import logging
import socket as skt
from typing import Union, List

SCP_OK = 200

########################################################################################################################
#                                                AUXILIARY FUNCTIONS                                                   #
########################################################################################################################


def make_request(cmd: dict, end_char: str):
    return json.dumps(cmd) + end_char


########################################################################################################################
#                                                   ERROR CLASSES                                                      #
########################################################################################################################

class BadAddress(Exception):
    pass


class BadPort(Exception):
    pass


class NotConnected(Exception):
    pass


class ApiError(Exception):

    def __init__(self, status: int, message: str, result: dict):
        self.status = status
        self.message = message
        self.result = result


########################################################################################################################
#                                                      MAIN CLASS                                                      #
########################################################################################################################

class ApiClient:
    """
    sc-rpi client
    https://github.com/brunopk/sc-rpi
    """

    def send_request(self, req: str):
        """
        Send request

        :raises BrokenPipeError:
        :raises NotConnected:
        """

        if self.skt is None:
            raise NotConnected()

        msg = req.encode('utf-8')
        size = self.skt.send(msg)
        msg = msg[size:]
        while len(msg) > 0:
            size = self.skt.send(msg)
            msg = msg[size:]

    def recv_response(self) -> dict:
        """
        Receive response

        :raises ConnectionResetError:
        :raises ApiError:
        """
        # TODO: timeout mechanism for self.skt.recv
        msg = ''
        end_char = self.end_char.encode('utf-8')
        chunk = self.skt.recv(1)
        while chunk != end_char:
            msg += chunk.decode('utf-8')
            chunk = self.skt.recv(1)
        msg += str(chunk.decode('utf-8'))
        resp = json.loads(msg)
        if resp['status'] != SCP_OK:
            self.logger.warning(f'Error {resp["status"]} from sc-rpi: {resp["message"]}, {resp["result"]}')
            raise ApiError(resp['status'], resp['message'], resp['result'])
        return resp['result']

    def __init__(self):
        # noinspection PyTypeChecker
        self.skt: skt.socket = None
        self.end_char = '\n'
        self.logger = logging.getLogger(__name__)

    def connect(self, address: str, port: int):
        """
        Connect to sc-rpi

        :param address: address (IP or hostname)
        :param port: port number
        :raises BadPort:
        :raises BadAddress:
        """
        self.skt = skt.socket(skt.AF_INET, skt.SOCK_STREAM)
        try:
            self.skt.connect((address, port))
        except ConnectionRefusedError as ex:
            raise ex
        except skt.gaierror:
            raise BadAddress()
        except OSError:
            raise BadPort()
        except Exception as ex:
            raise ex

    def disconnect(self):
        """
        Disconnect

        :raises BrokenPipeError:
        :raises ConnectionResetError:
        :raises NotConnected:
        :raises ApiError:
        """
        cmd = {"name": "disconnect"}
        req = make_request(cmd, self.end_char)
        self.send_request(req)

    def reset(self):
        """
        Remove all sections

        :raises BrokenPipeError:
        :raises ConnectionResetError:
        :raises NotConnected:
        :raises ApiError:
        """
        cmd = {"name": "reset"}
        req = make_request(cmd, self.end_char)
        self.send_request(req)

    def status(self) -> dict:
        """
        Gets information of the current status of sc-rpi

        :raises BrokenPipeError:
        :raises ConnectionResetError:
        :raises NotConnected:
        :raises ApiError:
        """
        cmd = {"name": "status"}
        req = make_request(cmd, self.end_char)
        self.send_request(req)
        return self.recv_response()

    def turn_on(self, section_id: str = None) -> dict:
        """
        Turns on a specific sections or the whole strip

        :raises BrokenPipeError:
        :raises ConnectionResetError:
        :raises NotConnected:
        :raises ApiError:
        """
        cmd = {'name': 'turn_on'}
        if section_id is not None:
            cmd['args'] = {
                'section_id': section_id
            }
        req = make_request(cmd, self.end_char)
        self.send_request(req)
        return self.recv_response()

    def turn_off(self, section_id: str = None) -> dict:
        """
        Turns on a specific sections or the whole strip

        :raises BrokenPipeError:
        :raises ConnectionResetError:
        :raises NotConnected:
        :raises ApiError:
        """
        cmd = {'name': 'turn_off'}
        if section_id is not None:
            cmd['args'] = {
                'section_id': section_id
            }
        req = make_request(cmd, self.end_char)
        self.send_request(req)
        return self.recv_response()

    def edit_section(self, section_id: str, start: int = None, end: int = None, color: str = None) -> dict:
        """
        Edit section

        :raises BrokenPipeError:
        :raises ConnectionResetError:
        :raises NotConnected:
        :raises ApiError:
        """
        cmd = {
            'name': 'edit_section',
            'args': {
                'section_id': section_id
            }
        }
        if start is not None:
            cmd['args']['start'] = start
        if end is not None:
            cmd['args']['end'] = end
        if color is not None:
            cmd['args']['color'] = color
        req = make_request(cmd, self.end_char)
        self.send_request(req)
        return self.recv_response()

    def new_section(self, start: int, end: str) -> dict:
        """
        Defines a new section

        :raises BrokenPipeError:
        :raises ConnectionResetError:
        :raises NotConnected:
        :raises ApiError:
        """
        cmd = {
            'name': 'new_section',
            'args': {
                'start': start,
                'end': end,
            }
        }
        req = make_request(cmd, self.end_char)
        self.send_request(req)
        return self.recv_response()

    def remove_sections(self, sections: List[str]) -> dict:
        """
        Removes sections specified in the list

        :raises BrokenPipeError:
        :raises ConnectionResetError:
        :raises NotConnected:
        :raises ApiError:
        """
        cmd = {
            'name': 'remove_sections',
            'args': {
                'sections': sections
            }
        }
        req = make_request(cmd, self.end_char)
        self.send_request(req)
        return self.recv_response()


scrpi_client = ApiClient()

