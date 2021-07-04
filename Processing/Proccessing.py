import numpy as np
from pandas import DataFrame
from utility import Utility


class Process:
    # filename the name of the pdf file to read from
    def __init__(self, blend_of_text_and_coordinates):
        self.blend_of_text_and_coordinates = blend_of_text_and_coordinates
        self.x_coordinates = []
        self.y_coordinates = []
        self.text_value = []
        self.dataframe = None
        self.__clean_the_data()

    # remove all the outliers, smaller numbers etc
    def __clean_the_data(self):
        (
            self.text_value,
            self.x_coordinates,
            self.y_coordinates,
        ) = self.__sort_coordinates()

        x_outliers = self.__get_outliers(self.x_coordinates)
        y_outliers = self.__get_outliers(self.y_coordinates)
        self.__update_dataframe(self.text_value, self.x_coordinates,
                                self.y_coordinates)

        single_digits = self.__get_single_digits()
        indexes_to_remove = x_outliers + y_outliers + single_digits
        (
            self.text_value,
            self.x_coordinates,
            self.y_coordinates,
        ) = Utility.remove_indexes(
            self.text_value, self.x_coordinates, self.y_coordinates
            , indexes_to_remove
        )
        self.__update_dataframe(self.text_value, self.x_coordinates,
                                self.y_coordinates)

    # sorts the bounding box coordinates of the text values based on their y values
    # returns text, x coordinates, y coordinates
    def __sort_coordinates(self):
        sorted_text = []
        sorted_y_coordinate = []
        sorted_x_coordinate = []
        first_index = 0
        second_index = 1

        for array_value in self.blend_of_text_and_coordinates:
            value_text = array_value[first_index]
            value_text = value_text.rsplit()
            sorted_text.append(value_text[first_index])

            bbox = array_value[second_index]
            coordinates = bbox.split(",")
            y_coordinate = float(coordinates[second_index])
            x_coordinate = float(coordinates[first_index])
            sorted_x_coordinate.append(x_coordinate)
            sorted_y_coordinate.append(y_coordinate)

        self.__update_dataframe(sorted_text, sorted_x_coordinate,
                                sorted_y_coordinate)

        return (
            list(self.dataframe.text),
            list(self.dataframe.x_coord),
            list(self.dataframe.y_coord),
        )

    def __get_single_digits(self):
        single_digit = []
        minimum_number_required = 10
        for idx, text_label in enumerate(self.text_value):
            if float(text_label) < minimum_number_required:
                single_digit.append(idx)
        return single_digit

    def __update_dataframe(self, sorted_text, sorted_x_coordinate,
                           sorted_y_coordinate):
        inputs = {
            "text": sorted_text,
            "x_coord": sorted_x_coordinate,
            "y_coord": sorted_y_coordinate,
        }
        dataframe = DataFrame(inputs)
        self.dataframe = dataframe.sort_values(
            by=["y_coord", "x_coord"], ascending=False
        )

    @staticmethod
    def __get_outliers(data):
        outliers = []
        threshold = 3
        mean_of_data = np.mean(data)
        std_of_data = np.std(data)

        for idx, record in enumerate(data):
            z_score = (record - mean_of_data) / std_of_data
            if np.abs(z_score) > threshold:
                outliers.append(idx)
        return outliers

    def get_sorted_dataframe(self):
        return self.dataframe

    def get_x_coordinates(self):
        return self.x_coordinates

    def get_y_coordinates(self):
        return self.y_coordinates

    def get_text_value(self):
        return self.text_value
