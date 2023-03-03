import csv
import glob
import os

path_read = './data/csv_format/*.csv'

check_files = glob.glob(path_read)
# print(check_files)

for check_file in check_files:

    filename = check_file.split('\\')
    log_path = './log_check/' + filename[-1].split('.')[0] + '.txt'

    if os.path.exists(log_path):
            with open(log_path, 'w', encoding='utf-8') as f:
                f.write('loc_has_dup\n')
    else:
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        with open(log_path, 'w', encoding='utf-8') as f:
            f.write('loc_has_dup\n')
    
    # print(log_path)
    with open(check_file, 'r', encoding='utf-8') as file:
        rows = csv.reader(file, delimiter=',')
        datas = []
        for row in rows:
            _, text = row
            datas.append(text)
        # print(datas[0])
        for i in range(0, len(datas)):
            for j in range(i+1, len(datas)):
                if datas[i] == datas[j]:
                    with open(log_path, 'a', encoding='utf-8') as f:
                        f.write(str(i) + '\t' + str(j) + '\n')
                    print(i, '\t', j, '\n')