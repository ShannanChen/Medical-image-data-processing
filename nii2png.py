import os
import SimpleITK as sitk
import cv2
import numpy as np

def nii2png_single(nii_path, IsData = True):
    ori_data = sitk.ReadImage(nii_path)  # 读取一个数据
    data1 = sitk.GetArrayFromImage(ori_data)  # 获取数据的array
    if IsData:  #过滤掉其他无关的组织，标签不需要这步骤
        data1[data1 > 250] = 250
        data1[data1 < -250] = -250
    img_name = os.path.split(nii_path)  #分离文件名
    img_name = img_name[-1]
    img_name = img_name.split('.')
    img_name = img_name[0]
    i = data1.shape[0]
    png_path = './png/single_png'   #图片保存位置
    if not os.path.exists(png_path):
        os.makedirs(png_path)
    for j in range(0, i):   #将每一张切片都转为png
        if IsData:  # 数据
            #归一化
            slice_i = (data1[j, :, :] - data1[j, :, :].min()) / (data1[j, :, :].max() - data1[j, :, :].min()) * 255
            cv2.imwrite("%s/%s-%d.png" % (png_path, img_name, j), slice_i)  #保存
        else:   # 标签
            slice_i = data1[j, :, :] * 122
            cv2.imwrite("%s/%s-%d.png" % (png_path, img_name, j), slice_i)  # 保存


def nii2png(data_path, label_path):
    dataname_list2 = os.listdir(label_path)
    for nii_label in dataname_list2:
        print("process:", nii_label)
        data1 = sitk.ReadImage(os.path.join(data_path, nii_label.replace('segmentation', 'volume'))) # 读取一个数据
        liver_tumor_data = sitk.GetArrayFromImage(data1)  # 获取数据的array
        data2 = sitk.ReadImage(os.path.join(label_path, nii_label))  # 读取一个数据
        liver_tumor_label = sitk.GetArrayFromImage(data2)  # 获取数据的array
        img_name = os.path.split(nii_label.replace('segmentation', 'volume'))     # 分离文件名，用以保存时的文件名前缀
        img_name = img_name[-1]
        img_name = img_name.split('.')
        img_name = img_name[0]
        i = liver_tumor_label.shape[0]
        liver_tumor_data[liver_tumor_data > 250] = 250
        liver_tumor_data[liver_tumor_data < -250] = -250
        outpath = r'./png/data_png'  # 数据保存文件夹
        outpath2 = r'./png/label_png'   # 标签保存文件夹
        if not os.path.exists(outpath):
            os.makedirs(outpath)
        if not os.path.exists(outpath2):
            os.makedirs(outpath2)
        for j in range(0, i):
            if liver_tumor_label[j, :, :].max() > 0:    # 只保存有肝脏的切片
                img1 = (liver_tumor_data[j, :, :] - liver_tumor_data[j, :, :].min()) / (liver_tumor_data[j, :, :].max() - liver_tumor_data[j, :, :].min()) * 255
                img2 = liver_tumor_label[j, :, :] * 122
                cv2.imwrite("%s/%s-%d.png" % (outpath, img_name, j), img1)
                cv2.imwrite("%s/%s-%d.png" % (outpath2, img_name, j), img2)



if __name__ == "__main__":

    # 单个nii文件转png
    nii_single = r'G:\Python\liversegment\ImageResource\ImageTraning\data\volume-0.nii'
    nii2png_single(nii_single, IsData=False)

    # 按照标签提取切片，只保存有肝脏的切片
    niipath = r'G:\Python\liversegment\ImageResource\ImageTraning\data'
    labpath = r'G:\Python\liversegment\ImageResource\ImageTraning\label'
    nii2png(niipath, labpath)



