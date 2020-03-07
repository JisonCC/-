#!/urs/bin/env python
# -*- conding: utf-8 -*-
# @Author : Senci
# @Time   : 2020/2/18 11:44
# @File   : data2save.py


import csv
import chardet

class Data2File():
    def __init__(self):
        self.file_txt = r'H:\chenshengqing_python_project\Default_project\51job\data\数据分析师.txt'
        self.file_csv = '数据分析师.csv'
        self.row = ['PositionTitle','Adds','Salary','CompanyName','CompanyType','Exp','Degree',
                    'RecruitNum','PostTime','Welfare','PositionInfo','Contact','ConpanyInfo']
    def File(self):
        # csvfile = open(self.file_csv, 'w', newline='')
        # writer = csv.writer(csvfile)
        # writer.writerow(self.row)
        # lines = open(self.file_txt,'r',encoding='utf-8').readlines()
        # for line in lines:
        #     csvfile.write(line)
        # csvfile.close()

        with open(self.file_csv, 'w+', newline='',encoding='utf-8') as csvfile:
            spamwriter = csv.writer(csvfile, dialect='excel')
            # 读要转换的txt文件，文件每行各词间以@@@字符分隔
            with open(self.file_txt, 'r', encoding='utf-8') as filein:
                for line in filein:
                    line_list = line.strip('\n').split('\t')
                    spamwriter.writerow(line_list)



if __name__ == '__main__':
    D = Data2File()
    D.File()