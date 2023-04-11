import numpy as np
import os  # 遍历文件夹
import shutil


def nii_to_image(filepath, type_name):
    filenames = os.listdir(filepath)  # 读取nii文件夹
    Note = open('G:/mmdetection/MICCAI2022/' + type_name, mode='w')

    for f in filenames:
        Note.write(f)  # \n 换行符
        Note.write('\n')  # \n 换行符

    Note.close()


if __name__ == '__main__':
        datasetpath = 'G:/DWI/MICCAI/MICCAI_2022/All_data/split_data/train/1/'
        # datasetpath = 'G:/DWI/MICCAI/MICCAI_2022/All_data/split_data/val/1/'
        type_name = 'train.txt'
        # type_name = 'test.txt'
        nii_to_image(datasetpath, type_name)


