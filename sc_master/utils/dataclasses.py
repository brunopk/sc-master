from dataclasses import dataclass
from sc_master.utils.scrpi_client import ScRpiClient


@dataclass
class Device:

    address: str

    port: int

    client: ScRpiClient

    number_of_led: int

    is_on: bool = False


@dataclass
class Section:

    start: int

    end: int

    color: str

    is_on: bool
