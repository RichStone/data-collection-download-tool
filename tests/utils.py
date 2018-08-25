from os import walk


def get_all_file_names_from_directory(path):
    files = []
    for (dirpath, dirnames, filenames) in walk(path):
        files.extend(filenames)
    return files
