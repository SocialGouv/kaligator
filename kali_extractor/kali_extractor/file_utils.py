import os


def get_nested_file_paths(dir_path):
    xml_paths = []
    for dir_name, _, file_list in os.walk(dir_path):
        for file_name in file_list:
            xml_paths.append(os.path.join(dir_name, file_name))
    return xml_paths
