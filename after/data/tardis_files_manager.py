import re
import pathlib


class TardisFilesManager:
    def __init__(self, results_path, root_project=''):

        self.results_path = []
        if isinstance(results_path, list):
            for path in results_path:
                self.results_path.append(pathlib.Path(path))
        else:
            self.results_path.append(pathlib.Path(path))

        self.results_apath = []
        if root_project:
            self.root_project = pathlib.Path(root_project)
            for path in self.results_path:
                self.results_apath.append(self.root_project / path)
        else:
            self.results_apath = self.results_path


    def dirs(self):
        lst = []
        for Dir in self.results_apath:
            for dir in Dir.iterdir():
                lst.append(dir)

        return sorted(lst)


    def files(self, r_expression=''):
        lst = []
        for dir in self.dirs():
            for file in dir.iterdir():
                if re.search(r_expression, str(file)):
                    lst.append(file)

        return sorted(lst)


    def clean(self, r_expression):
        for file in self.files():
            if re.search(r_expression, str(file)):
                file.unlink()

        return self


    def __repr__(self):
        dirs = list(map(str, self.dirs()))
        stg = ''
        stg += dirs[0] + '\n'
        stg += dirs[1] + '\n'
        stg += dirs[2] + '\n'
        stg += dirs[4] + '\n'
        stg += dirs[5] + '\n'

        stg += '...' + '\n'

        stg += dirs[-5] + '\n'
        stg += dirs[-4] + '\n'
        stg += dirs[-3] + '\n'
        stg += dirs[-2] + '\n'
        stg += dirs[-1] + '\n'
        return stg
