import os
import pydicom
import SimpleITK as sitk
import cv2
import numpy as np

def dcm2png_single(dcm_path):
    save_pa = r'G:\PE\000f7f114264\single'
    if not os.path.exists(save_pa):
        os.makedirs(save_pa)
    img_name = os.path.split(dcm_path.replace('.dcm', '.png'))  # 替换后缀名并分离路径
    img_name = img_name[-1]
    ds = pydicom.read_file(dcm_path, force=True)       # 注意这里，强制读取
    img = ds.pixel_array  # 提取图像信息
    cv2.imwrite(os.path.join(save_pa, img_name), img)

def alldcm2png(dcm_path):
    dcmlist = os.listdir(dcm_path)
    save_data = r'G:\PE\000f7f114264\dcm_png_data'
    if not os.path.exists(save_data):
        os.makedirs(save_data)
    for dcm in dcmlist:
        ds1 = pydicom.read_file(os.path.join(dcm_path, dcm))
        img = ds1.pixel_array  # 提取图像信息
        cv2.imwrite(os.path.join(save_data, dcm.replace('.dcm', '.png')), img)


def labeldcm2png(dcm_path, label_path):
    labellist = os.listdir(label_path)
    save_data = r'G:\PE\000f7f114264\dcm_png_data'
    save_lab = r'G:\PE\000f7f114264\dcm_png_lab'
    if not os.path.exists(save_data):
        os.makedirs(save_data)
    if not os.path.exists(save_lab):
        os.makedirs(save_lab)
    for lab in labellist:
        print('process', lab)
        ds = pydicom.read_file(os.path.join(label_path, lab), force=True)   # 注意这里，强制读取
        label = ds.pixel_array  # 提取图像信息
        ds1 = pydicom.read_file(os.path.join(dcm_path, lab), force=True)
        img = ds1.pixel_array  # 提取图像信息
        cv2.imwrite(os.path.join(save_data, lab.replace('.dcm', '.png')), img)
        cv2.imwrite(os.path.join(save_lab, lab.replace('.dcm', '.png')), label)


if __name__ == "__main__":
    # 单个dcm转png
    dcm_single = r'G:\PE\000f7f114264\9f7378c3b2ab\0c62ee63f2a9.dcm'
    dcm2png_single(dcm_single)

    # 所有的批量dcm转png
    dcm_pa = r'G:\PE\000f7f114264\9f7378c3b2ab'
    alldcm2png(dcm_pa)

    # 所有的批量dcm转png
    dcm_pa = r'G:\PE\000f7f114264\9f7378c3b2ab'
    lab_dcm = r'G:\PE\000f7f114264\9f7378c3b2ab'
    labeldcm2png(dcm_pa, lab_dcm)

