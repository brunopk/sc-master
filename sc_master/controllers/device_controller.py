from typing import List, Dict, Union, Optional
from dataclasses import dataclass
from functools import wraps
from rest_framework import status
from sc_master.controllers.section_controller import SectionController
from sc_master.utils.dataclasses import Section, Device
from sc_master.utils.errors import ApiError, DeviceClientError
from sc_master.utils.enums import ErrorCode, HardwareMode
from sc_master.utils.helpers import map_error_code_to_http_status
from sc_master.utils.scrpi_client import ScRpiClient


########################################################################################################################
#                                                   ERROR CLASSES                                                      #
########################################################################################################################


class SystemDeviceAlreadyConnected(ApiError):

    def __init__(self, *args):
        super().__init__(*args)

    def get_message(self) -> str:
        return 'Device already connected.'

    def get_error_code(self) -> ErrorCode:
        return ErrorCode.SY_DEVICE_ALREADY_CONNECTED


class SystemHasNoConnectedDevices(ApiError):

    def __init__(self, *args):
        super().__init__(*args)

    def get_message(self) -> str:
        return 'Connect at least one device.'

    def get_error_code(self) -> ErrorCode:
        return ErrorCode.SY_HAS_NO_CONNECTED_DEVICES


class SystemTurnedOff(ApiError):

    def __init__(self, *args):
        super().__init__(*args)

    def get_message(self) -> str:
        return 'Strips are turned off.'

    def get_error_code(self) -> ErrorCode:
        return ErrorCode.SY_TURNED_OFF


class SystemModeError(ApiError):

    def __init__(self, *args):
        super().__init__(*args)

    def get_message(self) -> str:
        return 'Set the corresponding mode before sending this command.'

    def get_error_code(self) -> ErrorCode:
        return ErrorCode.SY_MODE_ERROR

########################################################################################################################
#                                                    DATACLASSES                                                       #
########################################################################################################################


@dataclass
class Error:

    code: str

    message: str


@dataclass
class DeviceInfo:

    address: str

    port: int

    number_of_led: int

    is_on: bool = False

    error: Optional[Error] = None


@dataclass
class Data:

    mode: HardwareMode

    is_on: bool

    error: Optional[Error]

    devices: List[DeviceInfo]

    static_design: Optional[List[Section]]


@dataclass
class OperationResult:

    http_status: Optional[int]

    data: Data

########################################################################################################################
#                                                   DECORATORS                                                         #
########################################################################################################################


def handle_errors(func):

    @wraps(func)
    def _wrapped_func(cls, *args, **kwargs):
        try:
            return func(cls, *args, **kwargs)
        except DeviceClientError as e1:
            return cls._build_result(e1)
        except ApiError as e2:
            return cls._build_result(None, e2)

    return _wrapped_func


def require(mode: Optional[HardwareMode] = None, connected_devices: bool = False, one_device_on: bool = False):

    def decorator(func):

        @wraps(func)
        def _wrapped_func(cls, *args, **kwargs):
            if mode is not None and cls._mode != mode:
                raise SystemModeError()
            elif connected_devices and len(cls._devices) == 0:
                raise SystemHasNoConnectedDevices()

            # it don't make to much sense to filter on a list cause currently sc-master is intended to control one device

            elif one_device_on and len(list(filter(lambda d: d.is_on, cls._devices))) == 0:  # type: ignore
                raise SystemTurnedOff()
            else:
                return func(cls, *args, **kwargs)

        return _wrapped_func

    return decorator


########################################################################################################################
#                                                     MAIN CLASS                                                       #
########################################################################################################################

class DeviceController:
    """
    Provides methods to control devices. Currently sc-master is intended to control one device, it'is on the roadmap of
    sc-master to provide methods to control more than one device.

    All methods in this class will return objects of the same class: `OperationResult`.

    """

    ####################################################################################################################
    #                                                  STATIC ATTRIBUTES                                               #
    ####################################################################################################################

    _device: Optional[Device] = None

    _mode = HardwareMode.STATIC

    _section_controller = SectionController()

    ####################################################################################################################
    #                                                 PRIVATE STATIC METHODS                                           #
    ####################################################################################################################

    @classmethod
    def _generate_error_result(cls, error: Union[DeviceClientError, ApiError]) -> OperationResult:
        """
        Generates and returns a common object (an instance of `OperationResult`) in order to return the same object 
        after throwing an exception on any method.

        See also the description of the `_generate_successful_result` and decorator `handle_errors`.
        """
        pass

    @classmethod
    def _generate_successful_result(cls) -> OperationResult:
        """
        Generates and returns a common object (an instance of `OperationResult`) in order to return the same object at
        the end of the execution of any method (for exception cases, see `_generate_error_result`).

        For this purpose, it uses the information stored in class methods, for instance, the number of led.
        """

        device_with_error = None
        is_error = False
        error = None
        http_status = status.HTTP_200_OK

        """
        if e1 is not Non
            device_with_error = list(
              filter(
                lambda d: d.address == e1.get_device_address() and d.port == e1.get_device_port(),  # type: ignore
                devices
              )
            )[0]
            device_with_error.error = Error(str(e1.get_error_code()), e1.get_message())
            is_error = True
            http_status = map_error_code_to_http_status(e1.get_error_code())
        if e2 is not None:
            is_error = True
            error = Error(str(e2.get_error_code()), e2.get_message())
            http_status = map_error_code_to_http_status(e2.get_error_code())
      
        data = Data(
          is_on=any(map(lambda d: d.is_on, cls._devices)),
          is_error=is_error,
          mode=str(cls._mode),
          devices=devices,
          error=error,
          static_design=cls._section_controller.get_sections() if cls._mode == HardwareMode.STATIC else None
        )
        """
       
        return OperationResult(http_status, Data(HardwareMode.STATIC, True, None, [], []))

    ####################################################################################################################
    #                                                 PUBLIC STATIC METHODS                                            #
    ####################################################################################################################

    @classmethod
    @handle_errors
    def connect_device(cls, address: str, port: int) -> OperationResult:
        """
        Establish a connection with a device
        """

        if not cls._device is None:
            raise SystemDeviceAlreadyConnected()

        client = ScRpiClient()
        client.connect(address, port)
        status = client.status()
        number_of_led = int(status.get('strip_length'))  # type: ignore
        cls._device = Device(address, port, client, number_of_led)

        return cls._generate_successful_result()

    @classmethod
    @handle_errors
    def status(cls) -> OperationResult:
        """
        Gets information of the system including each connected device (if any)
        """
        if len(cls._devices) > 0:
            cls._devices[0].client.status()
        return cls._generate_successful_result()

    @classmethod
    @handle_errors
    @require(connected_devices=True)
    def reset(cls) -> OperationResult:
        """
        Sets the system on STATIC and remove all sections (executing this operation will turn off all the strips).
        """
        cls._devices[0].client.reset()
        cls._mode = HardwareMode.STATIC
        cls._section_controller.remove_all_sections()
        return cls._generate_successful_result()

    @classmethod
    @handle_errors
    @require(connected_devices=True)
    def turn_on(cls, index=None):
        """
        If index is not None, turns on an specific section. Otherwise, turns on an specific section or all the strips.
        """
        if index is not None:
            cls._devices[0].client.turn_on(cls._section_controller.get_section_hw_id(index))
            cls._section_controller.set_section_on(index)
        else:
            cls._devices[0].client.turn_on()
            for d in cls._devices:
                d.is_on = True
        return cls._generate_successful_result()

    @classmethod
    @handle_errors
    @require(connected_devices=True)
    def turn_off(cls, index=None) -> OperationResult:
        """
        If index is not None, turns off an specific section. Otherwise, turns off all the strips
        and reset the system to the initial state (like reset method).
        """

        if index is not None:
            cls._devices[0].client.turn_off(cls._section_controller.get_section_hw_id(index))
            cls._section_controller.set_section_on(index)
        else:
            cls._devices[0].client.reset()
            cls._devices[0].client.turn_off()
            cls._section_controller.remove_all_sections()
            for d in cls._devices:
                d.is_on = False
        cls._mode = HardwareMode.STATIC
        return cls._generate_successful_result()

    @classmethod
    @handle_errors
    @require(mode=HardwareMode.STATIC, one_device_on=True)
    def add_sections(cls, sections: List[Section]) -> OperationResult:
        """
        Add a list of sections to the current static design.

        :param sections: sections to add
        """
        cls._section_controller.validate_addition(sections)
        cls._section_controller.add_sections(sections)
        command_args = {'sections': [s.__dict__ for _, s in enumerate(sections)]}
        command_resp = cls._devices[0].client.section_add(command_args)
        for i, hw_id in enumerate(command_resp.get('sections')):  # type: ignore
            cls._section_controller.set_section_hw_id(sections[i].start, sections[i].end, hw_id)
        return cls._generate_successful_result()

    @classmethod
    @handle_errors
    @require(mode=HardwareMode.STATIC, one_device_on=True)
    def remove_sections(cls, indexes: List[int]) -> OperationResult:
        """
        Remove one or more section

        :param indexes: indexes or positions of the sections to be removed
        """
        section_ids = list(map(cls._section_controller.get_section_hw_id, indexes))
        cls._section_controller.validate_deletion(indexes)
        cls._devices[0].client.section_remove(section_ids)
        cls._section_controller.remove_sections(indexes)
        return cls._generate_successful_result()

    @classmethod
    @handle_errors
    @require(mode=HardwareMode.STATIC, one_device_on=True)
    def edit_section(cls, index: int, data: Section) -> OperationResult:
        """
        Change attributes of one section (set data.attr as None to leave data.attr unchanged).

        :param index: index of the section to be edited
        :param data: properties that will change
        """
        cls._section_controller.validate_edition(index, data)
        section_hw_id = cls._section_controller.get_section_hw_id(index)
        cls._devices[0].client.section_edit(
            section_hw_id,
            data.start,
            data.end,
            data.color
        )
        cls._section_controller.edit_section(index, data)
        return cls._generate_successful_result()
