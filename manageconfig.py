import yaml
import os
import datetime
import datastore as db
import sys

class ManageConfig(object):

    def read(self,filename):
        try:
            #logger.debug("Reading config from {0}".format(filename))
            with open(filename, "r") as f:
                return yaml.load(f)
        except FileNotFoundError:
            #logger.error("Config file {0} not found".format(filename))
            print("Config file {0} not found".format(filename), file=sys.stderr)
            sys.exit(1)


    def list_of_files(self, config_files):
        file_paths=[]
        for folders in config_files:
            path = folders["folder_path"]
            watch = folders["files"]
            for w in watch:
                file_paths.append("{0}/{1}".format(path, w))
                #print("{0}/{1}".format(path, w))
        return file_paths


    def populate_files_to_watch(self, source_files,dest_path):
        files = db.DataStore.read_files_copied(db.DataStore)
        print(files)
        for file in source_files:
            timestamp = os.path.getmtime(file)
            if file not in files.keys():
                files.update({file: {"modified": timestamp,
                                     "last_copied": "not_copied",
                                     "copy_path":"{0}/{1}-{2}".format(dest_path,datetime.datetime.fromtimestamp(timestamp),os.path.basename(file))
                                     }
                              })
            else:
                files[file]["modified"] = os.path.getmtime(file)
                files[file]["copy_path"]="{0}/{1}-{2}".format(dest_path, datetime.datetime.fromtimestamp(timestamp),
                                                 os.path.basename(file))
        return files

    def watch_files(self, config_file_path):
        try:
            self.config_file = self.read(self, config_file_path)
            file_paths = self.list_of_files(self, self.config_file["watch"])
            files = self.populate_files_to_watch(self, file_paths, self.config_file["backup_folder"])
            return files
        except:
            print("log bad configuartion")
            sys.exit(1)

