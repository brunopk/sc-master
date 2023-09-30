from typing import List, Optional
from dataclasses import dataclass
from functools import wraps
from rest_framework import status
from sc_master.controllers.section_controller import SectionController
from sc_master.utils.dataclasses import Section, Device
from sc_master.utils.errors import ApiError
from sc_master.utils.enums import ErrorCode, HardwareMode
from sc_master.utils.scrpi_client import ScRpiClient


########################################################################################################################
#                                                   ERROR CLASSES                                                      #
########################################################################################################################

# TODO: remove this error classes


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
        return ErrorCode.NO_CONNECTED_DEVICES


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
class DeviceInfo:

    address: str

    port: int

    number_of_led: int

    is_on: bool = False


@dataclass
class DeviceControllerResult:

    mode: HardwareMode

    is_system_on: bool = False

    device_info: Optional[DeviceInfo] = None

    static_design: Optional[List[Section]] = None

########################################################################################################################
#                                                    OTHER FUNCTIONS                                                   #
########################################################################################################################


def get_device_info(device: Device) -> DeviceInfo:
    """
    Maps a `Device` instance to a `DeviceInfo` instance extracting some specific attributes and discarding the rest.
    """
    return DeviceInfo(device.address, device.port, device.number_of_led, device.is_on)


def validate_mode(cls, mode: HardwareMode) -> bool:
    return mode is not None and cls._mode == mode


def validate_device_connected(cls) -> bool:
    return cls._device is not None


########################################################################################################################
#                                                   DECORATORS                                                         #
########################################################################################################################

def validate(mode: Optional[HardwareMode] = None, device_connected: bool = False, system_on: bool = False):

    def decorator(func):

        @wraps(func)
        def _wrapped_func(cls, *args, **kwargs):
            if mode is not None and not validate_mode(cls, mode):
                raise ApiError(ErrorCode.SY_MODE_ERROR)
            elif device_connected and not validate_device_connected(cls):
                raise ApiError(ErrorCode.NO_CONNECTED_DEVICES)
            else:
                return func(cls, *args, **kwargs)

        return _wrapped_func

    return decorator

########################################################################################################################
#                                                     MAIN CLASS                                                       #
########################################################################################################################

# TODO: 1 CONTINUE TESTING EDIT COMMAND
# TODO: 2 SEGUIR probando el turn_off, y add_sections. volver a probar turn_on (despues de hacer connect)
# TODO: 3 SEGUIR validar que para agregar secciones tiene que estar todo prendido y las secciones que se agreguen prendidas (is_on true)
# TODO: 4 HACER que el turn off apague todas las secciones
# TODO: 5 add section with is_on = True just after creating (adding) it
# TODO: agregar la info del device a la salida de todos los endpoints
# TODO: identificar el device por un nombre (y que aparezca el nombre en todos lados)
# TODO: ver que hace cuando se conecta un device (si prende o no, capaz conviene que haga un efecto o que sc-master le mande algo para que haga un efecto y se entienda que se conecto alguien)
# TODO: sacar para que no mande el comando status enseguida despues que conecta
# TODO: hacer que logue los errores (DeviceClientError) cuando se hace dos veces turn_on y la segunda falla porque ya esta prendido
# TODO: usar solo prefijos para cuando sean errores de device (por ejemplo GE_INTERNAL_ERROR -> INTERNAL_ERROR)
# TODO: cuando "is_system_on": false, no deberia mostrar "is_on": true en cada seccion
# TODO: validar doble turn_on
# TODO: do the same changes in https://github.com/brunopk/sc-master/pull/15/files#diff-d9df4f0f4d960efe93e5b9e9d003753f112fc5cd9d1a59b2ef5c483fd066a67f for all commands
# TODO: estaría bueno que en los datos del device se muestre el puerto origen para poder matchearlo con lo que muestra sc-rpi
# TODO: averiguar si esta bien retornar 503 cuando no hay un device conectado
# TODO: hacer test unitarios
# TODO: se podría hacer un wrapper del logger para que en sc_master/utils/decorators.py se configure solo para logear errores que no sean 400
# TODO: retornar cantidad de leds en la response


class DeviceController:
    """
    Provides a set of functions (static methods) to control a (only one) device. Each method can be thought as an 
    operation on a device, for example turing all lights on or just turning an specific section of the whole strip. All 
    operations return the same object (`DeviceControllerResult`).
    """

    ####################################################################################################################
    #                                                  STATIC ATTRIBUTES                                               #
    ####################################################################################################################

    _device: Optional[Device] = None

    # TODO: set it on True on turn_on (and off on turn off)
    _is_system_on = False

    _mode = HardwareMode.STATIC

    # TODO: consider moving this to an utils file with functions instead of a class
    _section_controller = SectionController()

    ####################################################################################################################
    #                                                 PRIVATE STATIC METHODS                                           #
    ####################################################################################################################

    @classmethod
    def _generate_successful_result(cls) -> DeviceControllerResult:
        """
        Returns an instance of `DeviceControllerResult` using information from class methods and class attributes.
        """

        device_info = get_device_info(cls._device) if cls._device is not None else None
        static_design = cls._section_controller.get_sections()
        return DeviceControllerResult(cls._mode, cls._is_system_on, device_info, static_design)

    ####################################################################################################################
    #                                                 PUBLIC STATIC METHODS                                            #
    ####################################################################################################################

    @classmethod
    def connect_device(cls, address: str, port: int) -> DeviceControllerResult:
        """
        Establish connection between sc-master an the device
        """

        if cls._device is not None:
            raise ApiError(ErrorCode.SY_DEVICE_ALREADY_CONNECTED)

        client = ScRpiClient()
        client.connect(address, port)
        status = client.status()
        number_of_led = int(status.get('strip_length'))
        new_device = Device(address, port, client, number_of_led)
        cls._device = new_device
        cls._section_controller.set_connected_device(new_device)

        return cls._generate_successful_result()

    @classmethod
    def status(cls) -> DeviceControllerResult:
        """
        Gets information of the system including each connected device (if any)
        """
        # TODO: capaz no sirve exponer lo que devuelve status, que sea algo interno nomas (ver https://github.com/brunopk/sc-rpi/blob/master/doc/commands.md#status)
        if cls._device is not None:
            cls._device.client.status()
        return cls._generate_successful_result()

    @classmethod
    @validate(device_connected=True)
    def reset(cls) -> DeviceControllerResult:
        """
        Sets the system on STATIC and remove all sections (executing this operation will turn off all the strips).
        """
        cls._device.client.reset()
        cls._mode = HardwareMode.STATIC
        cls._section_controller.remove_all_sections()
        return cls._generate_successful_result()

    @classmethod
    @validate(device_connected=True)
    def turn_on(cls, section_index: Optional[int] = None):
        """
        Turns on an specific section or all the strips.
        """
        if section_index is not None:
            if cls._section_controller.is_section_on(section_index):
                raise ApiError(ErrorCode.SECTION_ALREADY_ON)

            section_id = cls._section_controller.get_section_hw_id(section_index)
            cls._device.client.turn_on(section_id)
            cls._section_controller.set_section_on(section_index)
        else:
            if cls._device.is_on: 
                raise ApiError(ErrorCode.LIGHTS_ALREADY_ON)

            cls._device.client.turn_on()
            cls._is_system_on = True

        return cls._generate_successful_result()

    @classmethod
    @validate(device_connected=True)
    def turn_off(cls, section_index: Optional[int] = None) -> DeviceControllerResult:
        """
        If index is not None, turns off an specific section. Otherwise, turns off all the strips
        and reset the system to the initial state (like reset method).
        """

        if section_index is not None:
            if not cls._section_controller.is_section_on(section_index):
                raise ApiError(ErrorCode.SECTION_ALREADY_OFF)

            section_id = cls._section_controller.get_section_hw_id(section_index)
            cls._device.client.turn_off(section_id)
            cls._section_controller.set_section_off(section_index)
        else:
            if not cls._device.is_on: 
                raise ApiError(ErrorCode.LIGHTS_ALREADY_OFF)

            cls._device.client.turn_off()
            cls._is_system_on = False

        return cls._generate_successful_result()

    @classmethod
    @validate(device_connected=True, mode=HardwareMode.STATIC)
    def add_sections(cls, sections: List[Section]) -> DeviceControllerResult:
        """
        Add a list of sections to the current static design.

        :param sections: sections to add
        """
        cls._section_controller.validate_addition(sections)
        cls._section_controller.add_sections(sections)
        command_args = {'sections': [s.__dict__ for _, s in enumerate(sections)]}
        command_resp = cls._device.client.section_add(command_args)
        for i, hw_id in enumerate(command_resp.get('sections')):
            cls._section_controller.set_section_hw_id(sections[i].start, sections[i].end, hw_id)
        return cls._generate_successful_result()

    @classmethod
    @validate(mode=HardwareMode.STATIC, system_on=True)
    def remove_sections(cls, indexes: List[int]) -> DeviceControllerResult:
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
    @validate(mode=HardwareMode.STATIC, system_on=True)
    def edit_section(cls, index: int, data: Section) -> DeviceControllerResult:
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
