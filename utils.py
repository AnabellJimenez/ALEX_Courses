import csv
import os


def lol():
    print(os.path.dirname(os.path.realpath(__file__)))

def courses_to_csv(courses, file_name):
    """
    Writes courses to a csv file in the csv directory.
    :param courses: list of dictionaries, each dictionary should have same keys.
    :param file_name: name of the file
    """
    keys = courses[0].keys()

    full_path = '{}/CSV-info/{}'.format(
        os.path.dirname(os.path.realpath(__file__)),
        file_name
    )
    with open(full_path, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(courses)
