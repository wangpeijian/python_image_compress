from impl.folder import mdir


class Task:

    def __init__(self, source_path, target_path, files):
        self.source_path = source_path
        self.target_root_path = target_path
        self.files = files

        mdir(target_path)
