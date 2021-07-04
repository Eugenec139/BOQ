import numpy as np


class Utility:

    # check if string is a number
    # return boolean
    @staticmethod
    def is_number(string):
        try:
            float(string)
        except ValueError:
            try:
                complex(string)
            except ValueError:
                return False

        return True

    @staticmethod
    def remove_indexes(text_value, x_coordinates, y_coordinates,
                       indexes_to_remove):
        return (
            list(np.delete(text_value, indexes_to_remove)),
            list(np.delete(x_coordinates, indexes_to_remove)),
            list(np.delete(y_coordinates, indexes_to_remove)),
        )
