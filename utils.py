import csv
import os
import re


def clean_course(course_dict):
    """
    Goes over all values in the dict and strips out all newlines, tabs,
    and sequences of more then 2 spaces in a row
    :param course_dict: dictionary of a course
    :return: dictionary back
    """
    remove_others = re.compile(r'[\t\n]')
    remove_multiple_spaces = re.compile(r'[ ]{2,}')

    new_course_dict = {}

    for key, val in course_dict.iteritems():
        first = re.sub(remove_others, '', val)
        second = re.sub(remove_multiple_spaces, ' ', first)
        final = second.encode('ascii', 'ignore')
        new_course_dict[key] = final

    return new_course_dict


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
