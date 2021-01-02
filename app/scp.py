import re
import json
import logging
import socket as skt
import project.settings as settings

SCP_OK = 200


def make_request(cmd: dict, end_char: str):
    return json.dumps(cmd) + end_char


class ApiError(Exception):

    def __init__(self, status: int, message: str, result: dict):
        self.status = status
        self.message = message
        self.result = result


class ApiClient:
    """
    sc-driver client
    https://github.com/brunopk/sc-driver
    """

    def send_request(self, req: str):
        """
        Send request

        :raises BrokenPipeError:
        """

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
            self.logger.warning(f'Error {resp["status"]} from sc-driver: {resp["message"]}, {resp["result"]}')
            raise ApiError(resp['status'], resp['message'], resp['result'])
        return resp['result']

    def __init__(self):
        # noinspection PyTypeChecker
        self.skt: skt.socket = None
        self.end_char = '\n'
        self.logger = logging.getLogger(__name__)

    def connect(self):
        if not settings.SC_CONNECTION_DISABLED:
            self.skt = skt.socket(skt.AF_INET, skt.SOCK_STREAM)
            self.skt.connect((settings.SC_DRIVER_HOST, settings.SC_DRIVER_PORT))
            self.logger.warning(f'Connected with sc-driver on {settings.SC_DRIVER_HOST}:{settings.SC_DRIVER_PORT}')
        else:
            self.logger.warning('Connection to sc-driver disabled, set SC_CONNECTION_DISABLED = False on '
                                'project/settings.py or run django with --noreload argument.')

    def disconnect(self):
        """
        Disconnect

        :raises BrokenPipeError:
        :raises ConnectionResetError:
        :raises ApiError:
        """
        cmd = {"name": "disconnect"}
        req = make_request(cmd)
        self.send_request(req)

    # noinspection PyTypeChecker
    def edit_section(self, section_id: str, start: int = None, end: int = None, color: str = None) -> dict:
        """
        Edit section

        :raises BrokenPipeError:
        :raises ConnectionResetError:
        :raises ApiError:
        """
        cmd = {
            'name': 'edit_section',
            'args': {
                'id': section_id
            }
        }
        if start is not None:
            cmd['args']['start'] = start
        if end is not None:
            cmd['args']['end'] = end
        if color is not None:
            cmd['args']['color'] = color
        req = make_request(cmd)
        self.send_request(req)
        return self.recv_response()

    def new_section(self, start: int, end: str) -> dict:
        """
        Defines a new section

        :raises BrokenPipeError:
        :raises ConnectionResetError:
        :raises ApiError:
        """
        cmd = {
            'name': 'new_section',
            'args': {
                'start': start,
                'end': end,
            }
        }
        req = make_request(cmd)
        self.send_request(req)
        return self.recv_response()

    def set_color(self, color: str, section_id: str = None) -> dict:
        """
        Sets color for all LEDs in the strip or in a specific section

        :raises BrokenPipeError:
        :raises ConnectionResetError:
        :raises ApiError:
        """
        cmd = {
            'name': 'set_color',
            'args': {
                'color': color
            }
        }
        if section_id is not None:
            cmd['args']['id'] = section_id
        req = make_request(cmd, self.end_char)
        self.send_request(req)
        return self.recv_response()
