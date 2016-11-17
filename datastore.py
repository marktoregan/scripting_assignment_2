import pickle
import sys


class DataStore(object):

    STORE_FILES_TO_COPY = "db_store.dat"

    def __init__(self, store_files):
        self.files = store_files

    def record_files_copied(self):
        with open(self.STORE_FILES_TO_COPY, "wb") as f:
            pickle.dump(self.files, f)

    def read_files_copied(self):
        try:
            with open(self.STORE_FILES_TO_COPY, "rb") as f:
                return pickle.load(f)
        except FileNotFoundError:
            files = {}
            return files
