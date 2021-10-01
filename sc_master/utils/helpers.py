from typing import Dict, List
from rest_framework.serializers import ValidationError
from rest_framework import status
from webcolors import hex_to_rgb
from sc_master.utils.dataclasses import Section
from sc_master.utils.enums import ErrorCode


def validate_section_limits(limits: Dict):
    """
    Validate section limits

    :param limits: dictionary containing "start" and "end" keys
    :raise ValidationError: if don't pass validations
    :return: the same dict passed to this function
    """

    start: int = limits.get('start')
    end: int = limits.get('end')

    if start == end:
        raise ValidationError('start and end must be different')

    if start > end:
        raise ValidationError('start cannot be larger than end')

    if start < 0 or end < 0:
        raise ValidationError('start and end must be positive integers')

    return limits


def validate_hex(value: str):
    try:
        hex_to_rgb(value)
        return value
    except ValueError:
        raise ValidationError('Invalid hex')


def dict_to_section(data: Dict) -> Section:
    """
    Generate a Section from a dictionary storing values in the corresponding attribute.
    For instance, data["start"] will be copied to s.start (where s is an instance of Section).
    """
    return Section(data.get('start'), data.get('end'), data.get('color'), data.get('is_on'))


def map_error_code_to_http_status(e: ErrorCode) -> int:

    enum_list = list(ErrorCode)
    if e not in enum_list:
        raise Exception(f'Invalid error code #{int(e)}')

    if \
            e == ErrorCode.ST_EDITION_NOT_ALLOWED \
            or e == ErrorCode.SY_MODE_ERROR \
            or e == ErrorCode.GE_BAD_REQUEST \
            or e == ErrorCode.GE_PARSE_ERROR:
        return status.HTTP_400_BAD_REQUEST
    elif \
            e == ErrorCode.ST_NOT_FOUND or e == ErrorCode.RE_NOT_FOUND:
        return status.HTTP_404_NOT_FOUND
    elif \
            e == ErrorCode.ST_OVERLAPPING \
            or e == ErrorCode.SY_DEVICE_ALREADY_CONNECTED \
            or e == ErrorCode.SY_TURNED_OFF:
        return status.HTTP_409_CONFLICT
    elif \
            e == ErrorCode.GE_INTERNAL:
        return status.HTTP_500_INTERNAL_SERVER_ERROR
    elif \
            e == ErrorCode.DE_BROKEN_CONNECTION \
            or e == ErrorCode.DE_ESTABLISHING_CONNECTION \
            or e == ErrorCode.SY_HAS_NO_CONNECTED_DEVICES:
        return status.HTTP_503_SERVICE_UNAVAILABLE
    else:
        raise Exception(f'No HTTP status defined for error #{int(e)}')


def map_sections(data: List[Dict]) -> List[Section]:
    """
    Maps each element in the list using dict_to_section function
    """
    return list(map(lambda x: dict_to_section(x), data))
