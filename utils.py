import csv
import os
import unicodedata
import string
import glob

# creating CSV header
def create_csv(filename):
    path_file = "./data/csv_format/" + filename + ".csv"

    if os.path.exists(path_file):
        with open(path_file, "w+", newline='', encoding="utf-8") as save_file:
            writer = csv.writer(save_file)
            writer.writerow(["Idx", "Text"])
    else:
        os.makedirs(os.path.dirname(path_file), exist_ok=True)
        with open(path_file, "w+", newline='', encoding="utf-8") as save_file:
            writer = csv.writer(save_file)
            writer.writerow(["Idx", "Text"])

def create_log_file():
    filename = "./log_file.txt"
    with open(filename, "w+", encoding="utf-8") as f:
        f.write('*'*5 + "Summary infomation" + '*'*5 + '\n')
    
# clean all non-alphanumberic characters       
def strip(string):
    words = string.split()
    words = [word for word in words if "#" not in word]
    string = " ".join(words)
    clean = ""
    for c in string:
        if str.isalnum(c) or (c in [" ", ".", ","]):
            clean += c
    return clean

def write_to_csv(filename, data):
    path_file = "./data/csv_format/" + filename + "/" + filename + ".csv"
    with open(path_file, "a+", newline='', encoding="utf-8") as save_file:
        writer = csv.writer(save_file)
        writer.writerow(data)

def write_to_txt(filename, data, idx): 
    # When loading data from file, the path of file in Windows will change "/" to "\\"
    path_file = "./data/txt_format/" + filename + "/" + filename + str(idx) + ".txt"

    if os.path.exists(path_file):
        with open(path_file, "w", encoding="utf-8") as f:
            f.write(data)
    else:
        os.makedirs(os.path.dirname(path_file), exist_ok=True)
        with open(path_file, "w", encoding="utf-8") as f:
            f.write(data)

def write_log_file(data):
    filename = "./log_file.txt"
    with open(filename, "a", encoding="utf-8") as f:
        f.write(data)