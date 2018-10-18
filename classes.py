from enum import *
import logging
from exceptions import NoneValueException, WrongLengthException
from functions import *


class PivotChose(Enum):
    FIRST = 1
    LAST = 2
    MIDDLE = 3


class Sortable(object):
    """

    """
    inversion_counter = 0
    comparisons_counter = 0

    def null_comparisons_counter(self):
        self.comparisons_counter = 0

    def null_inversion_counter(self):
        self.inversion_counter = 0

    def _merge_combine(self, array):

        new_array = []
        logger = logging.getLogger(__name__)
        logger.debug("Combining method of " + str(self))
        lena = len(array)
        smaller = 0
        half = math.ceil(lena/2)
        bigger = half
        if_exit = False
        left_bound = 0
        right_bound = 0

        for i in range(lena):
            if array[smaller] < array[bigger]:
                new_array.append(array[smaller])
                smaller += 1
                if smaller == half:
                    if_exit = True
                    left_bound = bigger
                    right_bound = lena
            else:
                new_array.append(array[bigger])
                self.inversion_counter += half - smaller
                bigger += 1
                if bigger == lena:
                    if_exit = True
                    left_bound = smaller
                    right_bound = half
            if if_exit:
                # end case
                new_array[i+1:lena] = array[left_bound:right_bound]
                return new_array

        return new_array

    def merge_sort_int(self, array):
        lena = len(array)
        half = math.ceil(lena/2)
        if lena == 1:
            return array
        if lena == 2:
            if array[0] > array[1]:
                array[0], array[1] = array[1], array[0]
                self.inversion_counter += 1
            return array
        array[0:half] = self.merge_sort_int(array[0:half])
        array[half:lena] = self.merge_sort_int(array[half:lena])
        array[0:lena] = self._merge_combine(array)
        return array

    def quick_sort(self, array, start, end, approach):
        logger = logging.getLogger(__name__)
        pivot_index = start
        self.comparisons_counter += end - start - 1

        if (end - start) == 2:
            logger.debug('Simple case reached. Pivot index = ' + str(pivot_index) + ". Start index = " + str(start) +
                         ". End index = " + str(end))
            if array[start] > array[start+1]:
                array[start], array[start+1] = array[start+1], array[start]
            return

        logger.debug("Choosing pivot")
        if approach == PivotChose.FIRST:
            pivot_index = start
        if approach == PivotChose.LAST:
            pivot_index = end - 1
        if approach == PivotChose.MIDDLE:
            middle = start + int((end - start - 1)/2)
            try:
                pivot_index = median_of_three({array[start]: start,
                                              array[middle]: middle,
                                              array[end-1]: end-1})
            except WrongLengthException:
                pivot_index = middle

        if pivot_index is not None:
            pivot = array[pivot_index]
        else:
            raise NoneValueException

        logger.debug("Comparison counter = " + str(self.comparisons_counter))

        # swapping pivot index and the start of the partitioned array
        if pivot_index != start:
            array[start], array[pivot_index] = array[pivot_index], array[start]
        end_of_split = start  # the index of the last element of the smaller part
        end_of_partitioned = start + 1  # the index of the last bigger part element +1

        while end_of_partitioned < end:
            if array[end_of_partitioned] >= pivot:
                end_of_partitioned += 1
            else:
                if end_of_partitioned == end_of_split+1:
                    end_of_split += 1
                    end_of_partitioned += 1
                else:
                    array[end_of_partitioned], array[end_of_split + 1] = array[end_of_split + 1], \
                                                                         array[end_of_partitioned]
                    end_of_partitioned += 1
                    end_of_split += 1

        # putting the pivot into it's position
        if end_of_split != start:
            array[end_of_split], array[start] = array[start], array[end_of_split]

        if end_of_split-start >= 2:
            self.quick_sort(array, start, end_of_split, approach)
        if end_of_partitioned-end_of_split > 2:
            self.quick_sort(array, end_of_split+1, end, approach)


class Reader(object):

    @staticmethod
    def file_to_simple_list(file_name):
        logger = logging.getLogger(__name__)
        with open(file_name) as data_file:
            resulting_array = data_file.readlines()
            logger.debug("Array created from file: ")
            if logger.getEffectiveLevel() == 10:
                for index, element in enumerate(resulting_array):
                    logger.debug(str(index) + " : " + element)
        data_file.close()
        return resulting_array

    @staticmethod
    def file_to_dict(file_name):
        resulting_dict = {}
        with open(file_name) as data_file:
            for line in data_file:
                vertices_list = line.split("\t")
                for idx, item in enumerate(vertices_list):
                    try:
                        vertices_list[idx] = int(vertices_list[idx])
                    except ValueError:
                        print("ValueError")
                resulting_dict[vertices_list[0]] = vertices_list[1:len(vertices_list)]
        data_file.close()
        return resulting_dict

    @staticmethod
    def file_to_list(file_name):
        resulting_list = []
        with open(file_name) as data_file:
            for line in data_file:
                resulting_list.append(list(line.split()))
        data_file.close()
        return resulting_list

    @staticmethod
    def file_to_set_of_sets(file_name):
        resulting_set = set()
        with open(file_name) as data_file:
            for line in data_file:
                resulting_set.add(set(line.split()))
        data_file.close()
        return resulting_set


class Converter(object):

    @staticmethod
    def make_array_of_int(given_array):
        logger = logging.getLogger(__name__)
        logger.debug("Converting elements to int")
        for index, element in enumerate(given_array):
            given_array[index] = int(element)
            # check the types and if == raise and Exc


class CustomArray(Sortable):

    def __init__(self, file_name):
        logger = logging.getLogger(__name__)
        logger.debug("Reading values from file: " + file_name)
        self.array = Reader.file_to_simple_list(file_name)
        self.array_len = len(self.array)

    def make_integer(self):
        logger = logging.getLogger(__name__)
        logger.debug("Converting array elements to int")
        Converter.make_array_of_int(self.array)
