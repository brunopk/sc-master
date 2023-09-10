from typing import List
from dataclasses import dataclass
from sc_master.utils.dataclasses import Section, Device
from sc_master.utils.enums import ErrorCode
from sc_master.utils.errors import ApiError

########################################################################################################################
#                                                      DATACLASSES                                                     #
########################################################################################################################


@dataclass
class SectionAux(Section):
    hw_id: str

########################################################################################################################
#                                                     ERROR CLASSES                                                    #
########################################################################################################################


class SectionEditionNotAllowed(ApiError):

    def __init__(self, *args):
        super().__init__(*args)

    def get_message(self) -> str:
        return 'Edition not allowed.'

    def get_error_code(self) -> ErrorCode:
        return ErrorCode.ST_EDITION_NOT_ALLOWED

########################################################################################################################
#                                                        MAIN CLASS                                                    #
########################################################################################################################


class SectionController:

    ####################################################################################################################
    #                                               PRIVATE STATIC ATTRIBUTES                                          #
    ####################################################################################################################

    _sections: List[SectionAux] = []

    _devices: List[Device] = []

    ####################################################################################################################
    #                                                 PRIVATE STATIC METHODS                                           #
    ####################################################################################################################

    def _sort_sections(self, sections: List[Section]) -> List[Section]:
        """
        Sorts the list using merge sort algorithm

        :raise OverlappingError: in case of any section in the list overlaps another section.
        """
        if len(sections) > 1:
            result = []
            m = len(sections) // 2
            l1 = sections[:m]
            l2 = sections[m:]
            l1 = self._sort_sections(l1)
            l2 = self._sort_sections(l2)
            i = 0
            j = 0
            while i < len(l1) and j < len(l2):
                if (l2[j].start <= l1[i].start <= l2[j].end) or \
                    (l2[j].start <= l1[i].end <= l2[j].end) or \
                        (l1[i].start < l2[j].start and l1[i].end > l2[j].end):
                    raise ApiError(ErrorCode.ST_OVERLAPPING)
                elif l1[i].end < l2[j].start:
                    result.append(l1[i])
                    i += 1
                else:
                    result.append(l2[j])
                    j += 1
            return result + l1[i:] + l2[j:]
        else:
            return sections

    def _copy_section_list(self, section_list: List[SectionAux]) -> List[SectionAux]:
        return list(map(lambda x: SectionAux(x.start, x.end, x.color, x.is_on, x.hw_id), section_list))

    def _get_section_by_limits(self, sections: List[SectionAux], start: int, end: int) -> SectionAux:
        """
        Finds a section x in the list of sections passed as parameter

        :raise IndexError: in case of not finding the section
        """
        return list(filter(lambda x: x.start == start and x.end == end, sections))[0]

    ####################################################################################################################
    #                                                PUBLIC STATIC METHODS                                             #
    ####################################################################################################################

    def add_sections(self, sections: List[Section]):
        """
        Add a list of sections to the current static design.
        Use the corresponding validation before invoking this method.

        :param sections: sections to add
        :raise SectionOverlapping: for section overlapping
        """
        self._sections = self._sort_sections(self._sections + sections)

    def edit_section(self, index: int, data: Section):
        """
        Edits the section identified by its index.
        Use the corresponding validation before invoking this method.
        """
        self._sections[index].start = data.start
        self._sections[index].end = data.end
        self._sections[index].is_on = data.is_on
        self._sections[index].color = data.color

    def remove_sections(self, indexes: List[int]):
        """
        Remove one or more section

        :param indexes: indexes or positions of the sections to be removed
        """
        for (_, i) in enumerate(indexes):
            del self._sections[i]

    def remove_all_sections(self):
        """
        Remove all sections
        """
        self._sections = []

    def validate_addition(self, sections: List[Section]):
        """
        Checks following conditions :

        1. Section overlapping

        And raise the an exception in case of not passing any of them. 

        :param sections: sections that will be added and needs to be validated
        """
        self._sort_sections(sections + self._sections)  # type: ignore

    def validate_edition(self, index: int, data: Section):
        """
        Check some conditions :

        1. Section overlapping (after edition)
        2. index must point to a valid array position
        3. index cannot change after edition
        4. data.end < length of the strip

        :raise SectionOverlapping: if rule 1 is violated
        :raise SectionNotFound: if rule 2 is violated
        :raise SectionEditionNotAllowed: if rule 3 is violated
        """

        if len(self._sections) == 0:
            raise ApiError(ErrorCode.SECTION_NOT_FOUND)
        if data.end >= self._devices[0].number_of_led:
            raise SectionEditionNotAllowed()

        aux_list = self._copy_section_list(self._sections)
        try:
            aux_list[index].start = data.start
            aux_list[index].end = data.end
            aux_list[index].is_on = data.is_on
            aux_list[index].color = data.color
        except IndexError:
            raise ApiError(ErrorCode.SECTION_NOT_FOUND)
        aux_list = self._sort_sections(aux_list)  # type: ignore
        section_after_edition = self._get_section_by_limits(aux_list, data.start, data.end)  # type: ignore
        if aux_list.index(section_after_edition) != index:
            raise SectionEditionNotAllowed()

    def validate_deletion(self, indexes: List[int]):
        """
        Validates if all sections exists

        :raise SectionNotFound:
        """
        for index in indexes:
            if index < 0 or index >= len(self._sections):
                raise ApiError(ErrorCode.SECTION_NOT_FOUND)

    def is_section_on(self, index: int) -> bool:
        """
        Indicates if section is on

        Raise an exception if section not exist.
        """
        try:
            return self._sections[index].is_on
        except IndexError:
            raise ApiError(ErrorCode.SECTION_NOT_FOUND)

    def set_section_on(self, index: int):
        """
        Set section on

        Raise an exception if section not exist.
        """
        try:
            self._sections[index].is_on = True
        except IndexError:
            raise ApiError(ErrorCode.SECTION_NOT_FOUND)

    def set_section_off(self, index: int):
        """
        Set section off

        :raise SectionNotFound:
        """
        try:
            self._sections[index].is_on = False
        except IndexError:
            raise ApiError(ErrorCode.SECTION_NOT_FOUND)

    def set_section_hw_id(self, start: int, end: int, hw_id: str):
        """
        Finds the section for its limits (start and end) and sets its hw_id
        """
        s = self._get_section_by_limits(self._sections, start, end)
        s.hw_id = hw_id

    def get_section_hw_id(self, index: int) -> str:
        """
        Find section by index and returns its hw_id.

        Raise an exception if section not exist.
        """
        try:
            s = self._sections[index]
            return s.hw_id
        except IndexError:
            raise ApiError(ErrorCode.SECTION_NOT_FOUND)

    def get_sections(self) -> List[Section]:
        """
        Get all sections
        """
        return self._sections

    def update_device_list(self, devices: List[Device]):
        self._devices = devices
