import os

def extract_directory(path):
    if os.path.isdir(path):
        # If the path is a directory, return it as is
        return path
    elif os.path.isfile(path):
        # If the path is a file, return its directory
        return os.path.dirname(path)
    else:
        # If the path does not exist, raise an error
        raise ValueError("The provided path does not exist")