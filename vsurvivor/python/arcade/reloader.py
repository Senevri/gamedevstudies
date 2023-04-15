#!python3

#import importlib
import os

class Reloader():
    def __init__(self):
        self.location = os.path.dirname(os.path.abspath(__file__))
        self.files = self.get_filetimes()


    def update_filetimes(self):
        self.files = self.get_filetimes()

    def get_mtime_for_file(self, file):
        #logger.warn(self.location, file)
        full_path = os.path.join(self.location, file)
        if os.path.isfile(full_path):
            return os.path.getmtime(full_path)
            
    def list_updated_files(self):
        # NOTE: Could yield instead of append
        updated_files = []
        for file, old_mtime in self.files.items(): 
            mtime = self.get_mtime_for_file(file)
            if mtime != old_mtime:
                #self.files[file] = mtime
                updated_files.append(file)
        return updated_files

    def get_filetimes(self): 
        mtimes = {}
        files = os.listdir(self.location)
        for file in files:
                mtime = self.get_mtime_for_file(file)
                mtimes[file] = mtime
        return mtimes
    
if __name__ == "__main__":
    reload = Reloader()
    files = reload.list_updated_files()
    reload.update_filetimes()

