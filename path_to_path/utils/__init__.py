import os


def get_ui(dir_path='mc_log_view/', ext='.ui'):
    res = []
    for root, directories, filenames in os.walk(dir_path):
        for file_name in filenames:
            if file_name[-3:] == ext:
                res.append(os.path.join(root, file_name)[len(dir_path):])
    return res
