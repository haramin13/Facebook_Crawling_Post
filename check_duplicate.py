import csv
import os
import glob
import argparse

path_read = './data3/csv_format/*.csv'

def check_dup(isdel):
    check_files = glob.glob(path_read)
    # print(check_files)

    for check_file in check_files:
        filename = check_file.split('\\')[-1].split('.')[0]
        log_path = './log_check/' + filename + '.txt'
        
        if isdel == False:
            print('Load')
            if os.path.exists(log_path):
                with open(log_path, 'w', encoding='utf-8') as f:
                    f.write('loc_has_dup\n')
                    f.close()
            else:
                os.makedirs(os.path.dirname(log_path), exist_ok=True)
                with open(log_path, 'w', encoding='utf-8') as f:
                    f.write('loc_has_dup\n')
                    f.close()
        else:
            print('Delete')
            
        # print(log_path)
        with open(check_file, 'r', encoding='utf-8') as file:
            rows = csv.reader(file, delimiter=',')
            datas = []
            # num_dup = 0
            for row in rows:
                _, text = row
                datas.append(text)
            # print(datas[0])
            for i in range(0, len(datas)):
                for j in range(i+1, len(datas)):
                    if datas[i] == datas[j]:
                        # num_dup = num_dup + 1
                        # If do not del file dup, location of file dup will be stored in log file
                        if isdel:
                            del_dup(filename, str(j))
                        else:
                            with open(log_path, 'a', encoding='utf-8') as f:
                                f.write(str(i) + '\t' + str(j) + '\n')
                                f.close()
            # print(num_dup)
            file.close()

def del_dup(path_file, idx_dup):
    # path = str(path_file)
    file_dup = "./data3/txt_format/" + path_file + "/" + path_file + idx_dup + '.txt'
    # print(file_dup)
    if os.path.exists(file_dup):
        os.remove(file_dup)
        # print("11")
    else:
        # print('File does not exists!')
        return


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
   
    parser.add_argument("-d", "--is_del_dup",
			default=False,
                        dest="is_del_dup", type=bool,
                        help="Delete duplicate file or not?")

    args = parser.parse_args()

    idx_dup = check_dup(args.is_del_dup)