import os
import sys
import time
import glob
import datetime
import sqlite3
import shutil
import re

msd_subset_path = './MillionSongSubset'
msd_subset_data_path = os.path.join(msd_subset_path, 'data')
msd_subset_addf_path = os.path.join(msd_subset_path, 'AdditionalFiles')
assert os.path.isdir(msd_subset_path), 'wrong path'  # sanity check
# path to the Million Song Dataset code
# CHANGE IT TO YOUR LOCAL CONFIGURATION
msd_code_path = './MSongsDB'
assert os.path.isdir(msd_code_path), 'wrong path'  # sanity check
# we add some paths to python so we can import MSD code
# Ubuntu: you can change the environment variable PYTHONPATH
# in your .bashrc file so you do not have to type these lines
sys.path.append(os.path.join(msd_code_path, 'PythonSrc'))

# imports specific to the MSD
# import hdf5_getters as GETTERS

def findSongsInData():
    ctr_rock,ctr_pop,ctr_rap,ctr_electronic = 0,0,0,0

    f = open("canciones_generos.cls",'r')
    f1 = open("lista_final.cls",'w')
    conn = sqlite3.connect(os.path.join(msd_subset_addf_path,
                                        'subset_track_metadata.db'))
    count = 0
    for line in f:
        sep = re.split('\t|\n',line)
        # we build the SQL query
        q = "select * from songs where track_id = '" + sep[0] + "'"
        # we query the database
        res = conn.execute(q)
        ans = res.fetchall()
        # print all_artist_names_sqlite
        if (ans != []) :
            if (sep[1] == "Rock" and ctr_rock < 150):
                f1.write(line)
                ctr_rock += 1
            elif (sep[1] == "Pop" and ctr_pop < 150):
                f1.write(line)
                ctr_pop += 1
            elif (sep[1] == "Rap" and ctr_rap < 150):
                f1.write(line)
                ctr_rap += 1
            elif (sep[1] == "Electronic" and ctr_electronic < 150):
                f1.write(line)
                ctr_electronic += 1
    # we close the connection to the database
    conn.close()

def extractGenre():
    generos = ["Rock","Electronic","Pop","Rap"]
    f = open("generos.cls",'r')
    f1 = open("canciones_generos.cls",'w')
    for line in f:
        sep = re.split('\t|\n',line)
        # print (sep[1])
        if (sep[1] in generos): f1.write(line)

def move_files():
    lista = open("lista_final.cls", 'r')
    for line in lista:
        sep = re.split('\t|\n', line)
        file_name = sep[0] + ".h5"
        for root, dirs, files in os.walk(msd_subset_data_path):
            if file_name in files:
                shutil.copy(os.path.join(root, file_name), "./canciones/")