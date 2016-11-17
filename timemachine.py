import copyfile as backup
import datastore as db
import manageconfig as config
import argparse
import pickle
import logging
import yaml
import datetime
import sys
import os


def do_initial_copy(files):
    for copy_file in files.keys():
        if files[copy_file]["last_copied"] == "not_copied":
            print("copy_file")
            backup.CopyFile(copy_file,files[copy_file]["copy_path"])
            files[copy_file]["last_copied"] = files[copy_file]["modified"]
        else:
            print("any hit")
    return files

def do_changed_files_copy(xfiles):
    for copy_file in xfiles.keys():
        print(xfiles[copy_file]["modified"])
        print(xfiles[copy_file]["last_copied"])
        if xfiles[copy_file]["modified"] > xfiles[copy_file]["last_copied"]:
            print(copy_file)
            backup.CopyFile(copy_file,xfiles[copy_file]["copy_path"])
            xfiles[copy_file]["last_copied"] = xfiles[copy_file]["modified"]
        else:
            print('nothing new to report')


def run():
    #1

    files = config.ManageConfig.watch_files(config.ManageConfig,"config.dat")

    #2
    files = do_initial_copy(files)

    db1 = db.DataStore(files)
    db1.record_files_copied()


    #xfiles = db1.read_files_copied()
    xfiles = db.DataStore.read_files_copied(db.DataStore)
    do_changed_files_copy(xfiles)


    db2 = db.DataStore(xfiles)
    db2.record_files_copied()
    #return files
    print(xfiles)

run()
#print(loaded_files)