from typing import Dict, List, OrderedDict
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

    start = limits.get('start')
    end = limits.get('end')

    if start is not None and end is not None:
        if start == end:
            raise ValidationError('start and end must be different')

        if start > end:
            raise ValidationError('start cannot be larger than end')

    if (start is not None and start < 0) or (end is not None and end < 0):
        raise ValidationError('start and end must be positive integers')

    return limits


def validate_hex(value: str):
    try:
        hex_to_rgb(value)
        return value
    except ValueError:
        raise ValidationError('Invalid hex')


def remove_none_entries(input: OrderedDict) -> OrderedDict:
    """
    Recursively generates a new dictionary removing entries in `input` whose values are `None`
    """
    output = OrderedDict()
    for field in input.keys():
        value = input.get(field)
        if value is not None:
            output.setdefault(field, value)
        elif isinstance(value, OrderedDict):
            output.setdefault(field, remove_none_entries(value))
    return output


def map_error_code_to_http_status(e: ErrorCode) -> int:

    enum_list = list(ErrorCode)
    if e not in enum_list:
        raise Exception(f'Invalid error code #{int(e)}')

    if \
            e == ErrorCode.SECTION_EDITION_NOT_ALLOWED \
            or e == ErrorCode.SY_MODE_ERROR \
            or e == ErrorCode.BAD_REQUEST \
            or e == ErrorCode.GE_PARSE_ERROR:
        return status.HTTP_400_BAD_REQUEST
    elif \
            e == ErrorCode.SECTION_NOT_FOUND or e == ErrorCode.RE_NOT_FOUND:
        return status.HTTP_404_NOT_FOUND
    elif \
            e == ErrorCode.ST_OVERLAPPING \
            or e == ErrorCode.LIGHTS_ALREADY_ON \
            or e == ErrorCode.LIGHTS_ALREADY_OFF \
            or e == ErrorCode.SECTION_ALREADY_OFF \
            or e == ErrorCode.SECTION_ALREADY_ON \
            or e == ErrorCode.SECTION_ALREADY_OFF \
            or e == ErrorCode.SY_DEVICE_ALREADY_CONNECTED \
            or e == ErrorCode.SY_TURNED_OFF:
        return status.HTTP_409_CONFLICT
    elif \
            e == ErrorCode.INTERNAL_SERVER_ERROR \
            or e == ErrorCode.SCP_ERROR \
            or e == ErrorCode.SCP_TCP_CONNECTION_ERROR \
            or e == ErrorCode.SCP_TCP_ERROR_SENDING_REQUEST \
            or e == ErrorCode.SCP_TCP_ERROR_RECEIVING_RESPONSE:
        return status.HTTP_500_INTERNAL_SERVER_ERROR
    elif \
            e == ErrorCode.NO_CONNECTED_DEVICES:
        return status.HTTP_503_SERVICE_UNAVAILABLE
    else:
        raise Exception(f'No HTTP status defined for error #{int(e)}')
