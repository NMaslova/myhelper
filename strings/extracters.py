def extract_file_name(path):
    dirs = str(path).split('/')
    file_name = dirs.pop()
    name_parts = file_name.split('.')
    return name_parts[0]